# Crispframe demo — editable English and German pages

[![Packagist](https://img.shields.io/packagist/v/crispframe/agency-demo?label=release)](https://packagist.org/packages/crispframe/agency-demo)
[![License](https://img.shields.io/badge/license-GPL--2.0--or--later-blue)](LICENSE)

An optional starting point for the [Crispframe TYPO3 theme](https://github.com/PhantomPixelDev/crispframe-agency-theme): example pages, original demo photography, translated records, and practical combinations of all **27 Content Blocks**.

**[Explore the live demo →](https://dev-crispframe.ppxl.dev/)** · [Screenshot gallery](https://github.com/PhantomPixelDev/crispframe-agency-theme/blob/main/Documentation/Screenshots.md) · [New-site starter](https://github.com/PhantomPixelDev/crispframe/tree/main/starter)

![Crispframe homepage preview](https://raw.githubusercontent.com/PhantomPixelDev/crispframe-agency-theme/main/Documentation/Images/home-desktop.webp)

## Install on a new, empty site

Install the theme first, or start from the [starter project](https://github.com/PhantomPixelDev/crispframe/tree/main/starter). Then:

```sh
composer require crispframe/agency-demo:^1.6
vendor/bin/typo3 extension:setup --extension=agency_demo
vendor/bin/typo3 cache:flush
```

TYPO3 Initialisation imports the page tree, example files, and site configuration. Set the site base URL to your own domain, then follow the [first-run checklist](https://github.com/PhantomPixelDev/crispframe-agency-theme/blob/main/Documentation/FirstRun.md).

**Do not import this package over an existing site.** It is a starting point, not an update mechanism for edited content. Existing sites can install the theme alone.

## What is included?

| Pages | What they demonstrate |
| --- | --- |
| Home, Services, About | Hero layouts, services, features, proof, and calls to action |
| Work and two case studies | Project cards, photography, and editable long-form narratives |
| Contact and Request a project | Contact details and two TYPO3 Form Framework presets |
| Insights and two articles | Automatic child-page teasers, pull quotes, author cards, and an optional sidebar |
| Resources and Components | Tabs, curated links, pricing, video, gallery, and additional block examples |
| Locations and four service detail pages | Office cards, callouts, section navigation, and a two-level page tree |
| Components → Style variants | Editable examples of every Hero, Services, Features, Projects, Testimonials, and CTA presentation in both languages |

Editorial records have English/German versions. Internal links use TYPO3 page references. Images are imported as normal TYPO3 files with editable alternative text.

## Before publishing

Replace fictional names, contact details, prices, links, legal pages, form recipients, and SEO text. Configure mail transport and verify a submission. Replace or remove demo photographs as appropriate for your organization.

The import contains no backend users or credentials. You create your own administrator during TYPO3 setup. The reusable theme does not import these pages or install the demo photographs into your site.

The [live development demo](https://dev-crispframe.ppxl.dev/) can include updates ahead of the latest Composer release.

## Compatibility and license

Requires the Crispframe theme and its supported TYPO3 versions: 13.4.15+ or 14.3.7+, within those major versions. See [composer.json](composer.json) for exact constraints.

[GPL-2.0-or-later](LICENSE). For bugs, include your package versions and import steps in a [GitHub issue](https://github.com/PhantomPixelDev/crispframe-agency-demo/issues).
