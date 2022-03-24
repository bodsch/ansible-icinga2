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

[upstream documentation](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#influxdbwriter)

| Variable                | Type        |          | Description  |
| :---------              | :---        |          | :----------- |
| `host`                  | String      | Required | InfluxDB host address. Defaults to 127.0.0.1.                                                |
| `port`                  | Number      | Required | InfluxDB HTTP port. Defaults to 8086.                                                        |
| `database`              | String      | Required | InfluxDB database name. Defaults to icinga2.                                                 |
| `username`              | String      | Optional | InfluxDB user name. Defaults to none.                                                        |
| `password`              | String      | Optional | InfluxDB user password. Defaults to none.                                                    |
| `basic_auth`            | Dictionary  | Optional | Username and password for HTTP basic authentication.                                         |
| `ssl_enable`            | Boolean     | Optional | Whether to use a TLS stream. Defaults to false.                                              |
| `ssl_insecure_noverify` | Boolean     | Optional | Disable TLS peer verification.                                                               |
| `ssl_ca_cert`           | String      | Optional | Path to CA certificate to validate the remote host.                                          |
| `ssl_cert`              | String      | Optional | Path to host certificate to present to the remote host for mutual verification.              |
| `ssl_key`               | String      | Optional | Path to host key to accompany the ssl_cert.                                                  |
| `host_template`         | Dictionary  | Required | Host template to define the InfluxDB line protocol.                                          |
| `service_template`      | Dictionary  | Required | Service template to define the influxDB line protocol.                                       |
| `enable_send_thresholds`| Boolean     | Optional | Whether to send warn, crit, min & max tagged data.                                           |
| `enable_send_metadata`  | Boolean     | Optional | Whether to send check metadata e.g. states, execution time, latency etc.                     |
| `flush_interval` 	      | Duration    | Optional | How long to buffer data points before transferring to InfluxDB. Defaults to 10s.             |
| `flush_threshold`       | Number      | Optional | How many data points to buffer before forcing a transfer to InfluxDB. Defaults to 1024.      |
| `enable_ha`             | Boolean     | Optional | Enable the high availability functionality. Only valid in a cluster setup. Defaults to false.|


```yaml
icinga2_master_features_enabled:
  - influxdb

icinga2_features:
  influxdb:
    host: influxdb
    port: 8086
    database: icinga2
    username: "icinga2"
    password: "icinga2"
    flush_threshold: 1024
    flush_interval: 10s
    ssl_enable: false
    basic_auth:
      username: "icinga"
      password: "icinga"
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

## influxdb2

```yaml
icinga2_master_features_enabled:
  - influxdb2

icinga2_features:
  influxdb2:
    host: localhost
    port: 8086
    organization: "monitoring"
    bucket: "icinga2"
    auth_token: "rrDAHWjVEKScc5DzaFVN4vzg9HtZkcWvt433Yfdqju"
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

see also documentation at [icinga.com](https://icinga.com/docs/icinga-2/latest/doc/09-object-types/#notification)

All relevant files for notifications are stored under `/etc/icinga2/notifications`.  
3 definitions are needed:
- template: `notification-templates.conf`
- object: `notification-objects.conf`
- apply rules: `notification-apply-rules.conf`

The [vars/main.yml](`vars/main.yml`) already contains default definitions for notifications via email.

**At the moment the corresponding notification scripts have to be rolled out separately!**

### notification template

creates an `template Notification` object.

| Variable                | Type        |          | Description  |
| :---------              | :---        |          | :----------- |
| `description`           | String      | Optional |              |
| `command`               | String      | Required |              |
| `interval`              | String      | Required |              |
| `period`                | String      | Required |              |
| `extra_parameters`      | Text        | Required |              |
| `states`                | List        | Optional |              |
| `types`                 | List        | Optional |              |


```yaml
icinga2_notification_templates:
  generic-service-notification:
    description: |
      generic service notification to mail for 24/7 alarms
    command: "mail-service-notification"
    interval: 15m
    period: "24x7"
    extra_parameters: |
      vars += {
        // notification_icingaweb2url = "https://www.example.com/icingaweb2"
        // notification_from = "Icinga 2 Host Monitoring <icinga@example.com>"
        notification_logtosyslog = false
      }
    states:
      - Warning
      - Critical
      - Unknown
    types:
      - Problem
      - Acknowledgement
      - Recovery
      - Custom
      - FlappingStart
      - FlappingEnd
      - DowntimeStart
      - DowntimeEnd
      - DowntimeRemoved
```

### notification object

creates an `object NotificationCommand` object.

| Variable                | Type        |          | Description  |
| :---------              | :---        |          | :----------- |
| `description`           | String      | Optional |              |
| `command`               | List        | Required |              |
| `extra_parameters`      | Text        | Required |              |

```yaml
icinga2_notification_objects:
  mail-host-notification:
    description: |
      default mail notification
    command:
      - ConfigDir
      - '"/scripts/mail-host-notification.sh"'
    extra_parameters: |
      arguments += {
        "-4" = "$notification_address$"
        "-6" = "$notification_address6$"
        "-b" = "$notification_author$"
        "-c" = "$notification_comment$"
        "-d" = {
          required = true
          value = "$notification_date$"
        }

      }

      vars += {
        notification_address = "$address$"
        notification_address6 = "$address6$"
        notification_author = "$notification.author$"
        notification_comment = "$notification.comment$"
        notification_type = "$notification.type$"
        notification_date = "$icinga.long_date_time$"
        notification_hostname = "$host.name$"
        notification_hostdisplayname = "$host.display_name$"
        notification_hostoutput = "$host.output$"
        notification_hoststate = "$host.state$"
        notification_useremail = "$user.email$"
      }

```

### notification apply rules

creates an `apply Notification` object.

| Variable                | Type        |          | Description  |
| :---------              | :---        |          | :----------- |
| `type`                  | String      | Required | May be either `host` or `service`. |
| `import`                | List        | Required |              |
| `users`                 | List or String | Required | A list of user names who should be notified.<br>**Optional** if the `user_groups` attribute is set.    |
| `user_groups`           | List or String | Required | A list of user group names who should be notified.<br>**Optional** if the `users` attribute is set. |
| `interval`              | String      | Optional | The notification interval (in seconds). This interval is used for active notifications.<br>Defaults to 30 minutes. If set to 0, re-notifications are disabled.             |
| `extra_parameters`      | Text        | Required |              |
| `assign_where`          | String      | Required |              |
| `ignore_where`          | String      | Optional |              |

**note**

> For `users` and `user_groups`, a list of users or groups can be specified as well as an object reference!  
  Users or groups must be addressable via `icinga2_notification_user` or `icinga2_notification_usergroups`.  
  Object references such as `host.vars.notification.mail.groups` are defined as host variables via `icinga2_host_object`.


```yaml
icinga2_notification_apply_rules:
  #
  host-mail:
    type: host
    import: generic-host-notification
    users: []
    user_groups: []
    interval: '2h'
    extra_parameters: |
      vars.notification_logtosyslog = true
    assign_where: "host.vars.notification.mail"
  #
  service-mail:
    type: service
    import: generic-service-notification
    user_groups: host.vars.notification.mail.groups
    interval: '2h'
    extra_parameters: |
      vars.notification_logtosyslog = true

    assign_where: "host.vars.notification.mail"
  #
  host-slack:
    type: host
    import: slack-host-notification
    extra_parameters: |
      vars.notification_logtosyslog = true
    assign_where: host.vars.notification.slack
  service-slack:
    type: service
    import: slack-service-notification
    extra_parameters: |
      vars.notification_logtosyslog = true
    assign_where: host.vars.notification.slack
```

In addition to these definitions, the corresponding recipients must also be defined.
These can be groups, individual users or both.

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

**To trigger a notification, the corresponding host or service variable must be set!**

