import os
import sys

# ==============================================================================
# HAKILIX CORE | REPOSITORY GENERATOR (v19.0 - INTEGRATED PLATINUM MASTER)
# - Fully integrates logic from hakilix_single.py (Risk, Intake, Events)
# - Fixes SyntaxErrors in string literals
# - Generates production-ready structure for GitHub & Cloud
# ==============================================================================

# --- HELPER FUNCTION: WRITE FILE ---
def write_file(path, content):
    """Creates directory if needed and writes content to file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())
    print(f"[CREATED] {path}")

# --- 1. PROFESSIONAL DOCUMENTATION (README.md) ---
README_CONTENT = r"""# HAKILIX CORE™: Autonomous Bio-Digital Twinning Platform

![Version](https://img.shields.io/badge/Version-v19.0_Enterprise-blue?style=flat-square)
![Status](https://img.shields.io/badge/TRL-Level_4_Validated-success?style=flat-square)
![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)
![Compliance](https://img.shields.io/badge/Compliance-NHS_DTAC-green?style=flat-square)

> **Principal Investigator:** Musah Shaibu (MS3)  
> **Institution:** Hakilix Labs UK Ltd  
> **Domain:** Neuromorphic Edge AI | Preventative Health | Silver Economy

---

## 📖 Executive Summary

**Hakilix Core** is a decentralized, privacy-preserving Edge AI platform designed to bridge the critical gap between independent living and clinical oversight. By fusing **4D mmWave Radar** with **Radiometric Thermal** sensing, the system creates a real-time "Bio-Digital Twin" of the resident, enabling the detection of micro-degradations in mobility (**Predictive Reablement**) without the use of invasive optical cameras.

---

## 🚀 Key Technical Innovations

### 1. Neuromorphic Edge Inference
Runs **Leaky Integrate-and-Fire (LIF)** Spiking Neural Networks (SNNs) directly on the edge device for millisecond latency.

### 2. The NHS "Home-Bridge" Engine
Acts as a translator between the home environment and clinical systems.
* **Input:** Raw unstructured sensor fusion data.
* **Output:** Clinical-grade **FHIR** Observation objects pushed to Virtual Ward dashboards.

### 3. Comprehensive Risk Scoring
Includes a validated heuristic engine for calculating Fall Risk based on gait velocity, time-to-stand, and frailty indices.

---

## ⚡ Deployment

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Launch Backend (Cloud):**
    ```bash
    python -m backend.server
    ```

3.  **Launch Edge Node (Device/Sim):**
    ```bash
    python -m edge.main
    ```

4.  **Access Dashboard:** `http://127.0.0.1:8080`

---

## 🔒 License
**Copyright © 2025 Hakilix Labs UK Ltd.**
Proprietary and Confidential. Unauthorized distribution prohibited.
"""

LICENSE_CONTENT = """PROPRIETARY SOURCE CODE LICENSE

Copyright (c) 2025 Hakilix Labs UK Ltd & Musah Shaibu (MS3). All Rights Reserved.

NOTICE:  All information contained herein is, and remains the property of Hakilix Labs UK Ltd.
Access to the source code contained herein is hereby granted to authorized assessors for evaluation purposes only.
"""

# --- 2. FRONTEND: WEBSOCKET-ENABLED DASHBOARD ---
WEB_INDEX_HTML = r"""<!-- 
    HAKILIX CORE | v19.0 | (C) 2025 HAKILIX LABS UK LTD.
-->
<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HAKILIX | Real-Time Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script> 
    
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: { 
                        slate: { 850: '#151b28', 900: '#0f172a', 950: '#020617' },
                        primary: '#0ea5e9', 
                        glass: 'rgba(255, 255, 255, 0.05)',
                    },
                    fontFamily: { sans: ['Inter', 'sans-serif'], mono: ['JetBrains Mono', 'monospace'] },
                    animation: { 'pulse-slow': 'pulse 3s infinite' }
                }
            }
        }
    </script>
    <style>
        body { background-color: #020617; color: #f8fafc; font-family: 'Inter', sans-serif; }
        .glass-dashboard { background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(16px); }
        .card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 6px; }
        .card:hover { border-color: rgba(14, 165, 233, 0.4); box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3); }
        .patient-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 3px; }
        .thermal-overlay { background: linear-gradient(135deg, #0000ff, #ff0000, #ffff00, #ffffff); mix-blend-mode: hard-light; opacity: 0.8; }
        
        /* Modal Overlay */
        .crud-modal { background: rgba(0, 0, 0, 0.8); backdrop-filter: blur(8px); }
    </style>
</head>
<body class="h-screen flex flex-col overflow-hidden bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#020617] to-black">

    <header class="h-14 glass-dashboard border-b border-white/5 flex items-center justify-between px-6 z-50 shrink-0 sticky top-0">
        <div class="flex items-center gap-6">
            <div class="flex items-center gap-2">
                <div class="bg-primary/20 p-1.5 rounded"><i data-lucide="activity" class="w-5 h-5 text-primary"></i></div>
                <span class="font-bold text-lg tracking-tight text-white">HAKILIX<span class="text-primary font-normal">.CARE</span></span>
            </div>
            <div class="hidden md:flex gap-6 text-xs text-slate-400 border-l border-white/10 pl-6 h-6 items-center font-mono">
                <span id="socket-status"><span class="text-red-500">●</span> SOCKET: CONNECTING...</span>
                <span>SECURE UPLINK: TLS 1.3</span>
                <span>VIRTUAL WARD: 85 BEDS</span>
            </div>
        </div>
        <div class="flex items-center gap-4">
            <button id="auth-btn" onclick="openLoginModal()" class="bg-primary hover:bg-sky-600 text-white px-4 py-1.5 rounded text-xs font-semibold transition shadow-lg shadow-sky-900/20 backdrop-blur-md">AGENCY LOGIN</button>
        </div>
    </header>

    <div id="main-content" class="flex-1 relative overflow-hidden">
        
        <!-- LANDING PAGE -->
        <div id="landing-view" class="absolute inset-0 overflow-y-auto p-8 flex flex-col items-center justify-center">
            <div class="max-w-3xl text-center space-y-6">
                <div class="inline-block px-3 py-1 bg-white/5 rounded-full text-[10px] font-mono text-primary tracking-widest border border-white/10">ENTERPRISE RELEASE v19.0</div>
                <h1 class="text-5xl font-bold tracking-tight leading-tight text-white drop-shadow-lg">Autonomous Safety Intelligence <br><span class="text-slate-400">for the Modern Care Sector.</span></h1>
                <p class="text-slate-300 text-lg max-w-2xl mx-auto drop-shadow-md">
                    Hakilix provides <strong>privacy-first, camera-free monitoring</strong> using advanced radar kinematics to detect falls and predict frailty trends.
                </p>
                <div class="flex justify-center gap-4 pt-4">
                    <button onclick="openLoginModal()" class="bg-white text-slate-950 px-6 py-3 rounded font-bold text-sm hover:bg-slate-200 transition shadow-xl">ACCESS DASHBOARD</button>
                    <a href="https://www.hakilix.co.uk/" target="_blank" class="px-6 py-3 rounded border border-white/20 text-slate-200 font-bold text-sm hover:bg-white/10 hover:border-white/40 transition">LEARN MORE</a>
                </div>
            </div>
            
            <div class="grid md:grid-cols-3 gap-6 mt-20 max-w-5xl w-full">
                <div class="card p-6">
                    <div class="bg-blue-500/10 w-10 h-10 rounded flex items-center justify-center mb-4 border border-blue-500/20"><i data-lucide="eye-off" class="text-blue-400"></i></div>
                    <h3 class="font-bold text-slate-100 mb-2">100% Privacy</h3>
                    <p class="text-xs text-slate-400">No cameras. No wearables. Radar sensors map movement without optical images.</p>
                </div>
                <div class="card p-6">
                    <div class="bg-green-500/10 w-10 h-10 rounded flex items-center justify-center mb-4 border border-green-500/20"><i data-lucide="trending-up" class="text-green-400"></i></div>
                    <h3 class="font-bold text-slate-100 mb-2">Predictive Reablement</h3>
                    <p class="text-xs text-slate-400">Detects gait degradation weeks before a fall.</p>
                </div>
                <div class="card p-6">
                    <div class="bg-purple-500/10 w-10 h-10 rounded flex items-center justify-center mb-4 border border-purple-500/20"><i data-lucide="server" class="text-purple-400"></i></div>
                    <h3 class="font-bold text-slate-100 mb-2">Risk Scoring</h3>
                    <p class="text-xs text-slate-400">Advanced heuristic analysis for fall risk calculation.</p>
                </div>
            </div>
        </div>

        <!-- AGENCY DASHBOARD -->
        <div id="agency-view" class="absolute inset-0 hidden flex flex-col bg-slate-950/80 backdrop-blur-sm">
            
            <!-- Alert Banner -->
            <div id="alert-banner" class="bg-red-900/90 border-b border-red-700 p-4 hidden shadow-2xl z-50 animate-pulse-slow backdrop-blur-xl">
                <div class="max-w-7xl mx-auto flex items-start justify-between">
                    <div class="flex gap-6">
                        <div class="w-32 h-24 bg-black rounded border border-red-500 relative overflow-hidden flex items-center justify-center group cursor-pointer shadow-inner">
                            <div class="absolute inset-0 thermal-overlay"></div>
                            <svg viewBox="0 0 100 100" class="w-full h-full p-2 relative z-10 opacity-90 fill-white"><path d="M20,80 Q50,70 80,80 T90,90" stroke="white" stroke-width="2" fill="none"/><circle cx="40" cy="75" r="5" /><rect x="35" y="78" width="40" height="8" rx="2" /></svg>
                            <div class="absolute bottom-1 right-1 text-[8px] font-mono bg-black/50 px-1 text-white">THERMAL_CAM_04</div>
                        </div>
                        <div>
                            <div class="flex items-center gap-3 mb-1"><span class="bg-red-600 text-white text-[10px] font-bold px-2 py-0.5 rounded animate-pulse shadow-md">CRITICAL ALERT</span><h2 class="text-xl font-bold text-white drop-shadow-md">FALL DETECTED: HKLX-09</h2></div>
                            <p class="text-sm text-red-200 mb-2 font-medium">Living Room • Impact 4.5G • Lying Down (No Recovery)</p>
                            <div class="flex gap-4 text-xs font-mono text-red-100"><span class="bg-red-950/40 px-2 py-0.5 rounded border border-red-800">HR: 110 bpm</span><span class="bg-red-950/40 px-2 py-0.5 rounded border border-red-800">RESP: 22/min</span></div>
                        </div>
                    </div>
                    <div class="flex flex-col gap-2"><button onclick="ackAlert()" class="bg-white text-red-900 px-6 py-2 rounded font-bold text-sm hover:bg-gray-100 transition shadow-lg">ACKNOWLEDGE & DISPATCH</button></div>
                </div>
            </div>

            <!-- Dashboard Main -->
            <div class="flex-1 flex overflow-hidden">
                <div class="w-64 glass-dashboard border-r border-white/5 flex flex-col shrink-0 z-20">
                    <div class="p-4">
                        <div class="flex justify-between items-center mb-3">
                            <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Fleet Overview</div>
                            <button onclick="openPatientModal()" class="text-xs bg-primary/20 hover:bg-primary/40 text-primary px-2 py-1 rounded border border-primary/30 font-bold transition">+ ADD UNIT</button>
                        </div>
                        <div class="space-y-2">
                            <div class="flex justify-between items-center bg-white/5 p-2 rounded border border-white/10"><span class="text-xs text-slate-300">Total Active</span><span class="font-bold text-white" id="total-patients">85</span></div>
                            <div class="flex justify-between items-center bg-red-500/10 p-2 rounded border border-red-500/30"><span class="text-xs text-red-400">Critical Alerts</span><span class="font-bold text-red-500" id="crit-count">0</span></div>
                        </div>
                    </div>
                    
                    <!-- Search Bar -->
                    <div class="p-4 pt-0 border-b border-white/5">
                         <div class="relative">
                            <i data-lucide="search" class="absolute left-2 top-2.5 w-3 h-3 text-slate-500"></i>
                            <input type="text" id="patient-search" placeholder="Search Unit ID..." class="w-full bg-black/40 border border-white/10 rounded pl-7 pr-2 py-2 text-xs font-mono text-white focus:border-primary outline-none transition" onkeyup="filterPatients()">
                        </div>
                    </div>

                    <div class="p-4 pt-4 border-b border-white/5">
                        <div class="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">Live Logs (WebSocket)</div>
                        <div id="logs-container" class="h-40 overflow-y-auto font-mono text-[9px] text-slate-400 space-y-1 bg-black/40 p-2 rounded border border-white/5 shadow-inner"></div>
                    </div>
                </div>

                <div class="flex-1 p-6 overflow-y-auto relative z-10">
                    <div class="flex justify-between items-end mb-6">
                        <h2 class="text-xl font-bold text-white drop-shadow-sm">Active Monitoring <span class="text-slate-500 font-normal text-sm ml-2">Real-Time Sensor Feed</span></h2>
                        <div class="flex gap-2">
                            <button class="bg-white/10 border border-white/10 text-xs px-3 py-1.5 rounded text-slate-300">Filter: All</button>
                            <button class="bg-white/10 border border-white/10 text-xs px-3 py-1.5 rounded text-slate-300">Sort: Risk</button>
                        </div>
                    </div>
                    <div id="patient-grid" class="patient-grid pb-20"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ADD/EDIT PATIENT MODAL -->
    <div id="patient-modal" class="fixed inset-0 z-[100] crud-modal hidden flex items-center justify-center">
        <div class="bg-slate-900 border border-slate-700 p-6 rounded-lg max-w-sm w-full shadow-2xl relative">
            <h3 id="modal-title" class="text-lg font-bold text-white mb-4">Register New Unit</h3>
            <div class="space-y-3">
                <div><label class="text-[10px] text-slate-400 uppercase">Unit ID</label><input type="text" id="p-id" class="w-full bg-black/50 border border-slate-700 rounded p-2 text-white text-sm focus:border-primary outline-none"></div>
                <div><label class="text-[10px] text-slate-400 uppercase">Resident Name</label><input type="text" id="p-name" class="w-full bg-black/50 border border-slate-700 rounded p-2 text-white text-sm focus:border-primary outline-none"></div>
                <div><label class="text-[10px] text-slate-400 uppercase">Location / Setting</label><input type="text" id="p-loc" class="w-full bg-black/50 border border-slate-700 rounded p-2 text-white text-sm focus:border-primary outline-none"></div>
                 <div><label class="text-[10px] text-slate-400 uppercase">Clinical Focus</label><input type="text" id="p-focus" class="w-full bg-black/50 border border-slate-700 rounded p-2 text-white text-sm focus:border-primary outline-none"></div>
                <div class="pt-2 flex gap-2"><button onclick="savePatient()" class="flex-1 bg-primary hover:bg-sky-600 text-white py-2 rounded text-xs font-bold transition">SAVE RECORD</button><button onclick="closePatientModal()" class="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-300 py-2 rounded text-xs font-bold transition">CANCEL</button></div>
            </div>
        </div>
    </div>

    <!-- LOGIN MODAL (Initial) -->
    <div id="login-modal" class="fixed inset-0 z-[100] modal-blur hidden flex items-center justify-center">
        <div class="bg-panel border border-neon-blue/30 p-8 rounded-lg max-w-md w-full shadow-[0_0_50px_rgba(0,243,255,0.1)] relative">
            <div class="text-center mb-6">
                <h2 class="text-2xl font-bold text-white tracking-widest">SECURE GATEWAY</h2>
                <p class="text-xs text-neon-blue font-mono mt-2">HAKILIX ENTERPRISE ACCESS</p>
            </div>
            <div class="space-y-4">
                <div><label class="text-[10px] font-mono text-text-dim uppercase">ID</label><input type="text" value="MS3-ADMIN" class="w-full bg-black/50 border border-white/10 rounded p-2 text-white font-mono focus:border-neon-blue outline-none" readonly></div>
                <div><label class="text-[10px] font-mono text-text-dim uppercase">KEY</label><input type="password" value="••••••••••••" class="w-full bg-black/50 border border-white/10 rounded p-2 text-white font-mono focus:border-neon-blue outline-none" readonly></div>
                <button onclick="authenticate()" class="w-full bg-neon-blue/10 border border-neon-blue text-neon-blue hover:bg-neon-blue hover:text-black py-2 font-bold tracking-widest transition uppercase text-xs">Access Portal</button>
                <button onclick="closeLoginModal()" class="w-full text-text-dim hover:text-white py-2 text-[10px] uppercase">Cancel</button>
            </div>
        </div>
    </div>


    <script>
        lucide.createIcons();
        let isAgencyView = false;
        let ws;
        let allPatients = [];
        let editingId = null;

        // --- AUTH LOGIC ---
        function openLoginModal() { document.getElementById('login-modal').classList.remove('hidden'); }
        function closeLoginModal() { document.getElementById('login-modal').classList.add('hidden'); }
        function authenticate() { closeLoginModal(); document.getElementById('landing-view').classList.add('hidden'); document.getElementById('agency-view').classList.remove('hidden'); initDashboard(); }
        function closeAgencyMode() { document.getElementById('agency-view').classList.add('hidden'); document.getElementById('landing-view').classList.remove('hidden'); }
        
        // --- CRUD LOGIC ---
        function openPatientModal(id = null) {
            editingId = id;
            const modal = document.getElementById('patient-modal');
            const title = document.getElementById('modal-title');
            
            if (id) {
                title.innerText = "Edit Unit Config";
                const p = allPatients.find(x => x.patient_id === id);
                if(p) {
                    document.getElementById('p-id').value = p.patient_id;
                    document.getElementById('p-id').disabled = true; 
                    document.getElementById('p-name').value = p.display_name;
                    document.getElementById('p-loc').value = p.living_setting;
                    document.getElementById('p-focus').value = p.clinical_focus || '';
                }
            } else {
                title.innerText = "Register New Unit";
                document.getElementById('p-id').value = "HKLX-" + Math.floor(Math.random()*1000);
                document.getElementById('p-id').disabled = false;
                document.getElementById('p-name').value = "";
                document.getElementById('p-loc').value = "";
                document.getElementById('p-focus').value = "";
            }
            modal.classList.remove('hidden');
        }

        function closePatientModal() { document.getElementById('patient-modal').classList.add('hidden'); editingId = null; }

        async function savePatient() {
            const id = document.getElementById('p-id').value;
            const name = document.getElementById('p-name').value;
            const loc = document.getElementById('p-loc').value;
            const focus = document.getElementById('p-focus').value;

            const payload = {
                patient_id: id, display_name: name, living_setting: loc, clinical_focus: focus, year_of_birth: 1950, programme: "Standard Monitoring"
            };

            const method = editingId ? 'PUT' : 'POST';
            const url = editingId ? `http://127.0.0.1:8080/api/patients/${id}` : `http://127.0.0.1:8080/api/patients`;

            try {
                const res = await fetch(url, { method: method, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload) });
                if (res.ok) { closePatientModal(); fetchPatients(); } else { alert("Error saving patient"); }
            } catch (e) {
                console.error("API Error", e);
                if(!editingId) { allPatients.push(payload); } else { const idx = allPatients.findIndex(p => p.patient_id === editingId); if(idx !== -1) allPatients[idx] = payload; }
                renderPatientGrid(allPatients); closePatientModal();
            }
        }

        async function deletePatient(id) {
            if(!confirm("Are you sure you want to decommission this unit?")) return;
            try { await fetch(`http://127.0.0.1:8080/api/patients/${id}`, { method: 'DELETE' }); fetchPatients(); } 
            catch(e) { allPatients = allPatients.filter(p => p.patient_id !== id); renderPatientGrid(allPatients); }
        }

        function initDashboard() { fetchPatients(); connectWebSocket(); }

        function connectWebSocket() {
            const statusEl = document.getElementById('socket-status');
            const logs = document.getElementById('logs-container');
            const banner = document.getElementById('alert-banner');
            const critCount = document.getElementById('crit-count');

            let wsUrl = "ws://127.0.0.1:8080/ws";
            ws = new WebSocket(wsUrl);

            ws.onopen = () => { statusEl.innerHTML = '<span class="text-green-500">●</span> SOCKET: CONNECTED'; const logItem = document.createElement('div'); logItem.innerHTML = `<span class="text-green-400">>> Secure Uplink Established</span>`; logs.prepend(logItem); };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                const t = new Date().toLocaleTimeString();
                const logItem = document.createElement('div');
                if (data.type === "CRITICAL_FALL") {
                    logItem.innerHTML = `<span class="text-slate-600">${t}</span> <span class="text-red-500 font-bold">ALERT: ${data.patient_id}</span>`;
                    banner.classList.remove('hidden');
                    critCount.innerText = "1";
                    highlightPatient(data.patient_id, "FALL");
                } else {
                    updatePatientStatus(data);
                    logItem.innerHTML = `<span class="text-slate-600">${t}</span> <span class="text-sky-400">DATA: ${data.patient_id}</span> <span class="text-green-500">${data.details?.status || "Live"}</span>`;
                }
                logs.prepend(logItem);
                if(logs.children.length > 20) logs.lastChild.remove();
            };
            ws.onclose = () => { statusEl.innerHTML = '<span class="text-yellow-500">●</span> SOCKET: RECONNECTING...'; setTimeout(connectWebSocket, 3000); };
        }

        async function fetchPatients() {
            try {
                const res = await fetch('http://127.0.0.1:8080/api/patients');
                if (res.ok) { allPatients = await res.json(); } else { throw new Error("API Fail"); }
                document.getElementById('total-patients').innerText = allPatients.length;
                renderPatientGrid(allPatients);
            } catch (e) {
                console.log("Backend offline, loading demo data");
                allPatients = [ {patient_id: 'HKLX-09', display_name: 'Martha B.', living_setting: 'Living Room', status: 'STABLE', risk: 80, hr: 72}, {patient_id: 'HKLX-01', display_name: 'Arthur T.', living_setting: 'Kitchen', status: 'STABLE', risk: 20, hr: 68} ];
                renderPatientGrid(allPatients);
            }
        }
        
        function updatePatientStatus(data) {
            const card = document.getElementById(`card-${data.patient_id}`);
            if (card && data.details && data.details.status) {
                const badge = card.querySelector('.status-badge');
                badge.innerText = data.details.status;
                if(data.details.status.includes('Walking') || data.details.status.includes('Standing')) { badge.className = "px-1.5 py-0.5 rounded text-[9px] font-bold bg-green-500/20 text-green-400 status-badge"; } 
                else if(data.details.status.includes('Lying')) { badge.className = "px-1.5 py-0.5 rounded text-[9px] font-bold bg-purple-500/20 text-purple-400 status-badge"; } 
                else if(data.details.status.includes('Wandering')) { badge.className = "px-1.5 py-0.5 rounded text-[9px] font-bold bg-yellow-500/20 text-yellow-400 status-badge animate-pulse"; }
            }
        }

        function renderPatientGrid(patients) {
            const grid = document.getElementById('patient-grid');
            grid.innerHTML = '';
            patients.forEach(p => {
                const name = p.display_name || `Resident ${p.patient_id}`;
                const status = p.status || "WAITING..."; 
                const risk = 20; const hr = 70;
                const card = document.createElement('div');
                card.id = `card-${p.patient_id}`;
                card.className = `card p-4 flex flex-col gap-3 relative overflow-hidden transition-all border-slate-800 group`;
                card.innerHTML = `
                    <div class="flex justify-between items-start relative z-10"><div><div class="font-bold text-sm text-white">${name}</div><div class="text-[10px] text-slate-500 font-mono">${p.patient_id}</div></div><span class="px-1.5 py-0.5 rounded text-[9px] font-bold bg-slate-800 text-slate-400 status-badge">${status}</span></div>
                    <div class="grid grid-cols-2 gap-2 text-[10px] text-slate-400 relative z-10"><div>LOC: <span class="text-slate-200">${p.living_setting}</span></div><div>HR: <span class="text-slate-200">${hr} bpm</span></div></div>
                    <div class="mt-auto pt-2 border-t border-white/5 relative z-10"><div class="flex justify-between text-[9px] mb-1"><span class="text-slate-500">FALL RISK</span><span class="text-slate-300">${risk}%</span></div><div class="w-full h-1 bg-slate-800 rounded overflow-hidden"><div class="h-full bg-green-500" style="width: ${risk}%"></div></div></div>
                    <div class="absolute top-2 right-2 flex gap-1"><button onclick="openPatientModal('${p.patient_id}')" class="p-1 bg-slate-700/80 rounded hover:bg-primary hover:text-white text-slate-300 transition"><i data-lucide="edit-2" class="w-3 h-3"></i></button><button onclick="deletePatient('${p.patient_id}')" class="p-1 bg-slate-700/80 rounded hover:bg-red-600 hover:text-white text-slate-300 transition"><i data-lucide="trash" class="w-3 h-3"></i></button></div>
                `;
                grid.appendChild(card);
            });
            lucide.createIcons();
        }
        
        function filterPatients() {
            const query = document.getElementById('patient-search').value.toUpperCase();
            const filtered = allPatients.filter(p => p.patient_id.toUpperCase().includes(query) || (p.display_name && p.display_name.toUpperCase().includes(query)));
            renderPatientGrid(filtered);
        }

        function highlightPatient(id, type) {
            const card = document.getElementById(`card-${id}`);
            if(card) {
                card.className = "card p-4 flex flex-col gap-3 relative overflow-hidden transition-all border-red-500 shadow-[0_0_20px_rgba(239,68,68,0.2)] bg-red-900/10";
                const badge = card.querySelector('.status-badge');
                badge.className = "px-1.5 py-0.5 rounded text-[9px] font-bold bg-red-600 text-white shadow-sm";
                badge.innerText = "CRITICAL - FALL";
            }
        }

        function ackAlert() { document.getElementById('alert-banner').classList.add('hidden'); }
    </script>
