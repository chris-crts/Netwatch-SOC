const BASE_URL = "http://device_ip:8000";
const WS_URL = "ws://device_ip:8000/ws/soc/";
const TOKEN_STORAGE_KEY = "soc_device_token";

let socket = null;
let reconnectDelay = 1000;

function getToken() {
  return localStorage.getItem(TOKEN_STORAGE_KEY) || "";
}

function authHeaders(extra) {
  const headers = Object.assign({}, extra || {});
  const token = getToken();
  if (token) {
    headers["X-Device-Token"] = token;
  }
  return headers;
}

function setConnectionStatus(state) {
  const el = document.getElementById("connectionStatus");
  el.classList.remove("status-pill--ok", "status-pill--pending", "status-pill--down");
  if (state === "ok") {
    el.textContent = "Live";
    el.classList.add("status-pill--ok");
  } else if (state === "down") {
    el.textContent = "Disconnected";
    el.classList.add("status-pill--down");
  } else {
    el.textContent = "Connecting";
    el.classList.add("status-pill--pending");
  }
}

function connectSocket() {
  socket = new WebSocket(WS_URL);

  socket.onopen = () => {
    setConnectionStatus("ok");
    reconnectDelay = 1000;
  };

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    pushLiveEntry(data);
  };

  socket.onclose = () => {
    setConnectionStatus("down");
    setTimeout(connectSocket, reconnectDelay);
    reconnectDelay = Math.min(reconnectDelay * 2, 15000);
  };

  socket.onerror = () => {
    socket.close();
  };
}

function pushLiveEntry(data) {
  const log = document.getElementById("live");
  const entry = document.createElement("p");
  const time = new Date().toLocaleTimeString();

  if (data.type === "incident") {
    entry.textContent = `[${time}] ${data.severity} ${data.incident_type} from ${data.ip_address}`;
  } else if (data.type === "event") {
    entry.textContent = `[${time}] ${data.action} on ${data.service} from ${data.ip_address}`;
  } else if (data.message) {
    entry.textContent = `[${time}] ${data.message}`;
  } else {
    entry.textContent = `[${time}] ${JSON.stringify(data)}`;
  }

  log.appendChild(entry);
  while (log.children.length > 50) {
    log.removeChild(log.firstChild);
  }
}

