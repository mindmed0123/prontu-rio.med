import re,sys,subprocess,io
from PIL import Image
def get(u): return subprocess.run(['curl','-s','-L','-A','Mozilla/5.0',u],capture_output=True).stdout
out=sys.argv[1]
for page in sys.argv[2:]:
    owner,pid=re.search(r'/photos/([^/]+)/(\d+)',page).groups()
    t=get(f'https://www.flickr.com/photos/{owner}/{pid}/').decode('utf8','ignore').replace('\\/','/')
    lic=re.search(r'"license":"?(\d+)',t)
    urls=set(re.findall(r'(live\.staticflickr\.com/\d+/'+pid+r'_[a-z0-9]+_(6k|5k|4k|3k|k|h|b)\.jpg)',t))
    order=['6k','5k','4k','3k','k','h','b']; ok=None
    for u,_ in sorted(urls,key=lambda x:order.index(x[1])):
        d=get('https://i0.wp.com/'+u+'?quality=100')
        try: im=Image.open(io.BytesIO(d)); im.load(); open(f'{out}/{pid}.jpg','wb').write(d); ok=(u.split('_')[-1],im.size); break
        except Exception: pass
    print(pid,'lic',lic.group(1) if lic else '?',ok)
