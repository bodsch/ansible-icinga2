# apply rules

To create a `apply Service ... { ... }` block, you can use the `icinga2_apply_service` dictionary.

For example:
```yaml
icinga2_apply_service:
  https_for_host:
    import: generic-service
    check_command: http
    check_interval: 3m
    extra_parameters: |
      vars += config
      vars += {
        "http_vhost" = host.name
        "http_certificate" = "15"
        "http_sni" = true
        "http_ssl" = true
        "notify" = "true"
      }
    assign_where: 'host.vars.https_vhosts'
```
(for more, see the `icinga2_defaults_apply_service` in `vars/main.yml`)

```yaml
icinga2_defaults_apply_service:
  ssh:
    import: generic-service
    check_command: ssh
    assign_where: '(host.address || host.address6) && host.vars.os == "Linux"'
  ping4:
    import: generic-service
    check_command: ping4
    assign_where: host.address
```

With `event_command` an EventCommand can be defined.

It is important that the `endpoint_name` and the corresponding host definition match! ([See here](16-satellite.md#endpoint_name))

```yaml
icinga2_host_object:

  master-1:
    endpoint_name: master-1.matrix.lan
    display_name: master-1.matrix.lan
    import: generic-host
    address: '{{ ansible_default_ipv4.address }}'
    restart_services = [ "grapyhte_daemon" ]
    ...

icinga2_apply_service:
  graphyte_daemon:
    import: generic-service
    name: 'graphyte daemon'
    display_name: 'graphyte-daemon
    event_command: "restart_service"
    enable_notifications: false
    extra_parameters: |
      vars = {
        "restart_service" = "graphyte-daemon"
      }
    assign_where: '"grapyhte_daemon" in host.vars.restart_services'
```



for create an apply rule with `$keyword for (...)` you can enhance the cictionary with a `for` key:

```yaml
icinga2_apply_service:
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

```yaml
icinga2_apply_service:
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
