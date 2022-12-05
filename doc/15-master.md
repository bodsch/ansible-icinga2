# icnga2 master

```yaml
icinga2_mode: master

icinga2_server: '{{ inventory_hostname }}'
```

## Multi Master

```yaml
icinga2_ha: true
icinga2_masters:
  master-1.icinga.local:
    type: primary
    ip: 192.168.130.20
  master-2.icinga.local:
    ip: 192.168.130.21
```

Both Icinga2 instances should run as an HA capable network.
The corresponding host object of the instances must therefore contain a correspondingly identical zone definition!

### primary 1
```yaml
icinga2_mode: master

icinga2_host_object:
  primary1:
    import: generic-host
    address: '{{ ansible_default_ipv4.address }}'
    display_name: "{{ ansible_fqdn }}"
    zone: "primary"
    ...
```

### primary 2
```yaml
icinga2_mode: master

icinga2_host_object:
  primary2:
    import: generic-host
    address: '{{ ansible_default_ipv4.address }}'
    display_name: "{{ ansible_fqdn }}"
    zone: "primary"
    ...
```



behind a NAT you would overwrite the icinga2 host name?

try this:

```yaml
icinga2_masters:
  master-1.icinga.local:
    overwrite: master.test.com:
    ip: 192.168.130.20
```


### add host to icinga

```yaml
icinga2_host_object:

  localhost:
    import: generic-host
    address: '{{ ansible_default_ipv4.address }}'
    vars: |
      os = "Linux"
      dist = "{{ ansible_distribution }}"
      dist_ver = "{{ ansible_distribution_version }}"
      disks = {
        "disk /" = {
          disk_partitions = "/"
        }
        "disk /opt" = {
          disk_partitions = "/opt"
        }
      }
      http_vhosts = {
        "/" = {
          http_uri = "/"
        }
      }
```
