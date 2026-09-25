# Corporate navigation and conversion

## Two-level navigation

Crispframe reads the first two visible levels of the TYPO3 page tree. Set `navigation.submenuLayout` to `dropdown` for compact lists or `mega` for wide panels. The parent page remains a normal link and the adjacent toggle opens its children. The optional demo exposes its Showcase page in the main navigation so visitors can inspect every block. On narrow screens and whenever the desktop links do not fit, the header switches to the compact menu automatically.

Use short translated page titles and navigation titles. Keep the tree to two levels for predictable keyboard, touch, and no-JavaScript behavior.

## Announcement bar

Enable `announcement.enabled`, add English text, and optionally add German text. Empty German text hides the notice on German pages. Select `announcement.page` when the destination is a TYPO3 page; `announcement.link` remains available for existing external URLs. Choose neutral, brand, or dark presentation. A dismissible message is stored in the visitor's browser and appears again when its text changes.

## Footer page trees

`footer.servicesParent` and `footer.secondaryParent` each select a parent page. Their visible children form separate footer columns, and the translated parent title becomes the heading. Empty trees produce no column.

## Section navigation

Add a **Section navigation** block near the start of a long page. In the page module, enable **Include in section menus** on the content elements that should appear. Crispframe uses their translated headers and TYPO3 content anchors. Links work without JavaScript; active-section highlighting uses `IntersectionObserver` when available.

## Notices and offices

Use **Callout** for editorial information, success, warning, or critical notices. It is static page content and does not announce itself as a live alert. Use **Office locations** for two to eight offices. Map actions are ordinary links, so the theme never loads a third-party map automatically.

## Project inquiries

Add a TYPO3 **Form** content element and select **Project inquiry**. Configure receiver and sender overrides on the content element and set TYPO3 mail transport for the deployment. The bundled addresses use `example.invalid` and must be replaced before publishing.
