# Icinga2 ansible role

Ansible role to setup Icinga2 server with optional plugins like pnp4nagios, graphite or nagvis


## Requirements & Dependencies

### Ansible
It was tested on the following versions:
 * 2.7
 * 2.8
 * 2.9

### Operating systems

Tested on Ubuntu 18.04 and 18.10, Debian 8, 9 and 10, CentOS 7

## Example Playbook

Just include this role in your list.
For example

```
- host: myserver
  roles:
    - { role: icinga2 }
```


## Variables

```

tz: America/New_York
scriptsdir: /usr/local/scripts
backupdir: /srv/backup/{{ inventory_hostname }}

icinga2_mode: server
## server conf

## Client conf

#icinga2_mode: client
icinga2_server: monserver
icinga2_server_ip: 192.168.0.100

icinga2_master_port: 5665

icinga2_if: eth0
```

You can also used group 'monitored' inside inventory to apply basic alive monitoring.

## Troubleshooting & Known issues

```
# icinga2 feature list
Disabled features: api command compatlog debuglog gelf graphite icingastatus opentsdb statusdata syslog
Enabled features: checker ido-mysql livestatus mainlog notification perfdata
```

try to restart service


## License

BSD 2-clause



# master:
```
zones.d/mail.boone-schulz.de/mail.boone-schulz.de.conf


object Endpoint "mail.boone-schulz.de" { host = "185.244.193.175"; port = "5665" }
object Zone "mail.boone-schulz.de" { parent = "icinga.boone-schulz.de" ; endpoints = [ "mail.boone-schulz.de" ] }

object Host "mail.boone-schulz.de" {
  address = "185.244.193.175"
  import "generic-host"
  command_endpoint = "icinga.boone-schulz.de"
  zone = "icinga.boone-schulz.de"
  vars = {
    os = "Linux"
    dist = "Arch"
    zone = "mail.boone-schulz.de"
    satellite = "true"
    disks = {
      "disk /" = { disk_partitions = "/" }
    }
  }
}
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


# satellite
```
zones.conf
/*
 * Endpoint and Zone configuration for a cluster setup
 * This local example requires `NodeName` defined in
 * constants.conf.
 */
/*
object Endpoint NodeName {
  host = NodeName
}

object Zone ZoneName {
  parent = "icinga.boone-schulz.de"
  endpoints = [ NodeName ]
}
*/

object Endpoint "icinga.boone-schulz.de" {
  host = "icinga.boone-schulz.de"
  port = "5665"
}

object Zone "icinga.boone-schulz.de" {
  //this is the local node master named  = "master"
  endpoints = [ "icinga.boone-schulz.de" ]
}


object Zone "global-templates" {
  global = true
}

object Zone "director-global" {
  global = true
}
```

