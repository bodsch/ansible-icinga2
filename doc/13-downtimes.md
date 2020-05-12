# Downtimes


## service downtimes
```
icinga2_service_downtimes:
  backup-downtime:
    author: "icingaadmin"
    comment: "Scheduled downtime for backup"
    ranges:
      monday: service.vars.backup_downtime
      tuesday: service.vars.backup_downtime
      wednesday: service.vars.backup_downtime
      thursday: service.vars.backup_downtime
      friday: service.vars.backup_downtime
      saturday: service.vars.backup_downtime
      sunday: service.vars.backup_downtime
    assign_where: service.vars.backup_downtime != ""
```

## host downtimes
```
icinga2_host_downtimes:
  nas-downtime:
    author: "icingaadmin"
    comment: "Scheduled downtime for NAS"
    ranges
      monday: "21:00-24:00,00:00-07:00"
      tuesday: "21:00-24:00,00:00-07:00"
      wednesday: "21:00-24:00,00:00-07:00"
      thursday: "21:00-24:00,00:00-07:00"
      friday: "21:00-24:00,00:00-07:00"
      saturday:"21:00-24:00,00:00-07:00"
      sunday: "21:00-24:00,00:00-07:00"
    assign_where: host.name == "nas.matrix.local"
```

create a file like this:

```
cat downtime.json

{
  "icinga2_api": {
    "user": "icinga2",
    "password": "S0mh1TuFJI"
  },
  "icinga2_downtime_comment": "test",
  "icinga2_downtime_system_name": "master-1.icinga.local",
  "icinga2_downtime_duration": 10
}
```

and call a ansible task:

```
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars @downtime.json --tags downtime_schedule
```