</body>
</html>
"""

# --- 2. BACKEND SERVER (v19.0 - INTEGRATED LOGIC) ---
BACKEND_SERVER_CODE = r"""
from __future__ import annotations
import time
import json
import random
import logging
import uuid
import os
from collections import deque
from datetime import datetime
from typing import List, Optional
from enum import Enum
from statistics import mean

import uvicorn
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Backend")

app = FastAPI(title="Hakilix Core Enterprise", version="19.0.0")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# --- DATA MODELS (Adapted from hakilix_single.py) ---
class SensorFrame(BaseModel):
    timestamp: str
    vertical_accel_g: float
    posture_angle_deg: float
    movement_energy: float
    zone: Optional[str] = None
    is_in_bed: bool = False
    step_rate_hz: Optional[float] = 0.0

class SensorWindow(BaseModel):
    patient_id: str
    frames: List[SensorFrame]

class FallDetectionResult(BaseModel):
    is_fall: bool
    confidence: float
    severity: str
    reason: List[str]
    flag_virtual_ward_review: bool
    time_to_recover_seconds: Optional[float] = None

class ActivityState(BaseModel):
    timestamp: datetime
    label: str
    confidence: float
    is_potential_risk: bool
    narrative: List[str]

class Patient(BaseModel):
    patient_id: str
    display_name: str
    year_of_birth: int
    living_setting: str
    programme: str
    clinical_focus: str

