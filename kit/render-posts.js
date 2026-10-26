const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1200,height:1400}});
await p.goto('file://'+process.argv[2]);await p.waitForTimeout(2500);
const ids=await p.$$eval('section.s',s=>s.map(x=>x.id));
for(const id of ids){await p.locator('#'+id).screenshot({path:process.argv[3]+'/'+id+'.png'});}
const over=await p.$$eval('section.s',s=>s.filter(x=>x.scrollHeight>x.clientHeight+2).map(x=>x.id));
console.log(ids.length,'overflow:',over);
const f=await p.evaluate(()=>document.fonts.check('40px "Inter Tight"'));console.log('font',f);await b.close();})();
