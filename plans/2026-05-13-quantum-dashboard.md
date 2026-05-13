# QuantumAgent Live Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a live web dashboard that auto-opens on `/cosmos spawn` and shows ALL quantum signals (Resonance, Uncertainty, Degeneracy, Decoherence, Tunneling, Jump, Blockers, BEC, Heartbeat quality, Code findings) in real time via SSE.

**Architecture:** Node.js HTTP server (`tools/dashboard.js`) watches `.quantum/` via `fs.watch`, computes all signals from observe skill parity, and pushes state to browsers via SSE. A single-file HTML frontend (`tools/dashboard.html`) renders three panels + Mermaid diagram. The spawn skill is extended with Step 2.1 to auto-start the server.

**Tech Stack:** Node.js built-ins only (`http`, `fs`, `path`, `child_process`), Mermaid.js v10 via CDN, vanilla JS/CSS

**Signal coverage (parity with `/cosmos observe`):**

| Signal | Source | Method |
|--------|--------|--------|
| Resonance | insights | Content fingerprint appearing in ≥2 cosmos |
| Uncertainty | `decision` insights not in resonance | Non-resonant decisions per cosmos |
| Degeneracy | content overlap ≥60% across cosmos | Set intersection ratio |
| Decoherence | content overlap ≥60% between two cosmos | Set intersection ratio |
| Tunneling | `type:"tunnel"` + `[TUNNEL]` prefix | Type filter + legacy prefix |
| Jump | `type:"jump"` + `[JUMP]` prefix | Type filter + legacy prefix |
| Blockers | `type:"blocker"` | Type filter |
| BEC | resonance≥3 ∧ uncertainty=0 ∧ all cosmos in every resonance | Derived |
| Heartbeat quality | `heartbeat`/`heartbeat-ack` entries | Count ratio |
| Code findings | `.quantum/code/findings.jsonl` | Separate file read |

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `tools/dashboard.js` | Create | HTTP + SSE server, all signal computation |
| `tools/dashboard.html` | Create | SPA: 3 panels + all signal cards + Mermaid |
| `skills/spawn/SKILL.md` | Modify | Add Step 2.1 to auto-start dashboard |
| `.gitignore` | Modify | Ignore `dashboard.pid` |
| `README.ko.md` | Modify | Add dashboard section |
| `README.md` | Modify | Add dashboard section |

---

### Task 1: Create `tools/dashboard.js`

**Files:**
- Create: `tools/dashboard.js`

- [ ] **Step 1: Create tools/ directory**

```bash
mkdir -p tools
```

- [ ] **Step 2: Write `tools/dashboard.js`**

Create `tools/dashboard.js`:

```javascript
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
  // Schema: {"type","content","ts"} — legacy: missing type or [TUNNEL]/[JUMP] prefix
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

  // — Fingerprints: content[0..120] → Set<cosmos> —
  const fingerprints = {};
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      const key = (ins.content || '').slice(0, 120).trim();
      if (!key) continue;
      if (!fingerprints[key]) fingerprints[key] = new Set();
      fingerprints[key].add(name);
    }
  }

  // — Resonance: fingerprint in ≥2 cosmos —
  const resonance = [];
  const resonantKeys = new Set();
  for (const [content, ns] of Object.entries(fingerprints)) {
    if (ns.size >= 2) {
      resonance.push({ content, cosmos: [...ns] });
      resonantKeys.add(content);
    }
  }

  // — Uncertainty: decision insights NOT already in resonance —
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

  // — Tunnels / Jumps / Blockers (by type) —
  const tunnels = [], jumps = [], blockers = [];
  for (const [name, insights] of entries) {
    for (const ins of insights) {
      if (ins.type === 'tunnel')  tunnels.push({ cosmos: name, ...ins });
      if (ins.type === 'jump')    jumps.push({ cosmos: name, ...ins });
      if (ins.type === 'blocker') blockers.push({ cosmos: name, ...ins });
    }
  }

  // — Decoherence: cosmos pair with >60% content overlap —
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

  // — BEC: resonance≥3, uncertainty=0, all cosmos in every resonance item —
  const bec = (
    resonance.length >= 3 &&
    uncertainty.length === 0 &&
    names.length >= 1 &&
    resonance.every(r => names.every(n => r.cosmos.includes(n)))
  );

  // — Heartbeat quality (strict entanglement mode) —
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
  // Resonance edges (deduplicated pairs)
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
  // Decoherence edges
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
    // Send current state immediately on connect
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
```

