async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const failures = [];
  await page.emulateMedia({reducedMotion: 'reduce'});
  for (const path of ['/components/style-variants', '/de/components/stilvarianten']) {
    for (const width of [390, 1440]) {
      await page.setViewportSize({width, height: 900});
      await page.goto(base + path);
      await page.addScriptTag({url: 'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js'});
      for (const palette of ['ocean', 'forest', 'plum', 'ember']) {
        await page.locator('.site-shell').evaluate((element, value) => element.setAttribute('data-palette', value), palette);
        for (const background of ['dark', 'brand']) {
          await page.evaluate(value => {
            for (const selector of ['.cards--services-open', '.cards--features-open', '.cards--projects-rows', '.cards--testimonials-open', '.cta--open']) {
              const element = document.querySelector(selector);
              const section = element.closest('.section');
              section.classList.remove('section--default', 'section--subtle', 'section--dark', 'section--brand');
              section.classList.add('section--' + value);
              if (selector === '.cta--open') {
                element.classList.remove('cta--dark', 'cta--brand');
                element.classList.add('cta--' + value);
              }
            }
          }, background);
          await page.waitForTimeout(250);
          const violations = await page.evaluate(async () => {
            const result = await window.axe.run(document, {
              runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa']}
            });
            return result.violations.map(violation => ({
              rule: violation.id,
              targets: violation.nodes.slice(0, 3).map(node => node.target.join(' '))
            }));
          });
          if (violations.length) failures.push({path, width, palette, background, violations});
        }
      }
    }
  }
  if (failures.length) throw new Error(JSON.stringify(failures));
  return 'Style variants passed axe on dark and brand sections, in both languages, at 390 and 1440 px across four palettes.';
}
