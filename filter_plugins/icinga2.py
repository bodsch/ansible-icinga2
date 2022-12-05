# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'primary_master': self.filter_primary,
            'reorder_master': self.filter_reorder,
            'satellite_zone': self.satellite_zone,
            'apply_service_name': self.apply_service_name,
            'apply_notification': self.apply_notification,
            'dns_lookup': self.dns_lookup
        }

    def filter_primary(self, mydict):
        """
          return the primary icinga2 master

          icinga2_masters:
            blackbox.matrix.lan:
              type: primary
              ip: 192.168.0.5
            second:
              # overwrite: icinga.xanhaem.de
              ip: 192.168.10.10

          returns 'blackbox.matrix.lan'
        """
        seen = ''

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))

        if count == 1:
            k = mydict.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            seen = keys[0]
        else:
            for k, i in mydict.items():
                _type = None

                if isinstance(i, dict):
                    _type = i.get('type', None)

                if _type is not None and _type == 'primary':
                    seen = k
                    break

        display.vv("found primary: {}".format(seen))

        if seen == '':
            k = mydict.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            seen = keys[0]

        display.v("return primary: {}".format(seen))

        return seen

    def filter_reorder(self, mydict):
        """
          reorganize 'icinga2_masters' dict

          icinga2_masters:
            blackbox.matrix.lan:
              overwrite: icinga.boone-schulz.de

          to:

          icinga2_masters:
            icinga.boone-schulz.de:

        """
        seen = ''

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))

        seen = self.__transform(mydict)

        display.v("return reorder: {}".format(seen))

        return seen

    def satellite_zone(self, mydict, ansible_fqdn):
        seen = ansible_fqdn

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))
        display.vv("search zone for '{}'".format(ansible_fqdn))

        for zone, zone_entries in mydict.items():
            keys = zone_entries.keys()
            key_list = list(keys)
            found = self.__search(key_list, ansible_fqdn)

            display.vv("zone : {} -> values {} ({})".format(
                zone, key_list, found))

            if found:
                seen = zone

        display.v("return zone '{}' for {}".format(seen, ansible_fqdn))

        return seen

    def apply_service_name(self, data, default):
        """
        """
        display.v("apply_service_name({}, {})".format(data, default))

        result = ""
        _name = data.get('name', None)
        _for = data.get('for', None)

        if isinstance(_for, str) and isinstance(_name, str):
            result = '"{}" for {}'.format(_name, _for)
            _ = data.pop("name")
            _ = data.pop("for")
        elif isinstance(_name, str):
            result = '"{}"'.format(_name)
            _ = data.pop("name")
        else:
            result = '"{}"'.format(default)

        display.v("= result {}".format(result))

        return data, result

    def apply_notification(self, data, name):
        """
        """
        display.v("apply_notification({}, {})".format(data, name))

        notification_type = None
        valid_data = True

        data = data.get(name, {})

        notification_type = data.get('type', None)

        if notification_type:
            notification_type.capitalize()
            _ = data.pop('type')

        _users = data.get('users', None)
        _groups = data.get('user_groups', None)

        valid_users = (isinstance(_users, list) and len(_users) != 0) or (isinstance(_users, str) and len(_users) != 0)
        valid_groups = (isinstance(_groups, list) and len(_groups) != 0) or (isinstance(_groups, str) and len(_groups) != 0)

        if not valid_users and not valid_groups:
            valid_data = False
        else:
            if data.get('users') and _users is None:
                data.pop('users')
            if data.get('user_groups') and _groups is None:
                data.pop('user_groups')

        return data, notification_type, valid_data

    def dns_lookup(self, domain):
        """
        """
        from dns.exception import DNSException
        from dns.resolver import Resolver
        # from dns import reversename, query, zone

        def dns_lookup(input, timeout=3, server=""):
            """
              Perform a simple DNS lookup, return results in a dictionary
            """
            resolver = Resolver()
            resolver.timeout = float(timeout)
            resolver.lifetime = float(timeout)

            result = {}

            if server:
                resolver.nameservers = [server]
            try:
                records = resolver.resolve(input)
                result = {
                    "addrs": [ii.address for ii in records],
                    "error": "",
                    "name": input,
                }
            except DNSException as e:
                result = {
                    "addrs": [],
                    "error": repr(e),
                    "name": input,
                }

            return result

        # print(dns_lookup("boone-schulz.de"))
        # print(dns_lookup("satellite.matrix.lan"))

        return None

    def __transform(self, multilevelDict):
        """
        """
        new = {}

        for key, value in multilevelDict.items():

            display.v("key: {} == value: {}".format(key, value))

            if value is None:
                value = {}

            if value.get('overwrite'):
                new_key = value.get('overwrite')
                _ = value.pop('overwrite')
                new[new_key] = value
            else:
                new[key] = value

        return new

    def __search(self, list, fqdn):
        """
        """
        for i in range(len(list)):
            if list[i] == fqdn:
                return True
        return False