- [ ] **Step 3: Verify syntax**

```bash
node --check tools/dashboard.js
```

Expected: no output (exit code 0).

- [ ] **Step 4: Commit**

```bash
git add tools/dashboard.js
git commit -m "feat: add quantum dashboard server — all observe-parity signals via SSE"
```

---

### Task 2: Create `tools/dashboard.html`

**Files:**
- Create: `tools/dashboard.html`

- [ ] **Step 1: Write `tools/dashboard.html`**

Create `tools/dashboard.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🌌 QuantumAgent Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --bg:     #0d1117; --bg2: #161b22; --bg3: #1c2128;
      --border: #30363d; --text: #c9d1d9; --muted: #8b949e;
      --blue:   #58a6ff; --green: #3fb950; --red: #f85149;
      --purple: #bc8cff; --orange: #ffa657; --yellow: #d29922;
    }
    body {
      background: var(--bg); color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', monospace;
      font-size: 13px; height: 100vh;
      display: flex; flex-direction: column; overflow: hidden;
    }
    header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 16px; background: var(--bg2);
      border-bottom: 1px solid var(--border); flex-shrink: 0;
    }
    header h1 { font-size: 14px; font-weight: 600; }
    .live-badge { display: flex; align-items: center; gap: 6px; font-size: 11px; color: var(--green); }
    .live-dot {
      width: 8px; height: 8px; border-radius: 50%; background: var(--green);
      animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.3} }

    .main-grid {
      display: grid;
      grid-template-columns: 210px 1fr 260px;
      grid-template-rows: 1fr 180px;
      gap: 1px; background: var(--border); flex: 1; overflow: hidden;
    }
    .panel { background: var(--bg); overflow-y: auto; padding: 10px 12px; }
    .panel-title {
      font-size: 10px; font-weight: 700; text-transform: uppercase;
      letter-spacing: .1em; color: var(--muted);
      margin-bottom: 10px; padding-bottom: 6px; border-bottom: 1px solid var(--border);
    }
    .mermaid-wrap {
      grid-column: 1 / -1; background: var(--bg2);
      overflow-x: auto; display: flex; align-items: center;
      padding: 10px 16px; gap: 16px;
    }
    .mermaid-wrap .panel-title { margin-bottom: 0; border: none; padding: 0; flex-shrink: 0; }

    /* Cosmos cards */
    .cosmos-card {
      background: var(--bg2); border: 1px solid var(--border);
      border-left: 3px solid var(--blue); border-radius: 6px;
      padding: 9px 10px; margin-bottom: 8px;
    }
    .cosmos-name { font-weight: 600; color: var(--blue); font-size: 13px; }
    .type-bar { display:flex; height:4px; border-radius:2px; overflow:hidden; margin-top:6px; background:var(--bg3); }
    .cosmos-latest {
      font-size: 10px; color: var(--muted); margin-top: 6px; line-height: 1.4;
      display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
    }

    /* Signal sections */
    .signal-section { margin-bottom: 14px; }
    .signal-label {
      font-size: 11px; font-weight: 600; margin-bottom: 6px;
      display: flex; align-items: center; gap: 6px;
    }
    .signal-count {
      background: var(--bg3); border-radius: 10px;
      padding: 1px 7px; font-size: 10px; color: var(--muted);
    }
    .signal-item {
      background: var(--bg2); border: 1px solid var(--border);
      border-radius: 4px; padding: 7px 9px; margin-bottom: 5px;
      font-size: 11px; line-height: 1.5;
    }
    .cosmos-tags { display:flex; gap:4px; margin-bottom:4px; flex-wrap:wrap; }
    .cosmos-tag {
      font-size: 10px; background: #1e3a5f; color: var(--blue);
      border-radius: 3px; padding: 1px 5px;
    }

    /* BEC banner */
    .bec-banner {
      background: linear-gradient(135deg,#0d2a12,#1a2d00);
      border: 1px solid var(--green); border-radius: 6px;
      padding: 10px 12px; margin-bottom: 12px; font-size: 11px;
      line-height: 1.5; color: var(--green);
    }

    /* Heartbeat quality badge */
    .hb-badge {
      display: inline-flex; align-items: center; gap: 5px;
      border-radius: 4px; padding: 4px 8px; font-size: 11px; font-weight: 600;
    }

    /* Code findings bar */
    .code-row { display:flex; align-items:center; gap:8px; margin-bottom:5px; font-size:11px; }
    .code-bar-wrap { flex:1; height:6px; background:var(--bg3); border-radius:3px; overflow:hidden; }
    .code-bar-fill { height:100%; border-radius:3px; }

    /* Timeline */
    .tl-item { display:flex; gap:8px; margin-bottom:8px; align-items:flex-start; }
    .type-badge {
      flex-shrink: 0; font-size: 9px; font-weight: 700;
      padding: 2px 5px; border-radius: 3px;
      text-transform: uppercase; letter-spacing: .04em; margin-top: 1px;
    }
    .tl-cosmos { flex-shrink:0; width:22px; font-size:10px; color:var(--blue); font-weight:700; margin-top:2px; }
    .tl-content { font-size:11px; line-height:1.5; flex:1; }
    .tl-ts { font-size:9px; color:var(--muted); margin-top:2px; }

    .empty { text-align:center; color:var(--muted); font-size:11px; padding:18px 0; }
    ::-webkit-scrollbar { width:5px; height:5px; }
    ::-webkit-scrollbar-track { background:var(--bg); }
    ::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
  </style>
</head>
<body>

<header>
  <h1>🌌 QuantumAgent Live Dashboard</h1>
  <div class="live-badge">
    <div class="live-dot" id="live-dot"></div>
    <span id="status-text">Connecting...</span>
  </div>
</header>

<div class="main-grid">
  <div class="panel">
    <div class="panel-title">Cosmos</div>
    <div id="cosmos-list"><div class="empty">Waiting for spawn…</div></div>
  </div>

  <div class="panel">
    <div class="panel-title">Quantum Signals</div>
    <div id="signals-content"></div>
  </div>

  <div class="panel">
    <div class="panel-title">Timeline</div>
    <div id="timeline-list"><div class="empty">No insights yet</div></div>
  </div>

  <div class="mermaid-wrap">
    <div class="panel-title">Graph</div>
    <div id="mermaid-target"></div>
  </div>
</div>

<script>
  mermaid.initialize({
    startOnLoad: false, theme: 'dark',
    themeVariables: {
      background: '#0d1117', primaryColor: '#1e3a5f',
      primaryTextColor: '#c9d1d9', primaryBorderColor: '#4a9eff',
      lineColor: '#4a9eff', edgeLabelBackground: '#161b22',
    },
  });

  const TC = {
    discovery:       { fg: '#58a6ff', bg: '#0d2044' },
    decision:        { fg: '#3fb950', bg: '#0d2a12' },
    blocker:         { fg: '#f85149', bg: '#2a0d0d' },
    tunnel:          { fg: '#bc8cff', bg: '#1e0d3a' },
    jump:            { fg: '#ffa657', bg: '#2a1a0d' },
    resonance:       { fg: '#3fb950', bg: '#0d2a12' },
    complete:        { fg: '#56d364', bg: '#0d2a12' },
    crystallize:     { fg: '#ffd700', bg: '#2a2200' },
    heartbeat:       { fg: '#8b949e', bg: '#1c2128' },
    'heartbeat-ack': { fg: '#6e7681', bg: '#1c2128' },
  };

  function tc(type) { return TC[type] || { fg: '#8b949e', bg: '#1c2128' }; }

  function badge(type) {
    const {fg, bg} = tc(type);
    return `<span class="type-badge" style="color:${fg};background:${bg}">${type}</span>`;
  }

  function esc(s) {
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
  }

  function tags(cosmos) {
    return `<div class="cosmos-tags">${cosmos.map(c =>
      `<span class="cosmos-tag">${esc(c)}</span>`).join('')}</div>`;
  }

  // ── Cosmos panel ──────────────────────────────────────────────────────────
  function renderCosmos(cosmos) {
    const names = Object.keys(cosmos);
    const el = document.getElementById('cosmos-list');
    if (!names.length) { el.innerHTML = '<div class="empty">Waiting for spawn…</div>'; return; }
    el.innerHTML = names.map(name => {
      const ins = cosmos[name];
      const counts = {};
      for (const i of ins) counts[i.type || 'discovery'] = (counts[i.type || 'discovery'] || 0) + 1;
      const bar = Object.entries(counts)
        .map(([t,n]) => `<div style="flex:${n};background:${tc(t).fg};min-width:2px"></div>`).join('');
      const latest = ins[ins.length - 1];
      const summary = Object.entries(counts).map(([t,n]) => `${n} ${t}`).join(' · ');
      return `
        <div class="cosmos-card">
          <div class="cosmos-name">🌌 ${esc(name)}</div>
          <div style="font-size:10px;color:var(--muted);margin-top:2px">${ins.length} insights · ${esc(summary)}</div>
          <div class="type-bar">${bar}</div>
          ${latest ? `<div class="cosmos-latest">${esc(latest.content || '')}</div>` : ''}
        </div>`;
    }).join('');
  }

  // ── Signals panel (full observe parity) ───────────────────────────────────
  function renderSignals(signals, codeFindings) {
    const el = document.getElementById('signals-content');
    let html = '';

    // BEC banner
    if (signals.bec) {
      html += `<div class="bec-banner">
        🌡️ <strong>Bose-Einstein Condensate</strong><br>
        Complete convergence across all decisions. The goal was deterministic — any strategy would have found the same answer.
      </div>`;
    }

    // Heartbeat quality
    if (signals.heartbeatQuality) {
      const hq = signals.heartbeatQuality;
      const color = hq.quality === 'High' ? 'var(--green)' : hq.quality === 'Medium' ? 'var(--orange)' : 'var(--red)';
      html += `<div class="signal-section">
        <div class="signal-label" style="color:var(--muted)">🔗 Entanglement Quality</div>
        <div class="signal-item">
          <span class="hb-badge" style="color:${color};background:var(--bg3)">
            ${hq.quality} — ${hq.actual}/${hq.expected} ACKs (${hq.pct}%)
          </span>
        </div>
      </div>`;
    }

    // Main signal sections
    const sections = [
      {
        icon: '⚡', label: 'Resonance', color: 'var(--green)',
        items: signals.resonance || [],
        render: r => `${tags(r.cosmos)}<div>${esc(r.content)}</div>`,
      },
      {
        icon: '🌀', label: 'Uncertainty', color: 'var(--orange)',
        items: signals.uncertainty || [],
        render: u => `${tags(u.cosmos)}<div>${esc(u.content)}</div>`,
      },
      {
        icon: '⚠️', label: 'Decoherence', color: 'var(--yellow)',
        items: signals.decoherence || [],
        render: d => `<div>${esc(d.cosmos)} ↔ ${esc(d.other)}: ${d.overlap}% content overlap — may have lost strategic identity</div>`,
      },
      {
        icon: '⚛️', label: 'Tunneling', color: 'var(--purple)',
        items: signals.tunnels || [],
        render: t => `${tags([t.cosmos])}<div>${esc(t.content || '')}</div>`,
      },
      {
        icon: '⚡', label: 'Jumps', color: 'var(--orange)',
        items: signals.jumps || [],
        render: j => `${tags([j.cosmos])}<div>${esc(j.content || '')}</div>`,
      },
      {
        icon: '🚧', label: 'Blockers', color: 'var(--red)',
        items: signals.blockers || [],
        render: b => `${tags([b.cosmos])}<div>${esc(b.content || '')}</div>`,
      },
    ];

    for (const s of sections) {
      html += `<div class="signal-section">
        <div class="signal-label" style="color:${s.color}">
          ${s.icon} ${s.label} <span class="signal-count">${s.items.length}</span>
        </div>
        ${s.items.length === 0
          ? '<div class="empty" style="padding:6px 0">None detected</div>'
          : s.items.slice(0, 6).map(i => `<div class="signal-item">${s.render(i)}</div>`).join('')
        }
      </div>`;
    }

    // Code-scale findings (from /cosmos scan)
    if (codeFindings) {
      const { counts } = codeFindings;
      const total = Object.values(counts).reduce((a,b) => a+b, 0);
      const codeTypes = [
        { key: 'code-tunnel',       label: 'Tunnels',      color: '#bc8cff' },
        { key: 'code-decoherence',  label: 'Decoherence',  color: '#ffa657' },
        { key: 'code-superposition',label: 'Superposition',color: '#58a6ff' },
        { key: 'code-jump',         label: 'Jumps',        color: '#d29922' },
      ];
      html += `<div class="signal-section">
        <div class="signal-label" style="color:var(--muted)">⚛️ Code-Scale (/cosmos scan)</div>
        ${total === 0
          ? '<div class="empty" style="padding:6px 0">No scan data</div>'
          : codeTypes.filter(ct => counts[ct.key] > 0).map(ct => `
            <div class="code-row">
              <span style="color:${ct.color};width:80px;font-size:10px">${ct.label}</span>
              <div class="code-bar-wrap">
                <div class="code-bar-fill" style="width:${Math.min(100, counts[ct.key] * 5)}%;background:${ct.color}"></div>
              </div>
              <span style="color:var(--muted);font-size:10px;width:24px;text-align:right">${counts[ct.key]}</span>
            </div>`).join('')
        }
      </div>`;
    }

    el.innerHTML = html;
  }

  // ── Timeline panel ────────────────────────────────────────────────────────
  function renderTimeline(cosmos) {
    const el = document.getElementById('timeline-list');
    const all = [];
    for (const [name, ins] of Object.entries(cosmos))
      for (const i of ins) all.push({ ...i, _c: name });
    all.sort((a, b) => new Date(b.ts) - new Date(a.ts));

    if (!all.length) { el.innerHTML = '<div class="empty">No insights yet</div>'; return; }
    el.innerHTML = all.slice(0, 100).map(i => `
      <div class="tl-item">
        ${badge(i.type || 'discovery')}
        <div class="tl-cosmos">${esc((i._c||'').slice(0,3))}</div>
        <div>
          <div class="tl-content">${esc(i.content || '')}</div>
          <div class="tl-ts">${new Date(i.ts).toLocaleTimeString()}</div>
        </div>
      </div>`).join('');
  }

  // ── Mermaid ───────────────────────────────────────────────────────────────
  let mermaidSeq = 0;
  async function renderMermaid(def) {
    const target = document.getElementById('mermaid-target');
    try {
      const { svg } = await mermaid.render('mg' + (++mermaidSeq), def);
      target.innerHTML = svg;
    } catch {
      target.innerHTML = `<pre style="font-size:10px;color:var(--muted)">${esc(def)}</pre>`;
    }
  }

  // ── SSE ───────────────────────────────────────────────────────────────────
  const src = new EventSource('/events');
  src.onopen = () => {
    document.getElementById('status-text').textContent = 'LIVE';
    document.getElementById('live-dot').style.background = 'var(--green)';
  };
  src.onerror = () => {
    document.getElementById('status-text').textContent = 'Reconnecting…';
    document.getElementById('live-dot').style.background = 'var(--red)';
  };
  src.onmessage = e => {
    const d = JSON.parse(e.data);
    renderCosmos(d.cosmos || {});
    renderSignals(d.signals || {}, d.codeFindings || null);
    renderTimeline(d.cosmos || {});
    renderMermaid(d.mermaid || 'graph TD\n  W["No data yet"]');
  };
</script>
</body>
</html>
```

