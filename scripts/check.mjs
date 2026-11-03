import { readFile, readdir, access } from 'node:fs/promises';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { resolve, dirname } from 'node:path';

const root = fileURLToPath(new URL('../', import.meta.url));
let count = 0;
async function checkScripts(folder) {
  for (const entry of await readdir(folder, { withFileTypes: true })) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
    const file = resolve(folder, entry.name);
    if (entry.isDirectory()) await checkScripts(file);
    else if (/\.(?:mjs|js)$/.test(file)) { execFileSync(process.execPath, ['--check', file]); count++; }
  }
}
await checkScripts(root);
const current = resolve(root, 'graphic-print-world/kling-four');
for (const name of ['index.html', 'scroll.css', 'scroll.js', 'inspiration-film.js', 'bridge-parallax.js']) {
  const file = resolve(current, name), source = await readFile(file, 'utf8');
  const references = [...source.matchAll(/(?:src|href|data-video)=["']([^"']+)["']|url\(["']?([^\s)'";]+)["']?\)/g)];
  for (const match of references) {
    const value = match[1] || match[2];
    if (/^(?:#|https?:|data:|mailto:)/.test(value)) continue;
    await access(resolve(dirname(file), value.split(/[?#]/)[0]));
  }
}
console.log(`Checked ${count} JavaScript files and the current film page's local asset references.`);
