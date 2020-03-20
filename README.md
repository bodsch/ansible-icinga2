# Icinga2 ansible role

Ansible role to setup Icinga2 master or satellite.

## Requirements & Dependencies

 - ansible role to deploy a mariadb

### Operating systems

Tested on

* Debian 9 / 10
* Ubuntu 16.04 / 18.04 / 18.10
* CentOS 7

## Example Playbook

Just include this role in your list.
For example

```
- host: icinga-master
  roles:
    - role: icinga2

- host: icinga-satellite
  roles:
    - role: icinga2
      vars:
        icinga2_mode: satellite
        icinga2_server: icinga-master
        icinga2_master: icinga.foo-bar.com
```

## example configurations

### create API user

```
icinga2_api_user:
  root:
    password: seCr3t
    client_cn: NodeName
    permissions: '*'
  icingaweb:
    password: seCr3t_t00
    client_cn: NodeName
    permissions: '*'
```

### servicegroups

```
icinga2_servicegroups:
  - { name: ping      , displayname: 'Ping Checks', conditions: 'assign where match("ping*", service.name)' }
  - { name: disk      , displayname: 'Disk Checks', conditions: 'assign where match("disk*", service.name)' }
```
### create CheckCommands

to create an `object CheckCommand "service" { ... }` block, use the `icinga2_checkcommands` dictionary.

for example:

```
icinga2_checkcommands:
  hostname:
    import: plugin-check-command
    command: '[ PluginDir + "/check_hostname" ]'
  check_docker:
    name: check-docker
    import: plugin-check-command
    command: '[ PluginDir + "/check_docker_container" ]'
    arguments: |
      "-r" = {
        order = 0
        required = true
        value = "$docker_containers$"
      }
```

you can also use `arguments_append` to create an `arguments += {` line.

### create apply Service rules

to create a `apply Service ... { ... }` block, you can use the `icinga2_apply_service` dictionary.

for example see the `icinga2_apply_service_default` in `vars/main.yml`

```
icinga2_apply_service_default:
  ping4:
    import: generic-service
    check_command: ping4
    assign_where: host.address
```

for create an apply rule with `$keyword for (...)` you can enhance the cictionary with a `for` key:

```
icinga2_apply_service_default:
  http_for_host:
    name: "HTTP: "
    for: '(http_vhost => config in host.vars.http_vhosts)'
    import: generic-service
    check_command: http
    check_interval: 3m
    extra_parameters: |
      vars += config
```

for complex rules, you can use the `extra_parameters` key.

for example:

```
icinga2_apply_service_default:
  file_age:
    name: 'file_'
    for: '(file => config in host.vars.file_age)'
    check_command: file_age
    extra_parameters: |
      var warn_time = check_dictionary( config, "warning_time" )
      var crit_time = check_dictionary( config, "critical_time" )
      var warn_size = check_dictionary( config, "warning_size" )
      var crit_size = check_dictionary( config, "critical_size" )
      var description = check_dictionary( config, "description" )

      if( description ) {
        display_name = description
      } else {
        display_name = "File Age for " + file
      }
      notes        = "check a file age"

      vars = {
        "file_age_file" = file
      }

      if( warn_time && crit_time ) {
        vars += {
          "file_age_warning_time"  = config.warning_time
          "file_age_critical_time" = config.critical_time
        }
      }

      if( warn_size && crit_size ) {
        vars += {
          "file_age_warning_size"  = config.warning_size
          "file_age_critical_size" = config.critical_size
        }
      }

      max_check_attempts = 5
      check_interval = 10m
      retry_interval = 2
      enable_notifications = true
    assign_where: 'host.vars.file_age'
```

### notification

```
icinga2_notification_user:
  icinga_admin:
    import: generic-user
    display_name: "Icinga2 Admin"
    groups:
      - icinga_admins

icinga2_notification_usergroups:
  icinga_admins:
    display_name: "Icinga2 Admin Group"


icinga2_notification_apply:
  host_notification:
    import: slack-host-notification
    # interval: 2h
    users:
      - icinga_admin
    vars.notification_logtosyslog: true
    assign_where: host.vars.notification.slack
  service_notification:
    import: slack-service-notification
    # interval: 2h
    users:
      - icinga_admin
    vars.notification_logtosyslog: true
    assign_where: host.vars.notification.slack
```

### add host to icinga

```
icinga2_hosts:
  localhost:
    import: generic-host
    address: '{{ ansible_default_ipv4.address }}'
    vars: |
      os = "Linux"
      dist = "{{ ansible_distribution }}"
      dist_ver = "{{ ansible_distribution_version }}"
      disks = {
        "disk /" = {
          disk_partitions = "/"
        }
        "disk /opt" = {
          disk_partitions = "/opt"
        }
      }
      http_vhosts = {
        "/" = {
          http_uri = "/"
        }
      }
```

### add satellite

```
icinga2_satellite:

  mars.icinga.local:
    import: generic-host
    vars: |
      os = "Linux"
      dist = "{{ ansible_distribution }}"
      dist_ver = "{{ ansible_distribution_version }}"
      environment = "solarsystem"
      satellite = true

      disks = {
        "disk /" = {
          disk_partitions = "/"
        }
      }
```

## tests

for testing

```
tox -e py38-ansible29 -- molecule

tox -e py38-ansible29 -- molecule -s icinga2-satellite
```

## Troubleshooting & Known issues

```
# icinga2 feature list
Disabled features: api command compatlog debuglog gelf graphite icingastatus opentsdb statusdata syslog
Enabled features: checker ido-mysql livestatus mainlog notification perfdata
```

# Contribution

Please read [Contribution](CONTRIBUTIONG.md)

# Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-icinga2/-/tags)!


# Credits

- Michael 'dnsmichi' Friedrich
- Nikolai Buchwitz
- Julien Tognazzi
- and many others to make the icinga2 what it is

## License

BSD 2-clause
