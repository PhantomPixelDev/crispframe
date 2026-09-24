#!/bin/sh
set -eu

# Exercise distribution archives, not Composer path repositories. Run in a PHP
# environment with Composer, Python 3 and zip (the local Podman web container has all three).
root=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
typo3_major=${CRISPFRAME_TYPO3_MAJOR:-14}
case "$typo3_major" in 13|14) ;; *) echo "CRISPFRAME_TYPO3_MAJOR must be 13 or 14" >&2; exit 2;; esac
work=$(mktemp -d "${TMPDIR:-/tmp}/crispframe-release.XXXXXX")
trap 'rm -rf "$work"' EXIT
mkdir -p "$work/artifacts" "$work/theme" "$work/demo" "$work/site"
cp -R "$root/packages/agency_theme/." "$work/theme/"
cp -R "$root/packages/agency_demo/." "$work/demo/"
cp "$root/starter/composer.json" "$work/site/composer.json"

python3 - "$work/theme/composer.json" "$work/demo/composer.json" "$work/site/composer.json" "$typo3_major" <<'PY'
import json
import sys
for path in sys.argv[1:3]:
    with open(path, encoding='utf-8') as file:
        package = json.load(file)
    package['version'] = '1.3.0'
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(package, file, indent=2)
if sys.argv[4] == '13':
    path = sys.argv[3]
    with open(path, encoding='utf-8') as file:
        starter = json.load(file)
    for name in starter['require']:
        if name.startswith('typo3/'):
            starter['require'][name] = '^13.4.15'
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(starter, file, indent=2)
PY

(cd "$work/theme" && zip -qr "$work/artifacts/agency-theme.zip" .)
(cd "$work/demo" && zip -qr "$work/artifacts/agency-demo.zip" .)
cd "$work/site"
composer config repositories.crispframe-artifact artifact "$work/artifacts"
composer install --no-interaction --prefer-dist --no-progress
test -f vendor/crispframe/agency-theme/Resources/Private/Forms/Contact.form.yaml
test -f vendor/crispframe/agency-theme/LICENSE
test -f vendor/crispframe/agency-theme/Resources/Private/ThirdParty/LUCIDE-LICENSE
test ! -d vendor/crispframe/agency-demo

composer require crispframe/agency-demo:^1.3 --no-interaction --prefer-dist --no-progress
test -f vendor/crispframe/agency-demo/Initialisation/data.xml
test -f vendor/crispframe/agency-demo/Initialisation/Site/main/config.yaml
TYPO3_SETUP_ADMIN_PASSWORD='CleanInstall1234!' vendor/bin/typo3 setup --driver=sqlite --dbname="$work/site/var/site.sqlite" --admin-username=admin --admin-email=admin@example.invalid --project-name='Crispframe clean install' --server-type=apache --no-interaction
vendor/bin/typo3 extension:setup --extension=agency_demo --no-interaction
vendor/bin/typo3 content-blocks:lint
test -f config/sites/main/config.yaml
database_path=$(php -r '$s=require "config/system/settings.php"; echo $s["DB"]["Connections"]["Default"]["path"];')
python3 - "$database_path" <<'PY'
import sqlite3
import sys
from pathlib import Path
database = sqlite3.connect(sys.argv[1])
pages = database.execute("SELECT COUNT(*) FROM pages WHERE deleted = 0").fetchone()[0]
translations = database.execute("SELECT COUNT(*) FROM pages WHERE deleted = 0 AND sys_language_uid = 1").fetchone()[0]
files = [row[0] for row in database.execute("SELECT identifier FROM sys_file WHERE identifier LIKE '%workspace.svg' OR identifier LIKE '%collaboration.svg' OR identifier LIKE '%studio-team.webp' OR identifier LIKE '%project-worktable.webp' OR identifier LIKE '%meeting-space.webp' OR identifier LIKE '%services-team.webp' OR identifier LIKE '%about-team.webp' OR identifier LIKE '%case-study-service.webp' OR identifier LIKE '%case-study-product.webp'")]
blocks = {row[0] for row in database.execute("SELECT DISTINCT CType FROM tt_content WHERE CType LIKE 'crispframe_%' AND deleted = 0")}
assert pages >= 16, f'Expected sixteen bilingual example pages, found {pages}'
assert translations >= 8, f'Expected eight German pages, found {translations}'
assert len(files) >= 9, f'Expected demo galleries and case study photos, found {files}'
assert len(blocks) == 19, f'Expected all 19 block types, found {sorted(blocks)}'
heroes = database.execute("SELECT COUNT(*) FROM tt_content WHERE CType = 'crispframe_hero' AND crispframe_hero_image = 1 AND crispframe_hero_imageAlt != '' AND deleted = 0").fetchone()[0]
assert heroes >= 14, f'Expected English and German image references for seven heroes, found {heroes}'
localized_hero_refs = database.execute("SELECT COUNT(*) FROM sys_file_reference WHERE fieldname = 'crispframe_hero_image' AND sys_language_uid = 1 AND l10n_parent > 0 AND deleted = 0").fetchone()[0]
assert localized_hero_refs >= 7, f'Expected seven linked German hero image references, found {localized_hero_refs}'
for identifier in files:
    image = Path(sys.argv[1]).parents[2] / 'public' / 'fileadmin' / identifier.lstrip('/')
    assert image.is_file(), f'Missing imported gallery image: {image}'
