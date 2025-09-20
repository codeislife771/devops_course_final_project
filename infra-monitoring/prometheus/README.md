# Prometheus

Prometheus scrapes metrics and applies alerting rules.

---

## 📌 Config
- Main config: `prometheus.yml`  
- Alert rules: stored under `rules/`  
  - `alerts.yml` → main infra alerts (CPU, memory, disk, blackbox, etc.)  
  - `test-alert.sample.yaml` → example test alert (ignored by default)  

⚠️ **Note:** Prometheus loads all `*.yml` under `rules/`.  
That’s why test alerts are stored as `.sample.yaml` → they won’t be loaded unless you copy/rename them.

---

## 🚀 How to Run
```bash
docker stop prometheus 2>/dev/null && docker rm prometheus 2>/dev/null

docker run -d \
  --name prometheus \
  --network monitor \
  -p 9090:9090 \
  -v "$PWD/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro" \
  -v "$PWD/prometheus/rules:/etc/prometheus/rules:ro" \
  prom/prometheus

Access UI → http://localhost:9090
