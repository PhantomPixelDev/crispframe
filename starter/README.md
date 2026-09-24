# Crispframe starter

This is a clean TYPO3 14.3 Composer project. It requires the reusable theme without a local path repository. Copy this directory to a new project and run `composer install` once the tagged package is available on Packagist. The same theme and demo packages also support TYPO3 13.4.15 or newer; use the 13.4 constraints in your own root project if you are staying on that LTS.

1. Point the web server at `public/`, open the TYPO3 installer, and create an admin user and database.
2. On a fresh empty installation, optionally run `composer require crispframe/agency-demo:^1.4` followed by `vendor/bin/typo3 extension:setup --extension=agency_demo`. This imports editable sample pages and a bilingual site configuration.
3. To start without sample content, create a root page and a site configuration in the TYPO3 backend, then add the `crispframe/agency-theme` Site Set. Copy the 404 handler and language entries from `config/sites/main/config.yaml.example` if useful.
4. Complete the [first-run checklist](../packages/agency_theme/Documentation/FirstRun.md) before making the site public.

The demo package is intended for empty installations. Never install it into an existing production site.
