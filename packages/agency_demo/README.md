# Crispframe TYPO3 Demo: bilingual corporate website examples

[![Demo release](https://img.shields.io/github/v/release/PhantomPixelDev/crispframe-agency-demo?display_name=tag&sort=semver)](https://github.com/PhantomPixelDev/crispframe-agency-demo/releases)
[![Packagist](https://img.shields.io/packagist/v/crispframe/agency-demo?label=Packagist)](https://packagist.org/packages/crispframe/agency-demo)
[![License: GPL-2.0-or-later](https://img.shields.io/badge/license-GPL--2.0--or--later-blue)](LICENSE)

Optional bilingual English/German demo content for the [Crispframe TYPO3 theme](https://github.com/PhantomPixelDev/crispframe-agency-theme). It demonstrates a complete editable corporate site with Home, Work, Services, About, Contact, Insights, Resources, Locations, Request a Project, articles, case studies, forms, SEO fields, mega navigation, announcements, section navigation, callouts, and all 27 blocks.

This optional distribution contains an editable example page tree. Install it only in a **new, empty TYPO3 project** after `crispframe/agency-theme`. `extension:setup` imports `Initialisation/data.xml` and the sample site configuration. Existing sites should install the theme alone and create their own pages.

The example content uses fictional organization and contact details. Replace all names, prices, links, legal pages, form recipients, and SEO text before publishing. Do not use this package as an update mechanism for edited content.

The starter includes seven original, compressed WebP editorial photographs for Home, Work, Contact, Services, About and two case studies. They are imported as normal TYPO3 files and may be replaced or removed in the page editor. English and German hero records each carry their own editable alternative text. The theme package contains no demo photography.

The bilingual page tree contains Home, Work, Contact, Services, About, Insights, Resources, Locations, Request a Project, four Service detail pages, two Work case studies, two articles, plus a hidden Components showcase. Insights uses translated child-page cards and page media; Resources demonstrates tabs and curated links. One article uses the Article sidebar, pull quote and author card; the second shows the empty-sidebar layout. Services demonstrates generated section navigation, the comparison table, and a vertical timeline. Locations demonstrates office cards and a callout. All records are editable in TYPO3. Internal links use page references, so German navigation stays in German.

The XML export is generated from the local demo with TYPO3's `impexp:export` command. It includes only the page tree and records under that root. It contains no backend users or credentials.
