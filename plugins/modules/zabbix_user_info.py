#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2019, sky-joker
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
module: zabbix_user_info
short_description: Gather information about Zabbix user
author:
    - sky-joker (@sky-joker)
description:
    - This module allows you to search for Zabbix user entries.
requirements:
    - "python >= 2.6"
    - "zabbix-api >= 0.5.4"
options:
    username:
        description:
            - Name of the user alias in Zabbix.
            - username is the unique identifier used and cannot be updated using this module.
            - alias should be replaced with username
        aliases: [ alias ]
        required: true
        type: str
extends_documentation_fragment:
- community.zabbix.zabbix

'''

EXAMPLES = '''
- name: Get zabbix user info
  community.zabbix.zabbix_user_info:
    username: example
'''

RETURN = '''
zabbix_user:
  description: example
  returned: always
  type: dict
  sample: {
  "username": "example",
  "attempt_clock": "0",
  "attempt_failed": "0",
  "attempt_ip": "",
  "autologin": "0",
  "autologout": "0",
  "debug_mode": "0",
  "gui_access": "0",
  "lang": "en_GB",
  "medias": [
      {
        "active": "0",
        "mediaid": "668",
        "mediatypeid": "1",
        "period": "1-7,00:00-24:00",
        "sendto": "example@example.com",
        "severity": "63",
        "userid": "660"
      }
    ],
    "name": "user",
    "refresh": "30s",
    "rows_per_page": "50",
    "surname": "example",
    "theme": "default",
    "type": "1",
    "url": "",
    "userid": "660",
    "users_status": "0",
    "usrgrps": [
      {
        "debug_mode": "0",
        "gui_access": "0",
        "name": "Guests",
        "users_status": "0",
        "usrgrpid": "8"
      }
    ]
  }
'''


from ansible.module_utils.basic import AnsibleModule
from ansible_collections.community.zabbix.plugins.module_utils.version import LooseVersion

from ansible_collections.community.zabbix.plugins.module_utils.base import ZabbixBase
import ansible_collections.community.zabbix.plugins.module_utils.helpers as zabbix_utils


class User(ZabbixBase):
    def get_user_by_user_username(self, username):
        zabbix_user = ""
        try:
            data = {'output': 'extend', 'filter': {},
                    'getAccess': True, 'selectMedias': 'extend',
                    'selectUsrgrps': 'extend'}
            if LooseVersion(self._zbx_api_version) >= LooseVersion('5.4'):
                data['filter']['username'] = username
            else:
                data['filter']['alias'] = username

            zabbix_user = self._zapi.user.get(data)
        except Exception as e:
            self._zapi.logout()
            self._module.fail_json(msg="Failed to get user information: %s" % e)

        if not zabbix_user:
            zabbix_user = {}
        else:
            zabbix_user = zabbix_user[0]

        return zabbix_user


def main():
    argument_spec = zabbix_utils.zabbix_common_argument_spec()
    argument_spec.update(dict(
        username=dict(type='str', required=True, aliases=['alias']),
    ))
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    zabbix_utils.require_creds_params(module)

    username = module.params['username']

    user = User(module)
    zabbix_user = user.get_user_by_user_username(username)
    module.exit_json(changed=False, zabbix_user=zabbix_user)


if __name__ == "__main__":
    main()
