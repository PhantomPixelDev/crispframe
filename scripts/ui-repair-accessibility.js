async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)[0];
  const failures = [];
  for (const path of ['/components','/','/contact','/project-inquiry','/de/projektanfrage','/about/locations']) {
    for (const width of [390,1440]) {
      await page.setViewportSize({width,height:1000});
      await page.goto(base + path, {waitUntil:'domcontentloaded',timeout:60000});
      await page.addScriptTag({url:'https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.10.3/axe.min.js'});
      for (const palette of ['ocean','forest','plum','ember']) {
        await page.locator('.site-shell').evaluate((el,p)=>el.dataset.palette=p,palette);
        const violations = await page.evaluate(async () => (await axe.run(document, {
          runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}
        })).violations.map(v=>({id:v.id,nodes:v.nodes.slice(0,4).map(n=>({target:n.target,reason:n.failureSummary}))})));
        if (violations.length) failures.push({path,width,palette,violations});
      }
      await page.locator('.site-shell').evaluate(el=>el.dataset.palette='ocean');
      for (const selector of ['.service-card','.callout','.section--dark','.section--brand','.frame-type-form_formframework']) {
        const item=page.locator(selector).first();
        if(await item.count()) {
          await item.scrollIntoViewIfNeeded();
          await page.screenshot({path:'output/playwright/review-'+path.replaceAll('/','-')+'-'+selector.replaceAll('.','')+'-'+width+'.png'});
        }
      }
    }
  }
  if(failures.length) throw new Error(JSON.stringify(failures));
  return '48 axe checks passed: six routes, two widths, four palettes.';
}
