"""Render kinetic glass DevOps/MLOps workflows from local brand icons. Pillow required."""
from pathlib import Path
import math
import argparse
from functools import lru_cache
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
A=Path(__file__).resolve().parent.parent/'assets'
F='/System/Library/Fonts/Supplemental/'
def font(n,bold=False):return ImageFont.truetype(F+('Arial Bold.ttf' if bold else 'Arial.ttf'),n)
def text(d,xy,label,size=14,fill='#f5f5f7',bold=False):d.text(xy,label,font=font(size,bold),fill=fill,anchor='mm')
def load_icons(names):
    icons=[]
    for name in names:
        im=Image.open(A/'pipeline'/f'{name}.png').convert('RGBA');im.thumbnail((38,38),Image.Resampling.LANCZOS);icons.append(im)
    return icons
DEV_NAMES=['github','jenkins','github-actions','docker','kubernetes','grafana']
ML_NAMES=['azure','python','mlflow','docker','kubernetes','grafana']
DEV_ICONS=load_icons(DEV_NAMES);ML_ICONS=load_icons(ML_NAMES)

def glass_pod(im,xy,icon,active,t,index):
    x,y=map(round,xy);r=33;box=(x-r,y-r,x+r,y+r)
    w=66
    sample=im.crop(box).filter(ImageFilter.GaussianBlur(12)).convert('RGBA')
    tint=Image.new('RGBA',(w,w));d=ImageDraw.Draw(tint)
    for yy in range(w):
        shade=int(48+26*(1-yy/w)**2)
        d.line((0,yy,w,yy),fill=(183,207,240,shade))
    sample=Image.alpha_composite(sample,tint)
    # Moving, clipped reflection gives the lens surface depth.
    reflect=Image.new('RGBA',(w,w));rd=ImageDraw.Draw(reflect)
    xx=int(((t+index*.13)%1)*130)-70
    rd.polygon([(xx,0),(xx+17,0),(xx+65,w),(xx+48,w)],fill=(255,255,255,35))
    sample=Image.alpha_composite(sample,reflect)
    mask=Image.new('L',(w,w));ImageDraw.Draw(mask).ellipse((0,0,w-1,w-1),fill=255)
    im.paste(sample.convert('RGB'),(x-r,y-r),mask)
    d=ImageDraw.Draw(im)
    d.ellipse(box,outline='#d7f3ff' if active else '#5b738e',width=2 if active else 1)
    d.arc((x-r+2,y-r+2,x+r-2,y+r-2),200,294,fill='#c5d9ef',width=1)
    im.paste(icon,(x-icon.width//2,y-icon.height//2),icon)

def project(x,y,z,cx=690,cy=235,scale=1):
    return (cx+(x-z)*.87*scale,cy+(x+z)*.40*scale-y*scale)

def glass_cube(im,cx,cy,size,t,explode=0,logo=None):
    # Three translucent faces, separated glass layers, and travelling edge light.
    shadow=Image.new('RGB',im.size)
    sd=ImageDraw.Draw(shadow)
    sd.ellipse((cx-size*.85,cy+size*.65,cx+size*.85,cy+size*.95),fill='#102035')
    im.paste(ImageChops.add(im,shadow.filter(ImageFilter.GaussianBlur(15))))
    d=ImageDraw.Draw(im,'RGBA')
    def pt(x,y,z):return project(x,y,z,cx,cy,1)
    h=size/2
    faces=[([(-h,-h,-h),(h,-h,-h),(h,h,-h),(-h,h,-h)],(77,140,231,62)),
           ([(h,-h,-h),(h,-h,h),(h,h,h),(h,h,-h)],(122,98,226,78)),
           ([(-h,h,-h),(h,h,-h),(h,h,h),(-h,h,h)],(188,229,255,88))]
    for pts,color in faces:
        poly=[pt(*a) for a in pts]
        d.polygon(poly,fill=color);d.line(poly+[poly[0]],fill=(166,211,255,190),width=1)
    for k in range(3):
        yy=-h+k*size/2+explode*(k-1)
        pts=[pt(-h,yy,-h),pt(h,yy,-h),pt(h,yy,h),pt(-h,yy,h)]
        d.polygon(pts,fill=(118,190,255,18));d.line(pts+[pts[0]],fill=(157,213,255,90),width=1)
    sweep=(t%1)*size-h
    line=[pt(-h,sweep,-h),pt(h,sweep,-h),pt(h,sweep,h)]
    d.line(line,fill=(180,242,255,240),width=2)
    if logo:
        mark=logo.copy();mark.thumbnail((size*.40,size*.40),Image.Resampling.LANCZOS)
        im.paste(mark,(round(cx-mark.width/2),round(cy-size*.17-mark.height/2)),mark)

def visual(im,stage,u,t,ml):
    d=ImageDraw.Draw(im,'RGBA')
    # The workbench is a floating glass wafer with a luminous circuit substrate.
    platform=[(451,277),(681,383),(923,268),(693,161)]
    d.polygon([(x,y+9) for x,y in platform],fill=(16,23,47,200))
    d.polygon(platform,fill=(83,119,182,22));d.line(platform+[platform[0]],fill=(111,157,214,95),width=1)
    for k in range(1,8):
        a=k/8
        d.line((451+242*a,277-116*a,681+242*a,383-115*a),fill=(110,155,213,20),width=1)
        d.line((451+230*a,277+106*a,693+230*a,161+107*a),fill=(110,155,213,20),width=1)
    # A moving light underneath refracts through the platform.
    for k in range(28):
        q=(t+k/28)%1;x=470+q*440;y=330+18*math.sin(q*math.tau+t*math.tau)
        d.ellipse((x-1,y-1,x+1,y+1),fill=(125,154,234,70))
    if stage==0:
        # Data shards fly into a focal point, forming the first model/release.
        for k in range(30):
            q=(u+k/30)%1
            x=480+q*250;y=130+(k%6)*26+(235-(130+(k%6)*26))*q
            sz=4+3*(1-q)
            d.polygon([(x-sz,y),(x,y-sz/2),(x+sz,y),(x,y+sz/2)],fill=(115,204,255,130),outline=(170,225,255,200))
        glass_cube(im,724,230,48+30*u,t)
    elif stage==1:
        # A neural lattice lights up along connections layer by layer.
        layers=[]
        for j in range(4):
            layer=[]
            for k in range(5):
                x=541+j*83;y=152+k*28+j*8+8*math.sin(u*math.tau+j)
                layer.append((x,y))
            layers.append(layer)
        for j in range(3):
            for k,a in enumerate(layers[j]):
                for l,b in enumerate(layers[j+1]):
                    d.line((*a,*b),fill=(92,127,206,45),width=1)
                    if (k+l)%4==0:
                        q=(u*2+j*.25)%1;x=a[0]+(b[0]-a[0])*q;y=a[1]+(b[1]-a[1])*q
                        d.ellipse((x-2,y-2,x+2,y+2),fill=(183,215,255,230))
        for j,layer in enumerate(layers):
            for k,(x,y) in enumerate(layer):
                r=4+2*math.sin(u*math.tau+j+k)**2
                d.ellipse((x-r,y-r,x+r,y+r),fill=(106,151,242,130),outline=(196,219,255,220))
    elif stage==2:
        # The registry assembles a suspended glass artifact around its logo.
        glass_cube(im,690,230,118,t,explode=23*math.sin(u*math.pi)**2,logo=(ML_ICONS if ml else DEV_ICONS)[2])
        for k in range(3):
            y=167+k*42-12*math.sin(u*math.pi)
            d.line((821,y,867,y),fill=(146,206,243,130),width=1)
            d.ellipse((811,y-3,817,y+3),fill=(132,230,195,190))
    elif stage==3:
        # Panels lift and close around the packaged artifact.
        lift=30*math.sin(math.pi*u)**2
        glass_cube(im,690,235,104,t,explode=lift,logo=(ML_ICONS if ml else DEV_ICONS)[3])
        for dx in [-118,118]:
            x=690+dx*(1-.3*math.sin(u*math.pi));y=220
            d.line((x,y-38,x,y+38),fill=(166,193,247,115),width=2)
            d.line((x-8,y-30,x+8,y-23),fill=(164,219,255,180),width=1)
    else:
        # Deployment fans one artifact into a live three-node cluster.
        coords=[(597,234),(772,234),(686,309)]
        for j,(x,y) in enumerate(coords):
            d.line((690,181,x,y),fill=(125,159,221,100),width=1)
            q=(u+j/3)%1
            xx=690+(x-690)*q;yy=181+(y-181)*q
            d.ellipse((xx-3,yy-3,xx+3,yy+3),fill=(144,224,255,220))
            glass_cube(im,x,y-6*math.sin(u*math.tau+j),59,t+j/3,logo=(ML_ICONS if ml else DEV_ICONS)[4])
        if stage==5:
            # Telemetry becomes a continuous signal, closing the learning loop.
            pts=[]
            for x in range(490,902,3):
                y=130+18*math.sin(x*.04-u*math.tau)*math.exp(-((x-710)/160)**2)
                pts.append((x,y))
            d.line(pts,fill=(129,233,208,220),width=2)
            q=u
            d.arc((491,100,897,352),10,170,fill=(127,205,195,100),width=1)
            x=690+194*math.cos(q*math.pi);y=226+113*math.sin(q*math.pi)
            d.ellipse((x-3,y-3,x+3,y+3),fill=(163,245,216,240))

@lru_cache(maxsize=2)
def backdrop(ml):
    im=Image.new('RGB',(960,440),'#030508')
    glow=Image.new('RGB',im.size);d=ImageDraw.Draw(glow)
    d.ellipse((430,70,835,355),fill='#132c47')
    d.ellipse((650,150,940,395),fill='#271a47' if ml else '#152f3e')
    im=ImageChops.add(im,glow.filter(ImageFilter.GaussianBlur(65)))
    return im

def raw_scene(t,ml=False,stage=None,u=None):
    if stage is None:stage=int(t*6)%6
    if u is None:u=(t*6)%1
    im=backdrop(ml).copy()
    # A travelling beam quietly reveals the glass workbench.
    visual(im,stage,u,t,ml)
    d=ImageDraw.Draw(im)
    d.text((44,32),'MLOPS / THE MODEL ENGINE' if ml else 'DEVOPS / THE RELEASE ENGINE',font=font(12,True),fill='#8ba5c5')
    headlines=[('From data.','To intelligence.'),('Patterns emerge.','Models learn.'),('A model.','With a lineage.'),('Packaged once.','Ready to move.'),('One model.','Many possibilities.'),('Observe.','Learn. Repeat.')] if ml else [('An idea.','Becomes code.'),('Build with intent.','Ship with trust.'),('Every change.','Put to the test.'),('One artifact.','Ready anywhere.'),('Release safely.','Scale confidently.'),('Listen to signals.','Improve the system.')]
    for y,line in zip([101,146],headlines[stage]):d.text((44,y),line,font=font(31,True),fill='#eff4ff')
    descriptions=['Ingest and prepare the signal.','Turn experiments into models.','Track versions with MLflow.','Build a portable model image.','Serve on a resilient platform.','Feed evaluation into retraining.'] if ml else ['Version the source of every release.','Automate the repeatable work.','Validate before it reaches production.','Keep delivery portable and repeatable.','Roll out containers with control.','Turn telemetry into better decisions.']
    d.text((45,193),descriptions[stage],font=font(14),fill='#92a9c5')
    icons=ML_ICONS if ml else DEV_ICONS
    names=['Microsoft Azure','Python','MLflow','Docker','Kubernetes','Grafana'] if ml else ['GitHub','Jenkins','GitHub Actions','Docker','Kubernetes','Grafana']
    glass_pod(im,(69,263),icons[stage],True,t,stage)
    d=ImageDraw.Draw(im)
    d.text((116,245),names[stage],font=font(18,True),fill='#e5edf8')
    labels=['DATA INGESTION','MODEL TRAINING','MODEL REGISTRY','MODEL PACKAGING','MODEL SERVING','EVALUATION & FEEDBACK'] if ml else ['SOURCE CONTROL','BUILD AUTOMATION','QUALITY GATES','IMAGE PACKAGING','CONTAINER DEPLOYMENT','OBSERVABILITY & FEEDBACK']
    d.text((117,273),labels[stage],font=font(10),fill='#829bb8')
    # Six low-key timeline segments, rather than a diagram of static nodes.
    for j in range(6):
        x=45+j*49;d.rounded_rectangle((x,338,x+37,341),radius=1,fill='#2b394d')
        if j<=stage:
            w=37 if j<stage else max(2,round(37*u))
            d.rounded_rectangle((x,338,x+w,341),radius=1,fill='#b9d9f9' if ml else '#8fdfe7')
    d.text((45,360),f'0{stage+1} / 06   ·   CONTINUOUS '+('LEARNING' if ml else 'DELIVERY'),font=font(11),fill='#8296b0')
    # The visual itself is illustrative; do not invent production measurements.
    text(d,(690,414),'DATA → MODEL → PRODUCTION → FEEDBACK' if ml else 'CODE → ARTIFACT → PRODUCTION → FEEDBACK',10,'#758ba5')
    return im

def scene(t,ml=False):
    stage=int(t*6)%6
    u=(t*6)%1
    current=raw_scene(t,ml,stage,u)
    if u > .78:
        q=(u-.78)/.22
        eased=q*q*(3-2*q)
        return Image.blend(current,raw_scene(t,ml,(stage+1)%6,0),eased)
    return current

# Shared palette prevents per-frame palette changes and limits GIF banding.
def save_gif(frames,path):
    sheet=Image.new('RGB',(960,440*6))
    for j,k in enumerate([15,45,75,105,135,165]):sheet.paste(frames[k].resize((960,440)),(0,j*440))
    palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    encoded=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
    temporary=path.with_suffix(".tmp.gif")
    encoded[0].save(temporary,save_all=True,append_images=encoded[1:],duration=80,loop=0,optimize=True,disposal=1)
    temporary.replace(path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-mlops",action="store_true",help="Also render the optional standalone model-engine concept")
    include_mlops=parser.parse_args().include_mlops
    from generate_hero_hq import main as generate_hq_hero
    generate_hq_hero()
    if include_mlops:
        ml_frames=[scene(i/180,True) for i in range(180)]
        save_gif(ml_frames,A/'mlops-enhanced.gif')
        ml_frames[75].save(A/'mlops-workflow-preview.png')
    from generate_role_banner import main as generate_roles
    generate_roles()
    from generate_stack_showcase import main as generate_stack
    generate_stack()
    from generate_production_console import main as generate_console
    generate_console()
    print('Generated 4K hero and animated headings.')

if __name__ == "__main__":
    main()
