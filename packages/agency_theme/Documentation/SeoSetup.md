# SEO Setup — sitemap.xml, robots.txt, hreflang / language menu

This theme provides a **technical SEO baseline** via the `typo3/seo` system extension. No additional composer package is required. The theme includes English and German interface labels and a language switcher. Site owners configure the actual languages and translate editorial records.

## Site Set dependencies

`Configuration/Sets/SitePackage/config.yaml` depends on:

```yaml
dependencies:
  - typo3/fluid-styled-content
  - typo3/form
  - typo3/seo
```

`typo3/seo` provides: page fields (`seo_title`, `description`, `og_*`, `twitter_*`, `canonical_link`, `no_index`/`no_follow`), canonical generation, MetaTag API, and XML sitemap. The theme's `setup.typoscript` adds `page.meta` fallbacks and JSON-LD; it does **not** hand-roll canonical URLs.

After changing Site Set dependencies or settings, flush caches:

```bash
vendor/bin/typo3 cache:flush
```

## sitemap.xml

### How it works

- `typo3/seo` registers a PAGE `seo_sitemap` with `typeNum = 1533906435` (`Configuration/TypoScript/XmlSitemap/setup.typoscript` inside the extension).
- Available at `https://example.org/sitemap.xml` when the site config routes the type to a speaking URL, or at `https://example.org/?type=1533906435` without a route.
- Provider: `PagesXmlSitemapDataProvider` respects `pages.no_index = 0`, `canonical_link = ''`, `doktype` exclusions (`3,4,6,7,199,254`), `excludePagesRecursive` and `additionalWhere`.

### Integrator steps

1. **Enable the SEO set** — already satisfied via `config.yaml` dependency. If you fork the set, ensure you also include `typo3/seo` or `typo3/seo-sitemap` where applicable.
2. **Route `sitemap.xml`** in your site configuration (`config/sites/<identifier>/config.yaml`):

```yaml
routes:
  -
    route: sitemap.xml
    type: uri
    source: 't3://page?uid=1&type=1533906435'
```

Or use the core site-set `typo3/seo-sitemap` which ships its own route example. Verify in Site Management → Sites → *site* → Sitemap tab.

3. **Verify**: `curl -I https://example.org/sitemap.xml` → `Content-Type: application/xml`, `X-Robots-Tag: noindex`. The sitemap itself must not be indexed.
4. **Exclude pages**: set `no_index` in page properties → SEO tab, or add page UIDs to `seo.sitemap.pages.excludePagesRecursive` in `settings.definitions.yaml`.
5. **Scheduling**: sitemap is cached 900s by default; it reflects live `pages` state (no cron needed). For large sites, consider a warmup.

### Integrator customisation

- Override `seo.sitemap.pages.additionalWhere` via Site Settings if you need custom filtering.
- Provide a custom XSL via `seo.sitemap.view.*` or `plugin.tx_seo.view.*` paths.

## robots.txt

TYPO3 core serves `robots.txt` via site configuration **static routes** (not via the theme). Example `config/sites/<identifier>/config.yaml`:

```yaml
routes:
  -
    route: robots.txt
    type: staticText
    content: |
      User-agent: *
      Allow: /
      # Disallow search, admin, and sitemap XSL if needed
      # Disallow: /typo3/
      Sitemap: https://example.org/sitemap.xml
```

Adjust per environment (staging: `Disallow: /`). The theme does **not** ship a physical `robots.txt`; integrators add the route in their site config so it stays deploy-specific.

Verify: `curl https://example.org/robots.txt` and ensure the `Sitemap:` line points to the canonical sitemap URL.

## hreflang & language menu (multilingual)

The theme includes a language switcher driven by `LanguageMenuProcessor`. The optional demo configures English at `/` and German at `/de/`.

### 1. Site configuration

Add languages in `config/sites/<identifier>/config.yaml` (or via Site Management → Languages). Each language gets a `hreflang` (e.g. `en-US`, `de-DE`), `locale`, `base`, and `flag`.

### 2. Hreflang

`typo3/seo` automatically emits `<link rel="alternate" hreflang="...">` via `HrefLangGenerator` when multiple site languages exist and `canonical_link` is not forcing a single URL. No TypoScript needed.

Verify in page source: `<link rel="alternate" hreflang="de" href="https://example.org/de/...">` plus `x-default`.

### 3. Visible language switcher

The header renders only configured languages that have an available page translation. If a site uses one language, the switcher is hidden. Translate each page and its content in the TYPO3 backend; use the Page module's localization actions to keep records connected.

### 4. SEO implications

- Each translation needs its own `seo_title`/`description` (translated page record).
- `canonical_link` per language is language-aware; don't set a cross-language canonical manually.
- Test with `curl` and Google Search Console's hreflang validator.

## Verification checklist

- [ ] `vendor/bin/typo3 cache:flush` → exit 0, no TypoScript errors.
- [ ] Page source contains: `<meta name="description">`, `<meta property="og:site_name">`, `<meta property="og:type" content="website">`, `<meta name="twitter:card" content="summary">`, `<meta name="theme-color">`, `<link rel="canonical">` (from `typo3/seo`), and viewport.
- [ ] `…/sitemap.xml` returns XML with page URLs (no `no_index` or `canonical_link` pages).
- [ ] `/robots.txt` references `Sitemap:` correctly.
- [ ] JSON-LD `Organization` present site-wide (view source, guarded by companyName), `FAQPage` on FAQ block, `BreadcrumbList` on Default/Minimal pages with breadcrumbs.
- [ ] No empty meta content, no empty JSON-LD blocks, no empty footer Services column when `footer.servicesParent = 0`.
