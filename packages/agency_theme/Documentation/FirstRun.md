# First run: publish your own site

Use the theme alone for an existing site, or install `crispframe/agency-demo` on a **new empty site** to get editable English and German example pages. The demo is optional and should not be installed on a production site with content.

1. **Branding:** In Site Management → Sites → Settings, set the company name, tagline, logo and logo alternative text. Pick a palette, width, type scale, corners and spacing. Review the site title and each page title.
2. **Navigation:** Create your own visible pages. Check the main menu and language switcher. If the footer should list services, set `footer.servicesParent` to the parent page UID; leave it `0` to hide the column.
3. **Contact:** Set the contact email, phone and address. On the Form content element, enable finisher overrides and replace `contact@example.invalid` and `forms@example.invalid` with addresses you control. Set a sender address permitted by your mail provider.
4. **Mail:** Configure TYPO3's mail transport for the deployment. Send a real test inquiry and confirm delivery and reply-to behavior. The included Podman setup uses Mailpit only for local testing.
5. **Links:** Set the footer legal and privacy pages and any social links. Blank links, `#`, and the default `/` legal placeholders are hidden. Set real CTA links before enabling them in the header or footer.
6. **SEO:** Set each page's SEO title, description and sharing image. Verify canonical URLs, sitemap, robots rules, and language alternatives. See [SEO setup](SeoSetup.md).
7. **Content and publishing:** Replace every demo name, image, price and claim; check image rights and alternative text. Translate editorial records in TYPO3. Preview English and German on phone, tablet and desktop; check keyboard navigation, form errors, and the 404 page. Then remove `no_index` from pages intended for search.

## Updating

Run `composer update crispframe/agency-theme --with-dependencies` in your project, apply TYPO3 database schema updates, flush caches and review the changelog before publishing. Site Settings and editable page records live in the site, so package updates do not replace them. Back up the database and uploaded files before a major update.

## Removing

First replace Crispframe Content Blocks and page layouts on pages that use them, and remove the Crispframe Site Set from each site configuration. Remove the optional demo extension only after migrating its pages. Then run `composer remove crispframe/agency-theme` (and `composer remove crispframe/agency-demo` if installed), apply schema updates, and clear caches. Keep a database backup until the replacement site is verified.
