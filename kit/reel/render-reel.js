// Uso: node kit/reel/render-reel.js <arquivo.html> <saida.mp4> [fps]
// Renderiza quadro a quadro (determinístico) e monta o MP4 1080x1920 com ffmpeg.
const {chromium}=require('playwright');
const fs=require('fs');const path=require('path');const {execSync}=require('child_process');
(async()=>{
  const html=path.resolve(process.argv[2]);const out=path.resolve(process.argv[3]);const fps=+(process.argv[4]||30);
  const dir=fs.mkdtempSync('/tmp/reel-');
  const b=await chromium.launch();
  const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
  await p.goto('file://'+html);await p.waitForTimeout(2500);await p.evaluate(()=>document.fonts.ready);
  const fontsOk=await p.evaluate(()=>['Instrument Serif','Inter Tight','JetBrains Mono'].map(f=>f+':'+document.fonts.check('40px "'+f+'"')));
  console.log('fonts',fontsOk.join(' '));
  const dur=await p.evaluate(()=>window.DUR);const n=Math.round(dur*fps);
  for(let i=0;i<n;i++){
    await p.evaluate(t=>window.setT(t),i/fps);
    await p.screenshot({path:`${dir}/f${String(i).padStart(5,'0')}.png`});
    if(i%60===0)console.log('frame',i,'/',n);
  }
  await b.close();
  execSync(`ffmpeg -y -loglevel error -framerate ${fps} -i ${dir}/f%05d.png -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium -movflags +faststart ${out}`);
  fs.rmSync(dir,{recursive:true,force:true});
  console.log('ok',out);
})();
