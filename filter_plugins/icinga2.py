# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# from ansible.errors import AnsibleError, AnsibleParserError
# from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# https://blog.oddbit.com/post/2019-04-25-writing-ansible-filter-plugins/

display = Display()


class FilterModule(object):
    """
        Ansible file jinja2 tests
    """

    def filters(self):
        return {
            'primary_master': self.filter_primary,
            'reorder_master': self.filter_reorder,
            'satellite_zone': self.satellite_zone
        }

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

    def filter_primary(self, mydict):
        seen = ''

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))

        if(count == 1):
            k = mydict.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            seen = keys[0]
        else:
            for k, i in mydict.items():
                _type = None

                if(isinstance(i, dict)):
                    _type = i.get('type', None)

                if(_type is not None and _type == 'primary'):
                    seen = k
                    break

        display.vv("found primary: {}".format(seen))

        if(seen == ''):
            k = mydict.keys()
            keys = list(k)
            display.v("key: {}".format(k))
            display.v("{}".format(keys))
            seen = keys[0]

        display.v("return primary: {}".format(seen))

        return seen

    """
      reorganize 'icinga2_masters' dict

      icinga2_masters:
        blackbox.matrix.lan:
          overwrite: icinga.boone-schulz.de

      to:

      icinga2_masters:
        icinga.boone-schulz.de:

    """

    def filter_reorder(self, mydict):
        seen = ''

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))

        seen = self.__transform(mydict)

        display.v("return reorder: {}".format(seen))

        return seen

    """

    """

    def satellite_zone(self, mydict, ansible_fqdn):
        seen = ansible_fqdn

        count = len(mydict.keys())

        display.vv("found: {} entries in {}".format(count, mydict))
        display.vv("search zone for '{}'".format(ansible_fqdn))

        for zone, zone_entries in mydict.items():
            keys = zone_entries.keys()
            key_list = list(keys)
            found = self.__search(key_list, ansible_fqdn)

            display.vv("zone : {} -> values {} ({})".format(zone, key_list, found))

            if(found):
                seen = zone

        display.v("return zone '{}' for {}".format(seen, ansible_fqdn))

        return seen

    """

    """

    def __transform(self, multilevelDict):

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

    """

    """

    def __search(self, list, fqdn):
        for i in range(len(list)):
            if list[i] == fqdn:
                return True
        return False
