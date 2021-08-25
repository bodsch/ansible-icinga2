# API users

## create API user

```yaml
icinga2_api:
  enabled: true
  user:
    icinga2:
      password: seCr3t
      permissions: '*'

    icingaweb:
      password: seCr3t_t00
      permissions:
        - "status/query"
        - "actions/*"
        - "objects/modify/*"
        - "objects/query/*"

    dashing:
      password: seCr3t_t00
      client_cn: NodeName
      permissions: '*'
```
