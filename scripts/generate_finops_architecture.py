"""Glass FinOps architecture based on the user's allocated-vs-used reference."""
from pathlib import Path
from architecture_symbols import title_with_icon
import json,xml.etree.ElementTree as ET
from generate_reliability_architecture import box,txt,arrow
A=Path(__file__).resolve().parent.parent/'assets';OUT=A/'work'
TMP=Path('/tmp/profile-finops-architecture');TMP.mkdir(exist_ok=True)
ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
DEFS=ET.tostring(ET.parse(OUT/'reliability-glass-architecture.svg').getroot().find(f'{{{ns}}}defs'),encoding='unicode')
FLOWS=[[(740,280),(740,322),(210,322),(210,357)],[(395,442),(440,442)],[(790,442),(835,442),(1105,442),(1145,442)],[(1277,550),(1277,595),(155,595),(155,632)],[(280,704),(315,704),(565,704),(600,704),(920,704),(965,704)],[(1180,777),(1180,805),(1418,805),(1418,550),(1408,550)]]
BOXES=[(30,357,365,193),(440,357,350,193),(835,357,270,193),(30,632,250,145),(600,632,320,145),(965,632,445,145)]
def panel(x,y,w,h,title,lines,active=False,accent='#b7cce6',size=19):
 s=box(x,y,w,h,'#16233b' if active else '#101f34',accent if active else '#38536e')+title_with_icon(x,y,w,title,size,accent)
 for j,t in enumerate(lines):s+=txt(x+15,y+64+j*27,t,17,'#b8cce1')
 return s

def diagram(active=-1):
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="960" viewBox="0 0 1440 960" role="img" aria-labelledby="title desc"><title id="title">SCP FinOps — from allocation and usage to verified optimization</title><desc id="desc">Azure Cost Management, Prometheus and Resource Graph feed a weekly Azure Function. Azure OpenAI correlates allocation, usage and cost to recommend right-sizing, scheduling or SKU changes. Cosmos DB stores results for a report or portal. Applying a right-sizing recommendation creates a GitHub pull request, which the customer reviews and merges before GitHub Actions and Terraform update the workload. The system observes CPU limits, OOM events and latency for 48 hours before reporting the outcome.</desc>{DEFS}<rect width="1440" height="960" rx="24" fill="url(#bg)"/><ellipse cx="410" cy="430" rx="650" ry="550" fill="url(#cyan)"/><ellipse cx="1160" cy="510" rx="650" ry="560" fill="url(#violet)"/><g font-family="Helvetica, Arial, sans-serif">'''
 s+=txt(30,48,'Cloud spend. From signals to controlled change.',34,'#f1f6ff',True)
 s+=txt(31,83,'Allocated resources vs actual usage  /  Reviewable recommendations  /  Verified outcomes',19,'#9fb9d6')
 s+=txt(30,126,'01  COLLECT EXISTING SIGNALS FOR THE SAME PERIOD',16,'#9fc7e5',True)
 s+=panel(30,155,390,125,'Azure Cost Management API',['Cost by resource and time period','What are we paying for?'],active==0,'#a5cee9')
 s+=panel(470,155,500,125,'Prometheus / PromQL',['CPU · memory · database activity · storage','What are we actually using?'],active==0,'#c3aff3')
 s+=panel(1020,155,390,125,'Azure Resource Graph',['Resource metadata and inventory','Which resources and environments?'],active==0,'#a4d5cb',18)
 for pts in ['225,280 225,357','740,280 740,322 210,322 210,357','1215,280 1215,337 240,337 240,357']:s+=arrow(pts,'#9dc7df',True)
 s+=txt(30,320,'02  WEEKLY ANALYSIS',16,'#bba7ee',True)
 s+=panel(30,357,365,193,'Azure Function',['Query cost, usage and metadata','Align resource and time window','Combine into analysis payload','Send for AI recommendations','Store and publish results'],active==0,'#a7cce9')
 s+=panel(440,357,350,193,'Azure OpenAI / GPT-4o',['Correlate allocation vs usage','Assess peaks and headroom','Explain risk and reasoning','Estimate potential savings','Recommend controlled actions'],active==1,'#ceb8f4')
 s+=panel(835,357,270,193,'Cosmos DB',['Store recommendations','Resource + rationale','Status and outcome','Keep results available'],active==2,'#a6cbe9')
 s+=panel(1145,357,265,193,'Customer report',['Portal / dashboard','Email or notification','Savings + risk + details','Apply Now / Ignore'],active==2,'#a6ddc4')
 for pts in ['395,442 440,442','790,442 835,442','1105,442 1145,442']:s+=arrow(pts,'#b6c9ee')
 s+=arrow('1277,550 1277,595 155,595 155,632','#a2dfc6',True)
 s+=txt(30,589,'03  RIGHT-SIZING THROUGH GITOPS',16,'#a1dcc7',True)
 s+=txt(1013,578,'APPLY NOW → CREATE A PR',14,'#a2d9c2')
 s+=panel(30,632,250,145,'GitHub pull request',['Update appsconfig.json','CPU / memory proposal','Reviewable configuration'],active==3,'#b4cdeb',18)
 s+=panel(315,632,250,145,'Customer review',['Inspect proposed change','Review risk and savings','Approve and merge'],active==3,'#d4bef4',18)
 s+=panel(600,632,320,145,'GitHub Actions + Terraform',['Apply the reviewed change','Update the container workload','Keep delivery reproducible'],active==4,'#b0cfee',18)
 s+=panel(965,632,445,145,'Observe for 48 hours',['CPU within limits?  /  No OOM kills?','Latency unchanged?  /  SLIs healthy?','Validate outcome before reporting success'],active==5,'#a1e0c3',19)
 for pts in ['280,704 315,704','565,704 600,704','920,704 965,704']:s+=arrow(pts,'#9fdec7')
 s+=arrow('1180,777 1180,805 1418,805 1418,550 1408,550','#89c3b0',True)
 s+=txt(30,821,'OTHER RECOMMENDATIONS  /  SEPARATE EXECUTION PATHS',15,'#9fb9d4',True)
 s+=panel(30,839,660,95,'Development database schedules',['Scheduled Container Apps Jobs for approved operating windows.'],False,'#b7cce6',18)
 s+=panel(720,839,690,95,'PostgreSQL SKU changes',['Validate application performance before changing capacity.'],False,'#b7cce6',18)
 return s+'</g></svg>'
for i in range(6):(TMP/f'stage-{i}.svg').write_text(diagram(i))
(OUT/'finops-glass-architecture.svg').write_text(diagram())
(TMP/'flows.json').write_text(json.dumps(FLOWS));(TMP/'boxes.json').write_text(json.dumps(BOXES))
print('Authored FinOps glass architecture and six animation stages.')