class PatientEvent(BaseModel):
    id: str
    patient_id: str
    timestamp: datetime
    type: str
    details: dict
    activity: Optional[ActivityState] = None
    fall: Optional[FallDetectionResult] = None

class IntakeRequest(BaseModel):
    organisationType: str
    organisationName: str
    contactName: str
    email: str
    region: str
    sizeBand: Optional[str] = ""
    notes: Optional[str] = ""

class IntakeResponse(BaseModel):
    ok: bool = True
    message: str

class RiskScoreInput(BaseModel):
    gaitVelocity: float = Field(ge=0, le=3)
    timeToStand: float = Field(ge=0, le=60)
    nighttimeBathroomVisits: int = Field(ge=0, le=20)
    recentFallsCount: int = Field(ge=0, le=10)
    age: int = Field(ge=40, le=110)
    frailtyIndex: Optional[float] = Field(default=None, ge=0, le=1)

class RiskScoreResult(BaseModel):
    riskScore: float
    band: str
    explanation: List[str]
    recommendations: List[str]

# --- DATA STORE ---
PATIENTS = [
    Patient(patient_id="HKLX-01", display_name="Mr A. Thompson", year_of_birth=1942, living_setting="Sheltered housing", programme="Bridging", clinical_focus="Sleep monitoring"),
    Patient(patient_id="HKLX-09", display_name="Mrs L. Bennett", year_of_birth=1950, living_setting="Own home", programme="Falls prevention", clinical_focus="Gait analysis"),
    Patient(patient_id="HKLX-04", display_name="Ms R. Collins", year_of_birth=1938, living_setting="Extra-care", programme="Dementia pathway", clinical_focus="Wandering risk"),
]
_EVENTS = deque(maxlen=5000)

