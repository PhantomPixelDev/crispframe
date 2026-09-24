async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const expect = (condition, message) => { if (!condition) throw new Error(message); };
  for (const path of ['/', '/work', '/contact', '/services', '/about', '/components', '/insights', '/resources', '/insights/clear-service-pages', '/insights/content-checklist', '/work/clearer-public-service', '/work/customer-workspace', '/de/', '/de/work', '/de/contact', '/de/leistungen', '/de/ueber-uns', '/de/components', '/de/wissen', '/de/ressourcen', '/de/wissen/klare-service-seiten', '/de/wissen/inhaltscheckliste', '/de/work/clearer-public-service', '/de/work/customer-workspace']) {
    const response = await page.goto(base + path);
    expect(response && response.status() === 200, `${path} must return 200`);
    const language = await page.locator('html').getAttribute('lang');
    expect(language === (path.startsWith('/de/') ? 'de' : 'en'), `${path} has wrong language: ${language}`);
    expect(await page.locator('link[rel="canonical"]').count() > 0, `${path} is missing canonical`);
    if (['/', '/work', '/contact', '/services', '/about', '/work/clearer-public-service', '/work/customer-workspace', '/de/', '/de/work', '/de/contact', '/de/leistungen', '/de/ueber-uns', '/de/work/clearer-public-service', '/de/work/customer-workspace'].includes(path)) {
      const heroImage = page.locator('.hero__media img').first();
      expect(await heroImage.count() === 1, `${path} is missing its editorial hero image`);
      expect((await heroImage.getAttribute('alt') || '').length > 10, `${path} needs useful hero alt text`);
      expect(await heroImage.evaluate(image => image.complete && image.naturalWidth > 0), `${path} hero image did not load`);
    }
  }
  await page.goto(base + '/de/work');
  expect(await page.locator('.project-card a[href^="/de/work/"]').count() >= 2, 'German Work cards must link to German case studies');
  for (const image of await page.locator('.project-card__image').all()) {
    await image.scrollIntoViewIfNeeded();
    expect(await image.evaluate(element => element.complete && element.naturalWidth > 0), 'Project card image did not load');
    expect((await image.getAttribute('alt') || '').match(/Mitarbeitende/), 'Project card alt text is not translated');
  }
  await page.goto(base + '/de/work/customer-workspace');
  expect(await page.locator('.hero[data-image-position="left"][data-media-crop="square"]').count() === 1, 'Hero layout and crop options did not render');
  expect((await page.locator('meta[name="description"]').getAttribute('content')).includes('Arbeitsbereich'), 'German case-study description is not localized');
  expect((await page.locator('.hero__media img').getAttribute('alt')).includes('Zwei Mitarbeitende'), 'German case-study alt text is not localized');
  expect(await page.locator('meta[property="og:title"]').count() === 1, 'Duplicate or missing Open Graph title');
  expect(await page.locator('.hero__actions a[href="/de/contact"]').count() === 1, 'German case CTA should use the localized page');
  expect(await page.locator('.frame-type-text').count() === 1, 'Native TYPO3 text should render between case-study blocks');
  await page.getByRole('navigation', { name: 'Sprachen' }).getByRole('link', { name: 'English' }).click();
  expect(page.url().endsWith('/work/customer-workspace'), 'Case-study language switch lost the current page');
  for (const path of ['/services', '/de/leistungen']) {
    await page.goto(base + path);
    expect(await page.locator('.comparison tbody tr').count() >= 2, `${path} needs comparison rows`);
    expect(await page.locator('.timeline__item').count() >= 3, `${path} needs timeline milestones`);
    const breadcrumb = await page.locator('.breadcrumb').evaluate(nav => {
      const items = [...nav.querySelectorAll('.breadcrumb__item')];
      return { rows: new Set(items.map(item => Math.round(item.getBoundingClientRect().top))).size,
        separators: nav.querySelectorAll('.breadcrumb__sep').length,
        pseudo: getComputedStyle(items[1], '::before').content };
    });
    expect(breadcrumb.rows === 1 && breadcrumb.separators === 1 && breadcrumb.pseudo === 'none', `${path} breadcrumb is not a single row with one separator`);
  }
  await page.goto(base + '/insights');
  expect(await page.locator('.child-pages__item').count() === 2, 'Insights must list two child pages');
  for (const image of await page.locator('.child-pages__image').all()) {
    await image.scrollIntoViewIfNeeded();
    expect(await image.evaluate(element => element.complete && element.naturalWidth > 0), 'Child-page image did not load');
  }
  await page.goto(base + '/de/wissen');
  expect(await page.locator('.child-pages__link[href^="/de/wissen/"]').count() === 2, 'German page teasers must use German routes');
  expect((await page.locator('.child-pages__image').first().getAttribute('alt')).includes('Kolleginnen'), 'German page media alt text is missing');
  expect((await page.locator('.child-pages__image').last().getAttribute('alt')).includes('Ein Team'), 'Second German page media alt text is missing');
  expect((await page.locator('.child-pages__image').first().getAttribute('src')) !== (await page.locator('.child-pages__image').last().getAttribute('src')), 'German page teasers must retain distinct images');
  await page.goto(base + '/insights/clear-service-pages');
  expect(await page.locator('.article-layout__sidebar .author-card').count() === 1, 'Article sidebar needs its author card');
  expect(await page.locator('.pull-quote blockquote').count() === 1, 'Article quotation is missing');
  await page.goto(base + '/insights/content-checklist');
  expect(await page.locator('.article-layout__sidebar').count() === 0, 'Empty article sidebar must disappear');
  await page.goto(base + '/resources');
  expect(await page.locator('[data-tabs]').count() === 2, 'Resources should demonstrate independent tab groups');
  const firstGroup = page.locator('[data-tabs]').first();
  const secondGroup = page.locator('[data-tabs]').nth(1);
  await firstGroup.getByRole('tab').first().focus();
  await page.keyboard.press('ArrowRight');
  expect(await firstGroup.getByRole('tab').nth(1).evaluate(element => element === document.activeElement), 'ArrowRight did not move tab focus');
  await page.keyboard.press('Enter');
  expect(await firstGroup.getByRole('tab').nth(1).getAttribute('aria-selected') === 'true', 'Enter did not activate the focused tab');
  expect(await secondGroup.getByRole('tab').first().getAttribute('aria-selected') === 'true', 'First tab group changed the second group');
  expect(await page.locator('.resource-list__item').count() === 3, 'Resource list is incomplete');
  await page.goto(base + '/de/ressourcen');
  expect(await page.locator('.resource-list__link[href^="/de/"]').count() === 3, 'German resource links must remain localized');
  for (const path of ['/missing-page', '/de/fehlende-seite']) {
    const response = await page.goto(base + path);
    expect(response && response.status() === 404, `${path} must return 404`);
    expect(await page.getByRole('link', { name: /home|startseite/i }).count() > 0, `${path} needs a home link`);
  }
  await page.setViewportSize({ width: 390, height: 900 });
  await page.goto(base + '/');
  const ctaColors = await page.locator('.cta__actions .btn--primary').first().evaluate(button => ({
    button: getComputedStyle(button).backgroundColor,
    surface: getComputedStyle(button.closest('.cta')).backgroundColor,
  }));
  expect(ctaColors.button !== ctaColors.surface, 'Brand CTA button blends into its background');
  for (const width of [320, 390, 768, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    const layout = await page.evaluate(() => {
      const button = document.querySelector('.intro__action .btn').getBoundingClientRect();
      const container = document.querySelector('.intro__action').closest('.container').getBoundingClientRect();
      return {
        buttonOffset: button.left + button.width / 2 - (container.left + container.width / 2),
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
      };
    });
    expect(Math.abs(layout.buttonOffset) <= 1, `Intro button is off center at ${width}px: ${layout.buttonOffset}px`);
    expect(layout.overflow <= 1, `Homepage overflows at ${width}px: ${layout.overflow}px`);
  }
  await page.setViewportSize({ width: 390, height: 900 });
  const menu = page.getByRole('button', { name: 'Toggle navigation menu' });
  await menu.press('Enter');
  expect(await menu.getAttribute('aria-expanded') === 'true', 'Mobile menu did not open by keyboard');
  const mobileLinks = page.locator('#mobile-menu a');
  expect(await mobileLinks.count() > 0, 'Mobile menu has no links');
  for (let index = 0; index < await mobileLinks.count(); index++) {
    const link = mobileLinks.nth(index);
    const visible = await link.evaluate(link => {
      const panel = link.closest('#mobile-menu').getBoundingClientRect();
      const rect = link.getBoundingClientRect();
      return rect.top >= panel.top && rect.bottom <= panel.bottom;
    });
    expect(visible, `Mobile menu clips ${await link.innerText()}`);
  }
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
  for (const path of ['/', '/work', '/contact', '/services', '/about', '/components', '/insights', '/resources', '/insights/clear-service-pages', '/insights/content-checklist', '/work/clearer-public-service', '/work/customer-workspace', '/de/', '/de/leistungen', '/de/ueber-uns', '/de/wissen', '/de/ressourcen', '/de/wissen/klare-service-seiten', '/de/wissen/inhaltscheckliste', '/de/work/clearer-public-service', '/de/work/customer-workspace']) {
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
  return 'Browser smoke passed: bilingual editorial pages, tabs, article sidebar, page media, case studies, SEO, 404, contact, four palettes and responsive layouts.';
}
