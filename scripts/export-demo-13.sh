#!/bin/sh
set -eu

# TYPO3 13's impexp format is readable by both supported LTS versions.
# Work only in a restored temporary site; never reimport demo records on /app.
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
backup=${CRISPFRAME_EXPORT_BACKUP:-$root/output/backups/pre-live-14-v13-content-20260923.tar.gz}
test -s "$backup"
work=$(mktemp -d "${TMPDIR:-/tmp}/crispframe-export13.XXXXXX")
trap 'rm -rf "$work"' EXIT
cp "$root/composer.json" "$work/composer.json"
python3 - "$work/composer.json" <<'PY'
import json
import sys
from pathlib import Path
path = Path(sys.argv[1])
project = json.loads(path.read_text())
for name in project['require']:
    if name.startswith('typo3/'):
        project['require'][name] = '^13.4.15'
project['require']['friendsoftypo3/content-blocks'] = '^1.6'
path.write_text(json.dumps(project, indent=2) + '\n')
PY
mkdir -p "$work/packages"
cp -R "$root/packages/agency_theme" "$work/packages/agency_theme"
(cd "$work" && tar -xzf "$backup")
python3 - "$work/config/system/settings.php" "$work" <<'PY'
import sys
from pathlib import Path
settings, work = map(Path, sys.argv[1:])
settings.write_text(settings.read_text().replace('/app/var/', str(work / 'var') + '/'))
PY
cd "$work"
composer install --no-interaction --prefer-dist --no-progress
vendor/bin/typo3 cache:flush
vendor/bin/typo3 extension:setup --extension=agency_theme --no-interaction
CRISPFRAME_SITE_ROOT="$work" python3 "$root/.dev/seed-v13-demo.py"
CRISPFRAME_SITE_ROOT="$work" python3 "$root/.dev/seed-v14-demo.py"
vendor/bin/typo3 cache:flush
vendor/bin/typo3 impexp:export --type=xml --pid=1 --levels=999 --table=tt_content --include-related=_ALL --dependency=agency_theme --title='Crispframe 1.4 bilingual demo' crispframe-demo-v14
python3 - "$work/public/fileadmin/user_upload/_temp_/importexport/crispframe-demo-v14.xml" "$root/packages/agency_demo/Initialisation/data.xml" <<'PY'
import sys
from pathlib import Path
Path(sys.argv[2]).write_bytes(Path(sys.argv[1]).read_bytes().replace(bytes([13, 10]), bytes([10])))
PY
echo 'Wrote TYPO3 13 compatible bilingual demo export.'
