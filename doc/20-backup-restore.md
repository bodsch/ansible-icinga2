# Backup and Restore

## backup
```bash
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars icinga2_master_backup_enabled=true --tags backup
```

## restore
```bash
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars icinga2_master_backup_enabled=true --tags restore
```
