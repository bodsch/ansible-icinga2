#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) 2020-2022, Bodo Schulz <bodo@boone-schulz.de>
# BSD 2-clause (see LICENSE or https://opensource.org/licenses/BSD-2-Clause)
# SPDX-License-Identifier: BSD-2-Clause
#
# My thanks go to Thilo Wening and Nicolai Buchwitz for their input and support!

from __future__ import absolute_import, division, print_function
import json
# import os

from ansible.module_utils.basic import AnsibleModule
# from ansible.module_utils.urls import fetch_url, url_argument_spec

import urllib3
from requests import Session

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '0.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: icinga2_downtime

short_description: A module to deploy downtimes using the Icinga 2 API

description: The module to schedule and remove downtimes at hosts and their services.

version_added: "0.1.0"
author: "Bodo Schulz (bodo@boone-schulz.de)"
options:
    hostname:
      description: The name of the host this comment belongs to.
      required: true
      type: string

    state:
      description: Choose between present and absent.
      required: false
      type: string
      default: present

    start_time:
      description: Timestamp marking the beginning of the downtime.
      required: true
      type: string

    end_time:
      description: Timestamp marking the end of the downtime.
      required: true
      type: string

    duration
      description: |
        Required for flexible downtimes.
        Duration of the downtime in seconds if fixed is set to false.
      required: true
      type: int

    all_services
      description: |
        Sets downtime for all services for the matched host objects.
        If child_options are set, all child hosts and their services will schedule a downtime too.
      default: false
      type: bool
      default: false

    author
      description: Name of the author.
      required: false
      type: string
      default: ansible

    comment
      description: A comment to show in the Icinga Web 2 interface.
      required: false
      type: string
      default: generated downtime

    fixed
      description: If true, the downtime is fixed otherwise flexible.
      default: false
      type: bool
      default: false

