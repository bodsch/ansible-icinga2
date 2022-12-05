#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

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

    def __init__(self, path, timeout=None):
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
            except (OSError, IOError, BlockingIOError) as ex:
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
      Main Class
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self._icinga2 = module.get_bin_path('icinga2', True)
        self.requester = module.params.get("requester")
        self.wait = module.params.get("wait")
        self.timeout = module.params.get("timeout")

        self.pid_file = "/run/icinga2/icinga2.pid"
        self.lock_file = "/run/icinga2/reload.lock"

    def run(self):
        """
          runner
        """
        running_icinga2 = self.check_running_process()

        if not running_icinga2:
            return dict(
                failed=True,
                msg="missing running icinga2 process."
            )

        self.module.log(msg="Acquiring lock...")

        with SimpleFlock(self.lock_file, self.timeout):
            self.module.log(msg="Lock acquired.")

            pid = self._get_pid()

            if not pid:
                return dict(
                    failed=True,
                    msg=f"pid file {self.pid_file} not found."
                )

            self.module.log(msg="send SIGHUP")
            os.kill(pid, signal.SIGHUP)
            self.module.log(msg="done")

            time.sleep(int(self.wait))

        self.module.log(msg="Lock released.")

        return dict(
            failed=False,
            changed=False,
            msg="process reloaded"
        )

    def check_running_process(self):
        """
            Check if there is any running process that contains the given name processName.
        """
        import psutil

        running_proccesses = psutil.process_iter()
        # Iterate over the all the running process
        for proc in running_proccesses:
            # self.module.log(msg=f"running_proccess: {proc.name()}")
            try:
                # Check if process name contains the given name string.
                if "icinga2" in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False

    def _get_pid(self):
        """
        """
        try:
            with open(self.pid_file, "r") as inputFile:
                return int(inputFile.read().strip())
        except Exception:
            # No pid file --- maybe it was not running?
            self.module.log(msg=f"File not found: {self.pid_file}")
            return None


# ===========================================
# Module execution.
#


def main():

    module = AnsibleModule(
        argument_spec=dict(
            requester=dict(
                required=True,
                type='str'
            ),
            wait=dict(
                required=False,
                type='int',
                default=2
            ),
            timeout=dict(
                required=False,
                type='int',
                default=2
            ),
        ),
        supports_check_mode=True,
    )

    icinga = Icinga2ReloadMaster(module)
    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
