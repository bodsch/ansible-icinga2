# Service- and Hostgroups

## Host Groups

```
icinga2_hostgroups:
  - { name: 'linux-servers', displayname: 'Linux Servers', conditions: 'assign where host.vars.os == "Linux"' }
  - { name: 'icinga-satellites', displayname: 'Icinga2 Satellites', conditions: 'assign where host.vars.satellite' }
```

## Service Groups

```
icinga2_servicegroups:
  - { name: ping      , displayname: 'Ping Checks', conditions: 'assign where match("ping*", service.name)' }
  - { name: disk      , displayname: 'Disk Checks', conditions: 'assign where match("disk*", service.name)' }
```