- [ ] **Step 2: Smoke test — all signal types**

Start server:
```bash
node tools/dashboard.js
```

Open http://localhost:3141. Then run each injection test below and verify the corresponding signal appears within 1 second.

**Resonance test:**
```bash
mkdir -p .quantum/alpha .quantum/beta
echo '{"type":"discovery","content":"JWT has no expiration","ts":"2026-05-13T12:00:00Z"}' >> .quantum/alpha/insights.jsonl
echo '{"type":"discovery","content":"JWT has no expiration","ts":"2026-05-13T12:00:01Z"}' >> .quantum/beta/insights.jsonl
```
Expected: Resonance section shows 1 item with `alpha` + `beta` tags.

**Uncertainty test:**
```bash
echo '{"type":"decision","content":"Use HS256 algorithm","ts":"2026-05-13T12:00:02Z"}' >> .quantum/alpha/insights.jsonl
echo '{"type":"decision","content":"Use RS256 algorithm","ts":"2026-05-13T12:00:03Z"}' >> .quantum/beta/insights.jsonl
```
Expected: Uncertainty section shows 2 items (one per cosmos).

**Tunnel + legacy prefix test:**
```bash
echo '{"type":"tunnel","content":"Redis sorted sets make rate-limit table unnecessary","ts":"2026-05-13T12:00:04Z"}' >> .quantum/alpha/insights.jsonl
echo '{"content":"[TUNNEL] Legacy prefix still works","ts":"2026-05-13T12:00:05Z"}' >> .quantum/beta/insights.jsonl
```
Expected: Tunneling section shows 2 items.

