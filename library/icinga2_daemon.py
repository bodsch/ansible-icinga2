#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule


class Icinga2Daemon(object):
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
        self.parameters = module.params.get("parameters")

    def run(self):
        """
          runner
        """
        result = dict(
            failed=True,
            ansible_module_results='failed'
        )

        # # icinga2 daemon --validate --log-level debug --config /etc/icinga2/icinga2.conf

        parameter_list = [self._icinga2]
        parameter_list.append("daemon")
        parameter_list += self.flatten_parameter(self.parameters)

        rc, out, err = self._exec(parameter_list)

        result['ansible_module_results'] = "Command returns {out}"

        if rc == 0:
            result['failed'] = False

        return result

    def _exec(self, command):
        """
          execute commands
        """
        # self.module.log(msg="command: {}".format(command))

        rc, out, err = self.module.run_command(command, check_rc=True)
        # self.module.log(msg="  rc : '{}'".format(rc))
        # self.module.log(msg="  out: '{}'".format(out))
        # self.module.log(msg="  err: '{}'".format(err))
        return rc, out, err

    def flatten_parameter(self, arr):
        """
          split and flatten array
          input:  ['--validate', '--log-level debug', '--config /etc/icinga2/icinga2.conf']
          output: ['--validate', '--log-level', 'debug', '--config', '/etc/icinga2/icinga2.conf']
        """
        parameters = []

        for _parameter in arr:
            if (' ' in _parameter):
                _list = _parameter.split(' ')
                for _element in _list:
                    parameters.append(_element)
            else:
                parameters.append(_parameter)

        return parameters


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            parameters=dict(required=True, type='list'),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2Daemon(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
