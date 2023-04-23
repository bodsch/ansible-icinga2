# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.utils.display import Display
from ansible_collections.bodsch.core.plugins.module_utils.dns_lookup import dns_lookup

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'primary_master': self.filter_primary,
            'reorder_master': self.filter_reorder,
            'icinga_satellite_zone': self.satellite_zone,
            'apply_service_name': self.apply_service_name,
            'apply_notification': self.apply_notification,
            'host_object_values': self.host_object_values,
            'dns_icinga_primary': self.dns_primary,
            'dns_icinga_satellite': self.dns_satellite,
        }

    def filter_primary(self, data):
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
        result = ''

        count = len(data.keys())

        display.vv("found: {} entries in {}".format(count, data))

        if count == 1:
            k = data.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            result = keys[0]
        else:
            for k, i in data.items():
                _type = None

                if isinstance(i, dict):
                    _type = i.get('type', None)

                if _type is not None and _type == 'primary':
                    result = k
                    break

        display.vv("found primary: {}".format(result))

        if result == '':
            k = data.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            result = keys[0]

        display.v("return primary: {}".format(result))

        return result

    def filter_reorder(self, data):
        """
          reorganize 'icinga2_masters' dict

          icinga2_masters:
            blackbox.matrix.lan:
              overwrite: icinga.boone-schulz.de

          to:

          icinga2_masters:
            icinga.boone-schulz.de:

        """
        result = ''

        count = len(data.keys())

        display.vv(f"found: {count} entries in {data}")

        result = self.__transform(data)

        display.v(f"return reorder: {result}")

        return result

    def satellite_zone(self, data, fqdn):
        """
        """
        result = fqdn

        if isinstance(data, dict):

            count = len(data.keys())

            display.vv(f"found: {count} entries in {data}")
            display.vv(f"search zone for '{fqdn}'")

            for zone, zone_entries in data.items():
                keys = zone_entries.keys()
                key_list = list(keys)
                found = self.__search(key_list, fqdn)

                display.vv(f"zone : {zone} -> values {key_list} ({found})")

                if found:
                    result = zone

            display.v(f"return zone '{result}' for {fqdn}")

        return result

    def apply_service_name(self, data, default):
        """
        """
        display.v(f"apply_service_name({data}, {default})")

        result = ""
        _name = data.get('name', None)
        _for = data.get('for', None)

        if isinstance(_for, str) and isinstance(_name, str):
            result = f'"{_name}" for {_for}'
            _ = data.pop("name")
            _ = data.pop("for")
        elif isinstance(_name, str):
            result = f'"{_name}"'
            _ = data.pop("name")
        else:
            result = f'"{default}"'

        display.v(f"= result {result}")

        return data, result

    def apply_notification(self, data, name):
        """
        """
        display.v(f"apply_notification({data}, {name})")

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

    def host_object_values(self, data, primary, key, ansible_fqdn):
        """
        """
        _data = data.copy()

        endpoint = False
        endpoint_name = _data.get('endpoint_name', None)
        zone = _data.get('zone', None)
        display_name = _data.get('display_name', None)
        check_command = _data.get('check_command', None)
        address = _data.get('address', None)

        if endpoint_name:
            data.pop("endpoint_name")
            endpoint = True
        else:
            endpoint_name = key
        if zone:
            data.pop("zone")
        else:
            zone = ansible_fqdn
        if display_name:
            data.pop("display_name")
        if check_command:
            data.pop("check_command")
        if address:
            data.pop("address")

        return data, endpoint, endpoint_name, zone, display_name, check_command, address

    def dns_primary(self, data, object_name, object_data, alternatives=[]):
        """
            dns_primary({'instance': None}, [None, 'instance'])
        """
        display.v(f"dns_primary({data}, {object_name}, {object_data}, {alternatives})")

        result = None

        endpoint_name = object_data.get('endpoint_name', None)
        address = object_data.get('address', None)

        display.v(f"  - endpoint_name {endpoint_name}")
        display.v(f"  - address   {address}")

        if not endpoint_name:
            endpoint_name = object_name

        if address:
            result = address

        if not result:
            # try a given IP in 'icinga2_masters' for endpoint
            if isinstance(data, dict):
                primary_ip = data.get(endpoint_name, {}).get("ip", None)
                if primary_ip:
                    result = primary_ip

        if not result:
            result = self.__dns_alternatives(alternatives)

        display.v(f" = result {result}")

        return result

    def dns_satellite(self, data, object_name, object_data, satellite_zone, alternatives=[]):
        """
        """
        # display.v(f"dns_satellite({data}, {object_name}, {object_data}, {satellite_zone}, {alternatives})")

        result = None

        endpoint_name = object_data.get('endpoint_name', None)
        address = object_data.get('address', None)

        # display.v(f"  - endpoint_name {endpoint_name}")
        # display.v(f"  - address   {address}")

        if not endpoint_name:
            endpoint_name = object_name

        if address:
            result = address

        if not result:
            # try a given IP in 'icinga2_satellites' for icinga2_satellite_zone
            if isinstance(object_data, dict):
                primary_ip = object_data.get(satellite_zone, {}).get(object_name, {}).get("ip", None)
                if primary_ip:
                    result = primary_ip

        if not result:
            result = self.__dns_alternatives(alternatives)

        # display.v(f" = result {result}")

        return result

    def __transform(self, multilevelDict):
        """
        """
        new = {}

        for key, value in multilevelDict.items():

            display.v(f"key: {key} == value: {value}")

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

    def __dns_alternatives(self, alternatives=[]):
        """
        """
        # remove empty elements
        alternatives = [x for x in alternatives if x is not None]

        for n in alternatives:
            r = dns_lookup(n)

            display.v(f"  -> {r}")

            resolve_error = r.get("error", True)
            if not resolve_error:
                result = r.get("dns_name", [])

                if len(result) > 0:
                    display.v("  multiple DNS entries are a problem!")
                    display.v("  you should configure 'icinga2_satellites' properly")

                result = result[0]
                break

        display.v(f" = result {result}")

        return result
