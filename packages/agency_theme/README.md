# Crispframe Agency Theme

[![Packagist version](https://img.shields.io/packagist/v/crispframe/agency-theme?label=Packagist)](https://packagist.org/packages/crispframe/agency-theme)
![TYPO3 13.4 and 14.3](https://img.shields.io/badge/TYPO3-13.4%20%7C%2014.3_LTS-f49700)
[![License: GPL-2.0-or-later](https://img.shields.io/badge/license-GPL--2.0--or--later-blue)](LICENSE)
[![Release checks](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml/badge.svg)](https://github.com/PhantomPixelDev/crispframe/actions/workflows/ci.yml)

A reusable corporate site package for **TYPO3 13.4 and 14.3 LTS**. Build a services, product, or organization website with editable Content Blocks, four style palettes, and English/German interface labels. The theme has no build step and does not import demo content into an existing site. New starter sites use TYPO3 14.3.

## Preview

![Crispframe demo homepage at desktop width](Documentation/Images/home-desktop.webp)

| Mobile homepage | Editable pricing block |
| --- | --- |
| <img src="Documentation/Images/home-mobile.webp" alt="Crispframe demo homepage at mobile width" width="280"> | <img src="Documentation/Images/pricing-block.webp" alt="Three pricing tiers in the Crispframe demo" width="640"> |

| Work page | Contact page |
| --- | --- |
| <img src="Documentation/Images/work-desktop.webp" alt="Work page with project photography" width="640"> | <img src="Documentation/Images/contact-desktop.webp" alt="Contact page with meeting space photography" width="640"> |

![German case study with the image on the left and an editable project narrative](Documentation/Images/case-study-de-desktop.webp)

| Services page | About page |
| --- | --- |
| <img src="Documentation/Images/services-desktop.webp" alt="Services page with an editable comparison and timeline" width="640"> | <img src="Documentation/Images/about-desktop.webp" alt="About page with team photography and principles" width="640"> |

These screenshots show the [optional demo package](https://github.com/PhantomPixelDev/crispframe-agency-demo). Its branding, copy, photos, and prices are examples that you can edit in TYPO3.

## What is included

- **19 Content Blocks:** hero, intro, text/image, features, services, stats, logos, testimonials, projects, team, FAQ, CTA, contact, process, pricing, video, gallery, comparison, and timeline.
- **Site settings:** branding, contact details, navigation and footer links, CTAs, content width, typography, corners, spacing, sticky header, and ocean/forest/plum/ember palettes.
- **Publishing basics:** responsive PageView layouts, a branded 404, SEO metadata and structured data, language switcher, keyboard-friendly interactions, and reduced-motion support.
- **Icon choices:** a curated, locally bundled [Lucide](https://lucide.dev/) selection for services and features, plus custom SVG upload. Existing icon identifiers remain available; no icon CDN or JavaScript package is needed at runtime.
- **Contact form:** TYPO3 Form Framework definition with editable recipient overrides. Mail transport and real addresses are set by the site owner.

## Get started

In a TYPO3 13.4.15+ or 14.3.7+ Composer project, install the theme from [Packagist](https://packagist.org/packages/crispframe/agency-theme):

```bash
composer require crispframe/agency-theme:^1.3
```

Add the **Crispframe Agency Theme** Site Set under Admin → Site Management → Sites → *Your site* → Sets. Then follow the [first-run checklist](Documentation/FirstRun.md) to set branding, contact recipients, legal links, and SEO details.

For a **new empty site**, the [starter project](https://github.com/PhantomPixelDev/crispframe/tree/main/starter) and [optional demo package](https://packagist.org/packages/crispframe/agency-demo) provide an editable English/German page tree with examples of every block:

```bash
composer require crispframe/agency-demo:^1.3
vendor/bin/typo3 extension:setup --extension=agency_demo
```

The demo uses TYPO3's initialisation mechanism and should be installed only on a fresh site. The theme alone installs without example pages or site-specific configuration.

## Requirements

- TYPO3 13.4.15+ or 14.3.7+ (core, form, fluid-styled-content, rte-ckeditor)
- PHP 8.2+
- `friendsoftypo3/content-blocks` ^1.6 on TYPO3 13 or ^2.4 on TYPO3 14

Composer installs these extensions automatically through this package's requirements. `ext_emconf.php` declares the same required extensions for classic TYPO3 installations.

The Site Set includes TYPO3's Form Framework and SEO sitemap sets (`typo3/form`, `typo3/seo-sitemap`). Create your own site configuration with its base URL, root page, and languages. See the [page recipes](Documentation/PageRecipes.md) for services, product, and organization layouts.

For maintainers, [Release.md](Documentation/Release.md) describes clean-checkout verification, tags and Packagist publication. [Accessibility.md](Documentation/Accessibility.md) records the automated scope and launch checks.

## Contact form

The package includes `Resources/Private/Forms/Contact.form.yaml`. On a Contact page, add a **Form** content element and select **Contact inquiry**. The form ships with name, optional company, email and message fields, validation, email delivery and a confirmation message.

Before accepting live inquiries, edit the Form content element's finisher overrides: set the receiver address and sender address to addresses for your own domain. The bundled `example.invalid` addresses are safe placeholders. Configure TYPO3's mail transport for your installation; the demo can use Mailpit. The form definition remains read-only inside the extension, so an update cannot overwrite site-specific form content or finisher overrides. The Contact Content Block displays address and phone details; it is independent of the form.

## Site Set activation

The Site Set lives at `Configuration/Sets/SitePackage/`:

- `config.yaml` — set `crispframe/agency-theme`, depends on `typo3/fluid-styled-content`, `typo3/form`, `typo3/seo-sitemap`
- `settings.definitions.yaml` / `settings.yaml` — brand, contact, social, footer (`footer.servicesParent` — page picker that retains existing stored UIDs; 0 disables Services column), CTA page pickers and legacy URLs, style presets
- `setup.typoscript` — PageView paths, rendering (Default/Landing/Minimal), menus (`menuMain`, `menuServices` via `footer.servicesParent`, `breadcrumb` rootline), meta fallbacks (description ← page field → brand tagline → company name, `og:site_name` ← company name, `og:type` website, `twitter:card` summary, `theme-color` `#0f172a`), Form + SEO canonical/sitemap via `typo3/seo-sitemap`
- `page.tsconfig` — backend layouts (Default, Landing hero+main, Minimal), RTE preset, wizard

All brand/URL data comes from **Site Settings** — no hardcoded company URLs or page UIDs. Canonical URLs are provided by `typo3/seo` (no hand-rolled canonical). XML sitemap is available via the `seo` site set (see Documentation/SeoSetup.md).

## Dev workflow

No build step. Edit and reload:

- CSS: `Resources/Public/Css/` — tokens, base, layout, components, utilities, theme presets, form, block and visual refresh styles (loaded by the PageView layout)
- JS: `Resources/Public/JavaScript/` — `main.js` (nav, skip-link, year, sticky), `accordion.js`, `pricing.js`, `video.js` and `gallery.js`
- Icons: `Resources/Public/Icons/sprite.svg` — referenced through TYPO3's public asset URL by the icon partial
- Fluid: `Resources/Private/PageView/{Layouts,Pages,Partials/}` — layouts `Default`/`Landing`/`Minimal`, partials `Site/Header`, `Site/Navigation`, `Site/Footer`, `Components/*`

Clear caches after TypoScript or settings changes: `vendor/bin/typo3 cache:flush`.

## Directory tree

```
agency_theme/
├── composer.json
├── ext_emconf.php / ext_localconf.php
├── Configuration/
│   └── Sets/SitePackage/
│       ├── config.yaml
│       ├── settings.definitions.yaml
│       ├── settings.yaml
│       ├── setup.typoscript
│       └── page.tsconfig
├── ContentBlocks/ContentElements/
│   ├── hero / intro / text-image / feature-grid / services / stats
│   ├── logo-cloud / testimonials / projects / team / faq / cta / contact / process
│   ├── pricing / video / gallery
│   │   ├── config.yaml
│   │   └── templates/frontend.html
├── Resources/
│   ├── Private/PageView/
│   │   ├── Layouts/Default.html
│   │   ├── Pages/{Default,Landing,Minimal}.html
│   │   └── Partials/{Site/*,Components/*}
 │   └── Public/
 │       ├── Css/{tokens,base,layout,components,utilities,themes,forms,blocks}.css
 │       ├── JavaScript/{main,accordion,pricing,video,gallery}.js
 │       └── Icons/sprite.svg
 └── Documentation/
       ├── HomepageDemo.md
       └── SeoSetup.md  — sitemap.xml, robots.txt, hreflang/language-menu wiring
```

## Content Block editing

Each block is a Content Block (`crispframe/*`) with `config.yaml` fields:

- Common: `sectionSpacing` (small/default/large), `sectionBackground` (default/subtle/dark/brand), `width` (narrow/default/wide/full)
- Hero: `eyebrow`, `headline`, `subheadline`, `primaryLink`/`secondaryLink`, `image`, `isHero` (check **only** on first hero for single h1)
- Collections: `services`, `feature-grid`, `stats`, `logo-cloud`, `projects`, `team`, `testimonials`, `faq`, `process`, `pricing` — editor-controlled items, titles and copy
- Services and feature cards: choose a bundled icon or upload an SVG per item. Uploaded artwork takes precedence; leave both fields empty for no icon.
- Pricing: add 2–4 tiers with monthly and yearly prices, features and CTA links. The monthly price is visible without JavaScript; the yearly toggle appears when JavaScript is available. Enter display prices and suffixes explicitly, including currency and billing interval. Enable **Hide billing suffix** on quote-based tiers.
- Video: choose YouTube or Vimeo, enter the video ID, and optionally add a local 16:9 poster, caption and plain-text transcript. The external iframe is created only when a visitor clicks Play. Embed playback still uses the provider's own privacy and cookie behavior; configure consent for your deployment as needed.
- Gallery: add 2–12 images with captions and meaningful alternative text. Thumbnails link to the image when JavaScript is unavailable; the lightbox supports Escape, arrow keys and focus return.
- Accessibility: headings are h2; cards use h3; images have `alt` + `loading`/`decoding` + width/height; FAQ uses native `details/summary`

See `Documentation/HomepageDemo.md` for a complete homepage order with realistic copy.

## Theme settings

Site Settings → Crispframe Agency Theme:

- **Brand:** `brand.companyName`, `brand.tagline`, `brand.logo` (file), `brand.logoAlt`
- **Contact:** `contact.email`, `contact.phone`, `contact.address`
- **Social:** `social.linkedin`, `social.github`, `social.x`, `social.instagram`, `social.youtube` (link, placeholder `#`)
- **Footer:** `footer.text`, `footer.legalLink`, `footer.privacyLink`, `footer.servicesParent` (int UID, 0 = disabled — children of this page populate the Services column; hidden when 0), `footer.showCta`, `footer.ctaHeading`, `footer.ctaText`
- **CTA:** `cta.primaryLabel`/`cta.primaryLink`, `cta.secondaryLabel`/`cta.secondaryLink`
- **Styles:** `styles.palette` (ocean/forest/plum/ember), `styles.contentWidth` (compact/standard/wide), `styles.typeScale` (standard/expressive), `styles.corners` (sharp/soft/round), `styles.spacing` (compact/balanced/airy), `styles.stickyHeader` (on/off)
- **Header CTA:** `cta.showHeader` (on/off), plus `cta.primaryLabel` and `cta.primaryLink`

In Fluid: `{site.settings.brand.companyName}`, `{site.settings.contact.email}`, etc. Menu comes from `pageview` `MenuProcessor` as `{menuMain}` (levels 2). Footer Services column uses `{menuServices}` sourced from `footer.servicesParent`. Breadcrumbs use `{breadcrumb}` (rootline 0|-1) rendered via `Components/Breadcrumb` on Default/Minimal pages.

## SEO baseline

- **Meta:** `setup.typoscript` `page.meta` emits `description` (page field → tagline → company name), `og:site_name` (company name), `og:type` website, `twitter:card` summary, `theme-color` `#0f172a`, `viewport`. Page `seo_title`/`og_image`/`twitter_*` fields from `typo3/seo` are rendered by the core MetaTagGenerator. No marketing copy is hardcoded.
- **Canonical:** provided by `typo3/seo` CanonicalGenerator (no manual `<link rel="canonical">`). Respects `pages.canonical_link` and `no_index`.
- **Sitemap:** `typo3/seo` XML sitemap at `?type=1533906435` / `sitemap.xml` (route via site config). Enable the **SEO Sitemap** site set or ensure `typo3/seo-sitemap` is in your site set dependencies (this theme already depends on it). See `Documentation/SeoSetup.md` for route/robots notes.
- **JSON-LD:** `Layouts/Default.html` emits `Organization` (name, url, email, telephone, address, sameAs) guarded by `companyName` with empty-safe skips and JS-escaped values. `ContentBlocks/faq` emits `FAQPage` from its items. `Partials/Components/Breadcrumb.html` emits `BreadcrumbList` whenever breadcrumbs render. All scripts are `f:if` guarded to avoid empty blocks.
- **Robots / hreflang:** the theme includes a language menu and English/German labels; configure language bases, `robots.txt` and hreflang in your site's configuration. The optional starter includes `/de/`. See `Documentation/SeoSetup.md`.

## No build step

- No npm, no bundler, no webfonts, no icon libs beyond `sprite.svg`.
- System fonts via `tokens.css` (`--font-sans`/`--font-mono`).
- BEM-lite class names, CSS custom properties for theming.
- JS is vanilla and defer-safe.

## Contribution

- Branch from `main`, keep changes minimal and BEM-lite consistent.
- Do not hardcode URLs/UIDs; use site settings or `#`/`/` placeholders.
- Preserve h1-once, h2/h3 hierarchy, `aria-*` on nav/mobile, `loading`/`decoding` on images, `prefers-reduced-motion` and `:focus-visible`.
- Verify: `vendor/bin/typo3 content-blocks:lint`, `node --check` on JS, CSS total < 65 KB, no `TODO`/`lorem` placeholders and no upload-path hardcodes.

## License

GPL-2.0-or-later.
