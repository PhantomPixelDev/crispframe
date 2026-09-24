# Crispframe example pages

This optional distribution contains an editable example page tree. Install it only in a **new, empty TYPO3 project** after `crispframe/agency-theme`. `extension:setup` imports `Initialisation/data.xml` and the sample site configuration. Existing sites should install the theme alone and create their own pages.

The example content uses fictional organization and contact details. Replace all names, prices, links, legal pages, form recipients, and SEO text before publishing. Do not use this package as an update mechanism for edited content.

The starter includes seven original, compressed WebP editorial photographs for Home, Work, Contact, Services, About and two case studies. They are imported as normal TYPO3 files and may be replaced or removed in the page editor. English and German hero records each carry their own editable alternative text. The theme package contains no demo photography.

The bilingual page tree contains Home, Work, Contact, Services, About and two Work case studies, plus a hidden Components showcase. Services demonstrates the comparison table and vertical timeline; About demonstrates the card timeline. All records are editable in TYPO3. Work cards link to the case studies through page references, so German navigation stays in German.

The XML export is generated from the local demo with TYPO3's `impexp:export` command. It includes only the page tree and records under that root. It contains no backend users or credentials.
