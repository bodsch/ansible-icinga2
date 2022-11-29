#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause

from __future__ import absolute_import, division, print_function
import os

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.six.moves import configparser
from ansible.module_utils.mysql import mysql_driver, mysql_driver_fail_msg

# try:
#     import pymysql as mysql_driver
# except ImportError:
#     try:
#         import MySQLdb as mysql_driver
#     except ImportError:
#         mysql_driver = None
#
# mysql_driver_fail_msg = 'The PyMySQL (Python 2.7 and Python 3.X) or MySQL-python (Python 2.X) module is required.'


DOCUMENTATION = """
---
module: icinga2_ido_version.py
author:
    - 'Bodo Schulz'
short_description: returns the ido version from database.
description: ''
"""

EXAMPLES = """
- name: ensure, table_schema is present
  icinga2_ido_version:
    dba_host: ::1
    dba_user: root
    dba_password: password
"""

# ---------------------------------------------------------------------------------------


class Icinga2IdoVersion(object):
    """
      Main Class to implement the Icinga2 API Client
    """
    module = None

    def __init__(self, module):
        """
          Initialize all needed Variables
        """
        self.module = module

        self.dba_user = module.params.get("dba_user")
        self.dba_password = module.params.get("dba_password")
        self.dba_host = module.params.get("dba_host")
        self.dba_port = module.params.get("dba_port")
        self.dba_database = module.params.get("dba_database")
        self.database_config_file = module.params.get("database_config_file")

        self.db_connect_timeout = 30

    def run(self):
        """
          runner
        """
        state, ido_version = self._ido_version()

        res = dict(
            failed=False,
            exists=state,
            ido_version=ido_version
        )

        return res

    def _ido_version(self):
        """
          return IDO version from database
        """
        cursor, conn, error, message = self._mysql_connect()

        if error:
            return (False, error, message)

        query = f"select version from {self.dba_database}.icinga_dbversion"

        self.module.log(msg=f"query : {query}")

        failed = True
        ido_version = None

        try:
            cursor.execute(query)
            failed = False
        except mysql_driver.ProgrammingError as e:
            (errcode, message) = e.args

            self.module.log(msg=f"error code   : {errcode}")
            self.module.log(msg=f"error message: {message}")

            if errcode == 1146:
                pass
            else:
                self.module.fail_json(msg=f"Cannot execute query: {to_native(e)}")

        if not failed:
            ido_version, = cursor.fetchone()

        cursor.close()
        conn.close()

        self.module.log(msg=f"ido_version: {ido_version}")

        if ido_version:
            return True, ido_version

        return False, 0

    def _mysql_connect(self):
        """

        """
        config = {}

        config_file = self.database_config_file

        if config_file and os.path.exists(config_file):
            config['read_default_file'] = config_file

        # TODO
        # cp = self.__parse_from_mysql_config_file(config_file)

        config['host'] = self.dba_host
        config['port'] = self.dba_port

        # If dba_user or dba_password are given, they should override the
        # config file
        if self.dba_user is not None:
            config['user'] = self.dba_user
        if self.dba_password is not None:
            config['passwd'] = self.dba_password

        # self.module.log(msg="config : {}".format(config))

        if mysql_driver is None:
            self.module.fail_json(msg=mysql_driver_fail_msg)

        try:
            db_connection = mysql_driver.connect(**config)

        except Exception as e:
            message = "unable to connect to database. "
            message += "check login_host, login_user and login_password are correct "
            message += f"or {config_file} has the credentials. "
            message += f"Exception message: {to_native(e)}"

            self.module.log(msg=message)

            return (None, None, True, message)

        return (db_connection.cursor(), db_connection, False, "successful connected")

    def __parse_from_mysql_config_file(self, cnf):
        cp = configparser.ConfigParser()
        cp.read(cnf)
        return cp


# ---------------------------------------------------------------------------------------
# Module execution.
#

def main():
    ''' ... '''
    module = AnsibleModule(
        argument_spec=dict(
            dba_user=dict(type='str'),
            dba_password=dict(type='str', no_log=True),
            dba_host=dict(type='str', default='127.0.0.1'),
            dba_port=dict(type='int', default=3306),
            dba_database=dict(required=True, type='str'),
            database_config_file=dict(required=False, type='path'),
        ),
        supports_check_mode=False,
    )

    client = Icinga2IdoVersion(module)
    result = client.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
