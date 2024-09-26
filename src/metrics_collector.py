import logging

from .proxmox_client import ProxmoxClient


class MetricsCollector:
    def __init__(self):
        self.proxmox_client = ProxmoxClient()

    def collect_metrics(self):
        metrics = []
        pools = self.proxmox_client.get_pools()
        all_vm_tags = set()

        for pool in pools:
            pool_metrics = {"name": pool["poolid"], "virtual_machines": []}

            vms = self.proxmox_client.get_vms_in_pool(pool)

            for vm in vms:
                if vm["type"] == "qemu":
                    try:
                        vm_details = self.proxmox_client.get_vm_details(
                            vm["node"], vm["vmid"]
                        )
                        vm_status = self.proxmox_client.get_vm_status(
                            vm["node"], vm["vmid"]
                        )

                        # Calculate total storage
                        total_storage = 0
                        for key, value in vm_details.items():
                            if key.startswith(("scsi", "ide", "sata")) and isinstance(
                                value, str
                            ):
                                size_parts = value.split(",")
                                for part in size_parts:
                                    if part.startswith("size="):
                                        size = part.split("=")[1]
                                        if size.endswith("G"):
                                            total_storage += float(size[:-1])
                                        elif size.endswith("M"):
                                            total_storage += float(size[:-1]) / 1024
                                        break

                        # Get IP configuration
                        ipconfig = vm_details.get("ipconfig0", "")
                        if ipconfig:
                            ipconfig = (
                                ipconfig.split("ip=")[1].split(",")[0].split("/")[0]
                            )

                        # Collect VM tags
                        vm_tags = set()
                        tags_field = vm_details.get("tags", "")
                        if tags_field:
                            # Split tags by commas and semicolons
                            tag_items = tags_field.replace(";", ",").split(",")
                            vm_tags = {tag.strip() for tag in tag_items if tag.strip()}

                        # Add tags to the set of all VM tags
                        all_vm_tags.update(vm_tags)

                        vm_metrics = {
                            "id": vm["vmid"],
                            "name": vm["name"],
                            "ip": ipconfig,
                            "cpu_cores": int(vm_details.get("cores", 0)),
                            "vcpus": int(vm_details.get("vcpus", 0)),
                            "memory_gb": int(vm_details.get("memory", 0)) / 1024,
                            "storage_gb": round(total_storage),
                            "backup_storage_gb": round(
                                self.proxmox_client.get_backup_size(
                                    vm["node"], vm["vmid"]
                                )
                            ),
                            "os_type": vm_details.get("ostype", ""),
                            "tags": list(vm_tags),
                            "status": vm_status.get("status", ""),
                        }
                        pool_metrics["virtual_machines"].append(vm_metrics)
                    except Exception as e:
                        print(
                            f"Error fetching metrics for VM {vm['vmid']} in pool {pool['poolid']}: {str(e)}"
                        )

            metrics.append(pool_metrics)

        return metrics, all_vm_tags
