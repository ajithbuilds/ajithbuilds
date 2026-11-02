"""Split the shared animation at the workflow boundary for clickable social links."""
from pathlib import Path
from PIL import Image
import base64,json,subprocess
ROOT=Path(__file__).resolve().parent.parent

def render_identity():
 photo=base64.b64encode((ROOT/'assets/profile/ajith-kumar.png').read_bytes()).decode()
 source=f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="1128" viewBox="0 0 960 282" role="img" aria-labelledby="title desc"><title id="title">AJITH KUMAR BALASUBRAMANIAN</title><desc id="desc">Professional portrait with the role Senior DevOps / Platform Engineer, SRE and AIOps. Reliable by design.</desc><defs><linearGradient id="portraitRim" x2="1" y2="1"><stop stop-color="#c6d8e7" stop-opacity=".6"/><stop offset=".5" stop-color="#60758b" stop-opacity=".3"/><stop offset="1" stop-color="#b7abc9" stop-opacity=".55"/></linearGradient><linearGradient id="frame" x2="1" y2="1"><stop stop-color="#b7c7df" stop-opacity=".13"/><stop offset="1" stop-color="#536a8a" stop-opacity=".07"/></linearGradient><clipPath id="portraitClip"><rect x="53" y="38" width="164" height="200" rx="19"/></clipPath></defs><rect width="960" height="282" fill="#000"/><rect x="47" y="32" width="176" height="212" rx="25" fill="url(#frame)" stroke="url(#portraitRim)" stroke-width="1.2"/><image x="53" y="38" width="164" height="200" preserveAspectRatio="xMidYMid slice" clip-path="url(#portraitClip)" href="data:image/png;base64,{photo}"/><rect x="53" y="38" width="164" height="200" rx="19" fill="none" stroke="#e0e9f1" stroke-opacity=".18"/><path d="M73 33h67" stroke="#e4f2ff" stroke-opacity=".35" stroke-linecap="round"/><g font-family="Arial, Helvetica, sans-serif"><text x="264" y="92" font-size="44" font-weight="700" fill="#eff4ff">AJITH KUMAR</text><text x="264" y="146" font-size="44" font-weight="700" fill="#eff4ff">BALASUBRAMANIAN</text><text x="265" y="193" font-size="26" font-weight="700" fill="#d8d8dd">Reliable by design.</text><text x="266" y="227" font-size="16" fill="#a8adb8">Senior DevOps / Platform Engineer · SRE · AIOps</text></g></svg>'''
 (ROOT/'assets/hero-identity-4k.svg').write_text(source)
 js="const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let v=JSON.parse(fs.readFileSync(0,'utf8'));fs.writeFileSync(v.path,new Resvg(v.svg).render().asPng());"
 subprocess.run(['node','-e',js],input=json.dumps({'svg':source,'path':str(ROOT/'assets/hero-identity-4k.png')}),text=True,cwd=ROOT,check=True)
 # A stacked portrait composition keeps the name and role legible on phones.
 defs=source[source.index('<defs>'):source.index('</defs>')+7]
 defs=defs.replace('<rect x="53" y="38" width="164" height="200" rx="19"/>','<rect x="184" y="24" width="112" height="136" rx="17"/>')
 mobile=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1560" viewBox="0 0 480 390">{defs}<rect width="480" height="390" fill="#000"/><rect x="178" y="18" width="124" height="148" rx="23" fill="url(#frame)" stroke="url(#portraitRim)"/><image x="184" y="24" width="112" height="136" preserveAspectRatio="xMidYMid slice" clip-path="url(#portraitClip)" href="data:image/png;base64,{photo}"/><g font-family="Arial, Helvetica, sans-serif" text-anchor="middle"><text x="240" y="215" font-size="31" font-weight="700" fill="#eff4ff">AJITH KUMAR</text><text x="240" y="253" font-size="31" font-weight="700" fill="#eff4ff">BALASUBRAMANIAN</text><text x="240" y="302" font-size="24" font-weight="700" fill="#d8d8dd">Reliable by design.</text><text x="240" y="339" font-size="16" fill="#a8adb8">Senior DevOps / Platform Engineer</text><text x="240" y="365" font-size="15" fill="#a8adb8">SRE · AIOps</text></g></svg>'''
 (ROOT/'assets/hero-identity-mobile.svg').write_text(mobile)
 subprocess.run(['node','-e',js],input=json.dumps({'svg':mobile,'path':str(ROOT/'assets/hero-identity-mobile.png')}),text=True,cwd=ROOT,check=True)


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
