"""Animate the outcome illustrations without changing the reported metrics."""
from pathlib import Path
import json,math,subprocess,tempfile
from PIL import Image
from generate_impact import ROOT

def dot(x,y,color,r=3):
 return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r+4}" fill="{color}" opacity=".13"/><circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{color}"/>'
def along(points,t):
 lengths=[math.dist(a,b) for a,b in zip(points,points[1:])];dist=t*sum(lengths)
 for a,b,length in zip(points,points[1:],lengths):
  if dist<=length:
   q=dist/length;return a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q
  dist-=length
 return points[-1]
def main():
 base=(ROOT/'assets/impact.svg').read_text();svgs=[]
 for i in range(72):
  t=i/72;overlay='<g>'
  # Follow the actual availability pulse; the healthy indicator gently breathes.
  xy=along([(52,245),(100,245),(112,233),(125,257),(142,217),(160,253),(172,245),(284,245)],(t*2)%1)
  overlay+=dot(*xy,'#b6f4ff')
  overlay+=f'<circle cx="320" cy="241" r="{20+4*math.sin(t*math.tau)**2}" fill="none" stroke="#8be6c9" opacity="{.2+.25*math.sin(t*math.tau)**2}"/>'
  # A release passes through build, verification, and release in sequence.
  phase=t*3;stage=int(phase)%3;u=phase%1;xx=436+stage*116
  overlay+=f'<rect x="{xx}" y="203" width="92" height="76" rx="14" fill="#a9c9ff" fill-opacity=".09" stroke="#b9d9ff" stroke-width="1.6"/><path d="M{xx+32} {220+26*u:.2f}h28" stroke="#d6efff" stroke-width="2"/>'
  if stage<2:overlay+=dot(xx+98+12*u,240,'#b1e2ff',2.5)
  # Parallel query inputs converge, fan out into retrieval, and return an answer.
  for k,yy in enumerate([219,241,263]):
   q=(t*2+k/3)%1
   overlay+=dot(*along([(873,yy),(955,241),(1035,yy),(1121,241)],q),'#9ee9eb' if k%2==0 else '#c9b5ff',2.7)
  overlay+=f'<circle cx="955" cy="241" r="{20+3*math.sin(t*math.tau)**2}" fill="none" stroke="#9ce9ec" opacity=".28"/>'
  overlay+='</g>';svgs.append(base.replace('</svg>',overlay+'</svg>'))
 with tempfile.TemporaryDirectory(prefix='impact-animation-') as tmp:
  js="""const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let input=JSON.parse(fs.readFileSync(0,'utf8'));input.svgs.forEach((svg,i)=>fs.writeFileSync(input.dir+'/'+i+'.png',new Resvg(svg).render().asPng()));"""
  subprocess.run(['node','-e',js],input=json.dumps({'svgs':svgs,'dir':tmp}),text=True,cwd=ROOT,check=True)
  frames=[Image.open(Path(tmp)/f'{i}.png').convert('RGB') for i in range(72)]
  sheet=Image.new('RGB',(1200,314*6))
  for k,index in enumerate([0,12,24,36,48,60]):sheet.paste(frames[index],(0,314*k))
  palette=sheet.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
  frames=[im.quantize(palette=palette,dither=Image.Dither.NONE) for im in frames]
  target=ROOT/'assets/impact.gif';temporary=target.with_suffix('.tmp.gif')
  frames[0].save(temporary,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=True,disposal=1);temporary.replace(target)
 print('Generated 72-frame outcome animation.')
if __name__=='__main__':main()
