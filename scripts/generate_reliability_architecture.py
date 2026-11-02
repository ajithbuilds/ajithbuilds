"""Author a faithful token-refresh architecture from the user-supplied diagram."""
from pathlib import Path
from architecture_symbols import title_with_icon,symbol
import base64,html,json
A=Path(__file__).resolve().parent.parent/'assets'
OUT=A/'work';TMP=Path('/tmp/profile-token-architecture');TMP.mkdir(exist_ok=True)
def esc(t):return html.escape(t)
def txt(x,y,t,size=19,fill='#c5d6eb',bold=False):return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{600 if bold else 400}">{esc(t)}</text>'
def box(x,y,w,h,fill='#101f34',stroke='#38536e',r=14):
 kind='frameGlass' if fill=='#091422' else ('activeGlass' if fill in ['#16233b','#192a40'] else 'glass')
 rim=stroke if stroke not in ['#38536e','#2f435c','#39516b','#293e55'] else 'url(#glassRim)'
 return (f'<rect x="{x}" y="{y+6}" width="{w}" height="{h}" rx="{r}" fill="#000" fill-opacity=".20"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{kind})" stroke="{rim}" stroke-width="1.4"/>'
         f'<path d="M{x+r} {y+1}H{x+w-r}" stroke="#d8ecff" stroke-opacity=".33" stroke-width="1"/>')
def icon(name,x,y,w=44):
 return symbol(name,x,y,w)

