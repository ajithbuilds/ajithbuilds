"""Render the release-engine hero from native vectors at 3840 pixels wide."""
from pathlib import Path
import math,base64,json,subprocess,tempfile
from html import escape
from PIL import Image
from brand_icons import image as brand_image
ROOT=Path(__file__).resolve().parent.parent
A=ROOT/'assets'
NAMES=['github','jenkins','github-actions','docker','kubernetes','grafana']
LABELS=['GitHub','Jenkins','GitHub Actions','Docker','Kubernetes','Grafana']
HEADS=[('An idea.','Becomes code.'),('Build with intent.','Ship with trust.'),('Every change.','Put to the test.'),('One artifact.','Ready anywhere.'),('Release safely.','Scale confidently.'),('Listen to signals.','Improve the system.')]
DESCS=['Version the source of every release.','Automate the repeatable work.','Validate before it reaches production.','Keep delivery portable and repeatable.','Roll out containers with control.','Turn telemetry into better decisions.']
TAGS=['SOURCE CONTROL','BUILD AUTOMATION','QUALITY GATES','IMAGE PACKAGING','CONTAINER DEPLOYMENT','OBSERVABILITY & FEEDBACK']
ML_NAMES=['azure','python','mlflow','docker','kubernetes','grafana']
ML_LABELS=['Microsoft Azure','Python','MLflow','Docker','Kubernetes','Grafana']
ML_HEADS=[('From data.','To intelligence.'),('Train with intent.','Evaluate with care.'),('Every model.','With a lineage.'),('Package once.','Serve consistently.'),('Release a model.','Scale inference.'),('Observe drift.','Learn. Improve.')]
ML_DESCS=['Prepare and version the training data.','Train and compare model candidates.','Track experiments, metrics and versions.','Build a reproducible inference image.','Roll out a versioned inference service.','Monitor quality and feed back to training.']
ML_TAGS=['DATA PREPARATION','TRAINING & EVALUATION','EXPERIMENT TRACKING','MODEL PACKAGING','MODEL SERVING','MONITORING & FEEDBACK']
def text(x,y,s,size,fill='#eff4ff',bold=False,center=False):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{700 if bold else 400}" text-anchor="{"middle" if center else "start"}">{escape(s)}</text>'
def icon(name,x,y,size):
 return brand_image(name,x,y,size)
def pt(x,y,z,cx,cy):return (cx+(x-z)*.87,cy+(x+z)*.4-y)
def polygon(points,fill,stroke='#a6d3ff',opacity='.7'):
 return '<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-opacity=".65" stroke-width=".8"/>'
def cube(cx,cy,size,t,name=None):
 h=size/2;s=''
 for coords,color in [([(-h,-h,-h),(h,-h,-h),(h,h,-h),(-h,h,-h)],'#365e91'), ([(h,-h,-h),(h,-h,h),(h,h,h),(h,h,-h)],'#5c4c9e'),([(-h,h,-h),(h,h,-h),(h,h,h),(-h,h,h)],'#9fc8e9')]:s+=polygon([pt(*p,cx,cy) for p in coords],color,opacity='.48')
 for k in range(3):
  yy=-h+k*h+math.sin(t*math.tau)*10*(k-1)
  s+=polygon([pt(-h,yy,-h,cx,cy),pt(h,yy,-h,cx,cy),pt(h,yy,h,cx,cy),pt(-h,yy,h,cx,cy)],'#92caff',opacity='.07')
 yy=(t%1)*size-h;p=[pt(-h,yy,-h,cx,cy),pt(h,yy,-h,cx,cy),pt(h,yy,h,cx,cy)]
 s+='<polyline points="'+' '.join(f'{x},{y}' for x,y in p)+'" fill="none" stroke="#b4f2ff" stroke-width="1.2"/>'
 if name:s+=icon(name,cx-size*.17,cy-size*.3,size*.34)
 return s

