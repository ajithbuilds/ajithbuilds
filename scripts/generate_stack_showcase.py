"""Seven vector-animated technology exhibits using all 30 local product marks."""
from pathlib import Path
import base64,json,math,subprocess,tempfile,xml.etree.ElementTree as ET
from html import escape
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
GROUPS=[('Cloud & Infrastructure','Provision repeatable foundations.',['aws','azure','gcp','terraform','ansible']),('Containers & Orchestration','Package workloads. Orchestrate at scale.',['kubernetes','docker','openshift','helm','istio']),('CI/CD & GitOps','Verify changes. Reconcile desired state.',['argocd','github-actions','gitlab','jenkins','azure-devops']),('Observability & SRE','Connect telemetry to service health.',['prometheus','grafana','datadog','loki','opentelemetry']),('Security & Identity','Protect secrets and workload identity.',['vault','cert-manager']),('AI & MLOps','Orchestrate agents. Track model lineage.',['langgraph','langchain','mlflow']),('Languages & Scripting','Turn operational patterns into automation.',['python','go','bash','powershell','ruby'])]
COLORS=['#8edff1','#9cbfff','#b9a9ed','#91e0c4','#e5cb97','#c7b0f3','#9dc9ee']
NAMES={'aws':'AWS','azure':'Microsoft Azure','gcp':'Google Cloud','terraform':'Terraform','ansible':'Ansible','kubernetes':'Kubernetes','docker':'Docker','openshift':'Red Hat OpenShift','helm':'Helm','istio':'Istio','argocd':'Argo CD','github-actions':'GitHub Actions','gitlab':'GitLab CI/CD','jenkins':'Jenkins','azure-devops':'Azure DevOps','prometheus':'Prometheus','grafana':'Grafana','datadog':'Datadog','loki':'Grafana Loki','opentelemetry':'OpenTelemetry','vault':'HashiCorp Vault','cert-manager':'cert-manager','langgraph':'LangGraph','langchain':'LangChain','mlflow':'MLflow','python':'Python','go':'Go','bash':'Bash','powershell':'PowerShell','ruby':'Ruby'}
def mark(slug):
 colour=ROOT/'assets/stack-icons'/f'{slug}.svg'
 if colour.exists():return 'data:image/svg+xml;base64,'+base64.b64encode(colour.read_bytes()).decode()
 svg=ET.parse(ROOT/'assets/tech'/f'{slug}.svg').getroot()
 image=next((n for n in svg.iter() if n.tag.endswith('image')),None)
 if image is not None:return image.get('{http://www.w3.org/1999/xlink}href') or image.get('href')
 nested=next(n for n in svg if n.tag.endswith('svg'));nested.set('x','0');nested.set('y','0');nested.set('width','40');nested.set('height','40')
 return 'data:image/svg+xml;base64,'+base64.b64encode(ET.tostring(nested)).decode()
