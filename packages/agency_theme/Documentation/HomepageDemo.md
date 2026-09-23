# Homepage Demo — Block Order & Copy

Recommended composition for a shippable agency homepage. All copy is realistic agency placeholder (no lorem ipsum). Create a page with backend layout **Landing** or **Default**, colPos `0` = Main content, colPos `1` = Hero (Landing only). If using Default, place Hero in Main content as first block and check **Use h1 for headline**.

## Block order (colPos 0 — Main content)

> Drawn from the 14 Content Blocks. Suggested `sectionBackground`/`sectionSpacing` in brackets.

### 1. Hero — `crispframe/hero` [bg: default, spacing: large, width: default, isHero: checked]
- **Eyebrow:** Digital agency for ambitious brands
- **Headline (h1):** We design and build digital products that grow your business
- **Supporting text:** Crispframe combines strategy, design and engineering to ship TYPO3 and web platforms that are fast, accessible and easy to edit.
- **Primary:** Start a project → `#contact`
- **Secondary:** View our work → `#projects`
- **Image:** 1280×960, eager, alt “Team collaborating on a product workshop”

### 2. Logo cloud — `crispframe/logo-cloud` [bg: subtle, spacing: small]
- **Headline:** Trusted by ambitious teams
- **Lead:** From funded startups to established mid-market leaders.
- **Logos (6):** Nordlicht Labs, Alpenwerk, Klarfeld, Strand & Partner, Monto Systems, Veer Collective — each 240×120 SVG, linked to `#` case study or empty.

### 3. Intro — `crispframe/intro` [bg: default, width: narrow]
- **Headline (h2):** Strategy, design and code — under one roof
- **Lead:** We help mid-market companies modernise their digital presence without the agency overhead.
- **Supporting text:** From discovery to launch, one senior team owns the entire journey. No handoffs, no surprises — just measurable progress every sprint.
- **Link:** Our approach → `#about`

### 4. Services — `crispframe/services` [bg: default]
- **Headline:** Services built for growth
- **Lead:** From first sketch to scalable platform — pick the engagement that fits your stage.
- **Items:**
  1. **Digital Strategy** — Roadmaps that connect business goals to measurable outcomes.
  2. **Brand & Design** — Identity and product design that earns trust and shortens sales cycles.
  3. **TYPO3 & Web Engineering** — Accessible, performant builds editors can actually manage.
  4. **Growth & Optimisation** — Continuous improvement from analytics to conversion.
  5. **Content & Enablement** — Structured content models and editor training that stick.
  6. **Support & Hosting** — Hardened operations with clear SLAs.

### 5. Featured work — `crispframe/projects` [bg: subtle]
- **Headline:** Selected work
- **Lead:** A sample of platforms and websites we have shipped recently.
- **Projects:**
  - **Nordlicht Commerce Relaunch** — E-commerce — Headless TYPO3 storefront that lifted conversion by 34%. Image 640×420, alt “Nordlicht Commerce product listing”.
  - **Alpenwerk Corporate Site** — Corporate site — Multilingual platform with 40% faster editorial workflow. Image 640×420.
  - **Klarfeld Booking Platform** — SaaS — Availability and booking engine with TYPO3 headless API. Image 640×420.

### 6. Why us — `crispframe/feature-grid` [bg: default]
- **Headline:** Why teams choose Crispframe
- **Lead:** Senior product thinking applied to every content block — not just the homepage.
- **Features:**
  - **Editor-first content** — Structured blocks editors love — no developer needed for everyday changes.
  - **Performance by default** — Static-adjacent caching, system fonts, no heavy JS frameworks.
  - **Accessibility baked in** — Keyboard, screen reader and reduced-motion handled from the first component.
  - **Transparent delivery** — Weekly demos, fixed scope increments, no surprise invoices.
  - **Long-term stewardship** — Security updates and improvements without agency lock-in.
  - **Proven TYPO3 depth** — Content Blocks, Site Sets and PageView done properly.

