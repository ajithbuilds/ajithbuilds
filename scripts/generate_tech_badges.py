"""Animate locally rasterized vector tech tags. Requires Pillow; no network calls."""
from pathlib import Path
import math,re,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageChops
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'assets/tech'
SCALE=3

def build(slug):
    original=Image.open(A/'raster'/f'{slug}.png').convert('RGB')
    sw,sh=original.size
    w,h=sw+18,84
    # Original vector-rendered wordmark/text remains stable throughout the loop.
    bg=original.getpixel((sw-2,2))
    tile=Image.new('RGB',(w,h),bg)
    tile.paste(original,(9,12))
    svg=ET.parse(A/f'{slug}.svg').getroot()
    # Locate the actual logo viewport; do not move the product name.
    logo_node=next((n for n in svg.iter() if n.tag.endswith('image')),None)
    if logo_node is None:
        logo_node=next(n for n in svg if n.tag.endswith('svg'))
    x=int(float(logo_node.attrib.get('x',4))*SCALE)+9
    y=int(float(logo_node.attrib.get('y',3))*SCALE)+12
    iw=round(float(logo_node.attrib.get('width',16))*SCALE)
    ih=round(float(logo_node.attrib.get('height',14))*SCALE)
    icon=tile.crop((x,y,x+iw,y+ih))
    base=tile.copy();ImageDraw.Draw(base).rectangle((x-2,y-5,x+iw+2,y+ih+5),fill=bg)
    mask=Image.new('L',(w,h));ImageDraw.Draw(mask).rounded_rectangle((0,0,w-1,h-1),radius=12,fill=255)
    phase=int(hashlib.sha256(slug.encode()).hexdigest()[:4],16)/65536*math.tau
    frames=[]
    for i in range(32):
        t=i/32
        frame=base.copy()
        bob=round(3*math.sin(t*math.tau+phase))
        frame.paste(icon,(x,y+bob))
        overlay=Image.new('RGB',(w,h));d=ImageDraw.Draw(overlay)
        # Soft travelling sheen across the surface, never replacing the icon.
        xx=round(t*(w+90))-90
        for j in range(34):
            val=round(15*math.sin(j/34*math.pi)**2)
            d.line((xx+j,0,xx+j+28,h),fill=(val,val,val),width=1)
        frame=ImageChops.add(frame,overlay)
        d=ImageDraw.Draw(frame)
        strength=.25+.15*(.5+.5*math.sin(t*math.tau+phase))
        edge=tuple(round(c+(255-c)*strength) for c in bg)
        d.rounded_rectangle((1,1,w-2,h-2),radius=12,outline=edge,width=2)
        # Opaque dark corners avoid GIF transparency fringes on a dark profile.
        final=Image.new('RGB',(w,h),'#0d1117');final.paste(frame,(0,0),mask);frames.append(final)
    samples=Image.new("RGB",(w,h*4))
    for j,k in enumerate([0,8,16,24]):samples.paste(frames[k],(0,j*h))
    palette=samples.quantize(colors=128)
    frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    temporary=A/f'{slug}.tmp.gif'
    frames[0].save(temporary,save_all=True,append_images=frames[1:],duration=80,loop=0,optimize=True)
    temporary.replace(A/f'{slug}.gif')
    return round(w/3),28

readme=(ROOT/'README.md').read_text()
slugs=sorted(set(re.findall(r'assets/tech/([a-z0-9-]+)\.(?:svg|gif)',readme)))
sizes={slug:build(slug) for slug in slugs}
# Explicit display dimensions retain compact tags despite high-resolution GIFs.
pattern=r'!\[([^\]]+)\]\(assets/tech/([a-z0-9-]+)\.svg\)'
readme=re.sub(pattern,lambda m:f'<img src="assets/tech/{m[2]}.gif" width="{sizes[m[2]][0]}" height="28" alt="{m[1]}" />',readme)
(ROOT/'README.md').write_text(readme)
print(f'Generated {len(slugs)} animated tech tags (32 frames each).')
