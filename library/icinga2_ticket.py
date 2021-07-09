#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
# import json
# import os

from ansible.module_utils.basic import AnsibleModule

# import urllib3
# from requests import Session


class Icinga2TicketHelper(object):
    """
    Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.common_name = module.params.get("common_name")
        self.salt = module.params.get("salt")

        self._icinga2 = module.get_bin_path('icinga2', True)
        # module.log(msg="icinga2     : {}".format(self._icinga2))
        # module.log(msg="common_name : {}".format(self.common_name))
        # module.log(msg="salt        : {}".format(self.salt))

    def run(self):
        """
          runner
        """
        result = dict(
            failed=False,
            changed=False,
            ansible_module_results="none"
        )

        # Generates an Icinga 2 ticket
        self.module.log(msg="Generates an Icinga 2 ticket.")

        args = [self._icinga2]
        args.append("pki")
        args.append("ticket")
        args.append("--cn")
        args.append(self.common_name)
        args.append("--salt")
        args.append(self.salt)

        rc, out = self._exec(args)

        result['ticket'] = "{}".format(out.rstrip())

        if rc == 0:
            result['changed'] = True
        else:
            result['failed'] = True

        return result

    def _exec(self, commands):
        """
          execute shell program
        """
        rc, out, err = self.module.run_command(commands, check_rc=True)
        return rc, out


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            common_name=dict(required=True),
            salt=dict(required=True)
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2TicketHelper(module)
    result = icinga.run()

    module.log(msg="= result: {}".format(result))

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
