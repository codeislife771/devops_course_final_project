# Prometheus Rules

This folder contains Prometheus alerting rules.

## Files
- **alerts.yml** – Main infrastructure alerts (CPU, memory, disk, node down, blackbox checks, etc.).
- **test-alert.sample.yml** – A *sample* test alert you can enable to verify the alerting pipeline (Prometheus → Alertmanager → Grafana).

## How Alerts Work
- By default, `alerts.yml` is always loaded by Prometheus.
- The test file (`test-alert.sample.yml`) is **not active** unless you copy it or rename it to `test-alert.yml`.
- This ensures monitoring runs without firing test alerts on startup.

## How to Enable Test Alerts
To test the alerting pipeline, run:
cd infra-monitoring/prometheus/rules
cp test-alert.sample.yml test-alert.yml
docker restart prometheus
Now Prometheus will load the test alert, and you should see it in the Alerts tab at: http://localhost:9090/alerts

## How to Disable Test Alerts
To disable the test, run:
cd infra-monitoring/prometheus/rules
rm -f test-alert.yml
docker restart prometheus
After restart, the test alert disappears, and you are back to normal monitoring.
