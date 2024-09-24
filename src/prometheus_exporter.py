from prometheus_client import Gauge, start_http_server

from .metrics_collector import MetricsCollector


class PrometheusExporter:
    def __init__(self):
        self.metrics_collector = MetricsCollector()
        self.gauges = {
            "vm_count": Gauge("flexporter_vm_count", "Number of VMs", ["pool"]),
            "vm_cpu_cores": Gauge(
                "flexporter_vm_cpu_cores", 
                "VM CPU cores", 
                ["pool", "id", "name", "os_type", "ip", "tags", "status"],
            ),
            "vm_memory_gb": Gauge(
                "flexporter_vm_memory_gb",
                "VM memory in GB",
                ["pool", "id", "name", "os_type", "ip", "tags", "status"],
            ),
            "vm_storage_gb": Gauge(
                "flexporter_vm_storage_gb",
                "VM storage in GB",
                ["pool", "id", "name", "os_type", "ip", "tags", "status"],
            ),
            "vm_backup_storage_gb": Gauge(
                "flexporter_vm_backup_storage_gb",
                "VM backup storage in GB",
                ["pool", "id", "name", "os_type", "ip", "tags", "status"],
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
                    pool=pool_name, id=vm_id, name=vm_name, os_type=vm["os_type"], ip=vm["ip"], tags=vm["tags"], status=vm["status"],
                ).set(vm["cpu_cores"])
                self.gauges["vm_memory_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name, os_type=vm["os_type"], ip=vm["ip"], tags=vm["tags"], status=vm["status"],
                ).set(vm["memory_gb"])
                self.gauges["vm_storage_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name, os_type=vm["os_type"], ip=vm["ip"], tags=vm["tags"], status=vm["status"],
                ).set(vm["storage_gb"])
                self.gauges["vm_backup_storage_gb"].labels(
                    pool=pool_name, id=vm_id, name=vm_name, os_type=vm["os_type"], ip=vm["ip"], tags=vm["tags"], status=vm["status"],
                ).set(vm["backup_storage_gb"])
                

    def run(self, port=8000):
        start_http_server(port)
        print(f"Prometheus exporter running on port {port}")
        while True:
            self.update_metrics()
