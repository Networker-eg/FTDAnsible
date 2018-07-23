#!/usr/bin/python

# Copyright (c) 2018 Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: ftd_security_intelligence_network_policy
short_description: Manages SecurityIntelligenceNetworkPolicy objects on Cisco FTD devices
version_added: "2.7"
author: "Cisco Systems, Inc."
options:
  operation:
    description:
      - Specified the name of the operation to execute in the task.
    required: true
  register_as:
    description:
      - Specifies Ansible fact name that is used to register received response from the FTD device.
  blacklistForBlock
    description:
      - A set of Network Feeds categories and Network Objects to block.<br>Allowed types are: [NetworkObject, NetworkObjectGroup, NetworkFeed, NetworkFeedCategory]
  filter
    description:
      - The criteria used to filter the models you are requesting. It should have the following format: {field}{operator}{value}[;{field}{operator}{value}]. Supported operators are: "!"(not equals), ":"(equals), "<"(null), "~"(similar), ">"(null). Supported fields are: "name".
  id
    description:
      - A unique string identifier assigned by the system when the object is created. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete (or reference) an existing object.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  limit
    description:
      - An integer representing the maximum amount of objects to return. If not specified, the maximum amount is 10
  name
    description:
      - A string that represents the name of the object
  offset
    description:
      - An integer representing the index of the first requested object. Index starts from 0. If not specified, the returned objects will start from index 0
  sort
    description:
      - The field used to sort the requested object list
  type
    description:
      - A UTF8 string, all letters lower-case, that represents the class-type. This corresponds to the class name.
  version
    description:
      - A unique string version assigned by the system when the object is created or modified. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete an existing object. As the version will change every time the object is modified, the value provided in this identifier must match exactly what is present in the system or the request will be rejected.
  whitelist
    description:
      - A set of Network Feeds categories and Network Objects that should not to blocked.<br>Allowed types are: [NetworkObject, NetworkObjectGroup, NetworkFeed, NetworkFeedCategory]
"""

EXAMPLES = """
- name: Fetch SecurityIntelligenceNetworkPolicy with a given name
  ftd_security_intelligence_network_policy:
    operation: "getSecurityIntelligenceNetworkPolicyByName"
    name: "Ansible SecurityIntelligenceNetworkPolicy"
"""

RETURN = """
response:
  description: HTTP response returned from the API call.
  returned: success
  type: dict
error_code:
  description: HTTP error code returned from the server.
  returned: error
  type: int
msg:
  description: Error message returned from the server.
  returned: error
  type: dict
"""
import json

from ansible.module_utils.basic import AnsibleModule, to_text
from ansible.module_utils.http import iterate_over_pageable_resource
from ansible.module_utils.misc import dict_subset, construct_module_result, copy_identity_properties
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.connection import Connection


class SecurityIntelligenceNetworkPolicyResource(object):

    def __init__(self, conn):
        self._conn = conn

    def editSecurityIntelligenceNetworkPolicy(self, params):
        path_params = dict_subset(params, ['objId'])
        body_params = dict_subset(params, ['blacklistForBlock', 'id', 'name', 'type', 'version', 'whitelist'])

        return self._conn.send_request(
            url_path='/policy/securityintelligencenetworkpolicies/{objId}',
            http_method='PUT',
            body_params=body_params,
            path_params=path_params,
        )

    def getSecurityIntelligenceNetworkPolicy(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/policy/securityintelligencenetworkpolicies/{objId}',
            http_method='GET',
            path_params=path_params,
        )

    def getSecurityIntelligenceNetworkPolicyList(self, params):
        query_params = dict_subset(params, ['filter', 'limit', 'offset', 'sort'])

        return self._conn.send_request(
            url_path='/policy/securityintelligencenetworkpolicies',
            http_method='GET',
            query_params=query_params,
        )

    def getSecurityIntelligenceNetworkPolicyByName(self, params):
        search_params = params.copy()
        search_params['filter'] = 'name:%s' % params['name']
        item_generator = iterate_over_pageable_resource(self.getSecurityIntelligenceNetworkPolicyList, search_params)
        return next(item for item in item_generator if item['name'] == params['name'])

    def editSecurityIntelligenceNetworkPolicyByName(self, params):
        existing_object = self.getSecurityIntelligenceNetworkPolicyByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.editSecurityIntelligenceNetworkPolicy(params)


def main():
    fields = dict(
        operation=dict(type='str', choices=['editSecurityIntelligenceNetworkPolicy', 'getSecurityIntelligenceNetworkPolicy', 'getSecurityIntelligenceNetworkPolicyList', 'getSecurityIntelligenceNetworkPolicyByName', 'editSecurityIntelligenceNetworkPolicyByName'], required=True),
        register_as=dict(type='str'),

        blacklistForBlock=dict(type='list'),
        filter=dict(type='str'),
        id=dict(type='str'),
        limit=dict(type='int'),
        name=dict(type='str'),
        objId=dict(type='str'),
        offset=dict(type='int'),
        sort=dict(type='str'),
        type=dict(type='str'),
        version=dict(type='str'),
        whitelist=dict(type='list'),
    )

    module = AnsibleModule(argument_spec=fields)
    params = module.params

    try:
        conn = Connection(module._socket_path)
        resource = SecurityIntelligenceNetworkPolicyResource(conn)

        resource_method_to_call = getattr(resource, params['operation'])
        response = resource_method_to_call(params)

        result = construct_module_result(response, params)
        module.exit_json(**result)
    except HTTPError as e:
        err_msg = to_text(e.read())
        module.fail_json(changed=False, msg=json.loads(err_msg) if err_msg else {}, error_code=e.code)
    except Exception as e:
        module.fail_json(changed=False, msg=str(e))


if __name__ == '__main__':
    main()
