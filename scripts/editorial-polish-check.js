async (page) => {
  const base = new URL(page.url()).origin;
  const check = (ok, message) => { if (!ok) throw new Error(message); };
  const paths = ['/', '/de/', '/resources', '/de/ressourcen', '/insights/content-checklist', '/de/wissen/inhaltscheckliste', '/insights/clear-service-pages', '/components/style-variants'];
  let checks = 0;
  for (const width of [390, 768, 1440]) {
    await page.setViewportSize({width, height: 1000});
    for (const path of paths) {
      const response = await page.goto(base + path);
      check(response.status() === 200, `${path}: HTTP error`);
      await page.evaluate(() => document.fonts.ready);
      for (const palette of ['ocean', 'forest', 'plum', 'ember']) {
        const result = await page.evaluate(palette => {
          document.querySelector('.site-shell').dataset.palette = palette;
          const brand = document.querySelector('.site-header__brand').getBoundingClientRect();
          const actions = document.querySelector('.site-header__actions').getBoundingClientRect();
          const notice = document.querySelector('.announcement__inner');
          const panels = [...document.querySelectorAll('.article-layout .section--subtle,.article-layout .section--dark,.article-layout .section--brand')];
          return {
            overflow: document.documentElement.scrollWidth > innerWidth,
            brandOverlap: brand.right > actions.left + 1,
            panelInsets: panels.map(panel => {
              const content = panel.querySelector('.container');
              return content ? content.getBoundingClientRect().left - panel.getBoundingClientRect().left : 999;
            }),
            noticeInset: !notice || !notice.getBoundingClientRect().width ? 999 : notice.getBoundingClientRect().left,
          };
        }, palette);
        check(!result.overflow, `${path}/${width}/${palette}: horizontal overflow`);
        check(!result.brandOverlap, `${path}/${width}: brand overlaps controls`);
        check(result.panelInsets.every(inset => inset >= 19), `${path}/${width}: colored panel lacks inset`);
        check(result.noticeInset >= 15, `${path}/${width}: announcement lacks gutter`);
        checks++;
      }
      await page.evaluate(() => { document.querySelector('.site-shell').dataset.palette = 'ocean'; });
      if (['/', '/insights/content-checklist', '/insights/clear-service-pages', '/resources'].includes(path)) {
        await page.screenshot({path: `output/playwright/polish-${path === '/' ? 'home' : path.split('/').pop()}-${width}.png`, fullPage: true});
      }
    }
  }
  for (const path of ['/components', '/de/components', '/components/style-variants', '/de/components/stilvarianten']) {
    await page.goto(base + path);
    const heading = page.getByRole('heading', {name: path.startsWith('/de/') ? 'Beispiele entdecken' : 'Explore the showcase', exact: true});
    if (await heading.count()) {
      const links = heading.locator('xpath=ancestor::section').locator('.resource-list__link');
      check(await links.count() === 6, `${path}: showcase must contain six jump links`);
      for (const link of await links.all()) {
        const href = await link.getAttribute('href');
        const hash = new URL(href, page.url()).hash;
        check(hash && await page.locator(hash).count() === 1, `${path}: missing jump target ${hash}`);
      }
    }
  }
  console.log(`Editorial polish passed: ${checks} page/width/palette checks.`);
}