def svg(stage,u,ml=False):
 names=ML_NAMES if ml else NAMES
 labels=ML_LABELS if ml else LABELS
 heads=ML_HEADS if ml else HEADS
 descs=ML_DESCS if ml else DESCS
 tags=ML_TAGS if ml else TAGS
 t=(stage+u)/6
 s='''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="3040" viewBox="0 0 960 760" role="img" aria-labelledby="title"><title id="title">AJITH KUMAR BALASUBRAMANIAN — Reliable by design</title><defs><radialGradient id="glow"><stop stop-color="#19344f"/><stop offset="1" stop-color="#030508"/></radialGradient><linearGradient id="lens" x2="1" y2="1"><stop stop-color="#7a9cb7" stop-opacity=".45"/><stop offset="1" stop-color="#19263d" stop-opacity=".8"/></linearGradient></defs><rect width="960" height="760" fill="black"/><g font-family="Arial, Helvetica, sans-serif">'''
 s+=text(480,110,'AJITH KUMAR',52,bold=True,center=True)+text(480,171,'BALASUBRAMANIAN',52,bold=True,center=True)+text(480,222,'Reliable by design.',30,'#d8d8dd',True,True)+text(480,261,'Senior DevOps / Platform Engineer  ·  SRE  ·  AIOps',17,'#a1a1a6',center=True)
 s+='<g transform="translate(0,282)"><rect width="960" height="440" fill="#030508"/><ellipse cx="700" cy="235" rx="310" ry="220" fill="url(#glow)"/>'
 s+=text(44,44,'MLOPS / THE MODEL ENGINE' if ml else 'DEVOPS / THE RELEASE ENGINE',12,'#9cb5d2',True)
 for y,line in zip([127,172],heads[stage]):s+=text(44,y,line,31,bold=True)
 s+=text(45,207,descs[stage],14,'#a3b8d1')
 s+='<circle cx="69" cy="263" r="33" fill="url(#lens)" stroke="#bedbeb" stroke-width="1.2"/>'+icon(names[stage],50,244,38)
 s+=text(116,263,labels[stage],18,bold=True)+text(117,281,tags[stage],10,'#9fb8d5')
 platform=[(451,277),(681,383),(923,268),(693,161)]
 s+=polygon(platform,'#263858',opacity='.35')
 for k in range(1,8):
  q=k/8;s+=f'<path d="M{451+242*q} {277-116*q} {681+242*q} {383-115*q} M{451+230*q} {277+106*q} {693+230*q} {161+107*q}" stroke="#7d9dc8" stroke-opacity=".13" stroke-width=".6"/>'
 if stage==1:
  layers=[[(550+j*77,151+k*30+j*8) for k in range(5)] for j in range(4)]
  for j in range(3):
   for k,a in enumerate(layers[j]):
    for n,b in enumerate(layers[j+1]):
     s+=f'<path d="M{a[0]} {a[1]} {b[0]} {b[1]}" stroke="#7297d8" stroke-opacity=".2" stroke-width=".7"/>'
     if (k+n)%4==0:
      q=(u+j*.2)%1;x=a[0]+(b[0]-a[0])*q;y=a[1]+(b[1]-a[1])*q;s+=f'<circle cx="{x}" cy="{y}" r="2" fill="#b8e6ff"/>'
  for j,layer in enumerate(layers):
   for k,(x,y) in enumerate(layer):s+=f'<circle cx="{x}" cy="{y}" r="{4+math.sin(u*math.tau+j+k)**2}" fill="#5175ad" stroke="#bcdbff" stroke-width=".8"/>'
 elif stage>=4:
  for k,(x,y) in enumerate([(597,234),(772,234),(686,309)]):
   s+=f'<path d="M690 174 {x} {y}" stroke="#749bd0" stroke-opacity=".6"/>'
   q=(u+k/3)%1;xx=690+(x-690)*q;yy=174+(y-174)*q;s+=f'<circle cx="{xx}" cy="{yy}" r="2.5" fill="#a1e8ff"/>'
   s+=cube(x,y,59,t+k/3,'kubernetes')
  if stage==5:
   pts=[(x,130+18*math.sin(x*.04-u*math.tau)*math.exp(-((x-710)/160)**2)) for x in range(490,902,2)]
   s+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#81e9d0" stroke-width="1.5"/>'
 else:
  s+=cube(690,235,110,t,names[stage])
  if stage==0:
   for k in range(20):
    q=(u+k/20)%1;x=480+q*175;y=150+(k%5)*26;s+=polygon([(x-3,y),(x,y-2),(x+3,y),(x,y+2)],'#9adfff')
 if ml and stage==5:
  s+='<path d="M850 300C915 110 620 60 550 190" fill="none" stroke="#bdadf4" stroke-width="1.2" stroke-dasharray="5 5"/><path d="m545 182 5 9 10-3" fill="none" stroke="#bdadf4" stroke-width="1.5"/>'
  s+=text(710,90,'EVALUATE → RETRAIN',10,'#bcaee7',center=True)
 for j in range(6):
  x=45+j*49;s+=f'<rect x="{x}" y="338" width="37" height="3" rx="1" fill="#2b394d"/>'
  if j<=stage:s+=f'<rect x="{x}" y="338" width="{37 if j<stage else max(2,37*u)}" height="3" rx="1" fill="#a2e4ef"/>'
 s+=text(45,371,f'0{stage+1} / 06   ·   '+('CONTINUOUS LEARNING' if ml else 'CONTINUOUS DELIVERY'),11,'#9aafc8')+text(690,418,'DATA → MODEL → INFERENCE → FEEDBACK' if ml else 'CODE → ARTIFACT → PRODUCTION → FEEDBACK',10,'#9aafc8',center=True)
 return s+'</g>'+text(480,746,'8+ years  ·  AWS / Azure / GCP',13,'#a1a1a6',center=True)+'</g></svg>'

