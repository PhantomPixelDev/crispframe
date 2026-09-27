# Start a new Crispframe website

A TYPO3 **14.3** Composer project using the public [Crispframe theme](https://github.com/PhantomPixelDev/crispframe-agency-theme). Choose an empty site or add the optional editable English/German demo.

## 1. Create the project

Copy this `starter/` directory into your own project folder. Then run:

```sh
composer install
```

Use a PHP environment, database, and web server supported by TYPO3 14.3. Point the web server's document root to **`public/`**. Docker is optional; the repository's [development guide](https://github.com/PhantomPixelDev/crispframe/blob/main/DEVELOPMENT.md) covers Docker Compose.

## 2. Install TYPO3

Open your site's URL and follow the TYPO3 installer to configure the database and create your own backend administrator. Keep the generated credentials and system configuration private. There is no shared demo administrator password.

## 3. Choose your starting point

### Editable demo pages

On a **fresh, empty installation**:

```sh
composer require crispframe/agency-demo:^1.5
vendor/bin/typo3 extension:setup --extension=agency_demo
vendor/bin/typo3 cache:flush
```

The demo imports English/German pages, images, forms, and an example site configuration. Set the site base URL to your own domain and check the language URLs. Do not install the demo over existing content.

### Empty site

1. Create a root page and a site configuration in the TYPO3 backend.
2. Add the **Crispframe Agency Theme** Site Set (`crispframe/agency-theme`).
3. Select a Crispframe backend layout in page properties.
4. Add content elements and configure branding in Site Settings.

The [site configuration example](config/sites/main/config.yaml.example) shows language entries and a 404 handler. Replace example values with the correct domain and page IDs.

## 4. Make it yours

Follow the [first-run checklist](https://github.com/PhantomPixelDev/crispframe-agency-theme/blob/main/Documentation/FirstRun.md):

- Replace branding, example copy, photographs, and prices.
- Choose navigation, CTA, privacy, and legal pages.
- Set form recipients and production mail transport; test delivery.
- Translate your editorial records and check metadata.
- Preview mobile and desktop before publishing.

The theme and demo also support TYPO3 13.4.15+. This starter targets TYPO3 14.3; use a TYPO3 13 project with compatible root Composer constraints if you need that version.
