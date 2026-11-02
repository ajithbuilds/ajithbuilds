"""Offline acceptance checks for the real README, preview, links and image artifacts."""
from pathlib import Path
from urllib.parse import urlsplit,unquote
from html import unescape
import base64,hashlib,json,re,time,xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from PIL import Image,ImageChops
from build_preview import ROOT,COUNTER,render

def local_path(url):
    parsed=urlsplit(unescape(url))
    if parsed.scheme or not parsed.path:return None
    path=(ROOT/unquote(parsed.path)).resolve()
    if not path.is_relative_to(ROOT):raise AssertionError(f'Path escapes repository: {url}')
    return path

def main():
    start=time.monotonic();md=(ROOT/'README.md').read_text();static=(ROOT/'PROFILE-STATIC.md').read_text()
    assert md.count(COUNTER)==1 and static.count(COUNTER)==1,'Counter identifier changed or duplicated'
    assert 'Expedia' not in md and 'AWS Certified Developer' not in md,'A superseded career detail remains'
    assert 'Western Union' in md and 'AWS Certified Solutions Architect – Associate' in md
    assert 'AJITH KUMAR BALASUBRAMANIAN' in md
    assert not re.search(r'/(?:Users|private|tmp)/',md),'Local machine path leaked into public README'
    for h in ['## Built for Production','## Selected Work','## Professional Experience','## Tech Stack','## Certifications']:
        assert md.count(h)==1,f'Duplicate section: {h}'
    sources={};images=set();checked_links=0
    for name,html in [('README.md',render(md)),('PROFILE-STATIC.md',render(static)),('preview.html',(ROOT/'preview.html').read_text()),('preview-static.html',(ROOT/'preview-static.html').read_text())]:
        soup=BeautifulSoup(html,'html.parser')
        assert 'Static version' not in soup.get_text(), 'Removed static-version option returned'
        anchors={n.get('id') or n.get('name') for n in soup.find_all(attrs={'id':True})+soup.find_all('a',attrs={'name':True})}
        for image in soup.find_all('img'):
            assert image.get('alt','').strip(),f'Missing alt text in {name}'
            path=local_path(image.get('src',''))
            assert path and path.is_file(),f'Broken/nonlocal image: {name} {image.get("src")}'
            images.add(path)
        for source in soup.find_all('source',srcset=True):
            # Profile uses one source per element, not a comma-separated responsive list.
            path=local_path(source['srcset']);assert path and path.is_file();images.add(path)
        for a in soup.find_all('a',href=True):
            url=a['href'];parsed=urlsplit(url)
            if parsed.scheme:continue
            if url.startswith('#'):assert unquote(url[1:]) in anchors,f'Broken anchor {name}: {url}'
            else:
                path=local_path(url);assert path and path.is_file(),f'Broken local link {name}: {url}'
            checked_links+=1
        if name.startswith('preview'):
            headings=soup.find_all(re.compile(r'^h[1-6]$'))
            assert len(soup.find_all('h1'))==1, 'Preview must have one accessible page title'
            assert [h.get_text() for h in soup.find_all('h2')]==['Built for Production','Selected Work','Professional Experience','Tech Stack','Certifications']
            levels=[int(h.name[1]) for h in headings]
            assert all(b<=a+1 for a,b in zip(levels,levels[1:])), 'Heading level skipped'
            assert len({h.get('id') for h in headings if h.get('id')})==len([h for h in headings if h.get('id')]), 'Duplicate heading anchors'
            assert 'AJITHBUILDS' not in soup.title.get_text(), 'Old wordmark remains in page title'
            assert not soup.find(id='motion-toggle') and not soup.find('button'), 'Removed animation control returned'
            nav=soup.find('nav',attrs={'aria-label':'Profile navigation'})
            assert [a.get_text() for a in nav.find_all('a')]==['WORK','EXPERIENCE','STACK']
            badges=soup.select_one('.top-certifications')
            assert badges and len(badges.find_all('a',recursive=False))==4, 'Certification badges escaped their shared row'
            assert [a.get('aria-label') for a in badges.find_all('a',recursive=False)]==['Red Hat','Kubernetes','AWS','Azure']
            markup=str(soup)
            # Lean above-the-fold: identity → credentials → outcomes → one role strip.
            # Heavier workflow/stack animations live inside Selected Work / Tech Stack.
            assert markup.index('hero-identity') < markup.index('top-certifications') < markup.index('impact.') < markup.index('role-banner-4k')
            assert markup.index('role-banner-4k') < markup.index('stack-showcase-colour-4k') < markup.index('hero-devops-workflow-4k') < markup.index('hero-mlops-4k')
            identity=soup.select_one('.hero-identity')
            assert identity and identity.find('img',src=re.compile(r'hero-identity-4k\.png')), 'Missing desktop identity banner'
            assert identity.find('source',media='(max-width: 600px)'), 'Missing mobile identity composition'
            assert 'AJITH KUMAR BALASUBRAMANIAN' in (identity.find('img').get('alt') or '')
            assert not soup.find_all('img',src=re.compile(r'^https?://')),'Preview unexpectedly loads remote images'
        if name=='PROFILE-STATIC.md':assert not soup.find_all('img',src=re.compile(r'\.gif$')),'Static edition still animates'
    for architecture,slug in [('platform','terraform'),('platform','prometheus'),('ai-agent','langgraph'),('finops','github-actions')]:
        data=base64.b64encode((ROOT/f'assets/stack-icons/{slug}.svg').read_bytes()).decode()
        assert data in (ROOT/f'assets/work/{architecture}-glass-architecture.svg').read_text(), f'Stale product icon in {architecture}: {slug}'
    manifest=json.loads((ROOT/'assets/animation-manifest.json').read_text());assert len(manifest)==40
    assert 'assets/stack-showcase-colour-4k.gif' in manifest
    assert 'assets/impact.gif' in manifest
    assert len([x for x in manifest if '/tech/' in x])==30
    main_soup=BeautifulSoup(render(md),'html.parser')
    assert len([p for p in main_soup.find_all('picture') if p.find('img',src=re.compile(r'\.gif$'))])==len(manifest),'An animation has no reduced-motion poster'
    for picture in main_soup.find_all('picture'):
        if picture.find('img',src=re.compile(r'\.gif$')):
            assert picture.find('source',media='(prefers-reduced-motion: reduce)')
    identity=main_soup.select_one('.hero-identity')
    assert identity and identity.find('img',src=re.compile(r'hero-identity-4k\.png')), 'Missing centered identity banner'
    assert identity.find('source',media='(max-width: 600px)'), 'Missing mobile identity composition'
    assert 'portrait' not in (identity.find('img').get('alt') or '').lower(), 'Portrait should stay out of the identity header'
    assert 'portrait' not in (ROOT/'assets/hero-identity-4k.svg').read_text().lower(), 'Portrait artwork returned in identity SVG'
    gifs=[];frames_total=0;animated_bytes=0
    for path in sorted(images):
        if path.suffix=='.svg':
            root=ET.parse(path).getroot()
            assert not any(n.tag.endswith('script') for n in root.iter()),f'Script in SVG {path.name}'
        elif path.suffix=='.gif':
            with Image.open(path) as im:
                assert im.n_frames>1 and im.info.get('loop')==0,f'Invalid loop: {path}'
                total_ms=0;first=None;different=False
                for i in range(im.n_frames):
                    im.seek(i);im.load();total_ms+=im.info.get('duration',0)
                    if i==0:first=im.convert('RGB').copy()
                    elif i in [im.n_frames//3,im.n_frames//2]:different|=ImageChops.difference(first,im.convert('RGB')).getbbox() is not None
                assert total_ms>0 and different,f'Animation is empty/static: {path}'
                frames_total+=im.n_frames;animated_bytes+=path.stat().st_size
                gifs.append({'path':path.relative_to(ROOT).as_posix(),'frames':im.n_frames,'duration_ms':total_ms,'bytes':path.stat().st_size})
        else:
            with Image.open(path) as im:im.verify()
    build=json.loads((ROOT/'docs/preview-build.json').read_text())
    assert build['readme_sha256']==hashlib.sha256(md.encode()).hexdigest(),'Preview is stale; rebuild it'
    for rel,digest in build['asset_sha256'].items():
        assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,f'Preview asset changed since build: {rel}'
    for py in (ROOT/'scripts').glob('*.py'):compile(py.read_text(),str(py),'exec')
    assert not re.search(r'(?:/private/tmp|file:)',(ROOT/'tools/package-lock.json').read_text()),'Renderer lockfile is not portable'
    # Normalized DOM equality catches drift between README and the generated preview body.
    expected=BeautifulSoup(render(md),'html.parser');actual=BeautifulSoup((ROOT/'preview.html').read_text(),'html.parser').find('main')
    accessible_heading=actual.find('h1',class_='sr-only')
    assert accessible_heading, 'Missing accessible page heading'
    accessible_heading.decompose()
    assert expected.decode_contents()==actual.decode_contents(),'Preview differs from README'
    static_images={local_path(i.get('src','')) for i in BeautifulSoup(render(static),'html.parser').find_all('img')}
    result={'status':'passed','checks':['career corrections','counter URL invariant','relative image/file links','navigation anchors','unique sections','static edition','motion alternatives','all GIF frames decode','GIF loop/duration/motion','SVG/XML and raster validity','offline preview','preview content hash and DOM sync','Python syntax','portable renderer lock'], 'local_links_checked':checked_links,'unique_images_checked':len(images),'animated_assets':len(gifs),'decoded_gif_frames':frames_total,'animated_gif_bytes':animated_bytes,'static_edition_image_bytes':sum(p.stat().st_size for p in static_images),'elapsed_seconds':round(time.monotonic()-start,2),'animations':gifs}
    (ROOT/'docs/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['animations','checks']},indent=2))
if __name__=='__main__':main()
