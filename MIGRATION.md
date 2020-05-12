# Migration Guide

## from 0.9.x to greater

### Icinga2 Master

`icinga2_master` is replaced with `icinga2_masters`

e.g.

old:
```
icinga2_master: "{{ ansible_fqdn }}"
```

new:
```
icinga2_masters:
  master-1.icinga.local:
    ip: 192.168.130.20
```



`icinga2_ido_*` is replaced with `icinga2_ido`

e.g.

old:
```
icinga2_ido_type: mysql
icinga2_ido_enabled: true
icinga2_ido_username: 'icinga2_ido'
icinga2_ido_password: 'icinga2_ido'
icinga2_ido_host: '127.0.0.1'
icinga2_ido_database: 'icinga2_ido'
icinga2_ido_port: 3306
icinga2_ido_socket: /run/mysqld.sock
```

new:
```
icinga2_ido:
  type: mysql
  enabled: true
  username: 'icinga2_ido'
  password: 'icinga2_ido'
  host: '127.0.0.1'
  database: 'icinga2_ido'
  port: 3306
  socket: /run/mysqld.sock
```