**Blocker test:**
```bash
echo '{"type":"blocker","content":"Double-counting at window boundary","ts":"2026-05-13T12:00:06Z"}' >> .quantum/gamma/insights.jsonl 2>/dev/null || (mkdir -p .quantum/gamma && echo '{"type":"blocker","content":"Double-counting at window boundary","ts":"2026-05-13T12:00:06Z"}' >> .quantum/gamma/insights.jsonl)
```
Expected: Blockers section shows 1 item.

**BEC test (requires cleanup first, then fresh resonances ≥3):**
```bash
rm -rf .quantum/alpha .quantum/beta .quantum/gamma
mkdir -p .quantum/alpha .quantum/beta .quantum/gamma
for c in alpha beta gamma; do
  echo '{"type":"decision","content":"Use 15min access tokens","ts":"2026-05-13T13:00:00Z"}' >> .quantum/$c/insights.jsonl
  echo '{"type":"decision","content":"Separate JWT secrets for access and refresh","ts":"2026-05-13T13:00:01Z"}' >> .quantum/$c/insights.jsonl
  echo '{"type":"decision","content":"Store jti not raw token","ts":"2026-05-13T13:00:02Z"}' >> .quantum/$c/insights.jsonl
done
```
Expected: BEC banner appears (green "Bose-Einstein Condensate" card at top of signals panel).

