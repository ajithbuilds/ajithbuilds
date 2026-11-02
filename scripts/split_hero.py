"""Split the shared animation at the workflow boundary for clickable social links."""
from pathlib import Path
from PIL import Image
import json,subprocess
ROOT=Path(__file__).resolve().parent.parent

RENDER_JS="const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let v=JSON.parse(fs.readFileSync(0,'utf8'));fs.writeFileSync(v.path,new Resvg(v.svg).render().asPng());"

def _render_png(svg:str,path:Path)->None:
 subprocess.run(['node','-e',RENDER_JS],input=json.dumps({'svg':svg,'path':str(path)}),text=True,cwd=ROOT,check=True)

def render_identity():
 # Optional banner artwork kept in sync with the HTML identity line in README.md.
 # The public profile uses the HTML title; these PNGs remain for local/offline reuse.
 source='''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="560" viewBox="0 0 960 140" role="img" aria-labelledby="title desc"><title id="title">AJITH KUMAR BALASUBRAMANIAN</title><desc id="desc">Platform Engineer, SRE, MLOps and AI.</desc><rect width="960" height="140" fill="#000"/><g font-family="Arial, Helvetica, sans-serif" text-anchor="middle"><text x="480" y="68" font-size="36" font-weight="700" fill="#eff4ff" letter-spacing="2">AJITH KUMAR BALASUBRAMANIAN</text><text x="480" y="108" font-size="16" font-weight="500" fill="#9eb0c4" letter-spacing="3.5">PLATFORM ENGINEER  ·  SRE  ·  MLOPS  ·  AI</text></g></svg>'''
 (ROOT/'assets/hero-identity-4k.svg').write_text(source)
 _render_png(source,ROOT/'assets/hero-identity-4k.png')
 mobile='''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="560" viewBox="0 0 480 140" role="img" aria-labelledby="title desc"><title id="title">AJITH KUMAR BALASUBRAMANIAN</title><desc id="desc">Platform Engineer, SRE, MLOps and AI.</desc><rect width="480" height="140" fill="#000"/><g font-family="Arial, Helvetica, sans-serif" text-anchor="middle"><text x="240" y="52" font-size="20" font-weight="700" fill="#eff4ff">AJITH KUMAR</text><text x="240" y="78" font-size="20" font-weight="700" fill="#eff4ff">BALASUBRAMANIAN</text><text x="240" y="112" font-size="11" font-weight="500" fill="#9eb0c4" letter-spacing="1.5">PLATFORM ENGINEER · SRE · MLOPS · AI</text></g></svg>'''
 (ROOT/'assets/hero-identity-mobile.svg').write_text(mobile)
 _render_png(mobile,ROOT/'assets/hero-identity-mobile.png')


def main():
 render_identity()
 source=ROOT/'assets/hero-devops-mlops-glass-4k.gif'
 with Image.open(source) as im:
  palette=im.copy();count=im.n_frames;duration=im.info.get('duration',180)
  for name,box in [('hero-devops-workflow-4k',(0,1128,3840,2888)),('hero-mlops-4k',(0,2936,3840,4800))]:
   frames=[]
   for k in range(count):
    im.seek(k);frame=im.convert('RGB').crop(box).quantize(palette=palette,dither=Image.Dither.NONE);frames.append(frame)
   target=ROOT/'assets'/f'{name}.gif';tmp=target.with_suffix('.tmp.gif')
   frames[0].save(tmp,save_all=True,append_images=frames[1:],duration=duration,loop=0,optimize=False,disposal=1);tmp.replace(target)
   del frames
 print('Exported both 4K workflow panels with matching timing.')
if __name__=='__main__':main()
