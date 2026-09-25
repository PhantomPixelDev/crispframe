#!/bin/sh
set -eu

# Keep TYPO3's writable tree on the managed container volume when the project
# source is bind mounted from the host. A clean checkout has no var path yet.
if [ ! -e /app/var ]; then
    ln -s /data/var /app/var
fi

exec /entrypoint supervisord
