#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
from ansible.module_utils.basic import AnsibleModule
import re
__metaclass__ = type


DOCUMENTATION = '''
---
module: icinga2_features

short_description: Manage multiple Icinga2 features at once
description:
    - This module can be used to enable or disable more than on Icinga2 feature.
author: "Bodo Schulz <bodo@boone-schulz.de> (@schulzbo)"
options:
    features:
      type: list
      description:
      - This list conatins the feature names to enable or disable.
      required: True
    state:
      type: str
      description:
      - If set to C(present) and feature is disabled, then feature is enabled.
      - If set to C(present) and feature is already enabled, then nothing is changed.
      - If set to C(absent) and feature is enabled, then feature is disabled.
      - If set to C(absent) and feature is already disabled, then nothing is changed.
      choices: [ "present", "absent" ]
      default: present
'''

EXAMPLES = '''
- name: Enable ido-pgsql feature
  icinga2_features:
    feature:
      - ido-pgsql
    state: present

- name: Disable more features
  icinga2_features:
    feature:
      - perfdata
      - notification
      - livestatus
    state: absent

- name: Disable api feature
  icinga2_features:
    feature:
      - api
    state: absent
'''

RETURN = '''
#
'''


class Icinga2Features:
    """
    """

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module
        self._icinga2 = module.get_bin_path('icinga2', True)

        self.features = self.module.params.get('features')
        self.state = self.module.params.get('state')
        self.ignore_unknown = self.module.params.get('ignore_unknown')

    def run(self):
        """
        """
        result_state = []

        icinga2_features = self.list_features()

        if self.state == "present":
            """
            """
            for feature in self.features:
                """
                """
                if feature in icinga2_features.get("all"):
                    """
                    """
                    if feature in icinga2_features.get("enabled"):
                        """
                          already enabled
                        """
                        res = {}
                        res[feature] = dict(
                            changed=False,
                            state=f"feature {feature} already enabled."
                        )
                        result_state.append(res)

                        pass
                    if feature in icinga2_features.get("disabled"):
                        """
                          must be enabled
                        """

                        rc, out, err = self.handle_feature("enable", feature)

                        if rc == 0:
                            res = {}
                            res[feature] = dict(
                                changed=True,
                                state=f"feature {feature} successfuly enabled."
                            )
                            result_state.append(res)
                        else:
                            res = {}
                            res[feature] = dict(
                                failed=True,
                                state=f"feature {feature} could not be enabled."
                            )
                            result_state.append(res)
                        pass
                else:
                    """
                      unknow feature
                    """
                    res = {}
                    res[feature] = dict(
                        failed=True,
                        state=f"feature {feature} is unknown."
                    )
                    if not self.ignore_unknown:
                        result_state.append(res)

        else:
            """
            """
            for feature in self.features:
                """
                """
                if feature in icinga2_features.get("all"):
                    """
                    """
                    if feature in icinga2_features.get("disabled"):
                        """
                          already disabled
                        """
                        res = {}
                        res[feature] = dict(
                            changed=False,
                            state=f"feature {feature} already disabled."
                        )
                        result_state.append(res)

                    if feature in icinga2_features.get("enabled"):
                        """
                          must be disabled
                        """
                        rc, out, err = self.handle_feature("disable", feature)

                        if rc == 0:
                            res = {}
                            res[feature] = dict(
                                changed=True,
                                state=f"feature {feature} successfuly disabled."
                            )
                            result_state.append(res)
                        else:
                            res = {}
                            res[feature] = dict(
                                failed=True,
                                state=f"feature {feature} could not be disabled."
                            )
                            result_state.append(res)

                else:
                    """
                      unknow feature
                    """
                    res = {}
                    res[feature] = dict(
                        failed=True,
                        state=f"feature {feature} is unknown."
                    )
                    if not self.ignore_unknown:
                        result_state.append(res)

        # define changed for the running tasks
        # migrate a list of dict into dict
        combined_d = {key: value for d in result_state for key, value in d.items()}

        # find all changed and define our variable
        changed = (len({k: v for k, v in combined_d.items() if v.get('changed')}) > 0)
        # find all failed and define our variable
        failed = (len({k: v for k, v in combined_d.items() if v.get('failed')}) > 0)

        result = dict(
            changed=changed,
            failed=failed,
            state=result_state
        )

        return result

    def list_features(self):
        """
          - feature list (lists all available features)
        """
        _disabled = None
        _enabled = None
        _all = None

        # list all icinga2 features
        args = []
        args.append(self._icinga2)
        args.append('feature')
        args.append('list')

        rc, out, err = self._exec(args, False)

        if rc != 0:
            return dict(
                failed=True,
                msg="Unable to list icinga2 features.\nEnsure icinga2 is installed and present in binary path."
            )

        regex_disabled = re.compile(r"Disabled features: (?P<features_disabled>.*)")
        regex_enabled = re.compile(r"Enabled features: (?P<features_enabled>.*)")

        features_disabled = re.search(regex_disabled, out)
        features_enabled = re.search(regex_enabled, out)

        if features_disabled:
            _disabled = features_disabled.group('features_disabled')
        else:
            _disabled = ""

        if features_enabled:
            _enabled = features_enabled.group('features_enabled')
        else:
            _enabled = ""

        _all = _enabled + _disabled

        # features_ = sorted(_all.split(' '))
        features_disabled = sorted(_disabled.split(' '))
        features_enabled = sorted(_enabled.split(' '))

        return dict(
            all=_all,
            enabled=_enabled,
            disabled=_disabled
        )

    def handle_feature(self, state, feature):
        """
          - feature disable (disables specified feature)
          - feature enable (enables specified feature)
        """
        args = []
        args.append(self._icinga2)
        args.append('feature')
        args.append(state)
        args.append(feature)

        return self._exec(args, False)

    def _exec(self, commands, check_rc=True):
        """
          execute shell program
        """
        rc, out, err = self.module.run_command(commands, check_rc=check_rc)

        # self.module.log(msg=f"  rc : '{rc}'")
        # self.module.log(msg=f"  out: '{out}'")
        # self.module.log(msg=f"  err: '{err}'")

        return rc, out, err


def main():
    """
    """
    module = AnsibleModule(
        argument_spec=dict(
            features=dict(
                type='list',
                required=True
            ),
            state=dict(
                type='str',
                choices=["present", "absent"],
                default="present"
            ),
            ignore_unknown=dict(
                type='bool',
                required=False
            )
        ),
        supports_check_mode=True
    )

    module.run_command_environ_update = dict(
        LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C'
    )

    icinga = Icinga2Features(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


if __name__ == '__main__':
    main()
