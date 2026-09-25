# Crispframe TYPO3 corporate sitepackage

[![Theme release](https://img.shields.io/github/v/release/PhantomPixelDev/crispframe-agency-theme?display_name=tag&sort=semver)](https://github.com/PhantomPixelDev/crispframe-agency-theme/releases)
[![TYPO3 13 and 14](https://img.shields.io/badge/TYPO3-13.4%20%7C%2014.3_LTS-f49700)](packages/agency_theme/README.md)
[![CI](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml/badge.svg)](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-GPL--2.0--or--later-blue)](packages/agency_theme/LICENSE)

Modern open-source TYPO3 corporate website template and sitepackage for agencies, services companies, product teams, and organizations. Crispframe includes 24 editable Content Blocks, bilingual English/German labels, four visual palettes, responsive layouts, accessible vanilla JavaScript, SEO defaults, and a TYPO3 Form Framework contact flow.

![Crispframe modern TYPO3 corporate homepage](packages/agency_theme/Documentation/Images/home-desktop.webp)

## Packages

- `packages/agency_theme/` — reusable GPL theme for TYPO3 13.4 and 14.3, with 24 Content Blocks and English/German labels. See [`packages/agency_theme/README.md`](packages/agency_theme/README.md).
- `packages/agency_demo/` — optional editable bilingual example pages for a new empty site.
- `starter/` — Composer project without a local path repository. See [`starter/README.md`](starter/README.md).

The release workflow validates syntax, Content Blocks, a fresh Composer archive install, TYPO3 setup and browser behavior. The same checks can run in the development container; see [Development checks](#development-checks).

## Install the theme in an existing TYPO3 project

Docker is only used for this repository's local development environment. A normal TYPO3 installation can add Crispframe directly through Composer:

```shell
composer require crispframe/agency-theme:^1.4
vendor/bin/typo3 extension:setup --extension=agency_theme
```

Add the **Crispframe Agency Theme** Site Set to your site in the TYPO3 backend. For a new empty site, the optional `crispframe/agency-demo` package can import editable English and German example pages. See the [theme installation guide](packages/agency_theme/README.md#installation) and [starter project](starter/README.md).

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
docker compose exec web composer install --no-interaction
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

[`compose.vps.yaml`](compose.vps.yaml) extends the local stack for the Crispframe development VPS. It removes published application ports, joins the shared `edge` network, persists TYPO3 system settings and uploads, and sets the canonical development URL through `CRISPFRAME_BASE_URL`:

```shell
docker compose -f compose.yaml -f compose.vps.yaml up -d
```

The edge proxy serves the application at `https://dev-crispframe.ppxl.dev`. This override is intended for the registered Crispframe development host; other deployments should supply their own base URL and edge routing rather than editing the reusable theme package.

## Local demo

With TYPO3 installed and root page 1 created, prepare the theme and development demo inside the container:

```shell
docker compose exec web vendor/bin/typo3 extension:setup --extension=agency_theme --no-interaction
docker compose exec web php config/seed-demo.php
docker compose exec web php config/seed-gallery.php
docker compose exec web php config/localize-demo.php
docker compose exec web php config/seed-photography.php
docker compose exec web python3 .dev/seed-v12-demo.py
docker compose exec web python3 .dev/seed-v13-demo.py
docker compose exec web python3 .dev/seed-v14-demo.py
docker compose exec web vendor/bin/typo3 cache:flush
```

The helpers add editable Home, Work, Contact, Services, About, Insights, Resources, two Work case studies, two articles and a hidden Components page, plus localized gallery and hero images. Existing records are not reimported by the optional distribution package. Inspect Pricing, Video, and Gallery at [http://localhost:8080/components](http://localhost:8080/components). The optional distribution package uses TYPO3 Initialisation instead of these development helpers.

The seed script and this demo site's URL, branding and database are development examples. Installing `crispframe/agency-theme` in another TYPO3 project does not create pages or copy those site-specific values.
