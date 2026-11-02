/* Rasterize the local full-colour tech-tag sources at 3x for GIF generation. */
const fs=require('node:fs');
const path=require('node:path');
const {Resvg}=require('../tools/node_modules/@resvg/resvg-js');
const root=path.resolve(__dirname,'..');
for(const name of fs.readdirSync(path.join(root,'assets/stack-icons')).filter(x=>x.endsWith('.svg'))){
 const source=path.join(root,'assets/tech',name);
 if(!fs.existsSync(source))continue;
 const target=path.join(root,'assets/tech/raster',name.replace('.svg','.png'));
 fs.writeFileSync(target,new Resvg(fs.readFileSync(source),{fitTo:{mode:'zoom',value:3}}).render().asPng());
}
