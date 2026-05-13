'use strict';
const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const PORT = 3141;
const ROOT = process.cwd();
const QUANTUM_DIR = path.join(ROOT, '.quantum');
const HTML_FILE = path.join(__dirname, 'dashboard.html');
const PID_FILE = path.join(QUANTUM_DIR, 'dashboard.pid');

const clients = new Set();
let debounce = null;

// ── Parsing ──────────────────────────────────────────────────────────────────

function normalizeInsight(raw) {
  let { type, content = '', ts } = raw;
  if (!type) {
    if (content.startsWith('[TUNNEL]')) { type = 'tunnel'; content = content.replace('[TUNNEL]', '').trim(); }
    else if (content.startsWith('[JUMP]')) { type = 'jump';   content = content.replace('[JUMP]',   '').trim(); }
    else type = 'discovery';
  }
  return { type, content, ts };
}

function readAllInsights() {
  const result = {};
  if (!fs.existsSync(QUANTUM_DIR)) return result;
  const SKIP = new Set(['project', 'singularities', 'code', 'dashboard.pid']);
  for (const name of fs.readdirSync(QUANTUM_DIR)) {
    if (SKIP.has(name)) continue;
    try {
      const stat = fs.statSync(path.join(QUANTUM_DIR, name));
      if (!stat.isDirectory()) continue;
    } catch { continue; }
    const file = path.join(QUANTUM_DIR, name, 'insights.jsonl');
    if (!fs.existsSync(file)) continue;
    const lines = fs.readFileSync(file, 'utf8').trim().split('\n').filter(Boolean);
    result[name] = lines.flatMap(l => {
      try { return [normalizeInsight(JSON.parse(l))]; } catch { return []; }
    });
  }
  return result;
}

function readCodeFindings() {
  const file = path.join(QUANTUM_DIR, 'code', 'findings.jsonl');
  if (!fs.existsSync(file)) return null;
  const lines = fs.readFileSync(file, 'utf8').trim().split('\n').filter(Boolean);
  const items = lines.flatMap(l => { try { return [JSON.parse(l)]; } catch { return []; } });
  const counts = { 'code-tunnel': 0, 'code-decoherence': 0, 'code-superposition': 0, 'code-jump': 0 };
  for (const f of items) if (f.type in counts) counts[f.type]++;
  return { counts, hotspots: items.filter(i => i.type === 'code-tunnel').slice(0, 5) };
}

// ── Signal computation (parity with /cosmos observe) ─────────────────────────

function computeSignals(cosmos) {
  const entries = Object.entries(cosmos);
  const names = Object.keys(cosmos);

  const fingerprints = {};
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      const key = (ins.content || '').slice(0, 120).trim();
      if (!key) continue;
      if (!fingerprints[key]) fingerprints[key] = new Set();
      fingerprints[key].add(name);
    }
  }

  const resonance = [];
  const resonantKeys = new Set();
  for (const [content, ns] of Object.entries(fingerprints)) {
    if (ns.size >= 2) {
      resonance.push({ content, cosmos: [...ns] });
      resonantKeys.add(content);
    }
  }

  const uncertainty = [];
  const decisionMap = {};
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      if (ins.type !== 'decision') continue;
      const key = (ins.content || '').slice(0, 120).trim();
      if (resonantKeys.has(key)) continue;
      if (!decisionMap[key]) decisionMap[key] = [];
      decisionMap[key].push(name);
    }
  }
  for (const [content, cosmos] of Object.entries(decisionMap)) {
    uncertainty.push({ content, cosmos: [...new Set(cosmos)] });
  }

  const tunnels = [], jumps = [], blockers = [];
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      if (ins.type === 'tunnel')  tunnels.push({ cosmos: name, ...ins });
      if (ins.type === 'jump')    jumps.push({ cosmos: name, ...ins });
      if (ins.type === 'blocker') blockers.push({ cosmos: name, ...ins });
    }
  }

  const decoherence = [];
  for (let i = 0; i < entries.length; i++) {
    const [nameA, insA] = entries[i];
    const setA = new Set(insA.map(ins => (ins.content || '').slice(0, 120).trim()).filter(Boolean));
    for (let j = i + 1; j < entries.length; j++) {
      const [nameB, insB] = entries[j];
      const setB = new Set(insB.map(ins => (ins.content || '').slice(0, 120).trim()).filter(Boolean));
      const shared = [...setA].filter(x => setB.has(x)).length;
      const overlap = shared / Math.max(setA.size, 1);
      if (overlap > 0.6) {
        decoherence.push({ cosmos: nameA, other: nameB, overlap: Math.round(overlap * 100) });
      }
    }
  }

  const bec = (
    resonance.length >= 3 &&
    uncertainty.length === 0 &&
    names.length >= 1 &&
    resonance.every(r => names.every(n => r.cosmos.includes(n)))
  );

  const heartbeats = [], heartbeatAcks = [];
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      if (ins.type === 'heartbeat')      heartbeats.push({ cosmos: name, ...ins });
      if (ins.type === 'heartbeat-ack')  heartbeatAcks.push({ cosmos: name, ...ins });
    }
  }
  let heartbeatQuality = null;
  if (heartbeats.length > 0 && names.length > 1) {
    const expected = heartbeats.length * (names.length - 1);
    const actual   = heartbeatAcks.length;
    const ratio    = actual / Math.max(expected, 1);
    heartbeatQuality = {
      expected, actual,
      pct: Math.round(ratio * 100),
      quality: ratio >= 0.8 ? 'High' : ratio >= 0.4 ? 'Medium' : 'Low',
    };
  }

  return { resonance, uncertainty, tunnels, jumps, blockers, decoherence, bec, heartbeatQuality };
}