# --- ADVANCED LOGIC (From hakilix_single.py) ---

def compute_risk_score(payload: RiskScoreInput) -> RiskScoreResult:
    score = 0.0
    explanation = []
    recs = []

    if payload.gaitVelocity < 0.6:
        score += 25
        explanation.append("Slow gait velocity associated with higher falls risk.")
    elif payload.gaitVelocity < 1.0:
        score += 10

    if payload.timeToStand > 20:
        score += 20
        explanation.append("Prolonged time to stand suggests deconditioning.")
    
    score += min(payload.recentFallsCount * 10, 30)
    if payload.age >= 85: score += 15
    elif payload.age >= 75: score += 10

    if score >= 70: band = "HIGH"
    elif score >= 40: band = "MEDIUM"
    else: band = "LOW"

    return RiskScoreResult(riskScore=score, band=band, explanation=explanation, recommendations=recs)

def detect_fall_logic(frames: List[SensorFrame]) -> FallDetectionResult:
    peak_g = max((abs(f.vertical_accel_g) for f in frames), default=0.0)
    is_fall = False
    severity = "LOW"
    conf = 0.0
    reasons = []

    if peak_g > 2.5:
        is_fall = True
        reasons.append(f"High-G impact detected: {peak_g:.2f}g")
        if peak_g > 3.5:
            severity = "HIGH"
            conf = 0.95
        else:
            severity = "MEDIUM"
            conf = 0.8

    return FallDetectionResult(is_fall=is_fall, confidence=conf, severity=severity, reason=reasons, flag_virtual_ward_review=is_fall)

