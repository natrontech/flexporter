# Flexporter

A Prometheus exporter to gather consumption insights of Proxmox-based private clouds by customer.

## Environment Variables

| Variable                 | Description                    | Default            |
| ------------------------ | ------------------------------ | ------------------ |
| `PROXMOX_ENDPOINT`       | The URL of the Proxmox API     | `10.10.10.10:8006` |
| `PROXMOX_USER`           | The Proxmox username           | `root@pam`         |
| `PROXMOX_PASSWORD`       | The Proxmox password           | `password`         |
| `PROXMOX_VERIFY_SSL`     | Verify SSL certificate         | `true`             |
| `PROXMOX_BACKUP_STORAGE` | The name of the backup storage | `local`            |

## Running the Exporter

1. Set the environment variables or use the defaults.
2. Run the Docker container:

```bash
docker build -t flexporter .
docker run -p 8000:8000 flexporter
```

The exporter will be available at `http://localhost:8000`.

## Metrics

The following metrics are exported, grouped by Proxmox pool:
- Number of virtual machines
- Total CPU cores
- Total memory in GB
- Total disk size in GB
- Total backup size in GB

## Extending the Exporter

To add new metrics:
1. Update the `MetricsCollector` class in `src/metrics_collector.py`.
2. Add new Gauge metrics in the `PrometheusExporter` class in `src/prometheus_exporter.py`.
3. Update the `update_metrics` method in `src/prometheus_exporter.py` to set the new metrics.
