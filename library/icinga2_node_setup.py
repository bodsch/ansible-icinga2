#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
# import json
import os

from ansible.module_utils.basic import AnsibleModule

# import urllib3
# from requests import Session


class Icinga2NodeSetupHelper(object):
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

        self.lib_directory = "/var/lib/icinga2"

        self.hostname = module.params.get("hostname")
        self.common_name = module.params.get("common_name")
        self.trustedcert = module.params.get("trustedcert")
        self.ca_key = module.params.get("ca_key")
        self.ticket = module.params.get("ticket")
        self.parent_host = module.params.get("parent_icinga2_host")
        self.parent_port = module.params.get("parent_icinga2_port")
        self.zone = module.params.get("zone")
        self.endpoint = module.params.get("endpoint")
        self.force = module.params.get("force")

        # module.log(msg="icinga2     : {}".format(self._icinga2))
        # module.log(msg="hostname    : {}".format(self.hostname))
        # module.log(msg="common_name : {}".format(self.common_name))
        # module.log(msg="trustedcert : {}".format(self.trustedcert))
        # module.log(msg="ca_key      : {}".format(self.ca_key))
        # module.log(msg="ticket      : {}".format(self.ticket))
        # module.log(msg="parent_host : {}".format(self.parent_host))
        # module.log(msg="parent_port : {}".format(self.parent_port))
        # module.log(msg="zone        : {}".format(self.zone))
        # module.log(msg="endpoint    : {}".format(self.endpoint))
        # module.log(msg="force       : {} ({})".format(self.force, type(self.force)))

    def run(self):
        ''' ... '''
        result = dict(
            failed=False,
            changed=False,
            ansible_module_results="none"
        )

        if (self.force):
            self.module.log(msg="force mode ...")

            self._remove_directory(os.path.join(self.lib_directory, 'ca'))
            self._remove_directory(os.path.join(self.lib_directory, 'certs'))

        # Creates a new Certificate Signing Request, a self-signed X509 certificate or both.
        # icinga2 pki new-cert
        #   --cn {{ icinga2_certificate_cn }}
        #   --key {{ icinga2_pki_dir }}/{{ inventory_hostname }}.key
        #   --cert {{ icinga2_pki_fqdn_cert }}

        self.module.log(msg="Creates a new Certificate Signing Request, a self-signed X509 certificate or both.")

        key = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.key'))
        cert = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.crt'))

        self.module.log(msg=f"  key  : '{key}'")
        self.module.log(msg=f"  cert : '{cert}'")

        if (not os.path.isfile(key) and not os.path.isfile(cert)):
            rc, out = self._exec([
                "new-cert",
                "--cn", f"{self.common_name}",
                "--key", f"{key}",
                "--cert", f"{cert}"
            ])
            self.module.log(msg=f"  rc : '{rc}'")
            self.module.log(msg=f"  out: '{out}'")

            result['ansible_module_results'] = f"Command returns {out}"

            if (rc == 0):
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            result['ansible_module_results'] = "skip, key and cert already created"
            self.module.log(msg="skip, key and cert already created")

        # Saves another Icinga 2 instance's certificate.
        # icinga2 pki save-cert
        #   --trustedcert {{ icinga2_pki_master_cert }}
        #   --host {{ icinga2_primary_master }}

        self.module.log(msg="Saves another Icinga 2 instance's certificate.")

        key = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.key'))
        cert = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.crt'))
        trusted_master = os.path.join(os.path.join(self.lib_directory, 'certs', 'trusted-master.crt'))

        self.module.log(msg=f"  key     : '{key}'")
        self.module.log(msg=f"  cert    : '{cert}'")
        self.module.log(msg=f"  trusted : '{trusted_master}'")

        if (not os.path.isfile(trusted_master)):
            rc, out = self._exec([
                "pki",
                "save-cert",
                "--trustedcert", f"{trusted_master}",
                "--host", f"{self.parent_host}"
            ])
            self.module.log(msg=f"  rc : '{rc}'")
            self.module.log(msg=f"  out: '{out}'")

            result['ansible_module_results'] = f"Command returns {out}"

            if (rc == 0):
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            result['ansible_module_results'] = "skip, key and csr already created"
            self.module.log(msg="skip, key and csr already created")

        # Sends a PKI request to Icinga 2.
        # icinga2 pki request
        #   --host {{ icinga2_primary_master }}
        #   --port {{ icinga2_master_port | default(5665) }}
        #   --ticket {{ icinga2_fqdn_ticket }}
        #   --key {{ icinga2_pki_fqdn_key }}
        #   --cert {{ icinga2_pki_fqdn_cert }}
        #   --trustedcert {{ icinga2_pki_master_cert }}
        #   --ca {{ icinga2_pki_ca_key }}

        self.module.log(msg="Sends a PKI request to Icinga 2.")

        key = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.key'))
        cert = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.crt'))
        ca_key = os.path.join(os.path.join(self.lib_directory, 'certs', 'ca.key'))
        trusted_master = os.path.join(os.path.join(self.lib_directory, 'certs', 'trusted-master.crt'))

        self.module.log(msg=f"  key     : '{key}'")
        self.module.log(msg=f"  cert    : '{cert}'")
        self.module.log(msg=f"  ca.key  : '{ca_key}'")
        self.module.log(msg=f"  trusted : '{trusted_master}'")

        if (not os.path.isfile(ca_key) and not os.path.isfile(trusted_master)):
            rc, out = self._exec([
                "pki",
                "request",
                "--key", f"{key}",
                "--cert", f"{cert}",
                "--ca", f"{ca_key}",
                "--trustedcert", f"{trusted_master}",
                "--host", f"{self.parent_host}",
                "--port", f"{self.parent_port}",
                "--ticket", f"{self.ticket}"
            ])
            self.module.log(msg=f"  rc : '{rc}'")
            self.module.log(msg=f"  out: '{out}'")

            result['ansible_module_results'] = f"Command returns {out}"

            if (rc == 0):
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            msg = "skip, ca.key and trusted-master.crt already created"
            result['ansible_module_results'] = msg
            self.module.log(msg=msg)

        # Sets up an Icinga 2 node.
        # icinga2 node setup
        #   --ticket {{ icinga2_fqdn_ticket }}
        #   --endpoint {{ icinga2_primary_master }}
        #   --zone {{ ansible_fqdn }}
        #   --parent_host {{ icinga2_primary_master }}
        #   --trustedcert {{ icinga2_pki_master_cert }}

        self.module.log(msg="Sets up an Icinga 2 node.")

        key = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.key.orig'))
        cert = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.common_name}.crt.orig'))
        # ca_key = os.path.join(os.path.join(self.lib_directory, 'certs', 'ca.key'))
        trusted_master = os.path.join(os.path.join(self.lib_directory, 'certs', 'trusted-master.crt'))
        saved_ticket = os.path.join(os.path.join(self.lib_directory, 'certs', 'ticket'))

        self.module.log(msg=f"  ticket     : '{self.ticket}'")
        self.module.log(msg=f"  endpoint   : '{self.endpoint}'")
        self.module.log(msg=f"  zone       : '{self.zone}'")
        self.module.log(msg=f"  parent_host: '{self.parent_host}'")
        self.module.log(msg=f"  trusted    : '{trusted_master}'")

        if (not os.path.isfile(saved_ticket) and not os.path.isfile(key) and not os.path.isfile(cert)):
            rc, out = self._exec([
                "node",
                "setup",
                "--ticket", f"{self.ticket}",
                "--endpoint", f"{self.endpoint}",
                "--zone", f"{self.zone}",
                "--parent_host", f"{self.parent_host}",
                "--trustedcert", f"{trusted_master}"
            ])
            self.module.log(msg=f"  rc : '{rc}'")
            self.module.log(msg=f"  out: '{out}'")

            result['ansible_module_results'] = f"Command returns {out}"

            if (rc == 0):
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            msg = "skip, node already created"
            result['ansible_module_results'] = msg
            self.module.log(msg=msg)

        return result

    """

    """

    def _exec(self, args):
        '''   '''
        cmd = [self._icinga2] + args

        self.module.log(msg=f"cmd: {cmd}")

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        return rc, out

    def _remove_directory(self, directory):
        ''' .... '''
        self.module.log(msg=f"remove directory {directory}")

        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="present", choices=["absent", "present"]),
            # hostname     = dict(required=True),
            common_name=dict(required=True),
            # trustedcert  = dict(required=True),
            ca_key=dict(required=True),
            ticket=dict(required=True),
            parent_icinga2_host=dict(required=True),
            parent_icinga2_port=dict(required=False, default='5665'),
            zone=dict(required=True),
            endpoint=dict(required=True),
            force=dict(required=False, default=False, type='bool'),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2NodeSetupHelper(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
