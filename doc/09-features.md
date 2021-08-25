# Features


## enable master features
```yaml
icinga2_master_features_enabled:
  - checker
  - api
  - ido-mysql
  - mainlog
  - notification
```

## disable master features
```yaml
icinga2_master_features_disabled:
  - perfdata
  - livestatus
```

## graphite

if add 'graphite' to `icinga2_master_features_enabled` above, you can her configure this feature:

| Variable   | Description  |
| :--------- | :----------- |
| `host`                   | Graphite Carbon host address. Defaults to 127.0.0.1. |
| `port`                   | Graphite Carbon port. Defaults to 2003. |
| `host_name_template`     | Metric prefix for host name. Defaults to icinga2.$host.name$.host.$host.check_command$. |
| `service_name_template`  | Metric prefix for service name. Defaults to icinga2.$host.name$.services.$service.name$.$service.check_command$. |
| `enable_send_thresholds` | Send additional threshold metrics. Defaults to false. |
| `enable_send_metadata`   | Send additional metadata metrics. Defaults to false. |
| `enable_ha`              | Enable the high availability functionality. Only valid in a cluster setup. Defaults to false. |


```yaml
icinga2_master_features_enabled:
  - graphite

icinga2_features:
  graphite:
    host: localhost
```

## influxdb


```yaml
icinga2_master_features_enabled:
  - influxdb

icinga2_features:
  influxdb:
    host: localhost
    port: 8086
    enable_ha: true
    database: icinga2
    flush_threshold: 1024
    flush_interval: 10s
    host_template:
      measurement: "$host.check_command$"
      tags:
        hostname: "$host.name$"
    service_template:
      measurement: "$service.check_command$"
      tags:
        hostname: "$host.name$"
        service: "$service.name$"
```

## gelf

```yaml
icinga2_master_features_enabled:
  - gelf

icinga2_features:
  gelf:
    host: tsdb-1.icinga.local
    port: 12201
    source: "{{ ansible_fqdn }}"
    enable_send_perfdata: true
```


## FileLogger

```yaml
icinga2_filelogger:
  directory: /var/log/icinga2
  mainlog:
    severity: warning
    logfile: icinga2.log
  debuglog:
    severity: debug
    logfile: debug.log
```


## IDO

[original documentation](https://icinga.com/docs/icinga2/latest/doc/09-object-types/#objecttype-idomysqlconnection)

### ido parameter

| Variable   | Description  |
| :--------- | :----------- |
| `host`                 | MySQL database host address. Defaults to localhost.                                                                                       |
| `port`                 | MySQL database port. Defaults to 3306.                                                                                                    |
| `socket_path`          | MySQL socket path.                                                                                                                        |
| `user`                 | MySQL database user with read/write permission to the icinga database. Defaults to icinga.                                                |
| `password`             | MySQL database user’s password. Defaults to icinga.                                                                                       |
| `database`             | MySQL database name. Defaults to icinga.                                                                                                  |
| `enable_ssl`           | Use SSL. Defaults to false. Change to true in case you want to use any of the SSL options.                                                |
| `ssl_key`              | MySQL SSL client key file path.                                                                                                           |
| `ssl_cert`             | MySQL SSL certificate file path.                                                                                                          |
| `ssl_ca`               | MySQL SSL certificate authority certificate file path.                                                                                    |
| `ssl_capath`           | MySQL SSL trusted SSL CA certificates in PEM format directory path.                                                                       |
| `ssl_cipher`           | MySQL SSL list of allowed ciphers.                                                                                                        |
| `table_prefix`         | MySQL database table prefix. Defaults to icinga_.                                                                                         |
| `instance_name`        | Unique identifier for the local Icinga 2 instance, used for multiple Icinga 2 clusters writing to the same database. Defaults to default. |
| `instance_description` | Description for the Icinga 2 instance.                                                                                                    |
| `enable_ha`            | Enable the high availability functionality. Only valid in a cluster setup. Defaults to true.                                              |
| `failover_timeout`     | Set the failover timeout in a HA cluster. Must not be lower than 30s. Defaults to 30s.                                                    |
| `cleanup`              | Dictionary with items for historical table cleanup.                                                                                       |
| `categories`           | Array of information types that should be written to the database.                                                                        |


### ido cleanup parameter

| Variable   | Description  |
| :--------- | :----------- |
| `acknowledgements_age`            | Max age for acknowledgements table rows (entry_time). Defaults to 0 (never).
| `commenthistory_age`              | Max age for commenthistory table rows (entry_time). Defaults to 0 (never).
| `contactnotifications_age`        | Max age for contactnotifications table rows (start_time). Defaults to 0 (never).
| `contactnotificationmethods_age`  | Max age for contactnotificationmethods table rows (start_time). Defaults to 0 (never).
| `downtimehistory_age`             | Max age for downtimehistory table rows (entry_time). Defaults to 0 (never).
| `eventhandlers_age`               | Max age for eventhandlers table rows (start_time). Defaults to 0 (never).
| `externalcommands_age`            | Max age for externalcommands table rows (entry_time). Defaults to 0 (never).
| `flappinghistory_age`             | Max age for flappinghistory table rows (event_time). Defaults to 0 (never).
| `hostchecks_age`                  | Max age for hostalives table rows (start_time). Defaults to 0 (never).
| `logentries_age`                  | Max age for logentries table rows (logentry_time). Defaults to 0 (never).
| `notifications_age`               | Max age for notifications table rows (start_time). Defaults to 0 (never).
| `processevents_age`               | Max age for processevents table rows (event_time). Defaults to 0 (never).
| `statehistory_age`                | Max age for statehistory table rows (state_time). Defaults to 0 (never).
| `servicechecks_age`               | Max age for servicechecks table rows (start_time). Defaults to 0 (never).
| `systemcommands_age`              | Max age for systemcommands table rows (start_time). Defaults to 0 (never).

### Example

```yaml
icinga2_ido:
  type: mysql
  enabled: true
  username: 'icinga2_ido'
  password: 'icinga2_ido'
  host: '127.0.0.1'
  database: 'icinga2_ido'
  port: 3306
  socket: /run/mysqld.sock
  cleanup:
    acknowledgements_age: 48h
    hostchecks_age: 48h
    servicechecks_age: 48h
  mysql:
    schema_file: /usr/share/icinga2-ido-mysql/schema/mysql.sql
    schema_upgrade: /usr/share/icinga2-ido-mysql/schema/upgrade
```

## notification

```yaml
icinga2_notification:
  host:
    name: mail-icingaadmin
    import: mail-host-notification
    user_groups: host.vars.notification.mail.groups
    users: host.vars.notification.mail.users
    interval: 2h
    vars.notification_logtosyslog: true
    assign_where: host.vars.notification.mail
  service:
    name: mail-icingaadmin
    import: mail-service-notification
    user_groups: host.vars.notification.mail.groups
    users: host.vars.notification.mail.users
    interval: 2h
    vars.notification_logtosyslog: true
    assign_where: host.vars.notification.mail
```

```yaml
icinga2_notification_user:
  icingaadmin:
    import: generic-user
    display_name: "Icinga2 Admin"
    groups:
      - icingaadmins
  bodsch:
    import: generic-user
    display_name: Bodo Schulz
    groups:
      - icingaadmins
    email: ...
```

```yaml
icinga2_notification_usergroups:
  icingaadmins:
    display_name: "Icinga2 Admin Group"
```

```yaml
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