**Cleanup:**
```bash
rm -rf .quantum/alpha .quantum/beta .quantum/gamma
```

- [ ] **Step 3: Commit**

```bash
git add tools/dashboard.html
git commit -m "feat: add quantum dashboard frontend — full observe-parity signal coverage"
```

---

### Task 3: Integrate with spawn skill

**Files:**
- Modify: `skills/spawn/SKILL.md`

- [ ] **Step 1: Add Step 2.1**

In `skills/spawn/SKILL.md`, find this exact line:

```
### Step 2.5 — Load macro-scale context (optional)
```

Insert immediately before it:

```markdown
### Step 2.1 — Start live dashboard

Start the QuantumAgent live dashboard in the background before launching cosmos agents, so insights are visible in real time:

```bash
node <repo_root>/tools/dashboard.js &
```

The server listens on port 3141 and auto-opens http://localhost:3141 in the default browser. If already running (`EADDRINUSE`), it opens the browser and exits silently — no duplicate process.

Skip silently if `tools/dashboard.js` does not exist.

```

- [ ] **Step 2: Verify step order in SKILL.md**

Read `skills/spawn/SKILL.md` and confirm order:
1. Step 1 — Parse arguments
2. Step 2 — Detect repo root
3. **Step 2.1 — Start live dashboard** ← new
4. Step 2.5 — Load macro-scale context
5. Step 3 — Create quantum memory directories
6. Step 4 — Create git worktrees
7. Step 5 — Write CLAUDE.md into each worktree

