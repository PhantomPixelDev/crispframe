# Styling Crispframe

Change the palette, width, type scale, corners, spacing, header, or footer in TYPO3 Site Settings first. Editors can choose the documented [block style variants](StyleVariants.md) without editing CSS.

For a custom design, edit the source file that owns the element:

| File | Owns |
| --- | --- |
| `tokens.css` | Font face, colors, spacing, type, radii, and shadows |
| `base.css` | Element reset, typography, focus, and reduced motion |
| `layout.css` | Containers, sections, grids, and section headings |
| `themes.css` | Palette and Site Settings variants, including colored section controls |
| `components.css` | Header, navigation, heroes, cards, buttons, CTAs, and footer |
| `forms.css` | TYPO3 Form Framework and custom form controls |
| `blocks.css` | Pricing, gallery, callout, locations, and block presentation variants |
| `editorial.css` | Article layout and standard TYPO3 content elements |

The page layout loads these files in that order, with `utilities.css` after components. There is no catch-all refresh stylesheet. Keep changes beside the component they affect. For example, the CTA's panel, open, dark, and brand rules live together in `components.css`; the four palette values live in `themes.css`.

After changing color rules, check both CTA actions on default, subtle, dark, and brand sections in all four palettes. `scripts/cta-contrast-audit.js` checks the deployed demo. Run the browser smoke and clean-install checks before a package release. The demo's content and images remain in the optional demo package.

### Mobile branding and editorial panels

Set **Brand → Short mobile brand name** (`brand.mobileName`) when a company's full name is too long for a phone header. An empty value uses the company name, which can wrap instead of being cut off. Uploaded logos continue to use their existing setting.

Colored sections inside an Article layout have their own horizontal inset. Keep this in `editorial.css`: the outer page gutter does not provide padding inside a colored panel. The sidebar uses a smaller inset to retain readable content width.

All 27 blocks include backend previews with their real headings, introductory text, and collection labels. The previews escape editorial text and omit hidden collection items. Run `php scripts/check-previews.php` from the development repository to render them through Content Blocks' preview layouts. Both clean-install jobs run this check.