'''

EXAMPLES = r"""
- name: set downtime
  icinga2_downtime:
    host: "https://localhost"
    username: "ansible"
    password: "a_secret"
    hostname: "satellite-1"
    duration: "{{ icinga2_downtime_duration }}"
    start_time: "{{ downtime_start }}"
    end_time: "{{ downtime_end }}"
    state: present
  delegate_to: "master-1.icinga.local"
  vars:
    icinga2_downtime_duration: 10
    downtime_start: "{{ ansible_date_time.epoch }}"
    downtime_end: "{{ downtime_start | int + icinga2_downtime_duration * 60 }}"

- name: schedule downtime
  icinga2_downtime:
    host: "https://localhost"
    username: "ansible"
    password: "a_secret"
    hostnames:
        - satellite-1
        - satellite-2
        - satellite-9
    duration: "{{ icinga2_downtime_duration }}"
    start_time: "{{ downtime_start }}"
    end_time: "{{ downtime_end }}"
    state: present
  delegate_to: "master-1.icinga.local"
  vars:
    icinga2_downtime_duration: 10
    downtime_start: "{{ ansible_date_time.epoch }}"
    downtime_end: "{{ downtime_start | int + icinga2_downtime_duration * 60 }}"
"""

RETURN = r"""
name:
    description: The name used to create, modify or delete the host
    type: str
    returned: always
data:
    description: The data structure used for create, modify or delete of the host
    type: dict
    returned: always
"""


class Icinga2Api(object):
    """
      Main Class
    """
    module = None

    def __init__(self):
        """
          Initialize all needed Variables
        """
        self.icinga_host = module.params.get("host")
        self.icinga_port = module.params.get("port")
        self.icinga_username = module.params.get("username")
        self.icinga_password = module.params.get("password")
        self.state = module.params.get("state")
        self.hostname = module.params.get("hostname")
        self.hostnames = module.params.get("hostnames")
        self.start_time = module.params.get("start_time")
        self.end_time = module.params.get("end_time")
        self.duration = module.params.get("duration")
        self.object_type = module.params.get("object_type")
        self.all_services = module.params.get("all_services")
        self.author = module.params.get("author")
        self.comment = module.params.get("comment")
        self.fixed = module.params.get("fixed")
        self.filter_vars = None
        self.trigger_name = None

        self.icinga_url = "{0}:{1}/v1".format(self.icinga_host, self.icinga_port)

        self.connection = Session()
        self.connection.headers.update({'Accept': 'application/json'})
        self.connection.auth = (self.icinga_username, self.icinga_password)

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def run(self):
        res = dict(
            changed=False,
            ansible_module_results="none"
        )

        # print("hostname  : {} ({})".format(self.hostname, type(self.hostname)))
        # print("hostnames : {} ({})".format(self.hostnames, type(self.hostnames)))

        if self.hostname and self.hostnames:
            module.fail_json(
                msg=("Please choose whether to set downtimes for "
                     "'hostname' or 'hostnames'. "
                     "Both at the same time is not supported.")
            )

        if len(self.hostnames) != 0:

            res['changed'] = True

            r = dict()

            if iter(self.hostnames):

                for h in self.hostnames:

                    r[h] = dict()

                    if self.__host_exists(h):
                        """

                        """
                        payload = {
                            'type': self.object_type,
                            'filter': f"host.name == \"{h}\"",
                            'author': self.author,
                            'comment': self.comment,
                            'start_time': self.start_time,
                            'end_time': self.end_time,
                            'duration': self.duration
                        }
                        if self.fixed:
                            payload.update(fixed=True)
                        else:
                            payload.update(fixed=False)

                        if self.filter_vars:
                            payload.update(filter_vars=self.filter_vars)

                        if self.trigger_name:
                            payload.update(trigger_name=self.trigger_name)

                        if self.object_type == 'Host' and self.all_services is True:
                            payload.update(all_services=True)

                        module.log(msg=f"downtime for: {h}")
                        module.log(msg=f"payload: {payload}")

                        code, msg = self.__schedule_downtime(payload)

                        module.log(msg=f"{code}: {msg}")

                        r[h] = dict(
                            msg=msg,
                            status_code=code,
                        )

                    else:
                        msg = f"404: host {h} is not known"
                        module.log(msg=msg)
                        r[h] = dict(
                            msg=msg,
                            status_code=404,
                        )

                res['result'] = r

        elif len(self.hostname) != 0:
            pass

        else:
            print("hoo")

#        print(res)
#        result = dict(changed=True,
#                      ansible_module_results="Downtimes removed",
#                      result=dict(req.json(), status_code=req.status_code))

        return res

    def __call_url(self, method='GET', path=None, data=None, headers=None):
        """

        """
        if headers is None:
            headers = {
                'Accept': 'application/json',
                'X-HTTP-Method-Override': method,
            }

        url = f"{self.icinga_url}/{path}"
        module.log(msg=f"url: {url}")
        self.connection.headers.update(headers)

        try:
            if (method == 'GET'):
                ret = self.connection.get(
                    url,
                    verify=False
                )
                self.connection.close()

            elif (method == 'POST'):
                self.connection.close()
                ret = self.connection.post(
                    url,
                    data=data,
                    verify=False
                )

            else:
                print("unsupported")

            ret.raise_for_status()

            # self.module.log(msg="------------------------------------------------------------------")
            # self.module.log(msg=" text    : {}".format(ret.text))
            # self.module.log(msg=" headers : {}".format(ret.headers))
            # self.module.log(msg=" code    : {}".format(ret.status_code))
            # self.module.log(msg="------------------------------------------------------------------")

            return ret.status_code, json.loads(ret.text)

        except Exception as e:
            print(e)
            raise

    def __host_exists(self, hostname):
        """

        """
        code = 0

        data = {
            "type": "Host",
            "attrs": ["name"],
            "filter": f"match(\"{hostname}\", host.name)",
        }

        code, ret = self.__call_url(
            method='POST',
            path="objects/hosts",
            data=module.jsonify(data),
            headers={'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET'}
        )

        results = ret['results']

        if (code == 200 and len(results) != 0):
            # code   = results[0]['code']
            # status = results[0]['status']
            attrs = results[0]['attrs']

            if attrs.get('name') == hostname:
                return True

        return False

    def __schedule_downtime(self, data):
        """

        """
        code = 0
        status = "no status available"

        path = 'actions/schedule-downtime'

        code, ret = self.__call_url(
            method='POST',
            path=path,
            data=module.jsonify(data),
            headers={'Accept': 'application/json', 'X-HTTP-Method-Override': 'POST'}
        )

        results = ret['results']

        if (len(results) != 0):
            # print(json.dumps(results[0]))

            code = int(results[0]['code'])
            status = results[0]['status']

        return code, status

# ===========================================
# Module execution.
#


def main():
    global module
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default="present", choices=["absent", "present"]),
            host=dict(required=True),
            port=dict(required=False, default='5665'),
            username=dict(required=True, no_log=False),
            password=dict(required=True, no_log=True),
            hostname=dict(required=False, default=None),
            hostnames=dict(required=False, type='list'),
            start_time=dict(required=True, default=None),
            end_time=dict(required=True, default=None),
            duration=dict(required=True, default=None, type='int'),
            object_type=dict(default='Host', choices=["Service", "Host"]),
            all_services=dict(required=False, default=True, type='bool'),
            author=dict(required=False, default='ansible'),
            comment=dict(required=False, default='generated downtime'),
            fixed=dict(required=False, default=False, type='bool'),
        ),
        supports_check_mode=False,
    )

    try:
        icinga = Icinga2Api()
    except Exception as e:
        module.fail_json(
            msg=f"unable to connect to Icinga. Exception message: {e}"
        )

    result = icinga.run()

    module.log(msg=f"= result: {result}")

    module.exit_json(**result)


# import module snippets
if __name__ == '__main__':
    main()