- [ ] **Step 3: Commit**

```bash
git add skills/spawn/SKILL.md
git commit -m "feat: auto-start live dashboard on /cosmos spawn"
```

---

### Task 4: Housekeeping

**Files:**
- Modify: `.gitignore`

- [ ] **Step 1: Ignore PID file**

```bash
echo '.quantum/dashboard.pid' >> .gitignore
```

- [ ] **Step 2: Commit**

```bash
git add .gitignore
git commit -m "chore: ignore quantum dashboard PID file"
```

---

### Task 5: Update README

**Files:**
- Modify: `README.ko.md`
- Modify: `README.md`

- [ ] **Step 1: Add dashboard section to `README.ko.md`**

In `README.ko.md`, find `## 커맨드` and insert this section immediately before it:

```markdown
## 🖥️ 라이브 대시보드

`/cosmos spawn` 실행 시 브라우저가 http://localhost:3141 에 자동으로 열립니다.

| 패널 | 내용 |
|------|------|
| 왼쪽 | 코스모스별 인사이트 수 + 타입 분포 바 + 최신 인사이트 |
| 가운데 | 모든 양자 신호 카드 (아래 참조) |
| 오른쪽 | 전체 인사이트 타임라인 (최신순, 타입별 색상) |
| 하단 | Mermaid 그래프 — cosmos 노드 + 공명·결어긋남 엣지 실시간 갱신 |

**신호 카드 (중앙 패널):**

| 신호 | 설명 |
|------|------|
| 🌡️ BEC | 모든 결정에서 완전 수렴 시 배너 표시 |
| 🔗 Entanglement Quality | strict 모드 heartbeat ACK 비율 |
| ⚡ Resonance | 2개 이상 cosmos가 독립적으로 수렴한 결론 |
| 🌀 Uncertainty | cosmos가 다른 결정을 내린 트레이드오프 |
| ⚠️ Decoherence | 전략적 정체성을 잃은 cosmos 쌍 탐지 |
| ⚛️ Tunneling | 예상된 제약을 우회한 해결책 |
| ⚡ Jumps | 단일 얽힘 읽기로 발생한 불연속 전환 |
| 🚧 Blockers | 미해결 차단요소 |
| ⚛️ Code-Scale | `/cosmos scan` 결과 (tunnel·decoherence·superposition·jump) |

수동 실행: `node tools/dashboard.js`

---

```

