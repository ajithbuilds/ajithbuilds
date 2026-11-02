"""Consistent brand and semantic icons for the four architecture diagrams."""
from pathlib import Path
from html import escape
import base64
from PIL import ImageFont
from brand_icons import source as brand_source,image as brand_image
ASSETS=Path(__file__).resolve().parent.parent/'assets/architecture-icons'
FONT='/System/Library/Fonts/Supplemental/Arial Bold.ttf'
SHAPES={
 'document':'<path d="M8 3h11l6 6v20H8Z M19 3v7h6 M12 16h9 M12 21h9"/>',
 'server':'<rect x="4" y="5" width="24" height="9" rx="3"/><rect x="4" y="18" width="24" height="9" rx="3"/><path d="M9 9h1 M9 22h1 M16 9h7 M16 22h7"/>',
 'database':'<ellipse cx="16" cy="7" rx="11" ry="4"/><path d="M5 7v18c0 6 22 6 22 0V7 M5 16c0 6 22 6 22 0"/>',
 'search':'<circle cx="14" cy="13" r="9"/><path d="m21 20 8 8 M10 13h8 M14 9v8"/>',
 'model':'<path d="M7 7 25 7 16 25Z M7 7 7 23 25 23 25 7 M7 23 16 13 25 23"/><circle cx="7" cy="7" r="3"/><circle cx="25" cy="7" r="3"/><circle cx="16" cy="25" r="3"/>',
 'shield':'<path d="M16 3 27 7v9c0 7-11 13-11 13S5 23 5 16V7Z M10 15l4 4 8-9"/>',
 'key':'<circle cx="11" cy="11" r="7"/><path d="m16 16 13 13 M22 22l4-4 M25 25l4-4"/>',
 'identity':'<circle cx="16" cy="9" r="6"/><path d="M5 29v-5c0-10 22-10 22 0v5Z"/>',
 'refresh':'<path d="M27 12A12 12 0 0 0 6 7 M5 2v7h7 M5 20a12 12 0 0 0 21 5 M27 30v-7h-7"/>',
 'folder':'<path d="M3 9h10l3 4h13v15H3Z M3 9V5h10l3 4h13v4"/>',
 'function':'<path d="m19 2-13 17h9l-2 11 13-17h-9Z"/>',
 'graph':'<path d="M7 7h18 M7 7l9 18 9-18"/><circle cx="7" cy="7" r="4"/><circle cx="25" cy="7" r="4"/><circle cx="16" cy="25" r="4"/>',
 'chart':'<path d="M4 3v25h25 M8 22v-7h4v7 M16 22V9h4v13 M24 22V5h4v17"/>',
 'review':'<path d="M7 4h18v25H7Z M11 9h10 M11 14h10 M11 21l4 4 7-8"/>',
 'memory':'<rect x="7" y="7" width="18" height="18" rx="3"/><path d="M12 12h8v8h-8Z M2 10h5 M2 16h5 M2 22h5 M25 10h5 M25 16h5 M25 22h5 M10 2v5 M16 2v5 M22 2v5 M10 25v5 M16 25v5 M22 25v5"/>',
 'browser':'<rect x="3" y="4" width="26" height="24" rx="4"/><path d="M3 11h26 M8 7h1 M12 7h1 M10 18l-4 3 4 3 M22 18l4 3-4 3"/>',
 'tools':'<path d="m6 4 6 6-3 4-6-6v7l6 5 5-2 12 12 4-4-12-12 2-5-5-6h-7Z"/>',
}
def keys(title):
 t=title.lower()
 if 'secret' in t:return ['key']
 if t.strip() in ['dev','int','prod']:return ['kubernetes']
 if 'github actions + terraform' in t:return ['github-actions','terraform']
 if 'azure openai' in t:return ['azure','model']
 if 'azure ai search' in t:return ['azure','search']
 for term,key in [('github actions','github-actions'),('github','github'),('terraform','terraform'),('argo cd','argocd'),('prometheus','prometheus'),('grafana','grafana'),('python','python'),('fastify','fastify'),('cosmos','cosmosdb'),('postgres','postgresql'),('azure function','function'),('resource graph','graph'),('cost management','chart'),('azure openai','model'),('azure ai search','search'),('azure foundation','azure'),('workload configuration','helm'),('langgraph','langgraph'),('entra','identity'),('service principal','identity'),('external secrets','key'),('credentials secret','key'),('k8s secret','key'),('rbac','shield'),('serviceaccount','identity'),('init container','server'),('token refresher','refresh'),('emptydir','folder'),('evaluate','model'),('retrieve','search'),('embedding','model'),('model proxy','model'),('tool execution','tools'),('customer review','review'),('observe','grafana'),('verification','shield'),('controlled platform','shield'),('customer report','chart'),('feedback','chart'),('checkpoint','memory'),('identity','identity'),('browser','browser'),('documentation','document'),('in-memory','memory'),('option b','database')]:
  if term in t:return [key]
 return ['document']
def symbol(key,x,y,size=30):
 if brand_source(key):return brand_image(key,x,y,size)
 png=ASSETS/(key+'.png');svg=ASSETS/(key+'.svg')
 if png.exists() or svg.exists():
  src=png if png.exists() else svg;mime='image/png' if png.exists() else 'image/svg+xml'
  data=base64.b64encode(src.read_bytes()).decode()
  background=f'<rect x="{x-2}" y="{y-2}" width="{size+4}" height="{size+4}" rx="7" fill="#ecf3fa"/>' if key=='fastify' else ''
  return background+f'<image x="{x}" y="{y}" width="{size}" height="{size}" preserveAspectRatio="xMidYMid meet" href="data:{mime};base64,{data}"/>'
 return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 32 32"><g fill="none" stroke="#b6d8f0" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{SHAPES[key]}</g></svg>'
def title_with_icon(x,y,w,title,size=19,color='#b7cce6'):
 names=keys(title);count=len(names);icon_size=27
 start=x+15+count*35+4;available=x+w-12-start
 while ImageFont.truetype(FONT,size).getlength(title)>available and size>12:size-=1
 result=''.join(symbol(name,x+15+j*35,y+12,icon_size) for j,name in enumerate(names))
 return result+f'<text x="{start}" y="{y+31}" font-family="Helvetica, Arial, sans-serif" font-size="{size}" font-weight="600" fill="{color}">{escape(title)}</text>'
