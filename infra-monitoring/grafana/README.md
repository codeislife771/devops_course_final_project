# Grafana

This folder contains Grafana provisioning and dashboards.

## Files
- **provisioning/** – Pre-configured data sources and dashboard definitions.  
- **dashboards/** – JSON files with dashboards that Grafana loads on startup.  

## How to Run
Run Grafana container:
docker stop grafana 2>/dev/null && docker rm grafana 2>/dev/null
docker run -d \
  --name grafana \
  --network monitor \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_USER=admin \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -v "$PWD/grafana/provisioning:/etc/grafana/provisioning:ro" \
  -v "$PWD/grafana/dashboards:/var/lib/grafana/dashboards:ro" \
  grafana/grafana

## Access the UI
Open http://localhost:3000 in your browser.  
Default login → `admin / admin`

## Notes
- Dashboards placed in the `dashboards/` folder are automatically provisioned.  
- You can add new JSON dashboard files and restart Grafana to load them.
