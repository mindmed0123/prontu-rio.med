const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1300,height:1500},deviceScaleFactor:1});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(2500);await p.evaluate(()=>document.fonts.ready);
await p.evaluate(()=>{document.querySelectorAll('.escala').forEach(e=>{e.style.transform='none';e.parentElement.style.width='1080px';e.parentElement.style.height='1350px';});});
const names=['01-capa','02-noticia-1','03-noticia-2','04-noticia-3','05-newsletter'];
const n=await p.locator('section.slide').count();
for(let i=0;i<n;i++){await p.locator('section.slide').nth(i).screenshot({path:process.argv[3]+'/'+names[i]+'.png'});}
const ov=await p.$$eval('section.slide h2, section.slide p.texto',s=>s.map(x=>x.getBoundingClientRect().height));console.log('heights',ov.map(Math.round));
await b.close();})();
