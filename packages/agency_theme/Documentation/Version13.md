# Crispframe 1.3: TYPO3 13 and 14

New projects use the TYPO3 14.3 starter. The theme and optional demo resolve on TYPO3 13.4.15+ with Content Blocks 1.6+, or TYPO3 14.3.7+ with Content Blocks 2.4+. Keep all TYPO3 core packages on the same major version.

## Upgrade an existing site

1. Back up the database, `public/fileadmin`, and site configuration. Test the Composer upgrade and TYPO3 upgrade wizards in a copy of the site first.
2. On SQLite sites created under TYPO3 13, run `python3 scripts/prepare-sqlite-14.py /absolute/path/to/site.sqlite` after the backup. This removes legacy Content Blocks indexes that point at absent columns and makes the two old image-size fields nullable for TYPO3's migration. MySQL and MariaDB sites do not use this helper. Change the root project's TYPO3 constraints to `^14.3.7` and Content Blocks to `^2.4`; then run `composer update`, flush caches, and run `vendor/bin/typo3 extension:setup --extension=agency_theme`.
3. Run `vendor/bin/typo3 upgrade:run --no-interaction`, flush caches, and inspect your own forms, page tree, translations and configured integrations.
4. Keep the optional `agency-demo` package away from an existing site. Its XML initialisation is only for a fresh empty site. Theme updates do not reimport or overwrite edited pages.

## Language-safe Site Settings

The site editor offers page pickers for the primary and secondary CTAs, legal and privacy links, and the Services footer parent. A selected page wins over the older URL setting and resolves to the active language. Existing URL values and the stored Services UID continue to work. Leave both page and URL empty to hide a link. `#` and `/` also hide legacy optional links.

The English and German CTA labels, footer promotion, tagline and description have separate fields. German fields can be left empty to hide optional German copy. The starter demonstrates both languages; editorial page copy and image alt text remain regular translated TYPO3 records.

The Hero block also offers image side and landscape, square or portrait crop. Existing Hero records keep their right-hand landscape presentation until an editor selects an option. Native TYPO3 text, text and image, image, table and file-link elements receive the same spacing, colors and focus treatment as Crispframe blocks.

## Case study recipe

Create a child page under Work, add a Hero with the H1 option, then use Intro blocks for the challenge and outcome, followed by a CTA. Give the page a German translation and translate its content records and image reference alt text. Link a Projects card to the page with TYPO3's page selector; the link then follows the current language automatically. The optional demo includes two editable examples and their photos.

## Verify before release

Run `sh scripts/clean-install.sh` in the repository's web container for TYPO3 14 and `CRISPFRAME_TYPO3_MAJOR=13 sh scripts/clean-install.sh` for TYPO3 13. The local maintainer script `sh scripts/test-upgrade-v13.sh` restores a pre-upgrade database and uploads into an isolated temporary project, then runs the TYPO3 14 upgrade and serves a German page. Run browser checks on both installed versions before publishing.

The optional demo XML must be exported with TYPO3 13's impexp format so both supported versions can import it. Maintainers can regenerate it from a restored copy with `sh scripts/export-demo-13.sh`; never export the distribution XML from the TYPO3 14 site.
