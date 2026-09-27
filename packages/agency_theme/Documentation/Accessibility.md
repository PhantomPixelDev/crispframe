# Accessibility and responsive checks

The theme has 27 Content Blocks, demonstrated across the optional demo pages. The browser smoke script visits English and German routes, verifies 200/404 responses and canonical markup, opens the gallery with a keyboard-capable dialog, checks Escape and focus return, switches pricing, starts video on click, and submits both forms. It checks horizontal overflow at 390, 768 and 1440 CSS pixels for ocean, forest, plum and ember, with reduced motion enabled.

On 26 September 2026, the VPS demo passed the browser smoke and focused UI repair checks. Contact and project inquiry messages were confirmed in Mailpit. The focused accessibility script passed 48 axe runs: six routes (Home, Components, Contact, Project inquiry, German Project inquiry, and Locations), two widths (390 and 1440 px), and all four palettes. Its configured rule tags are WCAG 2 A/AA, 2.1 AA, and 2.2 AA. This is an automated check of those pages, not a claim of full WCAG conformance.

To reproduce against a running development site, open its base URL first. The scripts use that origin:

```sh
npx --yes --package @playwright/cli playwright-cli open https://dev-crispframe.ppxl.dev/
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/browser-smoke.js
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/ui-repair-check.js
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/ui-repair-accessibility.js
```

These scripts live in the source repository. The smoke test submits test inquiries, so use a development site with mail capture. The broader `scripts/axe-audit.js` covers additional routes; its presence does not imply that every run or editorial configuration has passed.

Automated checks do not cover every editorial combination. Before launch, use keyboard-only navigation through the menu, language switch, FAQ, gallery and form; inspect text over uploaded images; test 200% and 400% zoom, screen-reader announcements and form errors; and review translated content. Each site owner is responsible for the contrast and alternative text of their own imagery and custom palette changes.
