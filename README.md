# crispframe

Monorepo for the Crispframe TYPO3 theme.

## Packages

- `packages/agency_theme/` — reusable GPL theme for TYPO3 13.4, with 17 Content Blocks and English/German labels. See [`packages/agency_theme/README.md`](packages/agency_theme/README.md).
- `packages/agency_demo/` — optional editable bilingual example pages for a new empty site.
- `starter/` — Composer project without a local path repository. See [`starter/README.md`](starter/README.md).

The release workflow validates syntax, Content Blocks, a fresh Composer archive install, TYPO3 setup and browser behavior. Locally, run `podman compose exec -T web php scripts/check-static.php` and `podman compose exec -T web sh scripts/clean-install.sh`. The browser smoke script can be run with Playwright CLI against the local demo.

## Fast local Podman setup on Windows

The Compose setup bind mounts the source tree for live edits. Composer packages (`/app/vendor`) and TYPO3's SQLite database, caches and logs (`/app/var`, linked to the `/data/var` volume) live in Podman named volumes inside the Linux VM. This avoids repeated small-file access across the Windows/WSL filesystem boundary. The first Composer install needs network access; later starts reuse the volumes.

```powershell
podman machine start
podman compose up -d
podman compose exec web composer install --no-interaction
```

Open `http://localhost:8080/`. The local Mailpit inbox is at `http://localhost:8026/`; the Compose stack routes form email there for testing. `podman compose stop` preserves the database and dependencies; `podman compose up -d` starts them again. Use `podman compose exec web vendor/bin/typo3 cache:flush` after changing Site Set settings or TypoScript. If port 8080 is occupied, set `CRISPFRAME_HTTP_PORT` before `podman compose up -d` and set the demo site's base URL to match. Set `CRISPFRAME_MAILPIT_PORT` if port 8026 is occupied. Keep Composer and TYPO3 CLI commands inside the container so generated package paths point to `/app/vendor`.

For a fresh TYPO3 installation, follow the TYPO3 web installer to create its database, admin user, root page and site configuration. These local install details are outside the reusable theme package. The Compose setup does not overwrite an existing database volume.

## Local demo

With TYPO3 installed and root page 1 created, run `podman compose exec web vendor/bin/typo3 cache:flush`, `podman compose exec web vendor/bin/typo3 extension:setup --extension=agency_theme --no-interaction`, then the local demo helpers in this order: `php config/seed-demo.php`, `php config/seed-gallery.php`, `php config/localize-demo.php`, and `php config/seed-photography.php` inside the web container. Flush the cache afterward. The helpers add editable Home, Work, Contact and a hidden Components page, plus localized gallery and hero images. Existing records are not reimported by the optional distribution package. The demo is served at `http://localhost:8080/`; inspect Pricing, Video and Gallery at `http://localhost:8080/components`. The optional distribution package uses TYPO3 Initialisation instead of these development helpers.

The seed script and this demo site's URL, branding and database are development examples. Installing `crispframe/agency-theme` in another TYPO3 project does not create pages or copy those site-specific values.
