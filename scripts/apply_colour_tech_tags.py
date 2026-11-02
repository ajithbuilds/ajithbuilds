"""Update detailed tool tags to share the full-colour product icon collection."""
from pathlib import Path
import base64,xml.etree.ElementTree as ET
from brand_icons import COLOUR,LIGHT_BACKING
ROOT=Path(__file__).resolve().parent.parent
SVG='{http://www.w3.org/2000/svg}'
def main():
 for icon in COLOUR.glob('*.svg'):
  path=ROOT/'assets/tech'/icon.name
  if not path.exists():continue
  root=ET.parse(path).getroot();parents={n:p for p in root.iter() for n in p}
  node=next((n for n in root.iter() if n.tag==SVG+'image'),None)
  if node is None:node=next(n for n in root if n.tag==SVG+'svg')
  parent=parents[node]
  for plate in list(parent):
   if plate.tag==SVG+'rect' and plate.get('rx')=='2' and float(plate.get('width','0'))==float(node.get('width','14'))+2:parent.remove(plate)
  index=list(parent).index(node);attrs={k:node.get(k,v) for k,v in [('x','5'),('y','3'),('width','14'),('height','14')]}
  parent.remove(node)
  data='data:image/svg+xml;base64,'+base64.b64encode(icon.read_bytes()).decode()
  new=ET.Element(SVG+'image',{**attrs,'href':data});parent.insert(index,new)
  if icon.stem in LIGHT_BACKING:
   x,y,w,h=[float(attrs[k]) for k in ['x','y','width','height']]
   plate=ET.Element(SVG+'rect',{'x':str(x-1),'y':str(y-1),'width':str(w+2),'height':str(h+2),'rx':'2','fill':'#e8eef1'})
   parent.insert(index,plate)
  # Change only the tag surface, never product geometry or label text.
  for child in root:
   if child.tag==SVG+'rect' and float(child.get('width','0'))>0 and child.get('fill')!='#e8eef1':child.set('fill','#172331')
   if child.tag==SVG+'g' and child.get('shape-rendering')=='crispEdges':
    for r in child:
     if r.tag==SVG+'rect':r.set('fill','#172331')
  ET.register_namespace('',SVG[1:-1]);path.write_text(ET.tostring(root,encoding='unicode'))
 print('Updated 30 detailed tags to full-colour icons on dark glass surfaces.')
if __name__=='__main__':main()