### 7. Stats — `crispframe/stats` [bg: subtle]
- **Headline:** Results that speak for themselves
- **Lead:** We measure success in shipped products and lasting partnerships.
- **Items:**
  - **120+** — projects shipped
  - **98%** — client retention
  - **4.9/5** — average editor satisfaction
  - **10 weeks** — discovery to MVP

### 8. Process — `crispframe/process` [bg: default]
- **Headline:** How we work
- **Lead:** A proven five-step process — transparent, collaborative and built for predictable delivery.
- **Steps:**
  1. **Discovery** — Workshops and research to define goals and success metrics.
  2. **Design** — Iterative prototyping with real content and user testing.
  3. **Build** — Accessible, performant engineering with editor previews.
  4. **Launch** — Hardened hosting, analytics and training for a confident handover.
  5. **Evolve** — Continuous improvement from data and user feedback.

### 9. Testimonials — `crispframe/testimonials` [bg: subtle, width: wide]
- **Headline:** What clients say
- **Lead:** Long-term partnerships over one-off projects.
- **Items:**
  - “Crispframe shipped our platform in ten weeks — on time and without a content freeze.” — **Laura Meier**, Head of Digital, Nordlicht Labs
  - “The editor experience finally matches the frontend. Our team publishes daily without tickets.” — **Jonas Feld**, Marketing Lead, Alpenwerk
  - “Clear scope, clear costs, clear communication. The best agency process we have used.” — **Sofia Strand**, CEO, Strand & Partner

### 10. FAQ — `crispframe/faq` [bg: default, width: narrow]
- **Headline:** Questions, answered
- **Lead:** Everything you need to know before we start.
- **Items:**
  - **How long does a typical project take?** — Discovery takes 2 weeks, build 6–10 weeks. We ship an MVP early and iterate in sprints.
  - **Do you work with existing TYPO3 installations?** — Yes. We audit, stabilise and migrate content without a full rebuild when possible.
  - **Who will we work with?** — A senior team of 3–4: strategy, design, engineering and delivery. No bait-and-switch.
  - **What does it cost?** — Fixed increments from €25k. We scope to a budget and show trade-offs before we start.

### 11. CTA — `crispframe/cta` [bg: brand, spacing: large]
- **Headline:** Ready to move faster?
- **Text:** Tell us about your project and we will outline scope, timeline and investment within 48 hours.
- **Primary:** Start a project → `#contact`
- **Secondary:** See our process → `#process`

### 12. Contact — `crispframe/contact` [bg: default, id: contact anchor]
- **Headline:** Let’s talk
- **Lead:** We reply within one business day. No forms that go nowhere.
- **Email:** hello@crispframe.example
- **Phone:** +49 30 1234 5678
- **Address:** Rosenthaler Str. 42, 10178 Berlin, Germany
- **Hours:** Monday–Friday, 09:00–18:00 CET
- **Note:** Prefer email? Write to hello@crispframe.example and we will get back to you within 24 hours.
- **Image:** Optional office photo 640×480

## Header / Footer

- **Header:** Provided by `Site/Header` partial. Brand name from `site.settings.brand.companyName`, CTA from `site.settings.cta.*`, navigation from `menuMain` (MenuProcessor, levels 2). Mobile menu uses `#nav-toggle` / `#mobile-menu` with `aria-expanded`/`aria-controls`.
- **Footer:** Provided by `Site/Footer`. Brand, tagline, `footer.text`, contact (`contact.email/phone/address`), social links (`social.*`), legal links (`footer.legalLink`/`footer.privacyLink`). Year auto-filled via `[data-current-year]` + JS fallback.

## Notes for editors

- Use **only one** Hero with **Use h1 for headline** checked per page.
- Section headings are h2; card/process titles are h3 — keep hierarchy.
- Backgrounds: `dark`/`brand` switch text to on-dark; avoid long body copy on dark.
- Images: always provide alt text; hero is eager, all others lazy with `decoding="async"` and width/height to avoid CLS.
