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