async function fetchData(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

function renderRows(tbodyId, items, rowBuilder, emptyLabel) {
  const tbody = document.getElementById(tbodyId);
  if (!items || items.length === 0) {
    tbody.innerHTML = `<tr><td colspan="6" class="empty-state">${emptyLabel}</td></tr>`;
    return;
  }
  tbody.innerHTML = items.map(rowBuilder).join("");
}

async function loadDevices() {
  const data = await fetchData(`${BASE_URL}/api/devices/`);
  const items = data.results || data;
  renderRows("devices", items, (d) => `
    <tr>
      <td>${d.name}</td>
      <td>${d.ip_address}</td>
      <td><span class="tag ${d.is_active ? 'tag--ok' : 'tag--block'}">${d.is_active ? 'Active' : 'Inactive'}</span></td>
    </tr>
  `, "No devices registered");
  document.getElementById("statActiveDevices").textContent = items.filter(d => d.is_active).length;
}

async function loadEvents() {
  const data = await fetchData(`${BASE_URL}/api/events/`);
  const items = data.results || data;
  renderRows("events", items, (e) => `
    <tr>
      <td>${e.ip_address}</td>
      <td>${e.action}</td>
      <td>${e.service}</td>
      <td>${new Date(e.timestamp).toLocaleTimeString()}</td>
    </tr>
  `, "No network events yet");
}

async function loadIncidents() {
  const data = await fetchData(`${BASE_URL}/api/incidents/`);
  const items = data.results || data;
  renderRows("incidents", items, (i) => `
    <tr>
      <td><span class="tag tag--${i.severity.toLowerCase()}">${i.severity}</span></td>
      <td>${i.incident_type}</td>
      <td>${i.ip_address}</td>
    </tr>
  `, "No incidents detected");
}

async function loadFirewallRules() {
  const data = await fetchData(`${BASE_URL}/api/firewall-rules/`);
  const items = data.results || data;
  renderRows("firewall", items, (f) => `
    <tr>
      <td>${f.ip_address}</td>
      <td><span class="tag tag--${f.action.toLowerCase()}">${f.action}</span></td>
      <td>${f.reason || "-"}</td>
    </tr>
  `, "No firewall rules configured");
}

async function loadTrafficLog() {
  const data = await fetchData(`${BASE_URL}/api/traffic-logs/`);
  const items = data.results || data;
  renderRows("traffic", items, (t) => `
    <tr>
      <td>${t.ip_address}</td>
      <td>${t.method}</td>
      <td>${t.path}</td>
      <td><span class="tag ${t.blocked ? 'tag--block' : 'tag--allow'}">${t.blocked ? 'Blocked' : 'Allowed'}</span></td>
      <td>${new Date(t.timestamp).toLocaleTimeString()}</td>
    </tr>
  `, "No traffic recorded");
}

async function loadLanStatus() {
  const data = await fetchData(`${BASE_URL}/api/lan-status/`);
  document.getElementById("statEvents").textContent = data.total_events;
  document.getElementById("statIncidents").textContent = data.total_incidents;
  document.getElementById("statBlocked").textContent = data.blocked_ips;
}

function drawChart(brute, scan) {
  const canvas = document.getElementById("chart");
  const ctx = canvas.getContext("2d");
  const width = canvas.width;
  const height = canvas.height;
  ctx.clearRect(0, 0, width, height);

  const max = Math.max(brute, scan, 1);
  const barWidth = 70;
  const gap = 60;
  const baseY = height - 30;
  const scale = (height - 60) / max;

  const bruteHeight = brute * scale;
  const scanHeight = scan * scale;

  ctx.fillStyle = "#ef4444";
  ctx.fillRect(40, baseY - bruteHeight, barWidth, bruteHeight);

  ctx.fillStyle = "#f5a623";
  ctx.fillRect(40 + barWidth + gap, baseY - scanHeight, barWidth, scanHeight);

  ctx.fillStyle = "#7d8b99";
  ctx.font = "11px 'IBM Plex Mono'";
  ctx.fillText(String(brute), 40 + barWidth / 2 - 6, baseY - bruteHeight - 8);
  ctx.fillText(String(scan), 40 + barWidth + gap + barWidth / 2 - 6, baseY - scanHeight - 8);
  ctx.fillText("Brute force", 20, height - 10);
  ctx.fillText("Port scan", 40 + barWidth + gap - 10, height - 10);
}

async function loadChart() {
  const data = await fetchData(`${BASE_URL}/api/stats/`);
  drawChart(data.BRUTE_FORCE, data.PORT_SCAN);
  document.getElementById("chartLegend").innerHTML = `
    <span><span class="legend-dot" style="background:#ef4444"></span>Brute force: ${data.BRUTE_FORCE}</span>
    <span><span class="legend-dot" style="background:#f5a623"></span>Port scan: ${data.PORT_SCAN}</span>
  `;
}

async function refreshAll() {
  try {
    await Promise.all([
      loadDevices(),
      loadEvents(),
      loadIncidents(),
      loadFirewallRules(),
      loadTrafficLog(),
      loadLanStatus(),
      loadChart(),
    ]);
  } catch (err) {
    document.getElementById("toolbarMessage").textContent = "Unable to reach backend";
  }
}

async function simulate() {
  const messageEl = document.getElementById("toolbarMessage");
  try {
    const res = await fetch(`${BASE_URL}/api/simulate/`, {
      method: "POST",
      headers: authHeaders(),
    });
    if (res.status === 401 || res.status === 403) {
      messageEl.textContent = "Device token required to simulate an attack";
      return;
    }
    messageEl.textContent = "Attack simulation triggered";
    setTimeout(() => refreshAll(), 500);
  } catch (err) {
    messageEl.textContent = "Simulation failed";
  }
}

document.getElementById("simulateBtn").addEventListener("click", simulate);

document.getElementById("saveTokenBtn").addEventListener("click", () => {
  const value = document.getElementById("deviceToken").value.trim();
  if (value) {
    localStorage.setItem(TOKEN_STORAGE_KEY, value);
    document.getElementById("toolbarMessage").textContent = "Device token saved";
  }
});

document.getElementById("deviceToken").value = getToken();

connectSocket();
refreshAll();
setInterval(refreshAll, 3000);