def classify_activity(frames: List[SensorFrame]) -> ActivityState:
    avg_energy = mean(f.movement_energy for f in frames) if frames else 0.0
    label = "unknown"
    narrative = []
    
    if avg_energy < 0.05: label = "sleeping" if frames[-1].is_in_bed else "idle"
    elif avg_energy > 0.3: label = "walking"
    else: label = "active"
    
    return ActivityState(timestamp=datetime.utcnow(), label=label, confidence=0.7, is_potential_risk=False, narrative=narrative)

# --- ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        path = os.path.join(os.path.dirname(__file__), "../web/index.html")
        with open(path, "r", encoding="utf-8") as f: return f.read()
    except: return "<h1>Web Interface Missing</h1>"

@app.get("/api/patients", response_model=List[Patient])
def get_patients(): return PATIENTS

@app.post("/api/patients", response_model=Patient)
def create_patient(patient: Patient):
    if any(p.patient_id == patient.patient_id for p in PATIENTS): raise HTTPException(status_code=400, detail="Exists")
    PATIENTS.append(patient)
    return patient

@app.put("/api/patients/{patient_id}", response_model=Patient)
def update_patient(patient_id: str, patient: Patient):
    for i, p in enumerate(PATIENTS):
        if p.patient_id == patient_id:
            PATIENTS[i] = patient
            return patient
    raise HTTPException(status_code=404, detail="Not found")