ICONS={k:mark(k) for k in NAMES}
def text(x,y,label,size=14,color='#edf3fa',bold=False):return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{700 if bold else 400}">{escape(label)}</text>'
def scene(j,u):
 title,desc,tools=GROUPS[j];c=COLORS[j]
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="3840" height="1600" viewBox="0 0 960 400"><defs><radialGradient id="halo"><stop stop-color="{c}" stop-opacity=".14"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient><linearGradient id="glass" x2="1" y2="1"><stop stop-color="#a5bdd9" stop-opacity=".18"/><stop offset="1" stop-color="#314159" stop-opacity=".12"/></linearGradient></defs><rect width="960" height="400" rx="20" fill="#06090f"/><rect x=".5" y=".5" width="959" height="399" rx="20" fill="none" stroke="#324256"/><ellipse cx="720" cy="215" rx="280" ry="210" fill="url(#halo)"/><g font-family="Arial, Helvetica, sans-serif">'''
 s+=text(38,39,'TECH STACK / TOOLS IN MOTION',11,c,True)
 words=title.split();lines=['']
 for word in words:
  if len(lines[-1]+' '+word)>23:lines.append(word)
  else:lines[-1]=(lines[-1]+' '+word).strip()
 for k,line in enumerate(lines):s+=text(38,91+k*34,line,28,bold=True)
 s+=text(39,110+len(lines)*34,desc,13,'#a8bdd1')
 # A different operational visual anchors each category.
 s+=f'<g fill="none" stroke="{c}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">'
 if j in [0,1]:
  for k in range(3):
   x=62+k*88;y=220+8*math.sin(u*math.tau+k)
   s+=f'<path d="M{x} {y}l28-14 28 14v38l-28 14-28-14Z m0 0 28 14 28-14 m-28 14v38" fill="{c}" fill-opacity=".07"/>'
   if k<2:s+=f'<path d="M{x+58} {y+19}h25" stroke-opacity=".4"/>'
 elif j==2:
  s+='<path d="M62 246h254" stroke-opacity=".35"/>'
  for k,label in enumerate(['PLAN','CHECK','APPLY']):
   x=62+k*96;s+=f'<rect x="{x}" y="223" width="65" height="46" rx="10"/>'+text(x+11,250,label,10,c,True)
 elif j==3:
  pts=[(x,244+15*math.sin(x*.06-u*math.tau)*math.exp(-((x-190)/85)**2)) for x in range(48,335,2)]
  s+='<polyline points="'+' '.join(f'{x},{y}' for x,y in pts)+'"/>'
 elif j==4:
  s+='<path d="M190 202l48 17v28c0 32-48 54-48 54s-48-22-48-54v-28Z" fill="#e5cb97" fill-opacity=".06"/><rect x="174" y="237" width="32" height="28" rx="5"/><path d="M180 237v-9a10 10 0 0 1 20 0v9"/>'
 elif j==5:
  for k in range(3):
   for n in range(3):
    x=70+k*105;y=220+n*30
    if k<2:
     for z in range(3):s+=f'<path d="M{x} {y} {x+105} {220+z*30}" stroke-opacity=".25"/>'
    s+=f'<circle cx="{x}" cy="{y}" r="4"/>'
 else:
  s+='<path d="m110 220-25 25 25 25 m140-50 25 25-25 25 m-57-61-25 74"/>'
  for k in range(3):s+=f'<path d="M{300} {225+k*17}h{12+15*((u+k*.3)%1)}" stroke-opacity=".6"/>'
 s+='</g>'
 positions={5:[(528,130),(674,130),(820,130),(601,262),(747,262)],3:[(545,194),(695,194),(845,194)],2:[(617,194),(787,194)]}[len(tools)]
 # Soft signal links circulate between the official product marks.
 for k in range(len(positions)-1):
  a,b=positions[k],positions[k+1];s+=f'<path d="M{a[0]} {a[1]} {b[0]} {b[1]}" stroke="{c}" stroke-opacity=".16" fill="none"/>'
  q=(u+k*.19)%1;x=a[0]+(b[0]-a[0])*q;y=a[1]+(b[1]-a[1])*q;s+=f'<circle cx="{x}" cy="{y}" r="2.5" fill="{c}"/>'
 for k,(tool,(x,y)) in enumerate(zip(tools,positions)):
  y+=3*math.sin(u*math.tau+k)
  backing=f'<rect x="{x-26}" y="{y-27}" width="52" height="52" rx="10" fill="#e8eef1"/>' if tool in ['aws','helm','vault','langgraph','langchain','ansible','bash'] else ''
  s+=f'<rect x="{x-48}" y="{y-42}" width="96" height="84" rx="17" fill="url(#glass)" stroke="{c}" stroke-opacity=".4"/><path d="M{x-30} {y-41}h38" stroke="#e9f5ff" stroke-opacity=".4"/>{backing}<image x="{x-21}" y="{y-22}" width="42" height="42" href="{ICONS[tool]}"/>'
  label=NAMES[tool];s+=f'<text x="{x}" y="{y+65}" text-anchor="middle" fill="#d6e3f1" font-size="12" font-weight="600">{escape(label)}</text>'
 for k in range(7):s+=f'<rect x="{39+k*37}" y="351" width="27" height="3" rx="1" fill="{c if k==j else "#2c3a4b"}"/>'
 s+=text(39,378,f'0{j+1} / 07  ·  {len(tools)} TOOLS',10,'#91a8c1')
 return s+'</g></svg>'
def main():
 with tempfile.TemporaryDirectory(prefix='stack-showcase-') as tmp:
  sources=[scene(j,k/12) for j in range(7) for k in range(12)]
  (ROOT/'assets/stack-showcase.svg').write_text(scene(0,.4))
  js="""const fs=require('fs');const {Resvg}=require('./tools/node_modules/@resvg/resvg-js');let v=JSON.parse(fs.readFileSync(0,'utf8'));v.svgs.forEach((s,i)=>fs.writeFileSync(v.dir+'/'+i+'.png',new Resvg(s).render().asPng()));"""
  subprocess.run(['node','-e',js],input=json.dumps({'svgs':sources,'dir':tmp}),text=True,cwd=ROOT,check=True)
  sheet=Image.new('RGB',(960,400*7))
  for j in range(7):
   with Image.open(Path(tmp)/f'{j*12}.png') as im:sheet.paste(im.convert('RGB').resize((960,400)),(0,j*400))
  palette=sheet.quantize(colors=256);frames=[]
  for i in range(84):
   with Image.open(Path(tmp)/f'{i}.png') as im:frames.append(im.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE))
  target=ROOT/'assets/stack-showcase-colour-4k.gif';tmpout=target.with_suffix('.tmp.gif');frames[0].save(tmpout,save_all=True,append_images=frames[1:],duration=200,loop=0,optimize=False,disposal=1);tmpout.replace(target)
 print('Rendered all 30 tools across seven animated 4K stack exhibits.')
if __name__=='__main__':main()
