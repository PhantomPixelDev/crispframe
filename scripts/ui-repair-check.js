async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const check = (condition, message) => { if (!condition) throw new Error(message); };
  const results = [];
  for (const width of [390, 768, 1440]) {
    await page.setViewportSize({width, height: 1000});
    await page.goto(base + '/contact');
    const mobile = await page.locator('#nav-toggle').isVisible();
    if (mobile) await page.locator('#nav-toggle').click();
    const nav = page.locator(mobile ? '#mobile-menu' : '.site-header__nav');
    const toggle = nav.locator('.nav__submenu-toggle').first();
    const panel = page.locator('#' + await toggle.getAttribute('aria-controls'));
    await toggle.click();
    check(await toggle.getAttribute('aria-expanded') === 'true', 'Submenu state did not open');
    await panel.waitFor({state:'visible'});
    await panel.locator('a').first().click({trial:true});
    await page.screenshot({path:'output/playwright/menu-' + width + '.png'});
    await page.keyboard.press('Escape');
    await panel.waitFor({state:'hidden'});
    await toggle.click();
    await panel.waitFor({state:'visible'});
    await toggle.click();
    await panel.waitFor({state:'hidden'});
    if (mobile) {
      check(await page.locator('#mobile-menu').isVisible(), 'Escape closed both menu levels');
      await page.keyboard.press('Escape');
    }
    for (const path of ['/contact', '/project-inquiry', '/de/contact', '/de/projektanfrage', '/components', '/services', '/about/locations', '/resources', '/de/ressourcen', '/insights/content-checklist', '/de/wissen/inhaltscheckliste']) {
      const response = await page.goto(base + path);
      check(response.status() === 200, path + ' failed');
      await page.evaluate(() => document.fonts.ready);
      for (const palette of ['ocean','forest','plum','ember']) {
        await page.locator('.site-shell').evaluate((el,p) => el.dataset.palette=p,palette);
        check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), path + ' overflow at ' + width + ' ' + palette);
      }
      await page.locator('.site-shell').evaluate(el => el.dataset.palette='ocean');
      if (path === '/resources') {
        const section = page.locator('.section:has(.resource-list)').first();
        const balanced = await section.evaluate(el => parseFloat(getComputedStyle(el).paddingTop));
        check(balanced <= 80, 'Resource list has excessive section padding');
        await page.locator('.site-shell').evaluate(el => el.dataset.rhythm='airy');
        await page.evaluate(() => new Promise(resolve => requestAnimationFrame(resolve)));
        const airy = await section.evaluate(el => parseFloat(getComputedStyle(el).paddingTop));
        check(airy > balanced, 'Airy spacing setting no longer changes editorial sections');
        await page.locator('.site-shell').evaluate(el => el.dataset.rhythm='balanced');
      }
      if (path.endsWith('/content-checklist') || path.endsWith('/inhaltscheckliste')) {
        const articleText = page.locator('.article-layout__main > .frame-type-text').first();
        check(await articleText.evaluate(el => parseFloat(getComputedStyle(el).paddingTop) >= 40), 'Article text touches its hero');
      }
      const form = page.locator('.frame-type-form_formframework form');
      if (await form.count()) {
        const input = form.locator('input[type="text"]:not([aria-hidden="true"])').first();
        check(await input.evaluate(el => parseFloat(getComputedStyle(el).height) >= 48 && getComputedStyle(el).borderStyle === 'solid'), path + ' input is unstyled');
        await form.screenshot({path:'output/playwright/form-' + path.replaceAll('/','-') + '-' + width + '.png'});
      }
      if (path === '/components' || path === '/services') {
        await page.screenshot({path:'output/playwright/' + path.slice(1) + '-' + width + '.png',fullPage:true});
      }
      results.push(path + ' @ ' + width);
    }
  }
  return results;
}
