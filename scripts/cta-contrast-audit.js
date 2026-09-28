async (page) => {
  const base = page.url().match(/^https?:\/\/[^/]+/)?.[0];
  if (!base) throw new Error('Open the live demo before running this audit.');
  await page.goto(base + '/');
  // Check the current working tree against the VPS before deployment as well.
  await page.addStyleTag({path: 'packages/agency_theme/Resources/Public/Css/refresh.css'});
  await page.addStyleTag({content: '*,*::before,*::after{transition:none!important;animation:none!important}'});
  const result = await page.evaluate(() => {
    const shell = document.querySelector('.site-shell');
    const cta = document.querySelector('.cta');
    const section = cta?.closest('.section');
    if (!shell || !cta || !section) throw new Error('Homepage CTA is missing.');
    const primary = cta.querySelector('.btn--primary');
    const secondary = document.createElement('a');
    secondary.className = 'btn btn--secondary';
    secondary.href = '#';
    secondary.textContent = 'Secondary action';
    cta.querySelector('.cta__actions').append(secondary);
    const rgb = value => [...value.matchAll(/[\d.]+/g)].slice(0, 3).map(match => Number(match[0]) / 255);
    const luminance = color => rgb(color).map(channel => channel <= .04045 ? channel / 12.92 : ((channel + .055) / 1.055) ** 2.4).reduce((sum, channel, index) => sum + channel * [.2126, .7152, .0722][index], 0);
    const ratio = (a, b) => {
      const x = luminance(a), y = luminance(b);
      return (Math.max(x, y) + .05) / (Math.min(x, y) + .05);
    };
    const failures = [];
    const samples = [];
    for (const palette of ['ocean', 'forest', 'plum', 'ember']) {
      shell.dataset.palette = palette;
      for (const background of ['default', 'subtle', 'dark', 'brand']) {
        section.className = `section section--${background}`;
        for (const variant of ['panel', 'open']) {
          cta.className = `cta cta--${variant}${['dark', 'brand'].includes(background) ? ` cta--${background}` : ''}`;
          const surface = getComputedStyle(variant === 'panel' ? cta : section).backgroundColor;
          const primaryStyle = getComputedStyle(primary);
          const secondaryStyle = getComputedStyle(secondary);
          const sample = {
            palette, background, variant,
            primaryText: ratio(primaryStyle.color, primaryStyle.backgroundColor),
            primarySurface: ratio(primaryStyle.backgroundColor, surface),
            secondaryText: ratio(secondaryStyle.color, secondaryStyle.backgroundColor === 'rgba(0, 0, 0, 0)' ? surface : secondaryStyle.backgroundColor),
            panelSurface: variant === 'panel' ? ratio(surface, getComputedStyle(section).backgroundColor) : null
          };
          samples.push(sample);
          if (sample.primaryText < 4.5 || sample.primarySurface < 3 || sample.secondaryText < 4.5) failures.push(sample);
        }
      }
    }
    secondary.remove();
    return {failures, samples};
  });
  if (result.failures.length) throw new Error(JSON.stringify(result.failures));
  return `32 CTA combinations passed text and button contrast. Panel/section ratios: ${JSON.stringify(result.samples.filter(sample => sample.variant === 'panel').map(({palette, background, panelSurface}) => ({palette, background, ratio: Number(panelSurface.toFixed(2))})))}.`;
}
