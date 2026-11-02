"""A compact, native-vector operations illustration matching the profile glass theme."""
from pathlib import Path
import json,math,subprocess,tempfile
from PIL import Image
from brand_icons import image as icon
ROOT=Path(__file__).resolve().parent.parent

def scene(t):
 s='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="960" viewBox="0 0 300 240" role="img" aria-labelledby="title"><title id="title">Cloud platform operations console</title><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#101b29"/><stop offset="1" stop-color="#090c14"/></linearGradient><linearGradient id="glass" x2=".7" y2="1"><stop stop-color="#a7cce4" stop-opacity=".14"/><stop offset="1" stop-color="#4b6185" stop-opacity=".07"/></linearGradient><radialGradient id="glow"><stop stop-color="#7b9fd2" stop-opacity=".17"/><stop offset="1" stop-color="#7b9fd2" stop-opacity="0"/></radialGradient></defs><rect width="300" height="240" rx="22" fill="url(#bg)"/><ellipse cx="175" cy="131" rx="138" ry="106" fill="url(#glow)"/><rect x=".5" y=".5" width="299" height="239" rx="22" fill="none" stroke="#7291ad" stroke-opacity=".4"/><g font-family="Arial, Helvetica, sans-serif"><text x="21" y="27" fill="#abc4d9" font-size="8" font-weight="700" letter-spacing="1">PLATFORM / OPERATIONS</text><circle cx="268" cy="23" r="3" fill="#8cdec0"/>
<rect x="20" y="43" width="160" height="105" rx="12" fill="url(#glass)" stroke="#7192af" stroke-opacity=".6"/><path d="M32 44h88" stroke="#d5efff" stroke-opacity=".3"/>
<rect x="118" y="114" width="162" height="95" rx="12" fill="#111c2a" stroke="#778bab" stroke-opacity=".6"/><path d="M130 115h77" stroke="#ddd7ff" stroke-opacity=".3"/>'''
 s+=icon('azure',33,55,20)+icon('kubernetes',145,55,20)
 s+='<text x="61" y="68" fill="#cfdfef" font-size="8" font-weight="700">CLOUD PLATFORM</text>'
 for k,(x,y) in enumerate([(49,97),(100,97),(149,97)]):
  s+=f'<rect x="{x-12}" y="{y-11}" width="24" height="24" rx="6" fill="#66a5d8" fill-opacity=".12" stroke="#83b8df" stroke-width=".7"/>'
  if k<2:
   q=(t+k*.3)%1;xx=x+13+q*25;s+=f'<path d="M{x+13} {y+1}h25" stroke="#8bb6cc" stroke-opacity=".4"/><circle cx="{xx}" cy="{y+1}" r="1.8" fill="#b3e5f6"/>'
 s+='<path d="M34 130h36 M34 135h64 M34 140h48" stroke="#8096b4" stroke-width="1" stroke-opacity=".45"/>'
 s+=icon('grafana',130,126,20)+'<text x="158" y="139" fill="#d6deec" font-size="8" font-weight="700">SERVICE HEALTH</text>'
 pts=[(x,169+9*math.sin(x*.10-t*math.tau)*math.exp(-((x-199)/60)**2)) for x in range(132,267,2)]
 s+='<path d="M131 185h136 M131 157h136" stroke="#8195b5" stroke-opacity=".15"/>'
 s+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'" fill="none" stroke="#98dfcd" stroke-width="1.6" stroke-linecap="round"/>'
 for k in range(3):
  x=132+k*37;s+=f'<rect x="{x}" y="194" width="26" height="3" rx="1" fill="#8eb6d7" fill-opacity="{.25+.45*math.sin((t+k/3)*math.tau)**2}"/>'
 s+='<path d="M74 151v23h40" stroke="#92a8d3" stroke-width="1" stroke-dasharray="3 4" fill="none"/>'
 s+='<text x="22" y="221" fill="#8fa9c3" font-size="7" letter-spacing=".8">BUILD · OBSERVE · IMPROVE</text></g></svg>'
 return s

def main():
 with tempfile.TemporaryDirectory(prefix='production-console-') as tmp:
  svgs=[scene(k/24) for k in range(24)];(ROOT/'assets/production-console.svg').write_text(scene(.4))
  js="""const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let v=JSON.parse(fs.readFileSync(0,'utf8'));v.svgs.forEach((s,i)=>fs.writeFileSync(v.dir+'/'+i+'.png',new Resvg(s).render().asPng()));"""
  subprocess.run(['node','-e',js],input=json.dumps({'svgs':svgs,'dir':tmp}),text=True,cwd=ROOT,check=True)
  frames=[Image.open(Path(tmp)/f'{k}.png').convert('RGB') for k in range(24)];sheet=Image.new('RGB',(1200,960*3))
  for j,k in enumerate([0,8,16]):sheet.paste(frames[k],(0,j*960))
  palette=sheet.quantize(colors=256);frames=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
  target=ROOT/'assets/production-console.gif';temp=target.with_suffix('.tmp.gif');frames[0].save(temp,save_all=True,append_images=frames[1:],duration=100,loop=0,optimize=False,disposal=1);temp.replace(target)
 print('Rendered glass operations console with coloured Azure, Kubernetes and Grafana marks.')
if __name__=='__main__':main()
