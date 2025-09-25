# Infra Monitoring Stack

This folder (`infra-monitoring/`) contains a complete monitoring stack for the DevOps project.  
It provides metrics collection, alerting, and dashboards for your application and host system.  

The stack includes:
- **Prometheus** → metrics collection and alert rules.  
- **Alertmanager** → alert routing (UI + optional email).  
- **Grafana** → dashboards and visualization.  
- **Blackbox Exporter** → external HTTP probing of your app.  
- **Node Exporter** → host-level metrics (CPU, memory, disk, network).  

## Prerequisites
- Linux VM (tested on Ubuntu).  
- Docker installed and running.  
- No need for Docker Compose — everything runs with simple `docker run`.  

## How to Start
From project root:
cd infra-monitoring
./start_monitoring.sh

To check status:
./status_monitoring.sh

To stop and clean up:
./stop_monitoring.sh

## Access the Services
- Prometheus → http://localhost:9090  
- Alertmanager → http://localhost:9093  
- Grafana → http://localhost:3000 (login: admin / admin)  

## Alerts
- Main production alerts are defined in: `prometheus/rules/alerts.yml`.  
  These include CPU, memory, disk, node down, and blackbox checks.  
- Test alerts for demo are provided in: `prometheus/rules/test-alert.sample.yml`.  
  By default, Prometheus only loads files ending in `.yml`.  
  That’s why the test alert is stored as `.sample.yml` so it is not loaded automatically.  

To enable the test alert:
cd infra-monitoring/prometheus/rules
cp test-alert.sample.yml test-alert.yml
docker restart prometheus

To disable the test alert:
cd infra-monitoring/prometheus/rules
rm -f test-alert.yml
docker restart prometheus

## Notes
- Grafana automatically provisions dashboards from `grafana/dashboards/`.  
- Alertmanager uses placeholders for SMTP by default, so alerts are visible in the UI even without email configuration.  
- For detailed instructions, see the `README.md` files inside each folder:  
  - `prometheus/` → Prometheus config and rules  
  - `grafana/` → Dashboards and provisioning  
  - `alertmanager/` → Alertmanager configuration  
