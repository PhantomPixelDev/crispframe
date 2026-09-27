async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  await page.emulateMedia({reducedMotion:'reduce'});
  async function visit(path, width=1440, height=1000) {
    await page.setViewportSize({width,height});
    const response = await page.goto(base+path);
    if(response.status() !== 200) throw new Error(path+' returned '+response.status());
    await page.evaluate(()=>document.fonts.ready);
    // Load real lazy images before taking a viewport or component capture.
    await page.locator('main img').evaluateAll(images=>images.forEach(img=>img.loading='eager'));
    await page.waitForFunction(()=>[...document.querySelectorAll('main img[src]')].every(img=>img.complete&&img.naturalWidth>0));
    await page.evaluate(()=>scrollTo(0,0));
  }
  async function capture(name, selector) {
    if(selector) {
      await page.locator(selector).first().evaluate(el=>scrollTo(0,Math.max(0,el.getBoundingClientRect().top+scrollY-115)));
    }
    await page.waitForTimeout(300);
    await page.screenshot({path:'output/playwright/readme-'+name+'.png',animations:'disabled'});
  }
  for(const [name,path] of [
    ['home-desktop','/'],['work-desktop','/work'],['contact-desktop','/contact'],
    ['services-desktop','/services'],['about-desktop','/about'],
    ['insights-desktop','/insights'],['resources-desktop','/resources'],
    ['article-desktop','/insights/clear-service-pages'],['case-study-de-desktop','/de/work/customer-workspace'],
    ['style-variants-desktop','/components/style-variants'],['style-variants-de-desktop','/de/components/stilvarianten']
  ]) {
    await visit(path);
    const section = {
      '/resources': '.section:has(.editorial-tabs)',
      '/insights': '.section:has(.child-pages)',
      '/services': '.hero-section',
      '/components/style-variants': '.section:has(.cards--projects-rows)',
      '/de/components/stilvarianten': '.section:has(.cards--services-open)',
    }[path];
    await capture(name, section);
  }
  await visit('/components',1440,1200); await capture('pricing-block','.section:has(.pricing-grid)');
  await visit('/'); await capture('service-cards','.section:has(.cards--services)');
  await page.locator('.site-header__nav .nav__submenu-toggle').first().click();
  await page.locator('.site-header__nav .nav__submenu').first().waitFor({state:'visible'});
  await page.evaluate(()=>scrollTo(0,0));
  await capture('mega-menu');
  await visit('/contact',1440,1200); await capture('contact-form','.frame-type-form_formframework form');
  await visit('/',390,844); await capture('home-mobile');
  await page.locator('#nav-toggle').click();
  await page.locator('#mobile-menu .nav__submenu-toggle').first().click();
  await capture('mobile-menu');
  return '17 live demo screenshots saved to output/playwright/readme-*.png';
}