// ── Mermaid ───────────────────────────────────────────────────────────────────

function buildMermaid(cosmos, signals) {
  const names = Object.keys(cosmos);
  if (names.length === 0) return 'graph TD\n  W["⏳ Waiting for cosmos to spawn..."]';

  let d = 'graph TD\n';
  for (const name of names) {
    const count = cosmos[name].length;
    const latest = cosmos[name].at(-1);
    const tag = latest ? latest.type : 'waiting';
    d += `  ${name}["🌌 ${name}\\n${count} insights\\n${tag}"]\n`;
    d += `  style ${name} fill:#1e3a5f,stroke:#4a9eff,color:#fff\n`;
  }

  const pairs = new Set();
  for (const r of signals.resonance) {
    const sorted = [...r.cosmos].sort();
    for (let i = 0; i < sorted.length - 1; i++) {
      const key = `${sorted[i]}-${sorted[i+1]}`;
      if (!pairs.has(key)) {
        pairs.add(key);
        d += `  ${sorted[i]} -.resonance.- ${sorted[i+1]}\n`;
      }
    }
  }

  for (const dc of signals.decoherence) {
    d += `  ${dc.cosmos} ==>|"⚠️ ${dc.overlap}% overlap"| ${dc.other}\n`;
  }
  return d;
}

// ── SSE broadcast ─────────────────────────────────────────────────────────────

function broadcast(payload) {
  const msg = `data: ${JSON.stringify(payload)}\n\n`;
  for (const res of clients) res.write(msg);
}

function refresh() {
  const cosmos       = readAllInsights();
  const signals      = computeSignals(cosmos);
  const mermaid      = buildMermaid(cosmos, signals);
  const codeFindings = readCodeFindings();
  broadcast({ cosmos, signals, mermaid, codeFindings });
}

// ── File watcher ──────────────────────────────────────────────────────────────

function watchQuantum() {
  fs.mkdirSync(QUANTUM_DIR, { recursive: true });
  fs.watch(QUANTUM_DIR, { recursive: true }, () => {
    clearTimeout(debounce);
    debounce = setTimeout(refresh, 250);
  });
}

// ── HTTP server ───────────────────────────────────────────────────────────────

function openBrowser() {
  const url = `http://localhost:${PORT}`;
  const cmd = process.platform === 'win32' ? `start ${url}`
            : process.platform === 'darwin' ? `open ${url}`
            : `xdg-open ${url}`;
  exec(cmd, err => { if (err) console.log(`  → Open ${url} in your browser`); });
}

const server = http.createServer((req, res) => {
  if (req.url === '/events') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
    });
    res.write(':ok\n\n');
    clients.add(res);
    req.on('close', () => clients.delete(res));
    const cosmos       = readAllInsights();
    const signals      = computeSignals(cosmos);
    const mermaid      = buildMermaid(cosmos, signals);
    const codeFindings = readCodeFindings();
    res.write(`data: ${JSON.stringify({ cosmos, signals, mermaid, codeFindings })}\n\n`);
    return;
  }

  if (req.url === '/' || req.url === '/index.html') {
    try {
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(fs.readFileSync(HTML_FILE, 'utf8'));
    } catch {
      res.writeHead(500);
      res.end('dashboard.html not found — run from project root');
    }
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.on('error', err => {
  if (err.code === 'EADDRINUSE') {
    console.log(`⚡ Dashboard already running at http://localhost:${PORT}`);
    openBrowser();
    process.exit(0);
  }
  throw err;
});

server.listen(PORT, () => {
  console.log(`\n🌌 QuantumAgent Dashboard  →  http://localhost:${PORT}\n`);
  fs.mkdirSync(QUANTUM_DIR, { recursive: true });
  fs.writeFileSync(PID_FILE, String(process.pid));
  watchQuantum();
  openBrowser();
});

process.on('SIGINT', () => {
  try { fs.unlinkSync(PID_FILE); } catch {}
  process.exit(0);
});
