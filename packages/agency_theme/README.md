# Crispframe — a clean corporate theme for TYPO3

[![Packagist](https://img.shields.io/packagist/v/crispframe/agency-theme?label=release)](https://packagist.org/packages/crispframe/agency-theme)
[![TYPO3](https://img.shields.io/badge/TYPO3-13.4%20%7C%2014.3-f49700)](#requirements)
[![Checks](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml/badge.svg)](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-GPL--2.0--or--later-blue)](LICENSE)

Build an editable corporate, agency, or organization website with **27 Content Blocks**, English/German labels, four palettes, and TYPO3's native editing tools.

**[Live demo →](https://dev-crispframe.ppxl.dev/)** · [All elements](https://dev-crispframe.ppxl.dev/components) · [Get started](#installation) · [Documentation](#documentation)

![Crispframe homepage with editorial typography, clear actions, and demo photography](Documentation/Images/home-desktop.webp)

## Why Crispframe?

- **Build pages in TYPO3.** Reorder blocks, edit content, choose icons, and replace images without modifying theme code.
- **Shape the design.** Configure palettes, typography, spacing, corners, page width, and header/footer variants through Site Settings.
- **Handle larger sites.** Use two-level dropdown or mega menus, mobile disclosure controls, breadcrumbs, and selectable footer page trees.
- **Publish in English and German.** Interface labels are translated; editorial content stays in normal TYPO3 records.
- **Keep assets local.** Bundled Plus Jakarta Sans, Lucide SVG icons, and vanilla JavaScript. No font or icon CDN and no frontend build step.
- **Start with or without examples.** The theme installs without importing demo pages. The optional demo is a separate package.

## Installation

### Add to an existing TYPO3 site

From your Composer project root:

```sh
composer require crispframe/agency-theme:^1.5
vendor/bin/typo3 extension:setup --extension=agency_theme
vendor/bin/typo3 cache:flush
```

Then:

1. In **Site Management → Sites**, add the **Crispframe Agency Theme** Site Set to your site. Its identifier is `crispframe/agency-theme`.
2. In page properties, select a Crispframe backend layout: **Default**, **Landing**, **Minimal**, or **Article**.
3. Add content through the content-element wizard. Use **Site Settings** for branding and shared navigation.
4. Complete the [first-run checklist](Documentation/FirstRun.md) before publishing.

### Start a new site with examples

Use the [TYPO3 14.3 starter project](https://github.com/PhantomPixelDev/crispframe/tree/main/starter). On a **new, empty installation**, add the optional demo:

```sh
composer require crispframe/agency-demo:^1.5
vendor/bin/typo3 extension:setup --extension=agency_demo
vendor/bin/typo3 cache:flush
```

The [demo package](https://github.com/PhantomPixelDev/crispframe-agency-demo) imports editable pages and example assets through TYPO3 Initialisation. Do not import it over an existing site or rerun imports to update edited content.

## Preview

| Mega navigation | Service cards |
| --- | --- |
| ![Desktop mega menu showing four service pages](Documentation/Images/mega-menu.webp) | ![Simple service cards with locally bundled icons](Documentation/Images/service-cards.webp) |

| Mobile navigation | Styled contact form |
| --- | --- |
| <img src="Documentation/Images/mobile-menu.webp" alt="Expanded service links in the mobile navigation" width="260"> | <img src="Documentation/Images/contact-form.webp" alt="Contact form with labeled fields, a spacious message area, and a submit button" width="720"> |

[View Work, Resources, Insights, pricing, and German case-study screenshots →](Documentation/Screenshots.md)

Captured from the live development demo on **27 September 2026**. The demo can include changes ahead of the latest tagged release. Branding, images, copy, and prices are editable examples; they are not imported by the theme.

## Content Blocks

| Build | Blocks |
| --- | --- |
| Introductions and conversion | Hero, Intro, Text/image, CTA |
| Services and proof | Services, Feature grid, Stats, Logo cloud, Testimonials, Projects, Team, Process |
| Media and decisions | Gallery, Video, Pricing, FAQ, Comparison, Timeline |
| Articles and resources | Child page teasers, Tabs, Pull quote, Resource list, Author card |
| Orientation and contact | Section navigation, Callout, Office locations, Contact |

The **Contact block** displays contact details. For an inquiry form, add a separate **Form** element and select one of the included presets.

The Article layout places an optional sidebar after the main content on small screens. Standard TYPO3 text, images, tables, file links, and menu elements can be used alongside the theme blocks. See the [page recipes](Documentation/PageRecipes.md) for practical combinations.

## Visual customization

Set these values in **Site Settings**; no CSS edit is required.

| Setting | Choices |
| --- | --- |
| Palette — `styles.palette` | `ocean`, `forest`, `plum`, `ember` |
| Type scale — `styles.typeScale` | `standard`, `expressive` |
| Content width — `styles.contentWidth` | `compact`, `standard`, `wide` |
| Corners — `styles.corners` | `sharp`, `soft`, `round` |
| Section rhythm — `styles.spacing` | `compact`, `balanced`, `airy` |
| Header — `styles.headerVariant` | `standard`, `compact`; sticky header is a separate switch |
| Footer — `footer.layout` | `full`, `minimal` |
| Submenus — `navigation.submenuLayout` | `dropdown`, `mega`; two rendered page levels |
| Breadcrumbs — `navigation.showBreadcrumbs` | Show or hide |

Additional settings cover company details, logo, English/German CTA labels, announcements, social links, and two footer page trees. CTA and legal page pickers take precedence over legacy URL fields and keep internal links language-aware.

Content elements also expose their own width, background, and spacing controls. Hero blocks support split, centered, background-media, and minimal layouts.

## Forms

Add a **Form** content element and select **Contact inquiry** or **Project inquiry**. Both use TYPO3 Form Framework. The project preset includes service, organization, optional budget and timing, contact details, consent, and a message.

Before accepting inquiries:

1. Set **finisher overrides** on the Form element for recipient and sender addresses.
2. Configure TYPO3's mail transport for your host.
3. Send a test submission and verify delivery and reply-to behavior.

The bundled `example.invalid` addresses are placeholders. Mailpit in the development stack captures test emails; it is not a production mail provider. The extension's form definitions should remain unchanged—use site-level overrides or your own form for custom questions.

## Requirements

| Dependency | Supported range |
| --- | --- |
| TYPO3 | `^13.4.15 || ^14.3.7` |
| Content Blocks | `^1.6 || ^2.4` — Composer selects the line compatible with TYPO3 |
| PHP and extensions | Must meet the requirements of your selected TYPO3 version |
| TYPO3 extensions | Form, Frontend, Fluid Styled Content, RTE CKEditor, SEO; declared in Composer |

Composer resolves the required extensions. The Site Set includes `typo3/fluid-styled-content`, `typo3/form`, and `typo3/seo-sitemap`. Hosting, database, mail delivery, and your site's base URL remain deployment settings.

Docker is optional. Contributors can use the [Docker Compose development guide](https://github.com/PhantomPixelDev/crispframe/blob/main/DEVELOPMENT.md); Podman Compose is also supported.

## SEO and accessibility

Crispframe supplies metadata fallbacks, TYPO3 core canonical URLs, sitemap integration, and Organization, FAQPage, and BreadcrumbList structured data. Editors provide page titles, descriptions, sharing images, and useful image alternative text.

Interactions include visible focus, keyboard-operated navigation and tabs, gallery focus return, native FAQ disclosure, and reduced-motion support. Final accessibility depends on your content and configuration; use the [accessibility checklist](Documentation/Accessibility.md) and [SEO setup guide](Documentation/SeoSetup.md) before launch.

## Updates and troubleshooting

Back up your database and uploads, review the release notes, then run:

```sh
composer update crispframe/agency-theme --with-dependencies
vendor/bin/typo3 extension:setup --extension=agency_theme
vendor/bin/typo3 cache:flush
```

Review TYPO3's schema changes before applying them. Existing editorial records and Site Settings remain in your site; updating the theme does not reimport the demo.

| Symptom | Check |
| --- | --- |
| Theme or blocks do not appear | Site Set is active, extension setup ran, page layout is selected, caches are flushed |
| Page looks unstyled | Browser Network panel: CSS/font requests must succeed; check asset publishing and host/proxy errors |
| Form does not deliver | Finisher addresses and TYPO3 mail transport; inspect the mail capture service in development |
| German link opens English | Prefer a page picker or TYPO3 page reference; ensure the target page has a translation |
| Submenu is missing | Parent has visible child pages; only two navigation levels are rendered |

For removal steps, see [First run: updating and removing](Documentation/FirstRun.md#removing).

## Documentation

- [First-run checklist](Documentation/FirstRun.md)
- [Page recipes](Documentation/PageRecipes.md)
- [Screenshot gallery](Documentation/Screenshots.md)
- [SEO setup](Documentation/SeoSetup.md)
- [Accessibility checks](Documentation/Accessibility.md)
- [Release procedure](Documentation/Release.md)
- [Source and development guide](https://github.com/PhantomPixelDev/crispframe)

[Report a bug](https://github.com/PhantomPixelDev/crispframe-agency-theme/issues) with your TYPO3/theme versions, reproduction steps, and a screenshot. Do not include credentials or private content.

## License

[GPL-2.0-or-later](LICENSE). Plus Jakarta Sans is bundled under the [SIL Open Font License](Resources/Public/Fonts/OFL-PlusJakartaSans.txt). Lucide attribution and license notices are included with the [local icon assets](Resources/Public/Icons/).
