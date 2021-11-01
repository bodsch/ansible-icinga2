# python 3 headers, required if submitting to Ansible

from __future__ import (absolute_import, print_function)
__metaclass__ = type

import ipaddress

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
            'type': self.var_type,
            'has_valid_values': self.has_values
        }

    def var_type(self, var):
        '''
          Get the type of a variable
        '''
        return type(var).__name__

    def has_values(self, var):
        """

        """
        result = False
        result_value = var

        # display.v("var   : {} ({})".format(var, type(var)))

        if isinstance(var, int) and int(var) > 0:
            result = True
        if (isinstance(var, str) or type(var).__name__ == "AnsibleUnsafeText"):
          try:
            ip = ipaddress.ip_address(var)
            result_value = '{}'.format(str(var))
          except:
            result_value = '"{}"'.format(str(var))
          if len(var) > 0:
              result = True
        if isinstance(var, list) and len(var) > 0:
            result_value = "{}".format((', ').join(var))
            result = True

        # display.v(" = {} {}".format(result, result_value))

        return result, result_value