print(f'Clean install passed: {pages} pages, {translations} German translations, 19 block types, {len(files)} imported images.')
PY

if [ "${CRISPFRAME_BROWSER_SMOKE:-0}" = '1' ]; then
    if [ -n "${CRISPFRAME_TEST_SMTP:-}" ]; then
        cat > config/system/additional.php <<'PHP'
<?php
$GLOBALS['TYPO3_CONF_VARS']['MAIL']['transport'] = 'smtp';
$GLOBALS['TYPO3_CONF_VARS']['MAIL']['transport_smtp_server'] = getenv('CRISPFRAME_TEST_SMTP');
PHP
    fi
    php -S 127.0.0.1:8765 -t "$work/site/public" "$root/scripts/router.php" > "$work/server.log" 2>&1 &
    server_pid=$!
    trap 'kill "$server_pid" 2>/dev/null || true; rm -rf "$work"' EXIT
    python3 - <<'PY'
import time
import urllib.error
import urllib.request
for attempt in range(30):
    try:
        with urllib.request.urlopen('http://127.0.0.1:8765/') as response:
            assert response.status == 200
        break
    except Exception:
        time.sleep(1)
else:
    raise SystemExit('Clean starter HTTP server did not become ready')
for path in ['/work', '/contact', '/services', '/about', '/components', '/de/', '/de/contact', '/de/leistungen', '/de/ueber-uns', '/de/components', '/work/clearer-public-service', '/work/customer-workspace', '/de/work/clearer-public-service', '/de/work/customer-workspace']:
    with urllib.request.urlopen('http://127.0.0.1:8765' + path) as response:
        assert response.status == 200, (path, response.status)
with urllib.request.urlopen('http://127.0.0.1:8765/') as response:
    home = response.read().decode('utf-8')
for empty_section in ['site-footer__socials', 'site-footer__legal-links', 'site-footer__col--contact', 'site-footer__col--services']:
    assert empty_section not in home, f'Default site unexpectedly shows {empty_section}'
assert 'site-header__cta' in home and 'href="/contact"' in home
with urllib.request.urlopen('http://127.0.0.1:8765/de/') as response:
    german = response.read().decode('utf-8')
assert 'Kontakt aufnehmen' in german and 'href="/de/contact"' in german
for path in ['/missing-page', '/de/fehlende-seite']:
    try:
        urllib.request.urlopen('http://127.0.0.1:8765' + path)
        raise AssertionError(f'{path} should return 404')
    except urllib.error.HTTPError as error:
        assert error.code == 404, (path, error.code)
print('Clean starter HTTP routes passed.')
PY
    if command -v npx >/dev/null 2>&1; then
        npx --yes --package @playwright/cli playwright-cli open http://127.0.0.1:8765/
        npx --yes --package @playwright/cli playwright-cli run-code --filename "$root/scripts/browser-smoke.js"
        npx --yes --package @playwright/cli playwright-cli run-code --filename "$root/scripts/axe-audit.js"
        npx --yes --package @playwright/cli playwright-cli close
        if [ -n "${CRISPFRAME_MAILPIT_API:-}" ]; then
            python3 - <<'PY'
import json
import os
import urllib.request
with urllib.request.urlopen(os.environ['CRISPFRAME_MAILPIT_API']) as response:
    messages = json.load(response)['messages']
assert any(message['Subject'] == 'Website inquiry' and
           any(recipient['Address'] == 'contact@example.invalid' for recipient in message['To'])
           for message in messages), 'Contact mail not found in Mailpit'
print('Contact delivery passed in Mailpit.')
PY
        fi
    else
        printf 'npx is unavailable; browser check requires Node.js.\n'
    fi
fi
