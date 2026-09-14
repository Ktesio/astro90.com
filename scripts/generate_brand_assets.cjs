/** Export existing Astro90 vector artwork and HTML compositions. Authoring only.
 * Dependencies: sharp + playwright. See docs/WEB-ASSETS.md for reproduction.
 * This is deliberately separate from the Zola/Cloudflare build.
 */
const fs = require('node:fs/promises');
const path = require('node:path');
const { chromium } = require('playwright');
const sharp = require('sharp');
const root = path.resolve(__dirname, '..');
const brand = path.join(root, 'static/brand');
const social = path.join(brand, 'social');
const saffron = '#F4C84C';
const ink = '#0B101A';

async function main() {
  await fs.mkdir(social, { recursive: true });
  const mark = JSON.parse(await fs.readFile(path.join(root, 'assets/brand/monogram.json')));
  const catalog = JSON.parse(await fs.readFile(path.join(root, 'data/social.json')));
  const exports = [];
  async function svg(name, source, sizes = []) {
    await fs.writeFile(path.join(brand, name + '.svg'), source + '\n');
    exports.push('brand/' + name + '.svg');
    for (const size of sizes) {
      const filename = `${name}-${size}.png`;
      await sharp(Buffer.from(source), { density: 600 }).resize(size, size).png().toFile(path.join(brand, filename));
      exports.push('brand/' + filename);
    }
  }
  function icon(fraction, rounded = false, monochrome = false) {
    const width = 512 * fraction, height = width * mark.height / mark.width;
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${monochrome ? '' : `<rect width="512" height="512" rx="${rounded ? 112 : 0}" fill="${saffron}"/>`}<path d="${mark.path}" transform="translate(${(512-width)/2} ${(512-height)/2}) scale(${width/mark.width})" fill="${monochrome ? '#000' : ink}"/></svg>`;
  }
  // Preserve the selected boxed signature. OS masks get their own full-bleed file.
  const favicon = await fs.readFile(path.join(brand, 'favicon.svg'));
  for (const size of [16,32,48,96]) {
    await sharp(favicon, { density: 600 }).resize(size,size).png().toFile(path.join(brand, `favicon-${size}.png`));
    exports.push(`brand/favicon-${size}.png`);
  }
  await svg('icon', icon(.6875, true), [192,512]);
  await svg('icon-maskable', icon(.58), [192,512]);
  await svg('app-icon', icon(.66), [1024]);
  await svg('avatar', icon(.58), [1024]);
  await svg('safari-pinned-tab', icon(.6875, false, true));
  await sharp(Buffer.from(icon(.66)), {density:600}).resize(180,180).png().toFile(path.join(root,'static/apple-touch-icon.png'));
  exports.push('apple-touch-icon.png','brand/favicon.svg','brand/monogram.svg');
  // ICO directory with lossless PNG entries, supported by current desktop browsers.
  const sizes=[16,32,48], frames=await Promise.all(sizes.map(n=>fs.readFile(path.join(brand,`favicon-${n}.png`))));
  const directory=Buffer.alloc(6+16*sizes.length); directory.writeUInt16LE(1,2); directory.writeUInt16LE(sizes.length,4);
  let offset=directory.length;
  frames.forEach((frame,i)=>{const p=6+i*16;directory[p]=sizes[i];directory[p+1]=sizes[i];directory.writeUInt16LE(1,p+4);directory.writeUInt16LE(32,p+6);directory.writeUInt32LE(frame.length,p+8);directory.writeUInt32LE(offset,p+12);offset+=frame.length;});
  await fs.writeFile(path.join(root,'static/favicon.ico'),Buffer.concat([directory,...frames])); exports.push('favicon.ico');

  const uri=async (file,mime)=>`data:${mime};base64,${(await fs.readFile(path.join(root,file))).toString('base64')}`;
  let html=await fs.readFile(path.join(root,'assets/brand/social-card.html'),'utf8');
  for(const [token,file,mime] of [['SORA','static/fonts/sora.woff2','font/woff2'],['MANROPE','static/fonts/manrope.woff2','font/woff2'],['COAST','static/media/night-coast-1643.webp','image/webp'],['WORDMARK','static/brand/wordmark-reference.webp','image/webp']]) {
    html=html.replace(`__${token}__`,await uri(file,mime));
  }
  const browser=await chromium.launch({headless:true,channel:process.env.BRAND_BROWSER_CHANNEL || 'chrome'});
  try {
    const page=await browser.newPage({viewport:{width:1200,height:630},deviceScaleFactor:1});
    await page.setContent(html);
    await page.evaluate(()=>document.fonts.ready);
    async function render(card, filename, width=1200, height=630, format='') {
      await page.setViewportSize({width,height});
      const screen=card.screen ? await uri('static/media/'+card.screen,'image/webp') : '';
      await page.evaluate(({card,format,screen})=>{
        document.body.className=[format,screen ? 'has-screen' : ''].join(' ');
        const heading=document.querySelector('h1');heading.replaceChildren(...card.title.map(text=>{const span=document.createElement('span');span.textContent=text;return span;}));
        document.querySelector('.subtitle').textContent=card.subtitle;
        const img=document.querySelector('.screen'); if(screen)img.src=screen;else img.removeAttribute('src');
      },{card,format,screen});
      await page.evaluate(()=>Promise.all([document.fonts.ready,...[...document.images].filter(img=>img.hasAttribute('src')).map(img=>img.decode())]));
      await page.screenshot({path:path.join(root,'static',filename),type:filename.endsWith('.png')?'png':'jpeg',...(filename.endsWith('.jpg')?{quality:91}:{})});
      exports.push(filename);
    }
    for(const card of catalog) await render(card,`brand/social/${card.slug}.jpg`);
    await render(catalog[0],'media/social-cover.png');
    await render(catalog[0],'brand/social/post-square.jpg',1080,1080,'square');
    await render(catalog[0],'brand/social/post-portrait.jpg',1080,1350,'portrait');
    await render(catalog[0],'brand/social/profile-banner.jpg',1500,500,'banner');
    await render(catalog[0],'brand/social/repository-cover.jpg',1280,640);
    const wordmark=await uri('static/brand/wordmark-reference.webp','image/webp');
    await page.setViewportSize({width:1320,height:244});
    for(const [name,color] of [['saffron',saffron],['white','#F0F1EE'],['midnight','#090E17']]) {
      await page.setContent(`<style>html,body{margin:0;background:transparent}</style><svg xmlns="http://www.w3.org/2000/svg" width="1320" height="244" viewBox="108 289 1320 244" style="overflow:hidden"><defs><filter id="fill" color-interpolation-filters="sRGB"><feFlood flood-color="${color}"/><feComposite in2="SourceGraphic" operator="in"/></filter></defs><image href="${wordmark}" width="1536" height="1024" filter="url(#fill)"/></svg>`);
      const filename=`brand/wordmark-${name}.png`;
      await page.screenshot({path:path.join(root,'static',filename),omitBackground:true});
      exports.push(filename);
    }
  } finally { await browser.close(); }
  await fs.writeFile(path.join(root,'assets/brand/exports.json'),JSON.stringify(exports,null,2)+'\n');
  console.log(`Exported ${exports.length} Astro90 assets.`);
}
main().catch(error=>{console.error(error);process.exitCode=1;});
