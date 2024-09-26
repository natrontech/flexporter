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

The following metrics are exported:

```shell
# HELP flexporter_vm_count Number of VMs
# TYPE flexporter_vm_count gauge
flexporter_vm_count{pool="pool_name}
# HELP flexporter_vm_cpu_cores CPU cores
# TYPE flexporter_vm_cpu_cores gauge
flexporter_vm_cpu_cores{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_vcpus VM vCPUs
# TYPE flexporter_vm_vcpus gauge
flexporter_vm_vcpus{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_memory_gb VM memory in GB
# TYPE flexporter_vm_memory_gb gauge
flexporter_vm_memory_gb{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_total_disk_gb VM disk in GB
# TYPE flexporter_vm_total_disk_gb gauge
flexporter_vm_total_disk_gb{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_total_backup_gb VM backup in GB
# TYPE flexporter_vm_total_backup_gb gauge
flexporter_vm_total_backup_gb{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_running VM running status
# TYPE flexporter_vm_running gauge
flexporter_vm_running{id="vm_id",name="vm_name",pool="pool_name"}
# HELP flexporter_vm_info VM info
# TYPE flexporter_vm_info gauge
flexporter_vm_info{id="vm_id",name="vm_name",pool="pool_name",ip="vm_ip",os_type="vm_os_type",tags="vm_tags"}
```

## Extending the Exporter

To add new metrics:
1. Update the `MetricsCollector` class in `src/metrics_collector.py`.
2. Add new Gauge metrics in the `PrometheusExporter` class in `src/prometheus_exporter.py`.
3. Update the `update_metrics` method in `src/prometheus_exporter.py` to set the new metrics.
