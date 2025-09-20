#!/usr/bin/env bash
set -euo pipefail

# Resolve repo-relative paths no matter where you run from
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

NET=monitor

echo ">> Ensuring docker network '$NET' exists..."
if ! docker network inspect "$NET" >/dev/null 2>&1; then
  docker network create "$NET"
  echo ">> Created network: $NET"
fi

echo ">> Starting Blackbox Exporter..."
docker stop blackbox-exporter >/dev/null 2>&1 || true
docker rm   blackbox-exporter >/dev/null 2>&1 || true
docker run -d \
  --name blackbox-exporter \
  --network "$NET" \
  --add-host=host.docker.internal:host-gateway \
  -p 9115:9115 \
  -v "$SCRIPT_DIR/blackbox/blackbox.yml:/etc/blackbox/blackbox.yml:ro" \
  prom/blackbox-exporter \
  --config.file=/etc/blackbox/blackbox.yml

echo ">> Starting Node Exporter..."
docker stop node-exporter >/dev/null 2>&1 || true
docker rm   node-exporter >/dev/null 2>&1 || true
docker run -d \
  --name node-exporter \
  --network "$NET" \
  -p 9100:9100 \
  quay.io/prometheus/node-exporter:latest

echo ">> Starting Prometheus..."
docker stop prometheus >/dev/null 2>&1 || true
docker rm   prometheus >/dev/null 2>&1 || true
docker run -d \
  --name prometheus \
  --network "$NET" \
  --add-host=host.docker.internal:host-gateway \
  -p 9090:9090 \
  -v "$SCRIPT_DIR/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  -v "$SCRIPT_DIR/prometheus/rules:/etc/prometheus/rules:ro" \
  prom/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.retention.time=15d

echo ">> Starting Alertmanager..."
docker stop alertmanager >/dev/null 2>&1 || true
docker rm   alertmanager >/dev/null 2>&1 || true
docker run -d \
  --name alertmanager \
  --network "$NET" \
  -p 9093:9093 \
  -v "$SCRIPT_DIR/alertmanager:/etc/alertmanager:ro" \
  prom/alertmanager

echo ">> Starting Grafana..."
docker stop grafana >/dev/null 2>&1 || true
docker rm   grafana >/dev/null 2>&1 || true
docker run -d \
  --name grafana \
  --network "$NET" \
  -p 3000:3000 \
  -e GF_SECURITY_ADMIN_USER=admin \
  -e GF_SECURITY_ADMIN_PASSWORD=admin \
  -v "$SCRIPT_DIR/grafana/provisioning:/etc/grafana/provisioning:ro" \
  -v "$SCRIPT_DIR/grafana/dashboards:/var/lib/grafana/dashboards:ro" \
  grafana/grafana

echo ">> All services started."
echo "   Prometheus:   http://localhost:9090"
echo "   Alertmanager: http://localhost:9093"
echo "   Grafana:      http://localhost:3000  (admin/admin)"
