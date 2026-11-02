"""Animate rendered SVG stages from generate_reliability_architecture.py."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parent.parent
TMP=Path('/tmp/profile-token-architecture')
flows=json.loads((TMP/'flows.json').read_text())
stills=[Image.open(TMP/f'stage-{i}.png').convert('RGB') for i in range(6)]
def point(path,q):
    lengths=[math.dist(a,b) for a,b in zip(path,path[1:])];distance=q*sum(lengths)
    for a,b,length in zip(path,path[1:],lengths):
        if distance<=length:
            f=distance/length
            return a[0]+(b[0]-a[0])*f,a[1]+(b[1]-a[1])*f
        distance-=length
    return path[-1]
frames=[]
for i in range(120):
    t=i/120;stage=int(t*6);u=t*6-stage
    im=stills[stage].copy()
    if u>.82:
        q=(u-.82)/.18;im=Image.blend(im,stills[(stage+1)%6],q*q*(3-2*q))
    # A clipped low-opacity reflection moves across the active glass container.
    x=324 if stage<3 else (586 if stage==3 else 850)
    pane=Image.new('RGBA',(244,363));pd=ImageDraw.Draw(pane)
    sx=round(u*440)-130
    pd.polygon([(sx,0),(sx+20,0),(sx+160,363),(sx+140,363)],fill=(222,241,255,12))
    mask=Image.new('L',(244,363));ImageDraw.Draw(mask).rounded_rectangle((0,0,243,362),radius=14,fill=255)
    pane.putalpha(ImageChops.multiply(pane.getchannel('A'),mask))
    area=Image.alpha_composite(im.crop((x,179,x+244,542)).convert('RGBA'),pane)
    im.paste(area.convert('RGB'),(x,179))
    d=ImageDraw.Draw(im)
    path=flows[stage]
    for k in range(12):
        q=(u-k*.018)%1;x,y=point(path,q);a=1-k/12
        color=tuple(round(c*a) for c in ([203,168,255] if stage<3 else [122,235,192]))
        d.ellipse((x-4,y-4,x+4,y+4),fill=color)
    if stage>=4:
        path=[(978,179),(978,99),(150,99),(150,179)]
        x,y=point(path,u);d.ellipse((x-4,y-4,x+4,y+4),fill='#93eaca')
    frames.append(im)
sample=Image.new('RGB',(1440,850*3))
for j,k in enumerate([10,50,90]):sample.paste(frames[k],(0,j*850))
palette=sample.quantize(colors=256)
encoded=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
out=ROOT/'assets/work/reliability-glass-architecture.gif'
temporary=out.with_suffix(".tmp.gif")
encoded[0].save(temporary,save_all=True,append_images=encoded[1:],duration=100,loop=0,optimize=True)
temporary.replace(out)
print('Generated architecture GIF:',round(out.stat().st_size/1024),'KB')
