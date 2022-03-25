# Examples

```
icinga2_apply_service:
  ssh:
    import: generic-service
    check_command: ssh
    assign_where: '(host.address || host.address6) && host.vars.os == "Linux"'
  ping4:
    import: generic-service
    check_command: ping4
    assign_where: host.address
  ping6:
    import: generic-service
    check_command: ping6
    assign_where: host.address6
  load:
    import: generic-service
    check_command: load
    # Used by the ScheduledDowntime apply rule in `downtimes.conf`.
    extra_parameters: |
      if(host.vars.downtime) {
        vars.backup_downtime = host.vars.downtime
      }
    assign_where: 'host.vars.os == "Linux"'
  icinga:
    import: generic-service
    check_command: icinga
    assign_where: 'host.name == NodeName'
  procs:
    import: generic-service
    check_command: procs
    assign_where: 'host.name == NodeName'
  users:
    import: generic-service
    check_command: users
    assign_where: 'host.vars.os == "Linux"'
  sensors:
    import: generic-service
    check_command: sensors
    assign_where: '"sensors" in host.vars.services'
  file_age:
    import: generic-service
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

  apt:
    import: generic-service
    check_command: apt
    assign_where: 'host.vars.os == "Linux" && (host.vars.dist == "Debian" || host.vars.dist == "Ubuntu")'

  uptime:
    import: generic-service
    display_name: system uptime
    check_command: system_uptime
    assign_where: '"uptime" in host.vars.services'

  memory:
    import: generic-service
    display_name: system memory
    check_command: check_memory
    check_interval: '45s'
    retry_interval: '10s'
    assign_where: '"memory" in host.vars.services'
    ignore_where: 'host.vars.os == "Windows"'

```

```
icinga2_defaults_checkcommands:
  hostname:
    import: plugin-check-command
    command: '[ PluginDir + "/check_docker_container" ]'
  check_redis:
    import: plugin-check-command
    command: '[ PluginDir + "/check_redis" ]'
  system_uptime:
    import: plugin-check-command
    command: '[ PluginDir + "/check_uptime.sh" ]'
  check_memory:
    import: plugin-check-command
    command: '[ PluginDir + "/check_mem" ]'

```
