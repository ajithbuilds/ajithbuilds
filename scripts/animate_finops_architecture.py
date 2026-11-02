"""Animate the FinOps architecture from local SVG stage renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import math,json
ROOT=Path(__file__).resolve().parent.parent
TMP=Path('/tmp/profile-finops-architecture')
flows=json.loads((TMP/'flows.json').read_text())
stills=[Image.open(TMP/f'stage-{i}.png').convert('RGB') for i in range(6)]
def point(path,q):
 lengths=[math.dist(a,b) for a,b in zip(path,path[1:])];distance=q*sum(lengths)
 for a,b,length in zip(path,path[1:],lengths):
  if distance<=length:
   f=distance/length;return a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f
  distance-=length
 return path[-1]
frames=[]
boxes=json.loads((TMP/'boxes.json').read_text())
for i in range(144):
 t=i/144;stage=int(t*6);u=t*6-stage
 im=stills[stage].copy()
 if u>.82:
  q=(u-.82)/.18;im=Image.blend(im,stills[(stage+1)%6],q*q*(3-2*q))
 x,y,w,h=boxes[stage];reflect=Image.new('RGBA',(w,h));d=ImageDraw.Draw(reflect)
 sx=round(u*(w+180))-100
 d.polygon([(sx,0),(sx+18,0),(sx+98,h),(sx+80,h)],fill=(225,243,255,13))
 mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=14,fill=255)
 reflect.putalpha(ImageChops.multiply(reflect.getchannel('A'),mask))
 im.paste(Image.alpha_composite(im.crop((x,y,x+w,y+h)).convert('RGBA'),reflect).convert('RGB'),(x,y))
 d=ImageDraw.Draw(im)
 for k in range(12):
  q=(u-k*.015)%1;x,y=point(flows[stage],q);alpha=1-k/12
  color=tuple(round(c*alpha) for c in ([194,166,245] if stage<4 else [143,228,193]))
  d.ellipse((x-4,y-4,x+4,y+4),fill=color)

 frames.append(im)
sample=Image.new('RGB',(1440,960*3))
for j,k in enumerate([12,60,108]):sample.paste(frames[k],(0,j*960))
palette=sample.quantize(colors=256)
encoded=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
p=ROOT/'assets/work/finops-glass-architecture.gif'
temporary=p.with_suffix(".tmp.gif")
encoded[0].save(temporary,save_all=True,append_images=encoded[1:],duration=90,loop=0,optimize=True)
temporary.replace(p)
print('Generated FinOps glass animation:',round(p.stat().st_size/1024),'KB')
