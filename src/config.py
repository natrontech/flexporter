import os

PROXMOX_ENDPOINTS = [
    os.getenv(f"PROXMOX_ENDPOINT_{i}") for i in range(10)
]  # Support up to 10 nodes
PROXMOX_ENDPOINTS = [e for e in PROXMOX_ENDPOINTS if e]  # Remove None values

PROXMOX_USER = os.getenv("PROXMOX_USER", "root@pam")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD", "password")
PROXMOX_VERIFY_SSL = (
    not os.getenv("PROXMOX_INSECURE_SKIP_TLS_VERIFY", "false").lower() == "true"
)
PROXMOX_BACKUP_STORAGE = os.getenv("PROXMOX_BACKUP_STORAGE", "cloud-backup-001")
