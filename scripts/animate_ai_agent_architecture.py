"""Animate the SCP AI Agent architecture from local SVG stage renders."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
import math,json
ROOT=Path(__file__).resolve().parent.parent
TMP=Path('/tmp/profile-ai-agent-architecture')
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
boxes=[(592,158,273,113),(274,383,236,180),(548,383,230,230),(810,383,250,230),(1090,515,300,125),(1090,383,300,88)]
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
 if stage==5:
  x,y=point([(510,535),(520,535),(520,735),(495,735),(495,754)],u)
  d.ellipse((x-4,y-4,x+4,y+4),fill='#9fe4d0')
 frames.append(im)
sample=Image.new('RGB',(1440,1050*3))
for j,k in enumerate([12,60,108]):sample.paste(frames[k],(0,j*1050))
palette=sample.quantize(colors=256)
encoded=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
p=ROOT/'assets/work/ai-agent-glass-architecture.gif'
temporary=p.with_suffix(".tmp.gif")
encoded[0].save(temporary,save_all=True,append_images=encoded[1:],duration=90,loop=0,optimize=True)
temporary.replace(p)
print('Generated AI Agent glass animation:',round(p.stat().st_size/1024),'KB')
