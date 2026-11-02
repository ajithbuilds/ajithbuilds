"""Crisp animated role graphics using the existing official product icon set."""
from pathlib import Path
import base64,json,math,subprocess,tempfile
from PIL import Image
from brand_icons import source as brand_source
ROOT=Path(__file__).resolve().parent.parent
ROLES=[('Platform Engineering','kubernetes','#8eddeb','Build foundations. Promote with control.'),('Site Reliability Engineering','prometheus','#9ce2c3','Observe health. Recover. Prevent recurrence.'),('Generative AI & MLOps','mlflow','#c6adf2','Track models. Serve intelligence. Learn.')]
def frame(stage,u):
 title,name,color,sub=ROLES[stage];p=brand_source(name)
 if not p.exists():p=ROOT/'assets/architecture-icons'/f'{name}.svg'
 data=base64.b64encode(p.read_bytes()).decode()
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="640" viewBox="0 0 960 160"><defs><linearGradient id="bg"><stop stop-color="#131f2c"/><stop offset="1" stop-color="#0a0c14"/></linearGradient></defs><rect width="960" height="160" rx="18" fill="url(#bg)"/><rect x=".5" y=".5" width="959" height="159" rx="18" fill="none" stroke="#344252"/><g font-family="Arial, Helvetica, sans-serif"><circle cx="57" cy="64" r="27" fill="#ffffff" fill-opacity=".06" stroke="{color}" stroke-opacity=".6"/><image x="39" y="46" width="36" height="36" href="data:image/svg+xml;base64,{data}"/><text x="101" y="65" font-size="27" font-weight="700" fill="#edf3fb">{title.replace('&','&amp;')}</text><text x="102" y="93" font-size="13" fill="#aabbd0">{sub}</text>'''
 if stage==0:
  for k in range(3):
   x=658+k*94;y=55+(k%2)*17
   s+=f'<path d="M{x} {y}l25-13 25 13v32l-25 13-25-13Z m0 0 25 13 25-13 m-25 13v32" fill="#79b3d8" fill-opacity=".15" stroke="{color}" stroke-width="1"/>'
   if k<2:
    q=(u+k*.3)%1;xx=x+51+q*42;s+=f'<path d="M{x+50} {y+16}h44" stroke="#607e99"/><circle cx="{xx}" cy="{y+16}" r="3" fill="{color}"/>'
 elif stage==1:
  pts=[(x,79+13*math.sin(x*.065-u*math.tau)*math.exp(-((x-770)/100)**2)) for x in range(655,910,2)]
  s+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+f'" fill="none" stroke="{color}" stroke-width="2"/>'
  s+=f'<circle cx="{655+u*253}" cy="79" r="3" fill="#d9fff1"/><path d="M880 30l16 6v12c0 10-16 18-16 18s-16-8-16-18V36Z m-8 16 6 6 11-12" fill="none" stroke="{color}" stroke-width="1.3"/>'
 else:
  for j in range(3):
   for k in range(3):
    x=677+j*94;y=44+k*28
    if j<2:
     for n in range(3):s+=f'<path d="M{x} {y} {x+94} {44+n*28}" stroke="{color}" stroke-opacity=".2"/>'
     q=(u+j*.3+k*.2)%1;s+=f'<circle cx="{x+94*q}" cy="{y+(72-y)*q}" r="2" fill="#a4e7d3"/>'
    s+=f'<circle cx="{x}" cy="{y}" r="4" fill="#3c3251" stroke="{color}"/>'
 for j in range(3):s+=f'<rect x="{102+j*47}" y="126" width="35" height="3" rx="1" fill="{color if j==stage else "#344252"}"/>'
 return s+'</g></svg>'
def main():
 with tempfile.TemporaryDirectory(prefix='role-banner-') as tmp:
  sources=[frame(j,k/12) for j in range(3) for k in range(12)]
  js="""const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let v=JSON.parse(fs.readFileSync(0,'utf8'));v.svgs.forEach((s,i)=>fs.writeFileSync(v.dir+'/'+i+'.png',new Resvg(s).render().asPng()));"""
  subprocess.run(['node','-e',js],input=json.dumps({'svgs':sources,'dir':tmp}),text=True,cwd=ROOT,check=True)
  sheet=Image.new('RGB',(960,480))
  for j in range(3):
   with Image.open(Path(tmp)/f'{j*12}.png') as im:sheet.paste(im.convert('RGB').resize((960,160)),(0,j*160))
  palette=sheet.quantize(colors=256);frames=[]
  for i in range(36):
   with Image.open(Path(tmp)/f'{i}.png') as im:frames.append(im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE))
  target=ROOT/'assets/role-banner-4k.gif';temp=target.with_suffix('.tmp.gif');frames[0].save(temp,save_all=True,append_images=frames[1:],duration=180,loop=0,optimize=False,disposal=1);temp.replace(target)
 print('Rendered three animated role scenes at 3840 × 640.')
if __name__=='__main__':main()
