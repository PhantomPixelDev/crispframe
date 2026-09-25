#!/bin/sh
set -eu

# Keep TYPO3's writable tree on the managed container volume when the project
# source is bind mounted from the host. A clean checkout has no var path yet.
if [ ! -e /app/var ]; then
    ln -s /data/var /app/var
fi

# A hosted development stack can persist TYPO3's generated system settings in
# a named volume without committing credentials or environment-specific keys.
if [ -d /data/config ] && [ ! -e /app/config/system/settings.php ] && [ ! -L /app/config/system/settings.php ]; then
    ln -s /data/config/settings.php /app/config/system/settings.php
fi

# Composer creates the public entry point, while TYPO3's web installer normally
# writes this Apache rewrite file. Hosted clean checkouts need it before the
# installer or imported database can serve speaking URLs and the backend route.
if [ ! -f /app/public/.htaccess ] && [ -f /app/vendor/typo3/cms-install/Resources/Private/FolderStructureTemplateFiles/root-htaccess ]; then
    cp /app/vendor/typo3/cms-install/Resources/Private/FolderStructureTemplateFiles/root-htaccess /app/public/.htaccess
fi

exec /entrypoint supervisord
