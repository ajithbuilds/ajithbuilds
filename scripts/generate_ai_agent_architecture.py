"""Public-facing architecture based on the user's SCP Option A/B reference."""
from pathlib import Path
from architecture_symbols import title_with_icon,symbol
import json,xml.etree.ElementTree as ET
from generate_reliability_architecture import box,txt,arrow,icon
A=Path(__file__).resolve().parent.parent/'assets'
OUT=A/'work';TMP=Path('/tmp/profile-ai-agent-architecture');TMP.mkdir(exist_ok=True)
ns='http://www.w3.org/2000/svg';ET.register_namespace('',ns)
root=ET.parse(OUT/'reliability-glass-architecture.svg').getroot()
DEFS=ET.tostring(root.find(f'{{{ns}}}defs'),encoding='unicode')
FLOWS=[[(260,219),(311,219),(577,219),(865,219),(1090,219)],[(235,450),(274,450)],[(1240,271),(1240,296),(663,296),(663,383)],[(778,478),(810,478)],[(1240,640),(1240,710),(935,710),(935,613)],[(1060,425),(1090,425),(1265,425)]]
LABELS=['Index documentation when it changes','Authenticate the request','Retrieve grounded context','Evaluate with the language model','Call tools and return results','Respond and store conversation history']
def panel(x,y,w,h,title,lines,active=False,accent='#b3c8e6',title_size=19):
 s=box(x,y,w,h,'#16233b' if active else '#101f34',accent if active else '#38536e')+title_with_icon(x,y,w,title,title_size,accent)
 for j,line in enumerate(lines):s+=txt(x+15,y+61+j*27,line,17,'#b7cbe1')
 return s

def diagram(active=-1):
 s=f'''<svg xmlns="http://www.w3.org/2000/svg" width="1440" height="1050" viewBox="0 0 1440 1050" role="img" aria-labelledby="title desc"><title id="title">SCP AI Agent — persistent RAG and tool orchestration</title><desc id="desc">Option B indexes documentation into Azure AI Search and stores conversation history in Cosmos DB. An authenticated Fastify request enters LangGraph, retrieves hybrid search context, evaluates the question through a model proxy, and either responds or calls AWS, Azure and ServiceNow tools before evaluating again. The document compares Option A in-memory storage with Option B persistent storage. Graph checkpoint state remains in RAM in both designs.</desc>{DEFS}<rect width="1440" height="1050" rx="24" fill="url(#bg)"/><ellipse cx="400" cy="400" rx="650" ry="600" fill="url(#cyan)"/><ellipse cx="1160" cy="530" rx="650" ry="590" fill="url(#violet)"/><g font-family="Helvetica, Arial, sans-serif">'''
 s+=txt(30,48,'SCP AI Agent. Context into action.',34,'#f1f6ff',True)
 s+=txt(31,83,'Option B  /  Persistent retrieval + conversation history  /  LangGraph orchestration',19,'#96b3d1')
 s+=txt(30,126,'01  INDEX WHEN DOCUMENTATION CHANGES',16,'#bfa4ee',True)
 s+=panel(30,158,230,113,'Documentation',['Git repository','Markdown source'],active==0)
 s+=panel(311,158,230,113,'Python indexer',['Chunk Markdown source','Preserve source context'],active==0,title_size=19)
 s+=panel(592,158,273,113,'Embedding service',['Model proxy','Generate document vectors'],active==0)
 s+=panel(1090,158,320,113,'Azure AI Search',['Persistent document index','Vector + keyword retrieval'],active==0,'#9bcbea')
 for pts in ['260,219 311,219','541,219 592,219','865,219 1090,219']:s+=arrow(pts,'#bd9fef')
 s+=txt(905,204,'UPLOAD INDEX',14,'#a0bad5')
 s+=txt(30,330,'02  AUTHENTICATED REQUEST',16,'#9ed1eb',True)
 s+=panel(30,383,205,180,'Browser',['POST /chat','message + session_id','User bearer token'],active==1)
 s+=panel(274,383,236,180,'Fastify gateway',['Validate user identity','Request-scoped auth','Route to agent graph'],active==1)
 s+=arrow('235,450 274,450')+arrow('510,450 548,450')
 s+=box(530,318,880,370,'#091422','#38536e',18)+symbol('langgraph',550,331,26)+txt(587,351,'LANGGRAPH  /  RETRIEVE → EVALUATE → TOOLS OR RESPONSE',17,'#cfb6fa',True)
 s+=panel(548,383,230,230,'Retrieve',['Embed the query','Azure AI Search','Vector + BM25','RRF combines results','Semantic reranking','Top context results'],active==2,'#a6cff1')
 s+=panel(810,383,250,230,'Evaluate question',['Language-model call','Through model proxy','Ground answer in context','Tool call requested?','Yes → tools  /  No → reply'],active==3,'#d2b8f6')
 s+=panel(1090,383,300,88,'Respond',['Answer + session identifiers'],active==5,'#a3e2c4')
 s+=panel(1090,515,300,125,'Tool execution',['9 CRUD tools','AWS · Azure · ServiceNow','Return results to evaluator'],active==4,'#a3e2c4')
 s+=arrow('1240,271 1240,296 663,296 663,383','#9fcae4',True)
 s+=arrow('778,478 810,478','#c7b2f2')+arrow('1060,425 1090,425','#b0e4cf')+arrow('1060,559 1090,559','#b0e4cf')
 s+=arrow('1240,640 1240,710 935,710 935,613','#9ce0c7',True)+txt(981,700,'TOOL RESULT → RE-EVALUATE',14,'#a1d7c3')
 s+=panel(30,599,480,88,'Identity service',['User validation + cached machine-to-machine token'],active==1,title_size=18)
 s+=arrow('392,563 392,599','#9ec7df',True)
 s+=panel(30,754,235,117,'Model proxy',['Language-model calls','Document/query vectors'],active==0 or active==3,title_size=18)
 s+=panel(299,754,391,117,'Cosmos DB',['Sessions · messages · feedback','Analytics / unanswered-question gaps'],active==5,'#9bcbea')
 s+=panel(730,754,310,117,'Graph checkpoint state',['MemorySaver stays in RAM','Stored history ≠ graph recovery'],False,title_size=18)
 s+=panel(1080,754,330,117,'Feedback & analytics',['POST /feedback','GET /analytics/gaps'],active==5,title_size=18)
 s+=arrow('510,535 520,535 520,735 495,735 495,754','#8eaccd',True)
 s+=txt(35,727,'03  MODEL SERVICES & PERSISTENCE',15,'#a8c1e0',True)
 s+=txt(30,913,'TWO DESIGNS  /  DIFFERENT PERSISTENCE TRADE-OFFS',16,'#b9d0e9',True)
 s+=panel(30,931,660,99,'OPTION A  /  IN-MEMORY RAG',['Cosine search in Node.js RAM; rebuild index after restart.','Chunks and chat sessions do not survive process restart.'],False,'#bfa4ee',18)
 s+=panel(720,931,690,99,'OPTION B  /  AZURE AI SEARCH + COSMOS DB',['Document index and stored conversation history persist.','Graph checkpoint state still lives in RAM.'],False,'#9fdfc6',18)
 return s+'</g></svg>'
for i in range(6):(TMP/f'stage-{i}.svg').write_text(diagram(i))
(OUT/'ai-agent-glass-architecture.svg').write_text(diagram())
(TMP/'flows.json').write_text(json.dumps(FLOWS))
print('Authored SCP AI Agent glass architecture and six animation stages.')
