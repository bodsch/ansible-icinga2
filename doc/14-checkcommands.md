# check commands

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
