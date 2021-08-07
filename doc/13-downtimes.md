# Downtimes


## service downtimes
```yaml
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
```yaml
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

```bash
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

```bash
ansible-playbook --inventory inventories/icinga2  playbooks/master.yml --extra-vars @downtime.json --tags downtime_schedule
```

## own ansible module to create downtimes

example:

```yaml
- name: set downtime
  icinga2_downtime:
    url: "https://localhost:5665"
    url_username: "{{ icinga2_api.user }}"
    url_password: "{{ icinga2_api.password }}"
    comment: "{{ icinga2_downtime_comment }}"
    state: present
    name: "{{ item }}"
    object_type: 'Host'
    all_services: true
    duration: "{{ icinga2_downtime_duration }}"
    start_time: "{{ downtime_start }}"
    end_time: "{{ downtime_end }}"
    # fixed: false
  delegate_to: "master-1.icinga.local"
  vars:
    downtime_start: "{{ ansible_date_time.epoch }}"
    downtime_end: "{{ downtime_start | int + icinga2_downtime_duration * 60 }}"
  with_items:
    - "{{ icinga2_downtime_system_name }}"
  tags:
    - icinga2
    - downtime_schedule
    - downtime_remove
  when:
    - ansible_fqdn == "master-1.icinga.local"
```
