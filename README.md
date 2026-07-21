Project Overview

The Netwatch SOC System is a LAN‑based security and monitoring solution designed to safeguard local networks and connected
devices. It provides real‑time visibility, traffic analysis, and proactive defense against malicious activities such as unauthorized port scans, suspicious downloads, and access to harmful websites.

_____________________________________________________________________________________________________________________________

## SOC Dashboard Screenshots

!(https://raw.githubusercontent.com/chris-crts/Netwatch-SOC/main/Backend/SOC_Sys/SOC_App/screenshots/1st_dash.png)

!(https://raw.githubusercontent.com/chris-crts/Netwatch-SOC/main/Backend/SOC_Sys/SOC_App/screenshots/2nd_dash.png)

!(https://raw.githubusercontent.com/chris-crts/Netwatch-SOC/main/Backend/SOC_Sys/SOC_App/screenshots/3rd_dash.png)


_____________________________________________________________________________________________________________________________
Architecture
Core Engine: Built to run on a dedicated host (e.g., laptop or server) with a static IP inside the LAN.

Traffic Capture: Interfaces directly with the modem/router to mirror or intercept packets.

Analysis Layer: Uses deep packet inspection (DPI), IDS/IPS rules, and behavioral analytics to detect anomalies.

Device Registry: Automatically discovers and tracks all devices connected to the LAN.

Dashboard: Web‑based interface for administrators to view logs, alerts, and device activity.

_____________________________________________________________________________________________________________________________

🔑 Features
Device Discovery: Identifies all endpoints connected to the LAN.

Traffic Monitoring: Tracks websites visited, files downloaded, and services accessed.

Malicious Activity Detection: Flags Nmap scans, suspicious connections, and malware‑like behavior.

Firewall Integration: Blocks harmful traffic and enforces access control policies.

Scalability: Supports multiple clients and servers within the LAN.

Manageability: Provides configuration options via web UI or CLI.

_____________________________________________________________________________________________________________________________

🎯 Purposes & Uses
Network Security: Protects against intrusions, scans, and malware downloads.

Compliance: Ensures devices adhere to organizational security policies.

Visibility: Gives administrators full awareness of network activity.

Incident Response: Logs and alerts suspicious behavior for rapid action.

_____________________________________________________________________________________________________________________________

🔌 Connecting to Modem/Router
Assign a static IP to the SOC host (e.g., 192.168.1.50).

Keep the default gateway as the router’s IP (e.g., 192.168.1.1).

Configure port mirroring or run the SOC inline to capture all traffic.

Launch the SOC dashboard to view connected devices and their activity.

_____________________________________________________________________________________________________________________________

📡 Activity Tracking
Websites Visited: Logs DNS queries and HTTP/HTTPS requests.

Files Downloaded: Monitors traffic patterns and file transfers.

Port Scans: Detects sequential SYN requests typical of Nmap probing.

Behavioral Analysis: Flags anomalies compared to baseline device behavior.
_____________________________________________________________________________________________________________________________

🛡️ Security Enforcement
Real‑time Alerts: Notifies administrators of suspicious activity.

Blocking Rules: Prevents devices from accessing malicious domains or ports.

Audit Logs: Maintains detailed records for forensic analysis.

Continuous Monitoring: Automates scans and checks to ensure ongoing safety.

_____________________________________________________________________________________________________________________________
🚀 Getting Started
Clone the repository and install dependencies.

Configure your SOC host with a static IP.

Connect to your modem/router for traffic capture.

Launch the dashboard and begin monitoring.