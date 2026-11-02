"""Glass platform-engineering architecture from the user's profile narrative."""
from pathlib import Path
from architecture_symbols import title_with_icon
import json,xml.etree.ElementTree as ET
from generate_reliability_architecture import box,txt,arrow,icon
A=Path(__file__).resolve().parent.parent/'assets';OUT=A/'work'
TMP=Path('/tmp/profile-platform-architecture');TMP.mkdir(exist_ok=True)
ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
DEFS=ET.tostring(ET.parse(OUT/'reliability-glass-architecture.svg').getroot().find(f'{{{ns}}}defs'),encoding='unicode')
FLOWS=[[(290,240),(335,240)],[(665,240),(710,240),(1030,240),(1075,240)],[(390,489),(430,489)],[(430,749),(520,749),(920,749),(1010,749)],[(720,829),(720,850),(720,878),(280,878),(280,884)],[(1010,956),(1060,956),(1420,956),(1420,489),(1410,489)]]
BOXES=[(335,165,330,178),(710,165,320,178),(430,407,390,171),(520,662,400,167),(30,884,500,150),(860,407,550,171)]
def panel(x,y,w,h,title,lines,active=False,accent='#b7cce6',size=19):
 s=box(x,y,w,h,'#16233b' if active else '#101f34',accent if active else '#38536e')+title_with_icon(x,y,w,title,size,accent)
 for j,t in enumerate(lines):s+=txt(x+15,y+64+j*27,t,17,'#b8cce1')
 return s

def diagram(active=-1):
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1060" viewBox="0 0 1440 1060" role="img" aria-labelledby="title desc"><title id="title">Platform engineering — infrastructure delivery, GitOps and reliability</title><desc id="desc">GitHub Actions and Terraform golden paths provision shared Azure infrastructure using plan gates and just-in-time RBAC. Workload charts and environment configuration in Git are reconciled by Argo CD across DEV, INT and PROD AKS clusters. Controlled promotion and rolling updates are supported by verification gates and drift controls. Prometheus and Grafana provide SLI/SLO health signals. The profile reports three clusters, over 120 nodes collectively, over nine microservices, and 99.9 percent availability.</desc>{DEFS}<rect width="1440" height="1060" rx="24" fill="url(#bg)"/><ellipse cx="410" cy="450" rx="650" ry="620" fill="url(#cyan)"/><ellipse cx="1160" cy="560" rx="650" ry="620" fill="url(#violet)"/><g font-family="Helvetica, Arial, sans-serif">'''
 s+=txt(30,48,'Platforms that teams can build on.',34,'#f1f6ff',True)
 s+=txt(31,83,'3 AKS clusters  ·  120+ nodes across DEV / INT / PROD  ·  9+ microservices  ·  99.9% platform uptime',19,'#9fb9d6')
 s+=txt(30,132,'01  INFRASTRUCTURE DELIVERY  /  TERRAFORM GOLDEN PATHS',16,'#a8cce8',True)
 s+=panel(30,165,260,178,'GitHub source / PR',['Reusable Terraform modules','Environment configuration','Infrastructure changes'],active==0,size=18)
 s+=panel(335,165,330,178,'GitHub Actions',['Run infrastructure workflow','Validate the proposed change','Plan-before-apply gates','Just-in-time RBAC'],active==0,'#b6cdea')
 s+=panel(710,165,320,178,'Terraform',['Apply the planned change','Dependency-aware lifecycle','45+ Azure resource types','Provision in under 10 minutes'],active==1,'#c6b0ef')
 s+=panel(1075,165,335,178,'Azure foundation',['AKS · ACR · Key Vault','Networking · PostgreSQL','Shared platform resources','Infrastructure as code'],active==1,'#a5d3ea')
 for pts in ['290,240 335,240','665,240 710,240','1030,240 1075,240']:s+=arrow(pts,'#adcde7')
 s+=txt(30,380,'02  GITOPS DELIVERY  /  CHARTS + VALUES → DESIRED STATE',16,'#bda8ec',True)
 s+=panel(30,407,360,171,'Workload configuration in Git',['Helm charts and environment values','Versioned desired state','DEV → INT → PROD promotion'],active==2,'#b5cce7',18)
 s+=panel(430,407,390,171,'Argo CD',['App-of-apps pattern','Reconcile charts and environment values','Deploy the desired state to AKS','GitOps drift controls'],active==2,'#c6b0ef')
 s+=panel(860,407,550,171,'Controlled platform changes',['Rolling updates across 15+ platform components','Verification gates around upgrades and promotion','Health and drift signals inform operational decisions','Zero-downtime platform upgrades'],active==5,'#a9dfc8')
 s+=arrow('390,489 430,489','#b5c6e8')
 # Argo reconciles all environments; promotion is a separate gated path.
 for x in [230,720,1210]:s+=arrow(f'625,578 625,650 {x},650 {x},662','#9dbdda',True)
 s+=txt(30,643,'03  AKS ENVIRONMENTS  /  120+ NODES COLLECTIVELY',16,'#a0c9e6',True)
 for j,(x,name,role) in enumerate([(30,'DEV','Develop and validate'),(520,'INT','Integrate and verify'),(1010,'PROD','Operate production workloads')]):
  s+=panel(x,662,400,167,name,[role,'AKS workloads · Helm-managed configuration','Terraform-provisioned infrastructure'],active==3,'#a8d9ce')
 for pts in ['430,749 520,749','920,749 1010,749']:s+=arrow(pts,'#9cdbbc')
 s+=txt(439,728,'VERIFY',12,'#aedcc7')+txt(929,728,'VERIFY',12,'#aedcc7')
 s+=txt(30,867,'04  OBSERVABILITY + RELIABILITY FEEDBACK',16,'#a3dcc9',True)
 s+=panel(30,884,500,150,'Prometheus',['Collect workload and platform metrics','PromQL alerts · health signals · capacity analysis','Feed SLI/SLO dashboards'],active==4,'#b7d1e9')
 s+=panel(570,884,440,150,'Grafana',['SLI/SLO dashboards','Visualize reliability and service health','Support incident detection and response'],active==4,'#c9b4ed')
 s+=panel(1060,884,350,150,'Verification gates',['Review upgrade health and drift','Validate the next promotion','Feed improvements into delivery'],active==5,'#a6e1c7',18)
 for x in [230,720,1210]:s+=arrow(f'{x},829 {x},850','#8dc6b1',True)
 s+=f'<path d="M230 850H1210" fill="none" stroke="#8dc6b1" stroke-dasharray="6 6"/>'
 s+=arrow('720,850 720,878 280,878 280,884','#8dc6b1',True)
 s+=arrow('530,956 570,956','#a7cfe3')+arrow('1010,956 1060,956','#acd8c1')
 s+=arrow('1410,956 1420,956 1420,489 1410,489','#8ec8b3',True)
 return s+'</g></svg>'
for i in range(6):(TMP/f'stage-{i}.svg').write_text(diagram(i))
(OUT/'platform-glass-architecture.svg').write_text(diagram())
(TMP/'flows.json').write_text(json.dumps(FLOWS));(TMP/'boxes.json').write_text(json.dumps(BOXES))
print('Authored platform glass architecture and six animation stages.')
