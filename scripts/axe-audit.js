async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const failures = [];
  for (const path of ['/', '/work', '/contact', '/services', '/about', '/components', '/work/customer-workspace', '/de/', '/de/work', '/de/contact', '/de/work/customer-workspace']) {
    for (const width of [390, 768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(base + path);
      await page.addScriptTag({ url: 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js' });
      for (const palette of ['ocean', 'forest', 'plum', 'ember']) {
        await page.locator('.site-shell').evaluate((element, value) => element.setAttribute('data-palette', value), palette);
        const violations = await page.evaluate(async () => {
          const result = await window.axe.run(document, {
            runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] }
          });
          return result.violations.map(violation => ({
            rule: violation.id,
            impact: violation.impact,
            targets: violation.nodes.slice(0, 3).map(node => node.target.join(' '))
          }));
        });
        if (violations.length) failures.push({ path, width, palette, violations });
      }
    }
  }
  if (failures.length) throw new Error(JSON.stringify(failures));
  return 'axe WCAG 2.2 AA tagged checks passed on eleven English and German pages, three widths and four palettes.';
}
