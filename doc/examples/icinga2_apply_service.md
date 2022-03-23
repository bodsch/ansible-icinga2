
## icinga satellite check

integrates `notes` and `notes_url`

```yaml
icinga2_apply_service:
  icinga:
    check_command: icinga
    name: 'icinga'
    display_name: 'icinga satellite'
    notes: "icinga satellite"
    notes_url: "/operations/icinga.md"
    max_check_attempts: 2
    check_interval: 30s
    retry_interval: 10s
    enable_notifications: false

    assign_where: 'host.name == NodeName || host.vars.satellite'
```

```yaml
icinga2_apply_service:
  dnssec:
    import: generic-service
    name: 'dnssec '
    for: '(zone => config in host.vars.zones)'
    check_command: delv
    check_interval: 2h
    extra_parameters: |
      vars += config
    assign_where: host.vars.zones
```

```yaml
icinga2_apply_service:
  cert:
    # TODO:
    # all services - IMAPs / SMTPs ...
    name: 'tls certs '
    for: '(c => config in host.vars.tls_certificate)'
    import: generic-service
    check_command: http
    check_interval: 1h
    extra_parameters: |
      var port = check_dictionary(config, "port")
      if(!port) {
        port = "443"
      }
      # vars += config
      vars = {
        "http_port" = port
        "http_vhost" = host.name
        "http_certificate" = "15"
        "http_sni" = true
        "http_ssl" = true
      }

    assign_where: host.vars.tls_certificate
```

```yaml
icinga2_apply_service:
  ntp:
    display_name: NTP
    check_command: ntp_time
    extra_parameters: |
      vars += {
        "ntp_address" = "127.0.0.1"
        "ntp_quiet" = "true"
        "ntp_warning" = "0.5"
        "ntp_critical" = "1"
        "ntp_ipv4" = "true"
      }
    assign_where: '"ntp" in host.vars.services'
```


```yaml
icinga2_apply_service:
  https:
    name: 'HTTPS: '
    for: '(http_vhost => config in host.vars.https_vhosts)'
    import: generic-service
    check_command: http
    check_interval: 3m
    extra_parameters: |
      vars += config
      vars += {
        "http_vhost" = host.name
        "http_ssl" = true
      }
```


```yaml
icinga2_apply_service:
  file_age:
    name: 'file_'
    for: '( file => config in host.vars.file_age)'
    notes: "check a file age"
    # import: "generic-service"
    # import "icinga-satellite-service"
    check_command: "file_age"
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

    max_check_attempts: 5
    check_interval: 10m
    retry_interval: 2
    enable_notifications: true

    assign_where: host.vars.file_age
```