- [ ] **Step 2: Add dashboard section to `README.md`**

In `README.md`, find `## Commands` and insert this section immediately before it:

```markdown
## 🖥️ Live Dashboard

On `/cosmos spawn`, the browser opens http://localhost:3141 automatically.

| Panel | Contents |
|-------|----------|
| Left | Per-cosmos insight count + type bar + latest insight |
| Center | All quantum signal cards (see below) |
| Right | Full insight timeline (newest first, color-coded by type) |
| Bottom | Mermaid graph — cosmos nodes + resonance/decoherence edges, live |

**Signal cards (center panel):**

| Signal | Description |
|--------|-------------|
| 🌡️ BEC | Banner when all decisions converge completely |
| 🔗 Entanglement Quality | Heartbeat ACK ratio for strict-mode runs |
| ⚡ Resonance | Conclusions 2+ cosmos reached independently |
| 🌀 Uncertainty | Decisions where cosmos diverged — your tradeoff |
| ⚠️ Decoherence | Cosmos pairs that lost strategic identity |
| ⚛️ Tunneling | Solutions that bypassed assumed constraints |
| ⚡ Jumps | Discontinuous leaps from a single entanglement read |
| 🚧 Blockers | Unresolved blockers needing attention |
| ⚛️ Code-Scale | `/cosmos scan` output (tunnel·decoherence·superposition·jump) |

Manual start: `node tools/dashboard.js`

---

```

- [ ] **Step 3: Commit**

```bash
git add README.ko.md README.md
git commit -m "docs: add live dashboard section with full signal coverage"
```
