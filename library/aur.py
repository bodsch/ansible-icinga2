#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import absolute_import, print_function


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import open_url

import re
import json
import tarfile
import os
import pwd
import grp
import os.path
import urllib.parse

from pathlib import Path


class Aur():
    """
      Main Class
    """
    module = None

    def __init__(self, module):
        """

        """
        self.module = module
        self.state = module.params.get("state")
        self.name = module.params.get("name")
        self.repository = module.params.get("repository")

        self.upgrade = module.params.get("upgrade")
        self.aur_only = module.params.get("aur_only")

        user = pwd.getpwuid(os.geteuid())
        owner = user.pw_name
        uid = user.pw_uid
        gid = user.pw_gid
        group = grp.getgrgid(gid).gr_name
        home = str(Path.home())

        self.pacman_binary = self.module.get_bin_path('pacman', True)
        self.git_binary = self.module.get_bin_path('git', True)

        # self.module.log(msg="  owner       : {} ({})".format(owner, uid))
        # self.module.log(msg="  group       : {} ({})".format(group, gid))
        # self.module.log(msg="  home        : {}".format(home))
        # self.module.log(msg="  current dir : {}".format(os.getcwd()))

    def run(self):
        """
          runner
        """
        installed, installed_version = self.package_installed(self.name)

        self.module.log(msg="  {} is installed: {} / {}".format(self.name, installed, installed_version))

        if installed and self.state == "absent":
            sudo_binary = self.module.get_bin_path('sudo', True)

            args = [sudo_binary]
            args.append(self.pacman_binary)
            args.append("--remove")
            args.append("--cascade")
            args.append("--recursive")
            args.append("--noconfirm")
            args.append(self.name)

            rc, out, err = self._exec(args)

            return dict(
                changed=True,
                msg="Package {} succesfull removed.".format(self.name)
            )

        if self.state == "present":
            if self.repository:
                rc, out, err, changed = self.install_from_repository(installed_version)
            else:
                rc, out, err, changed = self.install_from_aur()

            if rc == 0:
                return dict(
                    failed=False,
                    changed=changed,
                    msg="package {} succesfull installed.".format(self.name)
                )

        return dict(
            failed=False,
            changed=False,
            msg="It's all right. Keep moving! There is nothing to see!"
        )

    def package_installed(self, package):
        """
          Determine if the package is already installed
        """
        self.module.log(msg="= {function_name}({package})".format(function_name="package_installed", package=package))

        args = [self.pacman_binary]
        args.append("--query")
        args.append(package)

        rc, out, _ = self._exec(args, check=False)

        version_string = None
        if out:
            pattern = re.compile(r"icinga2 (?P<version>.*)-.*", re.MULTILINE)

            version = re.search(pattern, out)
            if version:
                version_string = version.group('version')

        return (rc == 0, version_string)

    def run_makepkg(self, directory):
        """
          run makepkg to build and install pakage
        """
        self.module.log(msg="= {function_name}({dir})".format(function_name="run_makepkg", dir=directory))
        self.module.log(msg="  current dir : {}".format(os.getcwd()))

        local_directory = os.path.exists(directory)

        if not local_directory:
            rc = 1
            out = None
            err = "no directory {} found".format(directory)
        else:
            makepkg_binary = self.module.get_bin_path('makepkg', required=True)

            args = [makepkg_binary]
            args.append("--syncdeps")
            args.append("--install")
            args.append("--noconfirm")
            args.append("--needed")
            args.append("--clean")

            rc, out, err = self._exec(args, check=True)

        return (rc, out, err)

    def install_from_aur(self):
        """
          use repository for installation
        """
        import tempfile

        _url = 'https://aur.archlinux.org/rpc/?v=5&type=info&arg={}'.format(urllib.parse.quote(self.name))

        self.module.log(msg="  url {}".format(_url))

        f = open_url(_url)

        result = json.dumps(json.loads(f.read().decode('utf8')))

        self.module.log(msg="  result {}".format(result))

        if result['resultcount'] != 1:
            return (1, '', 'package {} not found'.format(self.name))

        result = result['results'][0]

        self.module.log(msg="  result {}".format(result))

        f = open_url('https://aur.archlinux.org/{}'.format(result['URLPath']))

        with tempfile.TemporaryDirectory() as tmpdir:

            tar = tarfile.open(mode='r|*', fileobj=f)
            tar.extractall(tmpdir)
            tar.close()

            rc, out, err = self.run_makepkg(str(Path.home()))

        return (rc, out, err, True)

    def install_from_repository(self, installed_version):
        """
          use repository for installation
        """
        os.chdir(str(Path.home()))
        self.module.log(msg="  current dir : {}".format(os.getcwd()))

        local_directory = os.path.exists(self.name)

        if not local_directory:
            rc, out, err = self.git_clone(repository=self.repository)

            if rc != 0:
                err = "can't run 'git clone ...'"
                return (rc, out, err, False)

        os.chdir(self.name)

        if os.path.exists(".git"):
            """
              we can update the current repository
            """
            rc, out, err = self.git_pull()

            if rc != 0:
                err = "can't run 'git pull ...'"
                return (rc, out, err, False)

                return dict(
                    failed=True,
                    msg="can't run 'git pull ...'",
                    error=err
                )

        pkgbuild_file = "PKGBUILD"
        if not os.path.exists(pkgbuild_file):
            """
              whaaaat?
            """
            err = "can't found PKGBUILD"
            return (1, None, err)

            return dict(
                failed=True,
                msg="can't found PKGBUILD"
            )

        """
          read first 10 lines of file
        """
        with open(pkgbuild_file) as myfile:
            lines = [next(myfile) for x in range(10)]

        data = "".join(lines)
        pattern = re.compile(r"pkgver=(?P<version>.*)", re.MULTILINE)

        package_version = ""
        version = re.search(pattern, data)

        if version:
            package_version = version.group('version')

        if installed_version == package_version:
            return (0, "Version {} is already installed.".format(installed_version), None, False)
            return dict(
                changed=False,
                msg="Version {} are installed.".format(installed_version)
            )

        self.module.log(msg="new version: {}".format(package_version))

        """
          icinga2 scheint nicht installiert zu sein ...
          dann mal los ..
        """
        rc, out, err = self.run_makepkg(str(Path.home()))

        return (rc, out, err, True)

    def git_clone(self, repository):
        """
          simply git clone ...
        """
        if not self.git_binary:
            return (1, None, "not git found")

        args = [self.git_binary]
        args.append("clone")
        args.append(repository)
        args.append(self.name)

        rc, out, err = self._exec(args)

        return (rc, out, err)

    def git_pull(self):
        """
          simply git clone ...
        """
        if not self.git_binary:
            return (1, None, "not git found")

        args = [self.git_binary]
        args.append("pull")

        rc, out, err = self._exec(args)

        return (rc, out, err)

    def _exec(self, cmd, check=True):
        """
          execute shell commands
        """
        self.module.log(msg="= {function_name}({cmd})".format(function_name="_exec", cmd=cmd))

        rc, out, err = self.module.run_command(cmd, check_rc=check)

        if rc != 0:
            self.module.log(msg="  rc : '{}'".format(rc))
            self.module.log(msg="  out: '{}'".format(out))
            self.module.log(msg="  err: '{}'".format(err))

        return (rc, out, err)


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="present", choices=["present", "absent"]),
            repository=dict(required=False, type='str'),
            name=dict(required=False, type='str'),
            upgrade=dict(default=False, type="bool"),
            aur_only=dict(default=False, type="bool"),
        ),
        mutually_exclusive=[['name', 'upgrade']],
        required_one_of=[['name', 'upgrade']],
        supports_check_mode=True,
    )

    aur = Aur(module)
    result = aur.run()

    module.log(msg="= result: '{}'".format(result))

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
