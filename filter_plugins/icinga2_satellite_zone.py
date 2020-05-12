# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# https://blog.oddbit.com/post/2019-04-25-writing-ansible-filter-plugins/

display = Display()

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

def filter_primary(mydict, ansible_fqdn):
    seen = ansible_fqdn

    count = len(mydict.keys())

    display.vv("found: {} entries in {}".format(count, mydict))
    display.vv("search zone for '{}'".format(ansible_fqdn))

    for zone, zone_entries in mydict.items():
        _type = None

        keys     = zone_entries.keys()
        key_list = list(keys)
        found    = search(key_list, ansible_fqdn)

        display.vv("zone : {} -> values {} ({})".format(zone, key_list, found))

        if(found):
            seen = zone

    display.v("return zone '{}' for {}".format(seen, ansible_fqdn))

    return seen

class FilterModule(object):
    ''' Ansible file jinja2 tests '''

    def filters(self):
        return { 'satellite_zone' : filter_primary, }
