#!/bin/sh
set -eu

# Keep TYPO3's writable tree on the Linux volume, even when the project is
# bind mounted from Windows. A clean checkout has no var path yet.
if [ ! -e /app/var ]; then
    ln -s /data/var /app/var
fi

exec /entrypoint supervisord
