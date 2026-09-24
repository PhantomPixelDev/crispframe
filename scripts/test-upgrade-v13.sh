#!/bin/sh
set -eu

# Rehearse the local TYPO3 13 -> 14 upgrade against a restored copy of the
# database and uploads. Never points Composer or TYPO3 at the live /app/var.
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
backup=${CRISPFRAME_UPGRADE_BACKUP:-$root/output/backups/pre-typo3-14-20260923.tar.gz}
test -s "$backup"
work=$(mktemp -d "${TMPDIR:-/tmp}/crispframe-upgrade.XXXXXX")
if [ "${CRISPFRAME_KEEP_UPGRADE_COPY:-0}" = '1' ]; then
    echo "Isolated upgrade copy: $work"
else
    trap 'rm -rf "$work"' EXIT
fi
cp "$root/composer.json" "$work/composer.json"
cp "$root/composer.lock" "$work/composer.lock"
mkdir -p "$work/packages"
cp -R "$root/packages/agency_theme" "$work/packages/agency_theme"
(cd "$work" && tar -xzf "$backup")
python3 - "$work/config/system/settings.php" "$work/config/sites/main/config.yaml" "$work" <<'PY'
import sys
from pathlib import Path
settings, site, work = map(Path, sys.argv[1:])
settings.write_text(settings.read_text().replace('/app/var/', str(work / 'var') + '/'))
site.write_text(site.read_text().replace('http://localhost:8080/', 'http://127.0.0.1:8766/'))
PY
database_path=$(php -r '$s=require $argv[1]; echo $s["DB"]["Connections"]["Default"]["path"];' "$work/config/system/settings.php")
python3 "$root/scripts/prepare-sqlite-14.py" "$database_path"
cd "$work"
composer update --no-interaction --prefer-dist --no-progress
vendor/bin/typo3 cache:flush
vendor/bin/typo3 extension:setup --extension=agency_theme --no-interaction
python3 "$root/scripts/prepare-sqlite-14.py" "$database_path"
vendor/bin/typo3 upgrade:run --no-interaction -vvv
vendor/bin/typo3 content-blocks:lint
test "$(vendor/bin/typo3 --version | grep -o '14\.3\.[0-9]*' | head -n 1)" != ''
php -S 127.0.0.1:8766 -t public "$root/scripts/router.php" > "$work/server.log" 2>&1 &
server_pid=$!
if [ "${CRISPFRAME_KEEP_UPGRADE_COPY:-0}" = '1' ]; then
    trap 'kill "$server_pid" 2>/dev/null || true' EXIT
else
    trap 'kill "$server_pid" 2>/dev/null || true; rm -rf "$work"' EXIT
fi
python3 - <<'PY'
import time
import urllib.request
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8766/de/contact') as response:
            page = response.read().decode()
            assert response.status == 200 and 'Kontakt' in page
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('Upgraded demo did not render: /de/contact')
print('Isolated TYPO3 13 database and uploads upgraded to TYPO3 14 and served German content.')
PY
