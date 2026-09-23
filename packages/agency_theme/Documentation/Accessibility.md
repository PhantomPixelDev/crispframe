# Accessibility and responsive checks

The optional Components page includes a specimen of all 17 Content Blocks. The browser smoke script visits English and German routes, verifies 200/404 responses and canonical markup, opens the gallery with a keyboard-capable dialog, checks Escape and focus return, switches pricing, starts video on click, and submits the contact form. It checks horizontal overflow at 390, 768 and 1440 CSS pixels for ocean, forest, plum and ember, with reduced motion enabled.

The axe audit uses WCAG 2 A/AA, 2.1 A/AA and 2.2 AA tagged rules on Home, Work, Contact and Components. It checks all four palettes at 390 px and ocean at 1440 px. The local Podman demo passed those automated checks on 23 September 2026. CI reruns them against a fresh starter installation. The contact form was submitted locally and its message was found in Mailpit.

To reproduce against the running local demo:

```powershell
npx --yes --package @playwright/cli playwright-cli open http://localhost:8080/components
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/browser-smoke.js
npx --yes --package @playwright/cli playwright-cli run-code --filename scripts/axe-audit.js
```

Automated checks do not cover every editorial combination. Before launch, use keyboard-only navigation through the menu, language switch, FAQ, gallery and form; inspect text over uploaded images; test 200% and 400% zoom, screen-reader announcements and form errors; and review translated content. Each site owner is responsible for the contrast and alternative text of their own imagery and custom palette changes.
