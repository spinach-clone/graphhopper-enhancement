#Team IntelleX
#Members:
# Diano, Francis Miguel
# Ejares, Allyssa Faith
# Espina, Christo Rey
# Roamar, Kaycee


import webview
import requests
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY")

# BUG FIX: Warn early if API key is missing instead of getting a cryptic error later
if not api_key:
    print("[ERROR] API_KEY not found in .env file. Please check your .env setup.")

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
        --bg:        #f0eff4;
        --shell:     #ffffff;
        --left-bg:   #f7f6fb;
        --right-bg:  #ffffff;
        --accent:    #7c5cbf;
        --accent2:   #a98ddf;
        --text:      #1a1a2e;
        --subtext:   #7a7a9a;
        --border:    #e4e2ee;
        --card:      #ffffff;
        --input-bg:  #f4f2fa;
        --shadow:    0 2px 16px rgba(100,80,180,0.08);
        --btn-track: #f4f2fa;
        --btn-track-t: #1a1a2e;
    }

    body.dark {
        --bg:        #13111f;
        --shell:     #1e1b30;
        --left-bg:   #181628;
        --right-bg:  #1e1b30;
        --accent:    #9c8dec;
        --accent2:   #c9c1f0;
        --text:      #e8e6f5;
        --subtext:   #8884aa;
        --border:    #2e2a45;
        --card:      #252240;
        --input-bg:  #2a2640;
        --shadow:    0 2px 16px rgba(0,0,0,0.35);
        --btn-track: #2a2640;
        --btn-track-t: #e8e6f5;
    }

    body {
        font-family: 'DM Sans', sans-serif;
        background: var(--bg);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 24px;
        transition: background 0.3s;
    }

    .shell {
        width: 100%;
        max-width: 1100px;
        background: var(--shell);
        border-radius: 18px;
        box-shadow: var(--shadow);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        min-height: 640px;
        transition: background 0.3s;
    }

    /* ── Top nav bar ── */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 22px;
        border-bottom: 1px solid var(--border);
        background: var(--shell);
        transition: background 0.3s, border-color 0.3s;
        z-index: 10;
    }

    .topbar-left {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.82em;
        color: var(--subtext);
    }

    .logo {
        font-size: 1.25em;
        font-weight: 600;
        color: var(--accent);
        letter-spacing: -0.5px;
        margin-right: 6px;
    }

    .breadcrumb-sep { opacity: 0.4; }
    .topbar-left span.active { color: var(--text); font-weight: 500; }

    .ham { display:flex; flex-direction:column; gap:4px; cursor:pointer; padding:4px; }
    .ham span { width:18px; height:2px; background:var(--text); border-radius:2px; transition: background 0.3s; }

    .toggle-wrap { display:flex; align-items:center; gap:8px; font-size:0.78em; color:var(--subtext); cursor:pointer; }
    .toggle-switch { position:relative; width:34px; height:18px; }
    .toggle-switch input { display:none; }
    .tog-slider { position:absolute; inset:0; background:#ccc; border-radius:18px; transition:0.3s; }
    .tog-slider:before { content:""; position:absolute; width:12px; height:12px; left:3px; bottom:3px; background:#fff; border-radius:50%; transition:0.3s; }
    input:checked + .tog-slider { background: var(--accent); }
    input:checked + .tog-slider:before { transform: translateX(16px); }

    .main { display: flex; flex: 1; min-height: 580px; }

    .left-panel {
        flex: 1.15;
        background: var(--left-bg);
        display: flex;
        flex-direction: column;
        padding: 20px 20px 16px;
        border-right: 1px solid var(--border);
        transition: background 0.3s, border-color 0.3s;
        min-width: 0;
    }

    .route-header { margin-bottom: 12px; }

    .route-title {
        font-size: 1.45em;
        font-weight: 600;
        color: var(--text);
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }

    .status-badge {
        display: none;
        font-size: 0.4em;
        font-weight: 500;
        padding: 3px 10px;
        border-radius: 20px;
        background: #e6f9ee;
        color: #27ae60;
    }

    body.dark .status-badge { background: #1a3a28; color: #5dca8a; }
    .route-sub { font-size: 0.78em; color: var(--subtext); margin-top: 4px; }

    .form-section { margin-bottom: 12px; }

    .form-row { display: flex; gap: 8px; align-items: center; }

    .form-row input, .form-row select {
        flex: 1;
        padding: 9px 12px;
        border: 1px solid var(--border);
        border-radius: 8px;
        background: var(--input-bg);
        color: var(--text);
        font-family: 'DM Sans', sans-serif;
        font-size: 0.84em;
        outline: none;
        transition: border-color 0.2s, background 0.3s;
        width: auto;
        margin: 0;
    }

    .form-row input:focus { border-color: var(--accent); }

    .go-btn {
        padding: 9px 18px;
        background: var(--accent);
        color: #fff;
        border: none;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.84em;
        font-weight: 600;
        cursor: pointer;
        white-space: nowrap;
        transition: background 0.2s;
        width: auto;
        margin: 0;
    }

    .go-btn:hover { background: var(--accent2); color: var(--text); }

    .error-msg { color: #e55; font-size: 0.8em; font-weight: 500; margin-top: 5px; }

    #map {
        flex: 1;
        border-radius: 12px;
        overflow: hidden;
        min-height: 340px;
        border: 1px solid var(--border);
        z-index: 1;
    }

    .leaflet-popup-content-wrapper {
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        font-family: 'DM Sans', sans-serif;
    }
    .leaflet-popup-content { font-size: 0.85em; }

    .right-panel {
        width: 330px;
        min-width: 290px;
        background: var(--right-bg);
        display: flex;
        flex-direction: column;
        transition: background 0.3s;
    }

    .details-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 20px 12px;
        border-bottom: 1px solid var(--border);
    }

    .details-header h3 { font-size: 1em; font-weight: 600; color: var(--text); }

    .dots-btn {
        background: none; border: none; cursor: pointer;
        color: var(--subtext); font-size: 1.2em;
        padding: 2px 6px; border-radius: 4px;
        width: auto; margin: 0;
    }
    .dots-btn:hover { background: var(--input-bg); color: var(--text); }

    .route-points {
        padding: 14px 20px;
        border-bottom: 1px solid var(--border);
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .rp-row { display: flex; align-items: flex-start; gap: 10px; }

    .rp-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--accent);
        margin-top: 5px;
        flex-shrink: 0;
    }
    .rp-dot.dest { background: #e74c3c; }

    .rp-label { font-size: 0.7em; color: var(--subtext); margin-bottom: 1px; }
    .rp-value { font-size: 0.87em; font-weight: 500; color: var(--text); }

    .time-stats {
        display: flex;
        padding: 12px 20px;
        border-bottom: 1px solid var(--border);
    }

    .ts-item { flex: 1; display: flex; flex-direction: column; gap: 2px; }
    .ts-item + .ts-item { border-left: 1px solid var(--border); padding-left: 12px; }
    .ts-label { font-size: 0.68em; color: var(--subtext); }
    .ts-value { font-size: 0.86em; font-weight: 600; color: var(--text); font-family: 'DM Mono', monospace; }

    .goods-header { padding: 12px 20px 6px; font-size: 0.88em; font-weight: 600; color: var(--text); }

    .goods-list {
        flex: 1;
        overflow-y: auto;
        padding: 0 20px 10px;
        display: flex;
        flex-direction: column;
        gap: 5px;
    }

    .goods-list::-webkit-scrollbar { width: 4px; }
    .goods-list::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

    .step-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 8px 10px;
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--card);
        transition: background 0.2s;
        cursor: default;
    }

    .step-item:hover { background: var(--input-bg); }

    .step-num-box {
        width: 32px; height: 32px;
        border-radius: 6px;
        background: var(--input-bg);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75em; font-weight: 600;
        color: var(--accent);
        font-family: 'DM Mono', monospace;
        flex-shrink: 0;
    }

    .step-info { flex: 1; min-width: 0; }
    .step-text { font-size: 0.76em; color: var(--text); line-height: 1.3; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .step-dist { font-size: 0.68em; color: var(--subtext); margin-top: 1px; }

    .step-tag {
        font-size: 0.64em; font-weight: 500;
        padding: 2px 7px; border-radius: 4px; flex-shrink: 0;
    }
    .tag-start { background: #e8f5e9; color: #27ae60; }
    .tag-end   { background: #fdecea; color: #c0392b; }
    body.dark .tag-start { background: #1a3328; color: #5dca8a; }
    body.dark .tag-end   { background: #3a1a1a; color: #e07070; }

    .empty-state {
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        flex: 1; gap: 8px;
        color: var(--subtext); font-size: 0.82em;
        text-align: center; padding: 20px;
    }
    .empty-state .ei { font-size: 2em; opacity: 0.3; }

    .fuel-section {
        border-top: 1px solid var(--border);
        padding: 12px 20px 14px;
    }

    .fuel-section h4 {
        font-size: 0.83em; font-weight: 600;
        color: var(--text); margin-bottom: 8px;
    }

    .fuel-inputs { display: flex; flex-direction: column; gap: 6px; }

    .fuel-inputs input {
        width: 100%; padding: 7px 11px;
        border: 1px solid var(--border);
        border-radius: 7px;
        background: var(--input-bg);
        color: var(--text);
        font-family: 'DM Mono', monospace;
        font-size: 0.8em; outline: none; margin: 0;
        transition: border-color 0.2s, background 0.3s;
    }

    .fuel-inputs input:focus { border-color: var(--accent); }

    .fuel-result-row {
        display: flex; align-items: center;
        justify-content: space-between;
        margin-top: 8px; padding: 8px 12px;
        background: var(--input-bg);
        border-radius: 8px; border: 1px solid var(--border);
    }
    .fr-label { font-size: 0.7em; color: var(--subtext); }
    .fr-value  { font-size: 1em; font-weight: 700; color: var(--accent); font-family: 'DM Mono', monospace; }

    .action-bar {
        display: flex; gap: 8px;
        padding: 12px 20px;
        border-top: 1px solid var(--border);
    }

    .action-btn {
        flex: 1; padding: 9px 10px;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8em; font-weight: 500;
        cursor: pointer;
        border: 1px solid var(--border);
        background: var(--btn-track);
        color: var(--btn-track-t);
        transition: all 0.2s;
        width: auto; margin: 0;
    }
    .action-btn:hover { background: var(--input-bg); }
    .action-btn.primary {
        background: var(--accent); color: #fff; border-color: var(--accent);
    }
    .action-btn.primary:hover { background: var(--accent2); color: var(--text); border-color: var(--accent2); }

    @media (max-width: 720px) {
        .main { flex-direction: column; }
        .right-panel { width: 100%; min-width: unset; }
    }
</style>
</head>
<body>
<div class="shell">

    <div class="topbar">
        <div class="topbar-left">
            <div class="ham"><span></span><span></span><span></span></div>
            <span class="logo">PRECISE</span>
            <span class="breadcrumb-sep">›</span>
            <span>Routes</span>
            <span class="breadcrumb-sep">›</span>
            <span>Navigation</span>
            <span class="breadcrumb-sep">›</span>
            <span class="active" id="breadcrumb-dest">#New Route</span>
        </div>
        <label class="toggle-wrap">
            🌗
            <div class="toggle-switch">
                <input type="checkbox" id="darkToggle" onchange="toggleDark()">
                <span class="tog-slider"></span>
            </div>
        </label>
    </div>

    <div class="main">

        <!-- LEFT PANEL -->
        <div class="left-panel">

            <div class="route-header">
                <div class="route-title">
                    Route <span id="route-id" style="color:var(--accent);">#---</span>
                    <span class="status-badge" id="status-badge">Calculated</span>
                </div>
                <div class="route-sub" id="route-sub">Enter locations below to calculate your route</div>
            </div>

            <div class="form-section">
                <div class="form-row">
                    <select id="vehicle" style="max-width:110px;">
                        <option value="car">🚗 Car</option>
                        <option value="bike">🚲 Bike</option>
                        <option value="foot">🚶 Foot</option>
                    </select>
                    <input type="text" id="start" placeholder="Starting location…">
                    <input type="text" id="dest"  placeholder="Destination…">
                    <button class="go-btn" onclick="calculateRoute()">Go →</button>
                </div>
                <div id="form-error"></div>
            </div>

            <div id="map"></div>

        </div>

        <!-- RIGHT PANEL -->
        <div class="right-panel">

            <div class="details-header">
                <h3>Details</h3>
                <button class="dots-btn">···</button>
            </div>

            <div class="route-points">
                <div class="rp-row">
                    <div class="rp-dot"></div>
                    <div>
                        <div class="rp-label">Departure</div>
                        <div class="rp-value" id="dep-value">—</div>
                    </div>
                </div>
                <div class="rp-row">
                    <div class="rp-dot dest"></div>
                    <div>
                        <div class="rp-label">Arrival</div>
                        <div class="rp-value" id="arr-value">—</div>
                    </div>
                </div>
            </div>

            <div class="time-stats">
                <div class="ts-item">
                    <div class="ts-label">Distance</div>
                    <div class="ts-value" id="stat-dist">—</div>
                </div>
                <div class="ts-item">
                    <div class="ts-label">Miles</div>
                    <div class="ts-value" id="stat-miles">—</div>
                </div>
                <div class="ts-item">
                    <div class="ts-label">Duration</div>
                    <div class="ts-value" id="stat-time">—</div>
                </div>
            </div>

            <div class="goods-header">Directions</div>
            <div class="goods-list" id="goods-list">
                <div class="empty-state">
                    <div class="ei">📍</div>
                    <div>No route calculated yet.<br>Enter locations and click Go.</div>
                </div>
            </div>

            <div class="fuel-section">
                <h4>⛽ Fuel Cost Calculator</h4>
                <div class="fuel-inputs">
                    <input type="number" id="fuel-dist"  placeholder="Distance (km) — auto-filled" min="0" oninput="calcFuel()">
                    <input type="number" id="fuel-eff"   placeholder="Fuel efficiency (km/L)" min="0.1" step="0.1" oninput="calcFuel()">
                    <input type="number" id="fuel-price" placeholder="Fuel price (per liter)" min="0" step="0.01" oninput="calcFuel()">
                </div>
                <div class="fuel-result-row">
                    <div>
                        <div class="fr-label">Estimated Fuel Cost</div>
                        <div class="fr-label" id="fuel-liters" style="margin-top:2px;"></div>
                    </div>
                    <div class="fr-value" id="fuel-cost">—</div>
                </div>
            </div>

            <div class="action-bar">
                <button class="action-btn" onclick="clearAll()">Clear Route</button>
                <button class="action-btn primary" onclick="calculateRoute()">Recalculate</button>
            </div>

        </div>
    </div>
</div>

<script>
    const map = L.map('map', { zoomControl: true }).setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    let routeLayer  = null;
    let markerStart = null;
    let markerEnd   = null;
    let routeCounter = Math.floor(Math.random() * 8000) + 1000;

    const iconStart = L.divIcon({
        className: '',
        html: `<div style="width:14px;height:14px;background:#9c8dec;border:2px solid #fff;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>`,
        iconSize: [14,14], iconAnchor: [7,7]
    });
    const iconEnd = L.divIcon({
        className: '',
        html: `<div style="width:14px;height:14px;background:#e74c3c;border:2px solid #fff;border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3);"></div>`,
        iconSize: [14,14], iconAnchor: [7,7]
    });

    function toggleDark() {
        document.body.classList.toggle('dark');
    }

    function calcFuel() {
        const dist  = parseFloat(document.getElementById('fuel-dist').value);
        const eff   = parseFloat(document.getElementById('fuel-eff').value);
        const price = parseFloat(document.getElementById('fuel-price').value);
        const costEl   = document.getElementById('fuel-cost');
        const litersEl = document.getElementById('fuel-liters');
        if (!dist || !eff || !price || eff <= 0) {
            costEl.textContent = '—'; litersEl.textContent = ''; return;
        }
        const liters = dist / eff;
        const total  = liters * price;
        costEl.textContent   = total.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
        litersEl.textContent = `⛽ ${liters.toFixed(2)} L needed`;
    }

    function decodePolyline(encoded) {
        let index = 0, lat = 0, lng = 0;
        const coords = [];
        while (index < encoded.length) {
            let b, shift = 0, result = 0;
            do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
            lat += (result & 1) ? ~(result >> 1) : (result >> 1);
            shift = 0; result = 0;
            do { b = encoded.charCodeAt(index++) - 63; result |= (b & 0x1f) << shift; shift += 5; } while (b >= 0x20);
            lng += (result & 1) ? ~(result >> 1) : (result >> 1);
            coords.push([lat / 1e5, lng / 1e5]);
        }
        return coords;
    }

    async function calculateRoute() {
        const vehicle = document.getElementById('vehicle').value;
        const start   = document.getElementById('start').value.trim();
        const dest    = document.getElementById('dest').value.trim();
        const errEl   = document.getElementById('form-error');
        errEl.innerHTML = '';

        // FIX 2: Input validation before hitting the API
        if (!start.trim() || !dest.trim()) {
            errEl.innerHTML = "<span class='error-msg'>⚠️ Please enter both a starting location and a destination.</span>";
            return;
        }
        if (start.trim().toLowerCase() === dest.trim().toLowerCase()) {
            errEl.innerHTML = "<span class='error-msg'>⚠️ Start and destination cannot be the same.</span>";
            return;
        }

        document.getElementById('goods-list').innerHTML =
            `<div class="empty-state"><div class="ei">⏳</div><div>Calculating route…</div></div>`;
        ['dep-value','arr-value','stat-dist','stat-miles','stat-time'].forEach(id =>
            document.getElementById(id).textContent = '…');

        const result = await pywebview.api.get_route(start, dest, vehicle);

        if (result.error) {
            errEl.innerHTML = `<span class='error-msg'>❌ ${result.error}</span>`;
            document.getElementById('goods-list').innerHTML =
                `<div class="empty-state"><div class="ei">❌</div><div>${result.error}</div></div>`;
            return;
        }

        lastResult = result;

        // Breadcrumb + header
        routeCounter++;
        document.getElementById('route-id').textContent        = '#' + routeCounter;
        document.getElementById('breadcrumb-dest').textContent = '#' + routeCounter;
        document.getElementById('status-badge').style.display  = 'inline-block';
        document.getElementById('route-sub').textContent       = `Calculated on ${new Date().toLocaleString()}`;

        document.getElementById('dep-value').textContent  = result.origin;
        document.getElementById('arr-value').textContent  = result.destination;
        document.getElementById('stat-dist').textContent  = result.km + ' km';
        document.getElementById('stat-miles').textContent = result.miles + ' mi';
        document.getElementById('stat-time').textContent  = result.time;

        // Directions list with color-coded turns — Roamar feature
        const list = document.getElementById('goods-list');
        list.innerHTML = '';
        result.instructions.forEach((step, i) => {
            const parts   = step.split(' (');
            const text    = parts[0];
            const dist    = parts[1] ? parts[1].replace(')', '') : '';
            const isFirst = i === 0;
            const isLast  = i === result.instructions.length - 1;
            const tag = isFirst ? "<span class='step-tag tag-start'>Start</span>"
                      : isLast  ? "<span class='step-tag tag-end'>Arrive</span>" : '';
            const s = text.toLowerCase();
            const turnClass = s.includes('arrive') ? 'turn-arrive'
                            : s.includes('left')   ? 'turn-left'
                            : s.includes('right')  ? 'turn-right'
                            : 'turn-other';
            list.innerHTML += `
                <div class="step-item ${turnClass}">
                    <div class="step-num-box">${String(i+1).padStart(2,'0')}</div>
                    <div class="step-info">
                        <div class="step-text" title="${text}">${text}</div>
                        ${dist ? `<div class="step-dist">${dist}</div>` : ''}
                    </div>
                    ${tag}
                </div>`;
        });

        document.getElementById('fuel-dist').value = result.km;
        calcFuel();

        if (routeLayer)  { map.removeLayer(routeLayer);  routeLayer = null; }
        if (markerStart) { map.removeLayer(markerStart); markerStart = null; }
        if (markerEnd)   { map.removeLayer(markerEnd);   markerEnd = null; }

        if (result.encoded_points) {
            const points = decodePolyline(result.encoded_points);
            routeLayer = L.polyline(points, { color: '#9c8dec', weight: 4, opacity: 0.85, lineJoin: 'round' }).addTo(map);
            map.fitBounds(routeLayer.getBounds(), { padding: [30, 30] });
        }

        if (result.start_lat) {
            markerStart = L.marker([result.start_lat, result.start_lng], { icon: iconStart })
                .addTo(map).bindPopup(`<b>📍 Start</b><br>${result.origin}`);
            markerEnd   = L.marker([result.end_lat, result.end_lng], { icon: iconEnd })
                .addTo(map).bindPopup(`<b>🏁 Destination</b><br>${result.destination}`);
        }
        return coords;
    }

    function clearAll() {
        document.getElementById('start').value = '';
        document.getElementById('dest').value  = '';
        document.getElementById('fuel-dist').value  = '';
        document.getElementById('fuel-eff').value   = '';
        document.getElementById('fuel-price').value = '';
        document.getElementById('fuel-cost').textContent   = '—';
        document.getElementById('fuel-liters').textContent = '';
        document.getElementById('dep-value').textContent   = '—';
        document.getElementById('arr-value').textContent   = '—';
        document.getElementById('stat-dist').textContent   = '—';
        document.getElementById('stat-miles').textContent  = '—';
        document.getElementById('stat-time').textContent   = '—';
        document.getElementById('status-badge').style.display = 'none';
        document.getElementById('route-id').textContent    = '#---';
        document.getElementById('breadcrumb-dest').textContent = '#New Route';
        document.getElementById('route-sub').textContent   = 'Enter locations below to calculate your route';
        document.getElementById('form-error').innerHTML    = '';
        document.getElementById('goods-list').innerHTML    =
            `<div class="empty-state"><div class="ei">📍</div><div>No route calculated yet.<br>Enter locations and click Go.</div></div>`;
        if (routeLayer)  { map.removeLayer(routeLayer);  routeLayer = null; }
        if (markerStart) { map.removeLayer(markerStart); markerStart = null; }
        if (markerEnd)   { map.removeLayer(markerEnd);   markerEnd = null; }
        map.setView([20, 0], 2);
        lastResult = null;
    }
</script>
</body>
</html>
"""


class ApiBridge:
    def __init__(self):
        self.route_url   = "https://graphhopper.com/api/1/route?"
        self.geocode_url = "https://graphhopper.com/api/1/geocode?"

    def _get_geocode(self, location):
        # FIX 3: Guard against missing API key
        if not api_key:
            return None

        url = self.geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": api_key})

        # FIX 1: Added try/except + timeout=10 to prevent crash/hang
        try:
            response = requests.get(url, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get("hits"):
                hit = data["hits"][0]
                return {
                    "lat": hit["point"]["lat"],
                    "lng": hit["point"]["lng"],
                    "name": hit.get("name", location)
                }
        except requests.exceptions.Timeout:
            print(f"[ERROR] Geocode request timed out for: {location}")
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Geocode request failed: {e}")

        return None

    def get_route(self, start_loc, dest_loc, vehicle):
        try:
            if not api_key:
                return {"error": "API key is missing. Please check your .env file."}

            origin = self._get_geocode(start_loc)
            dest   = self._get_geocode(dest_loc)

            if not origin:
                return {"error": f"Could not find starting location: '{start_loc}'"}
            if not dest:
                return {"error": f"Could not find destination: '{dest_loc}'"}

            # 3. Get Route
            params = {
                "key": api_key,
                "vehicle": vehicle,
                "point": [f"{origin['lat']},{origin['lng']}", f"{dest['lat']},{dest['lng']}"],
                "points_encoded": "true"
            }

            route_res  = requests.get(self.route_url, params=params, timeout=10)
            route_data = route_res.json()

            if route_res.status_code != 200:
                return {"error": route_data.get("message", "Routing failed. Check your API key or locations.")}

            path    = route_data["paths"][0]
            dist_km = path["distance"] / 1000

            # Format time
            total_ms = path["time"]
            seconds  = int((total_ms / 1000) % 60)
            minutes  = int((total_ms / (1000 * 60)) % 60)
            hours    = int((total_ms / (1000 * 60 * 60)))

            instructions = [f"{i['text']} ({i['distance'] / 1000:.1f} km)" for i in path["instructions"]]

            return {
                "origin":         origin["name"],
                "destination":    dest["name"],
                "km":             round(dist_km, 1),
                "miles":          round(dist_km / 1.61, 1),
                "time":           f"{hours:02d}:{minutes:02d}:{seconds:02d}",
                "instructions":   instructions,
                "encoded_points": path["points"],
                "start_lat":      origin["lat"],
                "start_lng":      origin["lng"],
                "end_lat":        dest["lat"],
                "end_lng":        dest["lng"],
            }

        except Exception as e:
            return {"error": str(e)}


if __name__ == "__main__":
    bridge = ApiBridge()
    window = webview.create_window(
        'PRECISE: An Enhanced Map Navigation System with Graphhopper',
        html=HTML_INTERFACE,
        js_api=bridge,
        width=1120,
        height=700
    )
    webview.start()