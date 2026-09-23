# Release procedure

The theme (`crispframe/agency-theme`) and optional example pages (`crispframe/agency-demo`) are separate Composer packages. Tag and publish each package from its own distribution repository, with the package's `composer.json` at the repository root. Both use GPL-2.0-or-later. The starter project requires the theme but does not require the demo.

1. Run the checks in `.github/workflows/ci.yml` and confirm the clean starter install, Content Blocks lint, browser smoke, Mailpit delivery and axe audit pass. The local equivalent is `php scripts/check-static.php`, `sh scripts/clean-install.sh`, and the Playwright CLI scripts against the Podman demo.
2. Review the optional example content for fictional names, prices, image rights and placeholder email addresses. Do not package site credentials, `config/system/settings.php`, runtime caches or uploaded files from the development project.
3. Tag the theme and demo with the version in their `ext_emconf.php` files (`v1.1.0` for this refresh) in their distribution repositories. Register the repositories on Packagist. Do not claim a new version is available there until the package pages resolve.
4. From a fresh checkout of `starter/`, run `composer install` using public package resolution. Install TYPO3 and optionally require `crispframe/agency-demo:^1.0` on a new empty site. Edit branding, contact recipients, legal pages and a German content record in the backend; test delivery and publish a page in both languages.
5. Only after those checks pass, announce the release. For later changes, update the package version and changelog, rerun the same checks, and tag a new release. Never reimport the optional demo over edited production records.

The test script builds temporary archive packages at the upcoming version solely to prove Composer dependency resolution before public tags exist. It does not modify the source package manifests or substitute for the final Packagist checkout.