def combined_svg(stage,u):
 dev=svg(stage,u,False);ml=svg(stage,u,True)
 marker='<g transform="translate(0,282)">'
 header=dev.split(marker)[0].replace('height="3040"','height="4800"').replace('viewBox="0 0 960 760"','viewBox="0 0 960 1200"').replace('height="760" fill="black"','height="1200" fill="black"')
 dev_scene=dev.split(marker)[1].split('</g>')[0]
 ml_scene=ml.split(marker)[1].split('</g>')[0]
 # Related material, distinct model-engine palette. Use separate gradient IDs
 # because both scenes share a single SVG document.
 header=header.replace('</defs>', '<radialGradient id="mlglow"><stop stop-color="#2b2349"/><stop offset="1" stop-color="#06060d"/></radialGradient><linearGradient id="mllens" x2="1" y2="1"><stop stop-color="#b5a0dd" stop-opacity=".42"/><stop offset="1" stop-color="#211d36" stop-opacity=".8"/></linearGradient></defs>')
 for old,new in [('url(#glow)','url(#mlglow)'),('url(#lens)','url(#mllens)'),('#030508','#06060d'),('#263858','#302844'),('#365e91','#655285'),('#5c4c9e','#4c727e'),('#9fc8e9','#d2c4ed'),('#92caff','#c2a9ef'),('#a6d3ff','#c8b9ed'),('#b4f2ff','#a5e9d5'),('#a2e4ef','#bda5ec'),('#9cb5d2','#c6b2e9'),('#9fb8d5','#baaed3'),('#7297d8','#a38ac9'),('#5175ad','#69538c'),('#bcdbff','#d5c2f3')]:
  ml_scene=ml_scene.replace(old,new)
 # Small orbit markers echo experiment/model lineage without changing layout.
 ml_scene+='<g fill="none" stroke="#c1a6e7" stroke-opacity=".28" stroke-width=".7"><ellipse cx="690" cy="275" rx="181" ry="62"/><ellipse cx="690" cy="275" rx="163" ry="48" stroke-dasharray="2 8"/></g>'
 orbit=u*math.tau
 ml_scene+=f'<circle cx="{690+181*math.cos(orbit):.2f}" cy="{275+62*math.sin(orbit):.2f}" r="2.5" fill="#a4e7d3"/>'
 return header+marker+dev_scene+'</g><g transform="translate(0,734)">'+ml_scene+'</g>'+text(480,1192,'8+ years  ·  AWS / Azure / GCP',13,'#a1a1a6',center=True)+'</g></svg>'

def main():
 with tempfile.TemporaryDirectory(prefix='hero-4k-') as tmp:
  sources=[combined_svg(j,k/8) for j in range(6) for k in range(8)]
  (A/'hero-enhanced.svg').write_text(combined_svg(3,.4))
  js="""const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');const v=JSON.parse(fs.readFileSync(0,'utf8'));v.svgs.forEach((s,i)=>fs.writeFileSync(v.dir+'/'+i+'.png',new Resvg(s).render().asPng()));"""
  subprocess.run(['node','-e',js],input=json.dumps({'svgs':sources,'dir':tmp}),text=True,cwd=ROOT,check=True)
  sheet=Image.new('RGB',(960,1200*6))
  for j in range(6):
   with Image.open(Path(tmp)/f'{j*8+3}.png') as im:sheet.paste(im.convert('RGB').resize((960,1200)),(0,j*1200))
  palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
  frames=[]
  for i in range(48):
   with Image.open(Path(tmp)/f'{i}.png') as im:frames.append(im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE))
  target=A/'hero-devops-mlops-glass-4k.tmp.gif';frames[0].save(target,save_all=True,append_images=frames[1:],duration=180,loop=0,optimize=False,disposal=1);target.replace(A/'hero-devops-mlops-glass-4k.gif')
  with Image.open(Path(tmp)/'27.png') as im:im.save(A/'hero-poster.png')
 from split_hero import main as split_panels
 split_panels()
 print('Rendered 3840 × 4800 hero: DevOps and MLOps visible together in all 48 frames.')
if __name__=='__main__':main()
