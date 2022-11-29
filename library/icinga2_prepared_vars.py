#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
import os
import re

from ansible.module_utils.basic import AnsibleModule


class Icinga2PreparedVars(object):
    """
    Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.default_file = module.params.get("default_file")
        self.variable = module.params.get("variable").upper()

        module.log(msg=f"default_file: {self.default_file}")
        module.log(msg=f"variable    : {self.variable}")

    def run(self):
        """
          runner
        """
        content = []
        pattern = re.compile(fr'.*{self.variable}:="(?P<var>[0-9A-Za-z]*)".*', re.MULTILINE)

        if os.path.isfile(self.default_file):
            with open(self.default_file, "r") as _data:
                content = _data.readlines()
        else:
            return dict(
                failed=True,
                msg=f"icinga2 is not correct installed. missing file {self.default_file}."
            )

        _list = list(filter(pattern.match, content))[0]  # Read Note
        result = re.search(pattern, _list)
        result = result.group(1)

        return dict(
            failed=False,
            value=result
        )

# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            default_file=dict(
                required=False,
                default='/usr/lib/icinga2/prepare-dirs'
            ),
            variable=dict(
                required=True
            ),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2PreparedVars(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
