# Migration Guide

## from 0.9.x to greater

### Icinga2 Master

`icinga2_master` is replaced with `icinga2_masters`

e.g.

old:
```
icinga2_master: "{{ ansible_fqdn }}"
```

new:
```
icinga2_masters:
  master-1.icinga.local:
    ip: 192.168.130.20
```

### IDO

`icinga2_ido_*` is replaced with `icinga2_ido`

e.g.

old:
```
icinga2_ido_type: mysql
icinga2_ido_enabled: true
icinga2_ido_username: 'icinga2_ido'
icinga2_ido_password: 'icinga2_ido'
icinga2_ido_host: '127.0.0.1'
icinga2_ido_database: 'icinga2_ido'
icinga2_ido_port: 3306
icinga2_ido_socket: /run/mysqld.sock

icinga2_ido_mysql_schema_file: /usr/share/icinga2-ido-mysql/schema/mysql.sql
icinga2_ido_mysql_schema_updates: /usr/share/icinga2-ido-mysql/schema/upgrade

```

new:
```
icinga2_ido:
  type: mysql
  enabled: true
  username: 'icinga2_ido'
  password: 'icinga2_ido'
  host: '127.0.0.1'
  database: 'icinga2_ido'
  port: 3306
  socket: /run/mysqld.sock
  mysql:
    schema_file: /usr/share/icinga2-ido-mysql/schema/mysql.sql
    schema_upgrade: /usr/share/icinga2-ido-mysql/schema/upgrade
```

### API

`icinga2_api_*` is replaced with `icinga2_api`

e.g.

old:
```
icinga2_api_enabled: true
icinga2_api_accept_config: true
icinga2_api_accept_commands: true
icinga2_api_ticket_salt: TicketSalt
icinga2_api_user:
  root:
    password: foo
    client_cn: NodeName
    permissions: '*'
```

new:
```
icinga2_api:
  enabled: true
  accept_config: true
  accept_commands: true
  ticket_salt: TicketSalt
  user:
    icinga2:
      password: S0mh1TuFJI
      permissions: '*'

    icingaweb:
      password: S0mh1TuFJI
      permissions:
        - "status/query"
        - "actions/*"
        - "objects/modify/*"
        - "objects/query/*"
```

### FileLogger

`icinga2_mainlog_*` is replaced with `icinga2_filelogger`

e.g.

old:
```
icinga2_mainlog_severity: warning
icinga2_mainlog_logfile: icinga2.log
icinga2_mainlog_directory: /var/log/icinga2
```

new:
```
icinga2_filelogger:
  directory: /var/log/icinga2
  mainlog:
    severity: warning
    logfile: icinga2.log
  debuglog:
    severity: debug
    logfile: debug.log
```

### Graphite

old:
```
icinga2_features:
  graphite:
    graphite_host: localhost
```

new:
```
icinga2_features:
  graphite:
    host: localhost
```

### Host Objects

`icinga2_hosts` and `icinga2_satellite` are replaced with `icinga2_host_object`