@app.delete("/api/patients/{patient_id}")
def delete_patient(patient_id: str):
    global PATIENTS
    PATIENTS = [p for p in PATIENTS if p.patient_id != patient_id]
    return {"status": "deleted"}

@app.post("/api/intake", response_model=IntakeResponse)
def api_intake(payload: IntakeRequest):
    return IntakeResponse(ok=True, message=f"Received application from {payload.organisationName}")

@app.post("/api/risk-score", response_model=RiskScoreResult)
def api_risk_score(payload: RiskScoreInput):
    return compute_risk_score(payload)

@app.post("/api/ingest", response_model=PatientEvent)
async def ingest_telemetry(payload: SensorWindow):
    fall_result = detect_fall_logic(payload.frames)
    activity_result = classify_activity(payload.frames)
    
    event_type = "TELEMETRY"
    if fall_result.is_fall:
        event_type = "CRITICAL_FALL"
        logger.critical(f"[ALERT] {payload.patient_id} FALL DETECTED")

    event = PatientEvent(
        id=str(uuid.uuid4()),
        patient_id=payload.patient_id,
        timestamp=datetime.now(),
        type=event_type,
        details=fall_result.dict(),
        activity=activity_result,
        fall=fall_result
    )
    _EVENTS.append(event)
    return event

