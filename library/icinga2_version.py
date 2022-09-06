#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
import re

from ansible.module_utils.basic import AnsibleModule


class Icinga2Version(object):
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._icinga2 = module.get_bin_path('icinga2', True)

    def run(self):
        """
          runner
        """
        result = dict(
            rc=127,
            failed=True,
            changed=False,
        )

        args = []
        args.append(self._icinga2)
        args.append("--version")

        self.module.log(msg=f"  args: '{args}'")

        rc, out, err = self._exec(args, False)

        version_string = "unknown"

        # debian:
        #  "icinga2 - The Icinga 2 network monitoring daemon (version: r2.12.3-1)"
        # CentOS Linux:
        #  "icinga2 - The Icinga 2 network monitoring daemon (version: 2.12.3)"
        pattern_1 = re.compile(r"icinga2.*\(.*version: (?P<version>.*).*\)")
        pattern_2 = re.compile(r"(?P<version>(\d+\.)?(\d+\.)?(\*|\d+))")

        version = re.search(pattern_1, out)

        if version:
            version = re.search(pattern_2, version.group('version'))
            version_string = version.group('version')

        result['rc'] = rc

        if rc == 0:
            result['failed'] = False
            result['version'] = version_string

        return result

    def _exec(self, commands, check_rc=True):
        """
          execute shell program
        """
        rc, out, err = self.module.run_command(commands, check_rc=check_rc)

        # self.module.log(msg=f"  rc : '{rc}'")
        # self.module.log(msg=f"  out: '{out}'")
        # self.module.log(msg=f"  err: '{err}'")

        return rc, out, err


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2Version(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
