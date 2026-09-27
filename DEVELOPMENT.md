# Developing Crispframe

This repository contains the theme source, optional demo, and starter. To use Crispframe on your own site, start with the [installation guide](packages/agency_theme/README.md#installation).

## Local development with Docker Compose

The included [`compose.yaml`](compose.yaml) works with Docker Compose on Linux, macOS, and Windows. It starts TYPO3 with PHP 8.3 and Apache, plus Mailpit for local email testing.

### Requirements

- Docker Engine with the Compose plugin, or Docker Desktop
- Git
- Free local ports `8080` and `8026`

Clone the repository and start the stack:

```shell
git clone https://github.com/PhantomPixelDev/crispframe.git
cd crispframe
docker compose up -d
docker compose exec --user application web composer install --no-interaction
docker compose restart web
```

Open the site at [http://localhost:8080/](http://localhost:8080/) and Mailpit at [http://localhost:8026/](http://localhost:8026/). On the first run, use TYPO3's web installer to create the SQLite database and backend administrator. A later `docker compose stop` keeps the database and Composer dependencies; `docker compose up -d` starts the same environment again.

Run Composer and TYPO3 commands inside the `web` container so paths and PHP extensions match the application environment:

```shell
docker compose exec web vendor/bin/typo3 cache:flush
docker compose exec web composer update crispframe/agency-theme --with-dependencies
```

The source tree is bind mounted for live editing. Composer packages use the `crispframe-vendor` named volume, while TYPO3's SQLite database, caches, and logs use `crispframe-var`. Keeping these small-file workloads in managed volumes improves performance on Docker Desktop and Podman Machine without changing the workflow on native Linux.

### Podman Compose

Podman is compatible with the same stack. Replace `docker compose` with `podman compose` in the commands above. On macOS and Windows, start the Podman virtual machine first:

```shell
podman machine start
podman compose up -d
podman compose exec web composer install --no-interaction
```

The repository uses the standard Compose specification, so no Podman-specific file is required.

### Ports and persistent data

Create a local `.env` file beside `compose.yaml` when the default ports are already occupied:

```dotenv
CRISPFRAME_HTTP_PORT=8081
CRISPFRAME_MAILPIT_PORT=8027
```

Update the demo site's base URL when changing the HTTP port. Compose does not overwrite an existing database volume. To inspect the active services, use `docker compose ps`; to view startup errors, use `docker compose logs web`.

## Development checks

Run the static and clean-install checks with Docker Compose:

```shell
docker compose exec -T web php scripts/check-static.php
docker compose exec -T web sh scripts/clean-install.sh
```

Podman users can run the same commands by substituting `podman compose`. The browser smoke and accessibility scripts use Playwright CLI against the running local demo.

### VPS development override

[`compose.vps.yaml`](compose.vps.yaml) extends the local stack for the Crispframe development VPS. It removes published application ports, joins the shared `edge` network, persists TYPO3 system settings and uploads, sets the canonical development URL through `CRISPFRAME_BASE_URL`, and limits TYPO3's trusted reverse proxy and host configuration to the registered development host:

```shell
docker compose -f compose.yaml -f compose.vps.yaml up -d
```

The edge proxy serves the application at `https://dev-crispframe.ppxl.dev`. This override is intended for the registered Crispframe development host; other deployments should supply their own base URL and edge routing rather than editing the reusable theme package.

## Demo data and source layout

Use the optional demo package on a fresh installation when you want sample pages. The scripts under `config/seed-*` and `.dev/seed-*` are maintainer tools for the development fixture; they are not a safe update path for sites with edited content. Read their behavior before using them.

- `packages/agency_theme/` — Fluid templates, Content Blocks, Site Settings, and frontend assets.
- `packages/agency_demo/` — Initialisation export, example site configuration, and demo images.
- `starter/` — clean Composer project using public packages.
- `scripts/` — syntax, installation, browser, and accessibility checks.

## Refresh the README screenshots

Capture the real running demo with Playwright CLI. This does not import data or change server-side content:

```sh
npx --yes --package @playwright/cli playwright-cli open https://dev-crispframe.ppxl.dev/
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/readme-screenshots.js
python scripts/prepare-readme-images.py
```

The capture script waits for fonts and images, uses desktop/mobile viewports, and opens the actual menu controls. PNG originals go to `output/playwright/`; the conversion script requires Pillow and writes optimized WebP files to the theme documentation. Review the images before committing. Update the capture date in both READMEs and [the gallery](packages/agency_theme/Documentation/Screenshots.md).

## Before submitting changes

Run the relevant checks, preserve existing content/settings compatibility, and include reproduction steps or screenshots for UI changes. Use [the release procedure](packages/agency_theme/Documentation/Release.md) for package publication. Documentation updates do not require moving existing release tags.
