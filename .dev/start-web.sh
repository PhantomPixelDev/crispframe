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

exec /entrypoint supervisord
