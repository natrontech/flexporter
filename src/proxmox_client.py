import logging

from proxmoxer import ProxmoxAPI

from .config import (
    PROXMOX_BACKUP_STORAGE,
    PROXMOX_ENDPOINTS,
    PROXMOX_PASSWORD,
    PROXMOX_USER,
    PROXMOX_VERIFY_SSL,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProxmoxClient:
    def __init__(self):
        self.client = None
        self.connected_endpoint = None

        for endpoint in PROXMOX_ENDPOINTS:
            try:
                logger.info(f"Attempting to connect to Proxmox API at {endpoint}")
                self.client = ProxmoxAPI(
                    endpoint,
                    user=PROXMOX_USER,
                    password=PROXMOX_PASSWORD,
                    verify_ssl=PROXMOX_VERIFY_SSL,
                )
                self.connected_endpoint = endpoint
                logger.info(f"Successfully connected to Proxmox API at {endpoint}")
                break
            except Exception as e:
                logger.warning(
                    f"Failed to connect to Proxmox API at {endpoint}: {str(e)}"
                )

        if self.client is None:
            raise Exception("Unable to connect to any Proxmox API endpoint")

    def get_pools(self):
        return self.client.pools.get()

    def get_vms_in_pool(self, pool):
        return self.client.pools(pool["poolid"]).get()["members"]

    def get_vm_details(self, node, vmid):
        try:
            return self.client.nodes(node).qemu(vmid).config.get()
        except Exception as e:
            print(f"Error fetching VM details for node {node}, VM {vmid}: {str(e)}")
            return {}

    def get_vm_status(self, node, vmid):
        try:
            return self.client.nodes(node).qemu(vmid).status.current.get()
        except Exception as e:
            print(f"Error fetching VM status for node {node}, VM {vmid}: {str(e)}")
            return {}

    def get_backup_size(self, node, vmid):
        try:
            backups = (
                self.client.nodes(node)
                .storage(PROXMOX_BACKUP_STORAGE)
                .content.get(vmid=vmid, content="backup")
            )
            # Get latest backup size and convert to GB
            return backups[0]["size"] / (1000**3) if backups else 0
        except Exception as e:
            print(f"Error fetching backup size for VM {vmid} on node {node}: {str(e)}")
            return 0

    def get_cluster_tags(self):
        try:
            return self.client.cluster.tags.get()
        except Exception as e:
            print(f"Error fetching cluster tags: {str(e)}")
            return []
