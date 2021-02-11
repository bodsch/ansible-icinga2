#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, division, print_function
import re

from ansible.module_utils.basic import AnsibleModule


class Icinga2Version(object):
    """
    Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module       = module

        self._icinga2     = module.get_bin_path('icinga2', True)

    def run(self):
        ''' ... '''
        result = dict(
            rc = 127,
            failed = True,
            changed = False,
        )

        rc, out, err = self._exec(['--version'])
        self.module.log(msg = "  rc : '{}'".format(rc))
        self.module.log(msg = "  out: '{}' ({})".format(out, type(out)))
        self.module.log(msg = "  err: '{}'".format(err))

        # icinga2 - The Icinga 2 network monitoring daemon (version: r2.12.3-1)
        pattern = re.compile(r"icinga2.*\(.*r(?P<version>.*)-.*\)")
        version = re.search(pattern, out)
        version = version.group(1)

        self.module.log(msg = "version: {}".format(version))

        result['rc'] = rc

        if(rc == 0):

            result['failed'] = False
            result['version'] = version

        return result

    def _exec(self, args):
        '''   '''
        cmd = [self._icinga2] + args

        self.module.log(msg = "cmd: {}".format(cmd))

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec = dict(
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2Version(module)
    result = icinga.run()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
