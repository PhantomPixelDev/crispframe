async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const expect = (condition, message) => { if (!condition) throw new Error(message); };
  for (const path of ['/', '/work', '/contact', '/components', '/de/', '/de/work', '/de/contact', '/de/components']) {
    const response = await page.goto(base + path);
    expect(response && response.status() === 200, `${path} must return 200`);
    const language = await page.locator('html').getAttribute('lang');
    expect(language === (path.startsWith('/de/') ? 'de' : 'en'), `${path} has wrong language: ${language}`);
    expect(await page.locator('link[rel="canonical"]').count() > 0, `${path} is missing canonical`);
    if (['/', '/work', '/contact', '/de/', '/de/work', '/de/contact'].includes(path)) {
      const heroImage = page.locator('.hero__media img').first();
      expect(await heroImage.count() === 1, `${path} is missing its editorial hero image`);
      expect((await heroImage.getAttribute('alt') || '').length > 10, `${path} needs useful hero alt text`);
      expect(await heroImage.evaluate(image => image.complete && image.naturalWidth > 0), `${path} hero image did not load`);
    }
  }
  for (const path of ['/missing-page', '/de/fehlende-seite']) {
    const response = await page.goto(base + path);
    expect(response && response.status() === 404, `${path} must return 404`);
    expect(await page.getByRole('link', { name: /home|startseite/i }).count() > 0, `${path} needs a home link`);
  }
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto(base + '/');
  const menu = page.getByRole('button', { name: 'Toggle navigation menu' });
  await menu.press('Enter');
  expect(await menu.getAttribute('aria-expanded') === 'true', 'Mobile menu did not open by keyboard');
  await page.keyboard.press('Escape');
  expect(await menu.getAttribute('aria-expanded') === 'false', 'Mobile menu did not close on Escape');
  await page.getByRole('navigation', { name: 'Languages' }).getByRole('link', { name: 'Deutsch' }).click();
  expect(page.url().endsWith('/de/'), 'Language switcher did not reach German homepage');
  await page.goto(base + '/components');
  await page.getByRole('link', { name: /View image: A clear workspace/ }).click();
  expect(await page.getByRole('dialog', { name: 'Image gallery' }).isVisible(), 'Gallery did not open');
  await page.getByRole('button', { name: 'Next image' }).click();
  expect((await page.getByRole('dialog').innerText()).includes('2 / 2'), 'Gallery next failed');
  await page.keyboard.press('Escape');
  expect(!(await page.getByRole('dialog').isVisible()), 'Gallery did not close on Escape');
  expect(await page.getByRole('link', { name: /View image: A clear workspace/ }).evaluate(element => element === document.activeElement), 'Gallery focus did not return to its opener');
  await page.getByRole('button', { name: 'Yearly' }).click();
  expect(await page.getByRole('button', { name: 'Yearly' }).getAttribute('aria-pressed') === 'true', 'Pricing toggle failed');
  await page.getByRole('button', { name: /Play video:/ }).click();
  expect(await page.locator('iframe').count() > 0, 'Video iframe was not created on click');
  await page.goto(base + '/contact');
  await page.getByRole('textbox', { name: 'Name *' }).fill('Release smoke');
  await page.getByRole('textbox', { name: 'Email *' }).fill('smoke@example.invalid');
  await page.getByRole('textbox', { name: 'How can we help? *' }).fill('Mail transport integration check');
  await page.getByRole('button', { name: 'Send inquiry' }).click();
  expect((await page.locator('body').innerText()).includes('Thank you. Your inquiry has been sent.'), 'Contact confirmation missing');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  for (const path of ['/', '/work', '/contact', '/components', '/de/']) {
    await page.goto(base + path);
    for (const width of [390, 768, 1440]) {
      await page.setViewportSize({ width, height: 900 });
      for (const palette of ['ocean', 'forest', 'plum', 'ember']) {
        await page.locator('.site-shell').evaluate((element, value) => element.setAttribute('data-palette', value), palette);
        const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
        expect(overflow <= 1, `Horizontal overflow on ${path} at ${width}px in ${palette}: ${overflow}px`);
      }
    }
  }
  return 'Browser smoke passed: pages, languages, SEO, 404, gallery, pricing, video, contact form, four palettes, three widths and reduced motion.';
}
