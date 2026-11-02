"""Bake the credential glass frames into self-contained SVG for GitHub READMEs."""
from pathlib import Path
import base64
from html import escape
ROOT=Path(__file__).resolve().parent.parent
CARDS=[('redhat','redhat-openshift.png','Red Hat','#ec8f8f'),('kubernetes','cka.svg','Kubernetes','#8bbaff'),('aws','aws-solutions-architect-associate.png','AWS','#e5c28c'),('azure','azure-administrator.svg','Azure','#9ecbe8')]
def main():
 out=ROOT/'assets/certifications/cards';out.mkdir(exist_ok=True)
 for slug,filename,label,colour in CARDS:
  src=out.parent/filename;mime='image/png' if src.suffix=='.png' else 'image/svg+xml';uri='data:'+mime+';base64,'+base64.b64encode(src.read_bytes()).decode()
  svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="104" height="116" viewBox="0 0 104 116" role="img" aria-labelledby="title"><title id="title">{escape(label)} certification</title><defs><linearGradient id="glass" x2=".7" y2="1"><stop stop-color="#1b2029"/><stop offset="1" stop-color="#0d1016"/></linearGradient></defs><rect x=".7" y=".7" width="102.6" height="114.6" rx="16" fill="url(#glass)" stroke="#728ba3" stroke-opacity=".38"/><path d="M17 1.3h69" stroke="#e3efff" stroke-opacity=".3"/><path d="M11 109q4 6 12 6h58q9 0 12-6" fill="none" stroke="{colour}" stroke-opacity=".48"/><image x="16" y="11" width="72" height="72" preserveAspectRatio="xMidYMid meet" href="{uri}"/><text x="52" y="103" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="10" fill="#c5d5e7">{escape(label)}</text></svg>'''
  (out/f'{slug}.svg').write_text(svg+'\n')
 print('Rendered four GitHub-compatible glass certification cards.')
if __name__=='__main__':main()
