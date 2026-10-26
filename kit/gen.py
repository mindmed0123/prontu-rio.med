import base64,io,re,sys,json
from PIL import Image, ImageFilter
cfg=json.load(open(sys.argv[1]))
def crop(path,W,H,fx=0.5,fy=0.5,zoom=1.0):
    im=Image.open(path).convert('RGB'); w,h=im.size
    s=max(W/w,H/h)*zoom; cw,ch=W/s,H/s
    x0=min(max(0,(w-cw)*fx),w-cw); y0=min(max(0,(h-ch)*fy),h-ch)
    im=im.crop((round(x0),round(y0),round(x0+cw),round(y0+ch))).resize((W,H),Image.LANCZOS)
    print(path.split('/')[-1],'scale',round(s,3),'(<=1 is no upscale)')
    return im
def uri(im,q=94):
    b=io.BytesIO(); im.save(b,'JPEG',quality=q,subsampling=0); return 'data:image/jpeg;base64,'+base64.b64encode(b.getvalue()).decode()
t=open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'template-carrossel.html')).read()
c=cfg['capa']; A=crop(c['img'],1080,1350,c.get('fx',.5),c.get('fy',.5),c.get('zoom',1))
if c.get('topshade'):
    from PIL import Image as I2
    g=I2.new('L',(1,1350)); 
    for y in range(1350): g.putpixel((0,y),int(255*c['topshade']*max(0,1-y/380)))
    A=I2.composite(I2.new('RGB',A.size,(10,15,18)),A,g.resize(A.size))
Au=uri(A)
fot=t.index('<div class="fotos">'); end=t.index('</div>\n        <div class="sombra">')
t=t[:fot]+'<div class="fotos">\n'+''.join(f'<div class="foto"><img src="{Au}" alt="" style="width:300%;max-width:none;margin-left:{m};object-position:50% 50%"></div>' for m in ['0','-100%','-200%'])+'\n'+t[end:]
for k,v in zip(['As notícias do','Mundo da <i>Medicina</i>','mais importantes do dia'],c['tarjas']): t=t.replace('>'+k+'<','>'+v+'<',1)
labels=['CAMPO: foto da notícia 1 · 976','CAMPO: foto da notícia 2 · 976','CAMPO: foto da notícia 3 · 976']
sizes=[(976,780),(976,640),(976,780)]
ims=[]
for lab,(W,H),s in zip(labels,sizes,cfg['slides']):
    im=crop(s['img'],W,H,s.get('fx',.5),s.get('fy',.5),s.get('zoom',1)); ims.append(im)
    i=t.index(lab); j=t.index('<div class="foto vazia"',i); k=t.index('</div>',j)+6
    t=t[:j]+f'<div class="foto"><img src="{uri(im)}" alt=""></div>'+t[k:]
hs=re.findall(r'<h2>(?!<span).*?</h2>',t)
for h,s in zip(hs,cfg['slides']): t=t.replace(h,'<h2>'+s['h']+'</h2>',1)
ps=re.findall(r'<p class="texto">.*?</p>',t,flags=re.S)
for p,s in zip(ps,cfg['slides']): t=t.replace(p,'<p class="texto">'+s['t']+'</p>',1); print(len(re.sub('<[^>]+>','',s['h'])),len(s['t']))
mini=[A]+ims[:2] if cfg.get('mini','capa')=='capa' else ims
mi=t.index('<div class="miniaturas">'); me=t.index('</div>\n            <!-- CAMPO: número',mi)
t=t[:mi]+'<div class="miniaturas">'+''.join(f'<div class="foto"><img src="{uri(m.resize((m.width//3,m.height//3),Image.LANCZOS),90)}" alt=""></div>' for m in mini)+t[me:]
t=t.replace('</head>','<style>.escala{transform:none!important}</style></head>')
open(cfg['out'],'w').write(t)
