# icinga2 satellite


```yaml
icinga2_mode: satellite
```

```yaml
icinga2_host_object:

  mars.matrix.local:
    import: generic-host
    vars: |
      os = "Linux"
      dist = "{{ ansible_distribution }}"
      dist_ver = "{{ ansible_distribution_version }}"
      environment = "solarsystem"
      satellite = true

      disks = {
        "disk /" = {
          disk_partitions = "/"
        }
      }
```

<a name="endpoint_name"></a>
When using an event handler, the `endpoint_name` must be set if necessary.

You can then use `display_name` to restore the desired display name.

```yaml
icinga2_host_object:

  mars.matrix.local:
    endpoint_name: dba.int.matrix.lan
    display_name: mars.matrix.local
    import: generic-host
```

## Zones

TODO
```yaml
    {% if icinga2_satellites[icinga2_satellite_zone] is defined and
          icinga2_satellites[icinga2_satellite_zone][_name] is defined and
          icinga2_satellites[icinga2_satellite_zone][_name]['ip'] is defined %}
      {% set satellite_ip = icinga2_satellites[icinga2_satellite_zone][_name]['ip'] %}
    {% else %}
      {% set satellite_ip = lookup('pipe', 'host ' + ansible_fqdn   + ' | grep "has address" | cut -d" " -f4') %}
    {% endif %}
```


For organize multiple Satellites in one Zone, you can define this over `icinga2_satellites`.

```yaml
icinga2_satellites:
  zone1:
    satellite-1.icinga.local:
      ip: 192.168.130.30
    satellite-2.icinga.local:
      ip: 192.168.130.31
  zone2:
    satellite-3.icinga.local:
      ip: 192.168.130.32
```
