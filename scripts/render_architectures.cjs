/* Rasterize authored SVG stages; no browser or network access. */
const fs = require('node:fs');
const path = require('node:path');
const { Resvg } = require('../tools/node_modules/@resvg/resvg-js');
const root = path.resolve(__dirname, '..');
const specs = {
  reliability: ['profile-token-architecture', 'reliability-glass-architecture'],
  'ai-agent': ['profile-ai-agent-architecture', 'ai-agent-glass-architecture'],
  finops: ['profile-finops-architecture', 'finops-glass-architecture'],
  platform: ['profile-platform-architecture', 'platform-glass-architecture'],
};
function writeAtomic(file, data) { fs.writeFileSync(file + '.tmp', data); fs.renameSync(file + '.tmp', file); }
const selected = process.argv.slice(2);
for (const key of selected.length ? selected : Object.keys(specs)) {
  if (!specs[key]) throw new Error(`Unknown architecture: ${key}`);
  const [scratch, name] = specs[key];
  for (let i = 0; i < 6; i++) {
    const svg = path.join('/tmp', scratch, `stage-${i}.svg`);
    writeAtomic(svg.replace(/\.svg$/, '.png'), new Resvg(fs.readFileSync(svg)).render().asPng());
  }
  const svg = path.join(root, 'assets/work', `${name}.svg`);
  writeAtomic(svg.replace(/\.svg$/, '.png'), new Resvg(fs.readFileSync(svg)).render().asPng());
  process.stdout.write(`Rendered ${key}\n`);
}
