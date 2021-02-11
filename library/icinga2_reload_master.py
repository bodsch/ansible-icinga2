#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)

from __future__ import print_function

from ansible.module_utils.basic import AnsibleModule

import time
import os
import fcntl
import errno
import signal


class SimpleFlock:
    """
      Provides the simplest possible interface to flock-based file locking.
      Intended for use with the `with` syntax.
      It will create/truncate/delete the lock file as necessary.
    """

    def __init__(self, path, timeout = None):
        self._path = path
        self._timeout = timeout
        self._fd = None

    def __enter__(self):
        self._fd = os.open(self._path, os.O_CREAT)
        start_lock_search = time.time()

        while True:
            try:
                fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                # Lock acquired!
                return
            except (OSError, IOError) as ex:
                if ex.errno != errno.EAGAIN:  # Resource temporarily unavailable
                    raise
                elif self._timeout is not None and time.time() > (start_lock_search + self._timeout):
                    # Exceeded the user-specified timeout.
                    raise

            # TODO It would be nice to avoid an arbitrary sleep here, but spinning
            # without a delay is also undesirable.
            time.sleep(0.1)

    def __exit__(self, *args):
        fcntl.flock(self._fd, fcntl.LOCK_UN)
        os.close(self._fd)
        self._fd = None

        # Try to remove the lock file, but don't try too hard because it is
        # unnecessary. This is mostly to help the user see whether a lock
        # exists by examining the filesystem.
        try:
            os.unlink(self._path)
        except Exception:
            pass


class Icinga2ReloadMaster(object):
    """
    Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module      = module

        self._icinga2    = module.get_bin_path('icinga2', True)
        self.requester   = module.params.get("requester")

        self.pid_file    = "/run/icinga2/icinga2.pid"
        self.lock_file   = "/run/icinga2/reload.lock"

    def run(self):
        ''' ... '''
        result = dict(
            failed = True,
            ansible_module_results = 'failed'
        )

        self.module.log(msg = "Acquiring lock...")

        with SimpleFlock(self.lock_file, 2):
            self.module.log(msg = "Lock acquired.")

            # pid = int(open(pid_file).read())

            pid = self._get_pid()

            if(pid is None):

                return dict(
                    failed = True,
                    msg = "pid file {pid} not found.".format(pid = self.pid_file)
                )

            self.module.log(msg = "= '{}'".format(pid))

            self.module.log(msg = "send SIGHUP")

            os.kill(pid, signal.SIGHUP)

            self.module.log(msg = "done")

            time.sleep(2)

            # rc, out, err = self._exec()
            # self.module.log(msg = "  rc : '{}'".format(rc))
            # self.module.log(msg = "  out: '{}'".format(out))
            # self.module.log(msg = "  err: '{}'".format(err))
            #
            # result['ansible_module_results'] = "Command returns {}".format(out)

            # if(rc == 0):
            #    result['failed'] = False

        self.module.log(msg = "Lock released.")

        result['failed'] = False

        return dict(
            failed = False
        )

    def _exec(self):
        '''   '''
        cmd = ['/usr/lib/icinga2/safe-reload', self._icinga2]

        self.module.log(msg = "cmd: {}".format(cmd))

        rc, out, err = self.module.run_command(cmd, check_rc=True)
        return rc, out, err

    def _get_pid(self):
        """
          split and flatten parameter list
          input:  ['--validate', '--log-level debug', '--config /etc/icinga2/icinga2.conf']
          output: ['--validate', '--log-level', 'debug', '--config', '/etc/icinga2/icinga2.conf']
        """

        try:
            with open(self.pid_file, "r") as inputFile:
                return int(inputFile.read().strip())
        except Exception:
            # No pid file --- maybe it was not running?
            self.module.log(msg = "File not found: {}".format(self.pid_file))
            return None


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec = dict(
            requester   = dict(required=True, type='str'),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2ReloadMaster(module)
    result = icinga.run()

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
