import http from 'node:http';
import { createReadStream } from 'node:fs';
import { stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(fileURLToPath(new URL('../', import.meta.url)));
const portIndex = process.argv.indexOf('--port');
const port = Number(portIndex < 0 ? 3002 : process.argv[portIndex + 1]);
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error('Choose a port between 1024 and 65535.');
const types = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8', '.json': 'application/json',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.webp': 'image/webp', '.svg': 'image/svg+xml', '.mp4': 'video/mp4',
  '.webm': 'video/webm', '.glb': 'model/gltf-binary', '.gltf': 'model/gltf+json',
  '.bin': 'application/octet-stream', '.woff2': 'font/woff2', '.txt': 'text/plain; charset=utf-8',
};
const headers = { 'X-Robots-Tag': 'noindex, nofollow, noarchive', 'X-Content-Type-Options': 'nosniff', 'Cache-Control': 'no-store' };
http.createServer(async (req, res) => {
  const fail = (status, extra = {}) => { res.writeHead(status, { ...headers, ...extra }); res.end(); };
  try {
    if (!['GET', 'HEAD'].includes(req.method)) return fail(405, { Allow: 'GET, HEAD' });
    const pathname = decodeURIComponent(new URL(req.url, 'http://localhost').pathname);
    if (pathname === '/') return fail(302, { Location: '/graphic-print-world/kling-four/' });
    if (pathname.split('/').some(part => part.startsWith('.'))) return fail(404);
    let file = resolve(root, pathname.slice(1));
    if (file !== root && !file.startsWith(root + sep)) return fail(404);
    let info = await stat(file);
    if (info.isDirectory()) {
      if (!pathname.endsWith('/')) return fail(301, { Location: pathname + '/' });
      file = resolve(file, 'index.html'); info = await stat(file);
    }
    const contentType = types[extname(file).toLowerCase()];
    if (!info.isFile() || !contentType) return fail(404);
    let start = 0, end = info.size - 1, status = 200;
    if (req.headers.range) {
      const range = /^bytes=(\d*)-(\d*)$/.exec(req.headers.range);
      if (!range || (!range[1] && !range[2])) return fail(416, { 'Content-Range': `bytes */${info.size}` });
      if (range[1]) { start = Number(range[1]); end = range[2] ? Math.min(Number(range[2]), end) : end; }
      else start = Math.max(0, info.size - Number(range[2]));
      if (!Number.isSafeInteger(start) || !Number.isSafeInteger(end) || start > end || start >= info.size) return fail(416, { 'Content-Range': `bytes */${info.size}` });
      status = 206;
    }
    res.writeHead(status, { ...headers, 'Content-Type': contentType, 'Accept-Ranges': 'bytes', 'Content-Length': end - start + 1,
      ...(status === 206 ? { 'Content-Range': `bytes ${start}-${end}/${info.size}` } : {}) });
    if (req.method === 'HEAD') return res.end();
    const stream = createReadStream(file, { start, end });
    stream.on('error', () => res.destroy());
    res.on('close', () => stream.destroy());
    stream.pipe(res);
  } catch { if (!res.headersSent) fail(404); else res.destroy(); }
}).listen(port, '127.0.0.1', () => console.log(`JuiceBuilder: http://127.0.0.1:${port}/ (local only)`));
