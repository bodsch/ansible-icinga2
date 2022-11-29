#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
import os

from ansible.module_utils.basic import AnsibleModule


class Icinga2CaHelper(object):
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
        self.key_file = module.params.get("key_file")
        self.csr_file = module.params.get("csr_file")
        self.cert_file = module.params.get("cert_file")
        self.force = module.params.get("force")

        # module.log(msg="icinga2     : {} ({})".format(self._icinga2, type(self._icinga2)))
        # module.log(msg="hostname    : {} ({})".format(self.hostname, type(self.hostname)))
        # module.log(msg="common_name : {} ({})".format(self.common_name, type(self.common_name)))
        # module.log(msg="key_file    : {} ({})".format(self.key_file, type(self.key_file)))
        # module.log(msg="csr_file    : {} ({})".format(self.csr_file, type(self.csr_file)))
        # module.log(msg="cert_file   : {} ({})".format(self.cert_file, type(self.cert_file)))
        # module.log(msg="force       : {} ({})".format(self.force, type(self.force)))

    def run(self):
        """
          runner
        """
        result = dict(
            failed=False,
            changed=False,
            ansible_module_results="none"
        )

        if (self.force):
            self.module.log(msg="force mode ...")

            self._remove_directory(os.path.join(self.lib_directory, 'ca'))
            self._remove_directory(os.path.join(self.lib_directory, 'certs'))

        # Sets up a new Certificate Authority.
        # icinga2 pki new-ca

        self.module.log(msg="Sets up a new Certificate Authority.")

        key = os.path.join(os.path.join(self.lib_directory, 'ca', 'ca.key'))
        cert = os.path.join(os.path.join(self.lib_directory, 'ca', 'ca.cert'))

        # self.module.log(msg="  key  : '{}'".format(key))
        # self.module.log(msg="  cert : '{}'".format(cert))

        if not os.path.isfile(key) and not os.path.isfile(key):

            args = [self._icinga2]
            args.append("pki")
            args.append("new-ca")

            rc, out, err = self._exec(args)

            result['ansible_module_results'] = f"Command returns {out}"

            if rc == 0:
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            result['ansible_module_results'] = "CA already exists"
            self.module.log(msg="skip, CA already exists")

        # Creates a new Certificate Signing Request, a self-signed X509 certificate or both.
        # icinga2 pki new-cert
        #   --cn {{ icinga2_certificate_cn }}
        #   --key {{ icinga2_pki_dir }}/{{ inventory_hostname }}.key
        #   --csr {{ icinga2_pki_dir }}/{{ inventory_hostname }}.csr

        self.module.log(msg="Creates a new Certificate Signing Request, a self-signed X509 certificate or both.")

        key = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.hostname}.key'))
        csr = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.hostname}.csr'))
        cert = os.path.join(os.path.join(self.lib_directory, 'certs', f'{self.hostname}.crt'))

        # self.module.log(msg="  key  : '{}'".format(key))
        # self.module.log(msg="  csr  : '{}'".format(csr))
        # self.module.log(msg="  cert : '{}'".format(cert))

        if not os.path.isfile(csr):
            args = [self._icinga2]
            args.append("pki")
            args.append("new-cert")
            args.append("--cn")
            args.append(self.common_name)
            args.append("--key")
            args.append(key)
            args.append("--csr")
            args.append(csr)

            rc, out, err = self._exec(args)
            # self.module.log(msg="  rc : '{}'".format(rc))
            # self.module.log(msg="  out: '{}'".format(out))

            result['ansible_module_results'] = f"Command returns {out}"

            if rc == 0:
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            result['ansible_module_results'] = "skip, csr already created"
            self.module.log(msg="skip, csr already created")

        # Reads a Certificate Signing Request from stdin and prints a signed certificate on stdout.
        # icinga2 pki sign-csr
        #   --csr {{ icinga2_pki_dir }}/{{ inventory_hostname }}.csr
        #   --cert {{ icinga2_pki_dir }}/{{ inventory_hostname }}.crt
        self.module.log(msg="Reads a Certificate Signing Request from stdin and prints a signed certificate on stdout.")

        if (not os.path.isfile(cert)):
            args = [self._icinga2]
            args.append("pki")
            args.append("sign-csr")
            args.append("--csr")
            args.append(csr)
            args.append("--cert")
            args.append(cert)

            rc, out, err = self._exec(args)
            # self.module.log(msg="  rc : '{}'".format(rc))
            # self.module.log(msg="  out: '{}'".format(out))

            result['ansible_module_results'] = f"Command returns {out}"

            if rc == 0:
                result['changed'] = True
            else:
                result['failed'] = True

        else:
            result['ansible_module_results'] = "skip, cert already created."
            self.module.log(msg="skip, cert already created.")

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
            hostname=dict(required=True),
            common_name=dict(required=True),
            key_file=dict(required=False),
            csr_file=dict(required=False),
            cert_file=dict(required=False),
            force=dict(required=False, default=False, type='bool'),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2CaHelper(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
