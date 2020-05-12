# Backup and Restore

## backup
```
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars icinga2_master_backup_enabled=true --tags backup
```

## restore
```
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars icinga2_master_backup_enabled=true --tags restore
```
