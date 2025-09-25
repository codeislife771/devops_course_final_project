#!/usr/bin/env bash
set -euo pipefail
echo ">> Containers:"
docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}" | grep -E 'prometheus|grafana|alertmanager|blackbox|node-exporter' || true
echo
echo ">> Quick checks:"
echo "Prometheus   : http://localhost:9090"
echo "Alertmanager : http://localhost:9093"
echo "Grafana      : http://localhost:3000"
