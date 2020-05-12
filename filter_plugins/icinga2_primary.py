# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleParserError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display

# https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
# https://blog.oddbit.com/post/2019-04-25-writing-ansible-filter-plugins/

display = Display()

def filter_primary(mydict):
    seen = ''

    count = len(mydict.keys())

    display.vv("found: {} entries in {}".format(count, mydict))

    if(count == 1):
        k  = mydict.keys()
        keys = list(k)
#        display.v("key: {}".format(k))
#        display.v("{}".format(keys))
        seen = keys[0]
    else:
        for k, i in mydict.items():
            _type = None

            if(isinstance(i, dict)):
                _type = i.get('type', None)

            if(_type != None and _type == 'primary' ):
                seen = k
                break

    display.vv("found primary: {}".format(seen))

    if(seen == ''):
        k  = mydict.keys()
        keys = list(k)
        #display.v("key: {}".format(k))
        #display.v("{}".format(keys))
        seen = keys[0]

    display.v("return primary: {}".format(seen))

    return seen

class FilterModule(object):
    ''' Ansible file jinja2 tests '''

    def filters(self):
        return { 'primary_master' : filter_primary, }
