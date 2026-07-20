const socket = new WebSocket("ws://127.0.0.1:8000/ws/soc/");
const base_url = "http://127.0.0.1:8000"

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    const log = document.getElementById("live");
    log.innerHTML += `<p>${data.message}</p>`;
};

async function fetchData(url) {
    const res = await fetch(url);
    return await res.json();
}

async function loadDevices() {
    const data = await fetchData(`${base_url}/api/devices/`);
    document.getElementById("devices").innerHTML =
        data.map(d => `<p>${d.ip_address} - ${d.name}</p>`).join("");
}

async function loadEvents() {
    const data = await fetchData(`${base_url}/api/events/`);
    document.getElementById("events").innerHTML =
        data.map(e => `<p>${e.ip_address} ${e.action}</p>`).join("");
}

async function loadIncidents() {
    const data = await fetchData(`${base_url}/api/incidents/`);
    document.getElementById("incidents").innerHTML =
        data.map(i => `<p>${i.severity} ${i.incident_type}</p>`).join("");
}

setInterval(() => {
    loadDevices();
    loadEvents();
    loadIncidents();
}, 3000);

async function loadChart() {
    const res = await fetch(`${base_url}/api/stats/`);
    const data = await res.json();

    document.getElementById("chart").innerHTML = `
        <p>Brute Force: ${data.BRUTE_FORCE}</p>
        <p>Port Scan: ${data.PORT_SCAN}</p>
    `;
}

setInterval(loadChart, 3000);
loadChart();
loadDevices();
loadEvents();
loadIncidents();