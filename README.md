
# Ansible Role:  `icinga2`

Ansible role to setup Icinga2 master or satellite.


[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/bodsch/ansible-icinga2/CI)][ci]
[![GitHub issues](https://img.shields.io/github/issues/bodsch/ansible-icinga2)][issues]
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/bodsch/ansible-icinga2)][releases]

[ci]: https://github.com/bodsch/ansible-icinga2/actions
[issues]: https://github.com/bodsch/ansible-icinga2/issues?q=is%3Aopen+is%3Aissue
[releases]: https://github.com/bodsch/ansible-icinga2/releases


## Requirements & Dependencies

 - running mariadb / mysql database

### Operating systems

Tested on

* Debian 9 / 10
* Ubuntu 18.04 / 18.10 / 19.10
* CentOS 7 / 8
* Oracle Linux 8
* Arch Linux

## Contribution

Please read [Contribution](CONTRIBUTING.md)

## Development,  Branches (Git Tags)

The `master` Branch is my *Working Horse* includes the "latest, hot shit" and can be complete broken!

If you want to use something stable, please use a [Tagged Version](https://gitlab.com/bodsch/ansible-icinga2/-/tags)!


## Credits

- [Michael Friedrich](https://gitlab.com/dnsmichi)
- [Nicolai Buchwitz](https://gitlab.com/nbuchwitz)
- [Julien Tognazzi](https://gitlab.com/jtognazzi)
- [Carsten Köbke](https://gitlab.com/Mikeschova)
- and many others to make icinga2 what it is

---

Please read the following documention for configuration points.


## Documentation

- [Features](doc/09-features.md)
- [API Users](doc/10-api-users.md)
- [groups](doc/11-groups.md)
- [apply rules](doc/12-apply-rules.md)
- [downtimes](doc/13-downtimes.md)
- [check commands](doc/14-checkcommands.md)
- [master](doc/15-master.md)
- [satellite](doc/16-satellite.md)
- [Backup and Restore](doc/20-backup-restore.md)

---

## Examples

A complete test setup can be found in the GitLab under [icinga2-infrastructure](https://gitlab.com/icinga2-infrastructure/deployment).

### Icinga2 Master

#### single-master

```
---
- host: icinga-master
  vars:
    icinga2_ido:
      user: icinga2_ido
      password: icinga2_ido
      host: localhost
      cleanup:
        acknowledgements_age: 72h

    icinga2_api:
      user:
        icinga2:
          password: S0mh1TuFJI
          permissions: '*'

    icinga2_salt: 42T2fYT7bIxj5v291ajAW6kK0njvNMww8eWinBdEO5vh02xwC5qaNMMx77qNkYFE

    icinga2_masters:
      master-1.icinga.local:

    icinga2_host_object:
      master-1.icinga.local:
        endpoint_name: master-1.icinga.local
        zone: master
        display_name: master-1.icinga.local
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
          }
          services = [ "uptime", "memory" ]


  roles:
    - role: icinga2
```

#### multi-master

```
---
- host: icinga-master
  vars:
    icinga2_ido:
      user: icinga2_ido
      password: icinga2_ido
      host: localhost
      cleanup:
        acknowledgements_age: 72h

    icinga2_api:
      user:
        icinga2:
          password: S0mh1TuFJI
          permissions: '*'

    icinga2_salt: 42T2fYT7bIxj5v291ajAW6kK0njvNMww8eWinBdEO5vh02xwC5qaNMMx77qNkYFE

    icinga2_ha: true

    icinga2_masters:
      master-1.icinga.local:
        # type: primary
        ip: 192.168.130.20
        port: 5665
      master-2.icinga.local:
        ip: 192.168.130.21

  roles:
    - role: icinga2
```

### Icinga satellite

#### simple

```
---
- host: icinga-master
  vars:
    icinga2_mode: satellite

    icinga2_salt: 42T2fYT7bIxj5v291ajAW6kK0njvNMww8eWinBdEO5vh02xwC5qaNMMx77qNkYFE

    icinga2_masters:
      master-1.icinga.local:

    icinga2_host_object:

      satellite-1.icinga.local:
        endpoint_name: satellite-1.icinga.local
        zone: "{{ icinga2_satellite_zone }}"
        display_name: satellite-1.icinga.local
        import: generic-host
        address: '{{ ansible_default_ipv4.address }}'
        vars: |
          os = "Linux"
          dist = "{{ ansible_distribution }}"
          dist_ver = "{{ ansible_distribution_version }}"
          satellite = true
          disks = {
            "disk /" = {
              disk_partitions = "/"
            }
          }
          services = [ "uptime" ]

  roles:
    - role: icinga2
```

#### multi satellite with zones

```
---
- host: icinga-master
  vars:
    icinga2_mode: satellite

    icinga2_salt: 42T2fYT7bIxj5v291ajAW6kK0njvNMww8eWinBdEO5vh02xwC5qaNMMx77qNkYFE

    icinga2_masters:
      master-1.icinga.local:

    icinga2_satellites:
      zone1:
        satellite-1.icinga.local:
          ip: 192.168.130.30
        satellite-2.icinga.local:
          ip: 192.168.130.31

  roles:
    - role: icinga2
```


## tests

for testing

```
tox -e py38-ansible29 -- molecule

tox -e py38-ansible29 -- molecule -s icinga2-satellite
```

## Troubleshooting & Known issues


### API

```
export CURL_OPTS="--silent --insecure"
export ICINGA_CREDS="--user icinga2:S0mh1TuFJI"
export ICINGA_API_URL="https://master-1.icinga.local:5665/v1"
```
```
$ curl ${ICINGA_CREDS} ${CURL_OPTS} --header 'Accept: application/json' ${ICINGA_API_URL}/status/ApiListener | jq --raw-output ".results[].status.api.zones"
```

```
$ curl ${ICINGA_CREDS} ${CURL_OPTS} --header 'Accept: application/json' ${ICINGA_API_URL}/status/CIB | jq --raw-output '.results[].status.uptime'
```

```
$ curl ${ICINGA_CREDS} ${CURL_OPTS} --header 'Accept: application/json' ${ICINGA_API_URL}/status/ApiListener | jq --raw-output ".results[].status.api"
```

```
$ curl ${ICINGA_CREDS} ${CURL_OPTS} ${ICINGA_API_URL}/objects/hosts | jq
```

```
$ curl ${ICINGA_CREDS} ${CURL_OPTS} --header 'Accept: application/json' --header 'X-HTTP-Method-Override: GET' --request POST --data '{ "attrs": [ "name" ], "type": "Host", "filter": "host.name==\"master-1.icinga.local\"" }' ${ICINGA_API_URL}/objects/hosts
```


## License

BSD 2-clause
