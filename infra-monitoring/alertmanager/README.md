# Alertmanager

This folder contains Alertmanager configuration.

## File
- **alertmanager.yml** – Main configuration file for Alertmanager.  
  - By default, it contains placeholder SMTP settings.  
  - You can leave them as-is and only use the Alertmanager web UI to view alerts.  
  - To enable email notifications, update `smtp_from`, `smtp_auth_username`, and `smtp_auth_password` with valid credentials.

## How to Run
Run Alertmanager container:
docker stop alertmanager 2>/dev/null && docker rm alertmanager 2>/dev/null
docker run -d \
  --name alertmanager \
  --network monitor \
  -p 9093:9093 \
  -v "$PWD/alertmanager:/etc/alertmanager:ro" \
  prom/alertmanager

## Access the UI
Open http://localhost:9093 in your browser.  
You will see alerts sent from Prometheus in this interface.  

## Notes
- If you configure email (Gmail or another SMTP server), alerts will also be delivered to your inbox.  
- Without SMTP configured, all alerts remain visible in the Alertmanager UI only.
