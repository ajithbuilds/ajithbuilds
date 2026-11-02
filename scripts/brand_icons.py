"""Shared original-colour product artwork for every portfolio renderer."""
from pathlib import Path
import base64
ROOT=Path(__file__).resolve().parent.parent
COLOUR=ROOT/'assets/stack-icons'
LIGHT_BACKING={'aws','helm','vault','langgraph','langchain','ansible','bash','fastify'}
def source(name):
 for p in [COLOUR/f'{name}.svg',ROOT/'assets/architecture-icons'/f'{name}.svg',ROOT/'assets/pipeline'/f'{name}.svg']:
  if p.exists():return p
 return None
def image(name,x,y,size=30):
 p=source(name)
 if p is None:raise ValueError(f'No product artwork: {name}')
 uri='data:image/svg+xml;base64,'+base64.b64encode(p.read_bytes()).decode()
 backing=f'<rect x="{x-3}" y="{y-3}" width="{size+6}" height="{size+6}" rx="6" fill="#e8eef1"/>' if name in LIGHT_BACKING else ''
 return backing+f'<image x="{x}" y="{y}" width="{size}" height="{size}" preserveAspectRatio="xMidYMid meet" href="{uri}"/>'
