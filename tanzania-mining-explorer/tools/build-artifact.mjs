/* Build the Artifact-hosted variant of the console.
 *
 * index.html is a standalone document you can open from disk or serve
 * anywhere. The Artifact host supplies its own <!doctype>/<head>/<body>
 * skeleton and expects page content only, so this strips the wrapper and
 * leaves <title>, the font <link>s, the <style> block and the body content
 * exactly as they are. Nothing else differs between the two files.
 */
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const src  = readFileSync(resolve(root, 'index.html'), 'utf8');

const strip = [
  /^<!doctype html>\s*/i,
  /^<html[^>]*>\s*/i,
  /^<head>\s*/i,
  /^<meta charset="utf-8">\s*/i,
  /^<meta name="viewport"[^>]*>\s*/i,
];

let out = src;
for (const re of strip) out = out.replace(re, '');
out = out.replace(/\n<\/head>\n<body>\n/, '\n');
out = out.replace(/\n<\/body>\n<\/html>\s*$/, '\n');

for (const tag of ['<!doctype', '<html', '<head>', '</head>', '<body>', '</body>', '</html>']) {
  if (out.toLowerCase().includes(tag)) throw new Error(`wrapper tag survived: ${tag}`);
}
if (!out.startsWith('<title>')) throw new Error('expected <title> first');

const dest = resolve(root, 'dist/ngao-exploration-console.html');
mkdirSync(dirname(dest), { recursive: true });
writeFileSync(dest, out);
console.log(`wrote ${dest} — ${(out.length / 1024).toFixed(0)} KB`);
