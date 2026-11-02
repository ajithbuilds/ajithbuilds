"""Vector illustrations for the three career outcomes; no synthetic metric charts."""
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parent.parent
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="314" viewBox="0 0 1200 314" role="img" aria-labelledby="title desc"><title id="title">Selected career outcomes</title><desc id="desc">99.9% platform availability at BMW TechWorks India, 65% faster deployments at Cognizant for Western Union, and 50K+ monthly AIOps queries at BMW TechWorks India. Decorative uptime pulse, release flow, and query network illustrate the three areas, not measured time-series data.</desc><defs><linearGradient id="accent"><stop stop-color="#8ce8ff"/><stop offset="1" stop-color="#dba1ff"/></linearGradient><linearGradient id="glass" x2="0.7" y2="1"><stop stop-color="#263747" stop-opacity=".7"/><stop offset="1" stop-color="#141722" stop-opacity=".6"/></linearGradient><radialGradient id="halo"><stop stop-color="#6bb9df" stop-opacity=".15"/><stop offset="1" stop-color="#6bb9df" stop-opacity="0"/></radialGradient></defs><rect width="1200" height="314" rx="24" fill="#08080a"/><g font-family="Helvetica, Arial, sans-serif">''']
for j,(value,label,company) in enumerate([('99.9%','Platform availability','BMW TechWorks India'),('65%','Faster deployments','Cognizant · Western Union'),('50K+','Monthly AIOps queries','BMW TechWorks India')]):
 x=j*400
 parts.append(f'<g transform="translate({x},0)"><ellipse cx="205" cy="235" rx="185" ry="73" fill="url(#halo)"/><text x="36" y="92" fill="url(#accent)" font-size="60" font-weight="700" letter-spacing="-2">{value}</text><text x="36" y="134" fill="#f5f5f7" font-size="22" font-weight="600">{escape(label)}</text><text x="36" y="168" fill="#a1a1a6" font-size="16">{escape(company)}</text>')
 if j==0:
  parts.append('''<rect x="36" y="203" width="324" height="76" rx="16" fill="url(#glass)" stroke="#354c60"/><path d="M52 245h48l12-12 13 24 17-40 18 36 12-8h112" fill="none" stroke="url(#accent)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="320" cy="241" r="18" fill="#173b38" stroke="#72d7bb"/><path d="m311 241 6 6 12-13" fill="none" stroke="#a0f0d7" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>''')
 elif j==1:
  for k,label2 in enumerate(['BUILD','VERIFY','RELEASE']):
   xx=36+k*116
   parts.append(f'<rect x="{xx}" y="203" width="92" height="76" rx="14" fill="url(#glass)" stroke="#43516e"/><path d="m{xx+33} 224 13-7 13 7v15l-13 7-13-7Z m0 0 13 7 13-7 m-13 7v15" fill="#668bb5" fill-opacity=".22" stroke="#a6c9f0" stroke-width="1.2"/><text x="{xx+46}" y="265" text-anchor="middle" font-size="9" letter-spacing="1" fill="#b9cde3">{label2}</text>')
   if k<2:parts.append(f'<path d="M{xx+97} 240h13m-4-4 4 4-4 4" fill="none" stroke="#9bc9e5" stroke-width="1.5"/>')
 else:
  parts.append('<rect x="36" y="203" width="324" height="76" rx="16" fill="url(#glass)" stroke="#354c60"/>')
  for yy in [219,241,263]:
   parts.append(f'<path d="M73 {yy} 155 241 235 {yy} 321 241" fill="none" stroke="#718eaf" stroke-opacity=".65"/><circle cx="73" cy="{yy}" r="5" fill="#18384a" stroke="#8cdef4"/><circle cx="235" cy="{yy}" r="5" fill="#26384d" stroke="#c4b2ef"/>')
  parts.append('<circle cx="155" cy="241" r="18" fill="#244452" stroke="#92e5ec"/><path d="m145 241 10-9 10 9-10 9Z" fill="none" stroke="#bbf3f4" stroke-width="1.4"/><circle cx="321" cy="241" r="11" fill="#36405b" stroke="#c3b6ee"/><path d="m316 241 4 4 7-8" fill="none" stroke="#e0d7ff" stroke-width="1.6"/>')
 parts.append('</g>')
 if j<2:parts.append(f'<path d="M{(j+1)*400} 42V277" stroke="#303035"/>')
parts.append('</g></svg>')
(ROOT/'assets/impact.svg').write_text(''.join(parts)+'\n')
