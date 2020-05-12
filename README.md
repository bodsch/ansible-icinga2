# Icinga2 ansible role

Ansible role to setup Icinga2 master or satellite.

## Requirements & Dependencies

 - ansible role to deploy a mariadb

### Operating systems

Tested on

* Debian 9 / 10
* Ubuntu 16.04 / 18.04 / 18.10
* CentOS 7

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

## Example Playbook

Just include this role in your list.
For example

```
- host: icinga-master
  roles:
    - role: icinga2

- host: icinga-satellite
  roles:
    - role: icinga2
      vars:
        icinga2_mode: satellite
        icinga2_server: icinga-master
        icinga2_master: icinga.foo-bar.com
```

## Documentation

- [About](doc/01-about.md)
- [Features](doc/09-features.md)
- [API Users](doc/10-api-users.md)
- [groups](doc/11-groups.md)
- [apply rules](doc/12-apply-rules.md)
- [downtimes](doc/13-downtimes.md)
- [check commands](doc/14-checkcommands.md)
- [master](doc/15-master.md)
- [satellite](doc/16-satellite.md)
- [Backup and Restore](doc/20-backup-restore.md)


## tests

for testing

```
tox -e py38-ansible29 -- molecule

tox -e py38-ansible29 -- molecule -s icinga2-satellite
```

## Troubleshooting & Known issues

```
# icinga2 feature list
Disabled features: api command compatlog debuglog gelf graphite icingastatus opentsdb statusdata syslog
Enabled features: checker ido-mysql livestatus mainlog notification perfdata
```



## License

BSD 2-clause