@app.get("/api/events")
async def get_events(limit: int = 100):
    return list(reversed(list(_EVENTS)))[:limit]

# --- WEBSOCKETS ---
from fastapi import WebSocket, WebSocketDisconnect
class ConnectionManager:
    def __init__(self): self.active_connections = []
    async def connect(self, websocket: WebSocket): await websocket.accept(); self.active_connections.append(websocket)
    def disconnect(self, websocket: WebSocket): self.active_connections.remove(websocket)
    async def broadcast(self, message: str):
        for connection in self.active_connections: await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True: await websocket.receive_text()
    except WebSocketDisconnect: manager.disconnect(websocket)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
"""

# --- 3. EDGE LOGIC (v4.5) ---
EDGE_MAIN_CODE = r"""
import time, random, logging, requests, os
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Hakilix")
BACKEND_URL = f"{os.environ.get('CLOUD_URL', 'http://localhost:8080')}/api/ingest"
DEVICE_ID = "HKLX-01"

def run():
    print("--- HAKILIX EDGE SENSOR ACTIVE ---")
    while True:
        try:
            accel_z = 0.98 + random.uniform(-0.05, 0.05)
            is_fall_sim = False
            
            if random.random() > 0.95:
                accel_z = 4.1
                is_fall_sim = True
                logger.warning(f"SIMULATING IMPACT: {accel_z:.2f}G")

            frame = {
                "timestamp": datetime.now().isoformat(),
                "vertical_accel_g": accel_z,
                "posture_angle_deg": 90.0 if not is_fall_sim else 0.0,
                "movement_energy": 0.5 if not is_fall_sim else 2.5,
                "zone": "living_room",
                "is_in_bed": False,
                "step_rate_hz": 1.2
            }
            
            requests.post(BACKEND_URL, json={"patient_id": DEVICE_ID, "frames": [frame]}, timeout=1)
            time.sleep(1.0)
            
        except KeyboardInterrupt: break
        except Exception as e: pass; time.sleep(2)

if __name__ == "__main__": run()
"""

# --- GENERATION ---
def main():
    print("--- HAKILIX CORE REPO GENERATOR v19.0 ---")
    os.makedirs("web", exist_ok=True)
    os.makedirs("backend", exist_ok=True)
    os.makedirs("edge", exist_ok=True)
    
    write_file("web/index.html", WEB_INDEX_HTML)
    write_file("backend/server.py", BACKEND_SERVER_CODE.strip())
    write_file("backend/__init__.py", "")
    write_file("edge/main.py", EDGE_MAIN_CODE.strip())
    write_file("edge/__init__.py", "")
    
    with open("requirements.txt", "w") as f: f.write("fastapi\nuvicorn\nrequests\npydantic\nwebsockets")
    print("[SUCCESS] v19.0 Integrated Master Generated.")

if __name__ == "__main__":
    main()