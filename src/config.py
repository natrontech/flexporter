import os

PROXMOX_ENDPOINT = os.getenv("PROXMOX_ENDPOINT", "10.10.10.10:8006")
PROXMOX_USER = os.getenv("PROXMOX_USER", "root@pam")
PROXMOX_PASSWORD = os.getenv("PROXMOX_PASSWORD", "password")
PROXMOX_VERIFY_SSL = (
    not os.getenv("PROXMOX_INSECURE_SKIP_TLS_VERIFY", "false").lower() == "true"
)
PROXMOX_BACKUP_STORAGE = os.getenv("PROXMOX_BACKUP_STORAGE", "cloud-backup-001")
