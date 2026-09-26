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
    for (const path of ['/contact', '/project-inquiry', '/de/contact', '/de/projektanfrage', '/components', '/services', '/about/locations']) {
      const response = await page.goto(base + path);
      check(response.status() === 200, path + ' failed');
      await page.evaluate(() => document.fonts.ready);
      for (const palette of ['ocean','forest','plum','ember']) {
        await page.locator('.site-shell').evaluate((el,p) => el.dataset.palette=p,palette);
        check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), path + ' overflow at ' + width + ' ' + palette);
      }
      await page.locator('.site-shell').evaluate(el => el.dataset.palette='ocean');
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