def arrow(points,color='#7fd9ec',dash=False):return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2" {"stroke-dasharray=\"6 6\"" if dash else ""} marker-end="url(#arrow)"/>'
# Explicit directed flows, reused by the animated packet renderer.
FLOWS=[[(258,277),(287,277),(287,245),(324,245)],[(258,467),(288,467),(288,430),(324,430)],[(446,542),(446,579)],[(570,607),(708,607),(708,542)],[(978,542),(978,579)],[(850,438),(830,438)]]
STEPS=['Authenticate & get token','Discover databases','Write provisioning YAML','Grafana provisions sources','Refresh token / update secret','Update Grafana via REST API']
def diagram(active=-1):
 s='''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="850" viewBox="0 0 1440 850" role="img" aria-labelledby="title desc"><title id="title">Automated Azure AD token refresh for Grafana PostgreSQL data sources</title><desc id="desc">Azure service principal authenticates with Entra ID. A Kubernetes pod has an init container, Grafana main container, and token-refresher sidecar. Init discovers databases and writes data source YAML to shared EmptyDir. The sidecar refreshes tokens every 45 minutes, updates a Kubernetes secret and updates Grafana data source passwords through its REST API. External Secrets, service-principal credentials, RBAC and a service account support the workflow.</desc><defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#030508"/><stop offset="1" stop-color="#080e18"/></linearGradient>
<radialGradient id="cyan"><stop stop-color="#23627f" stop-opacity=".47"/><stop offset="1" stop-color="#23627f" stop-opacity="0"/></radialGradient>
<radialGradient id="violet"><stop stop-color="#67408b" stop-opacity=".38"/><stop offset="1" stop-color="#67408b" stop-opacity="0"/></radialGradient>
<linearGradient id="glass" x1="0" y1="0" x2=".7" y2="1"><stop stop-color="#b5d8f4" stop-opacity=".23"/><stop offset=".44" stop-color="#89abd7" stop-opacity=".08"/><stop offset="1" stop-color="#c0c4f2" stop-opacity=".15"/></linearGradient>
<linearGradient id="activeGlass" x2=".8" y2="1"><stop stop-color="#c8e5ff" stop-opacity=".33"/><stop offset=".5" stop-color="#a2b9ed" stop-opacity=".15"/><stop offset="1" stop-color="#b0c5ff" stop-opacity=".24"/></linearGradient>
<linearGradient id="frameGlass" x2=".6" y2="1"><stop stop-color="#a9c8ec" stop-opacity=".08"/><stop offset="1" stop-color="#9da9d1" stop-opacity=".035"/></linearGradient>
<linearGradient id="glassRim" x2="1" y2="1"><stop stop-color="#d1e7fb" stop-opacity=".7"/><stop offset=".5" stop-color="#8faccd" stop-opacity=".25"/><stop offset="1" stop-color="#bad5ee" stop-opacity=".5"/></linearGradient><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#8ccddd"/></marker></defs><rect width="1440" height="850" rx="24" fill="url(#bg)"/><ellipse cx="410" cy="375" rx="650" ry="450" fill="url(#cyan)"/><ellipse cx="1150" cy="470" rx="670" ry="460" fill="url(#violet)"/><g font-family="Helvetica, Arial, sans-serif">'''
 s+=txt(30,48,'Tokens renewed. Connections stay healthy.',34,'#f1f6ff',True)
 s+=txt(31,83,'Azure AD / Entra ID  ·  Dynamic PostgreSQL discovery  ·  Kubernetes init + main + sidecar',19,'#96b3d1')
 for x,w,title in [(24,252,'AZURE'),(304,820,'GRAFANA POD  /  3 CONTAINERS'),(1152,264,'KUBERNETES SUPPORT')]:
  s+=box(x,118,w,540,'#091422','#2f435c',18)+txt(x+17,151,title,17,'#a5c9ed',True)
 s+=box(42,179,216,167)+icon('azure',221,130,20)+title_with_icon(42,189,216,'Microsoft Entra ID',17,'#e4eefb')
 s+=txt(59,262,'Service principal',19,'#cbdff3',True)+txt(59,294,'Authenticate → token',17)+txt(59,324,'Resource: oss-rdbms',16,'#8ca8c8')
 s+=box(42,389,216,172)+title_with_icon(42,392,216,'Azure PostgreSQL',19,'#dbeaff')+txt(60,451,'Flexible Server',18)+txt(60,495,'Multiple databases',17)
 for j,c in enumerate(['#77bce6','#a48be0','#75d0b4']):s+=f'<ellipse cx="{89+j*45}" cy="530" rx="13" ry="6" fill="{c}"/><path d="M{76+j*45} 530v13c0 8 26 8 26 0v-13" fill="{c}" stroke="#bad2eb"/>'
 titles=['01  INIT CONTAINER','02  GRAFANA','03  TOKEN REFRESHER'];colors=['#bc9aff','#edb176','#79d9ba']
 for j,x in enumerate([324,586,850]):
  on=(j==0 and active in [0,1,2]) or (j==1 and active==3) or (j==2 and active in [4,5])
  s+=box(x,179,244,363,'#16233b' if on else '#101b2d',colors[j] if on else '#39516b')
  s+=title_with_icon(x,180,244,titles[j],17,colors[j])+txt(x+14,238,['Runs once at startup','Main container','Sidecar · every 45 minutes'][j],16,'#95aecb')
  s+=f'<path d="M{x} 253h244" stroke="#34485f"/>'
 init=['Azure login (SP)','Get access token','Discover databases','Generate data source YAML','Update Kubernetes secret','Write YAML to EmptyDir']
 for j,t in enumerate(init):s+=txt(339,291+j*39,t,17)
 s+=icon('grafana',664,277,87)+txt(607,402,'Reads provisioned sources',17)+txt(607,432,'from shared EmptyDir.',17)+box(607,462,201,46,'#2d2330','#84653f',8)+txt(622,491,'datasources.yaml',17,'#efc28c')
 for j,t in enumerate(['Get a fresh access token','Update Kubernetes secret','Get all Grafana sources','Update source passwords','through Grafana REST API']):s+=txt(864,291+j*39,t,16)
 s+=box(324,579,246,56,'#15253a','#6983aa',10)+title_with_icon(324,582,246,'Shared EmptyDir volume',17,'#bdd7f3')
 s+=box(728,579,378,56,'#102c2b','#4c9f8a',10)+title_with_icon(728,582,378,'K8s Secret: postgres-token-secret',17,'#a5e6cf')
 for y,h,title,lines in [(179,80,'External Secrets',['From external secret store']),(292,100,'SP credentials secret',['client-id · secret · tenant-id']),(422,70,'RBAC',['Allows secret updates']),(520,69,'ServiceAccount',['grafana'])]:
  s+=box(1170,y,228,h)+title_with_icon(1170,y-3,228,title,18,'#dfeafb')
  for k,t in enumerate(lines):s+=txt(1184,y+55+k*22,t,15,'#93aecb')
 s+=arrow('1284,259 1284,291')+arrow('1170,342 1107,342','#80dab9',True)+txt(1119,330,'SP',14,'#80dab9')
 # The mint return route represents token renewal using the same SP identity.
 s+=arrow('978,179 978,99 150,99 150,179','#70baac',True)
 s+=arrow('446,579 446,561 708,561 708,542','#94b6ed',True)
 s+=arrow('850,438 830,438','#7ce4bb')
 for i,flow in enumerate(FLOWS):s+=arrow(' '.join(f'{x},{y}' for x,y in flow), '#d4b2ff' if i<3 else '#7ddabd',True)
 s+=txt(30,696,'BOOTSTRAP ONCE',15,'#c4a2f5',True)
 startup=['Authenticate / token','Discover databases','Write provisioning YAML','Provision Grafana sources']
 for i,label in enumerate(startup):
  x=30+i*351;c='#bfa1ef'
  s+=box(x,711,335,38,'#192a40' if active==i else '#0d1929',c if active==i else '#293e55',9)+txt(x+12,736,f'{i+1:02d}  {label}',16,c if active==i else '#9cb4ce')
 s+=txt(30,779,'EVERY 45 MINUTES  /  NO MANUAL RESTART',15,'#92dfc3',True)
 for i,label in enumerate(['Fresh token → update Kubernetes secret','Grafana REST API → update data source passwords']):
  x=30+i*702;step=i+4;c='#8bddbf'
  s+=box(x,793,686,38,'#192a40' if active==step else '#0d1929',c if active==step else '#293e55',9)+txt(x+12,818,f'{step+1:02d}  {label}',17,c if active==step else '#9cb4ce')
 return s+'</g></svg>'
def main():
    for i in range(6):(TMP/f'stage-{i}.svg').write_text(diagram(i))
    (OUT/'reliability-glass-architecture.svg').write_text(diagram())
    (TMP/'flows.json').write_text(json.dumps(FLOWS))
    print('Authored six stages and a full-resolution vector diagram.')

if __name__ == "__main__":
    main()
