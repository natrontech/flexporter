from prometheus_client import Gauge, start_http_server

from .metrics_collector import MetricsCollector


class PrometheusExporter:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.gauges = {
            "vm_count": Gauge("flexporter_vm_count", "Number of VMs", ["pool"]),
            "vm_cpu_cores": Gauge(
                "flexporter_vm_cpu_cores", 
                "CPU cores", 
                ["pool", "id", "name"],
            ),
            "vm_vcpus": Gauge(
                "flexporter_vm_vcpus", 
                "VM vCPUs", 
                ["pool", "id", "name"],
            ),
            "vm_memory_gb": Gauge(
                "flexporter_vm_memory_gb",
                "VM memory in GB",
                ["pool", "id", "name"],
            ),
            "vm_storage_gb": Gauge(
                "flexporter_vm_storage_gb",
                "VM storage in GB",
                ["pool", "id", "name"],
            ),
            "vm_backup_storage_gb": Gauge(
                "flexporter_vm_backup_storage_gb",
                "VM backup storage in GB",
                ["pool", "id", "name"],
            ),
            "vm_running": Gauge(
                "flexporter_vm_running",
                "VM running status",
                ["pool", "id", "name"],
            ),
            "vm_info": Gauge(
                "flexporter_vm_info",
                "VM info",
                ["pool", "id", "name", "ip", "os_type", "tags"],
            ),
        }

    def update_metrics(self):
        metrics = self.metrics_collector.collect_metrics()
        for pool in metrics:
            pool_name = pool["name"]
            vms = pool["virtual_machines"]

            self.gauges["vm_count"].labels(pool=pool_name).set(len(vms))

            for vm in vms:
                vm_id = str(vm["id"])
                vm_name = vm["name"]

                self.gauges["vm_cpu_cores"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(vm["cpu_cores"])
                self.gauges["vm_vcpus"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(vm["vcpus"])
                self.gauges["vm_memory_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(vm["memory_gb"])
                self.gauges["vm_storage_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(vm["storage_gb"])
                self.gauges["vm_backup_storage_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(vm["backup_storage_gb"])
                self.gauges["vm_running"].labels(
                    pool=pool_name, id=vm_id, name=vm_name,
                ).set(1 if vm["status"] == "running" else 0)
                self.gauges["vm_info"].labels(
                    pool=pool_name,
                    id=vm_id,
                    name=vm_name,
                    ip=vm["ip"],
                    os_type=vm["os_type"],
                    tags=",".join(vm["tags"]),
                ).set(1)

    def run(self, port=8000):
        start_http_server(port)
        print(f"Prometheus exporter running on port {port}")
        while True:
            self.update_metrics()
