#!/usr/bin/env bash
set -euo pipefail
docker stop grafana alertmanager prometheus blackbox-exporter node-exporter 2>/dev/null || true
docker rm   grafana alertmanager prometheus blackbox-exporter node-exporter 2>/dev/null || true
echo ">> Stopped & removed monitoring containers."
