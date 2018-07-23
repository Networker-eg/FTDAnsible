#!/usr/bin/python

# Copyright (c) 2018 Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: ftd_radius_identity_source
short_description: Manages RadiusIdentitySource objects on Cisco FTD devices
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
  capabilities
    description:
      - The capabilities that the identity source has.
  description
    description:
      - An optional description of the RADIUS identity source<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  filter
    description:
      - The criteria used to filter the models you are requesting. It should have the following format: {field}{operator}{value}[;{field}{operator}{value}]. Supported operators are: "!"(not equals), ":"(equals), "<"(null), "~"(similar), ">"(null). Supported fields are: "name".
  host
    description:
      - The name of the RADIUS Identity Source<br>Field level constraints: cannot be null, length must be between 0 and 128 (inclusive), must match pattern ([0-9a-zA-Z]([0-9a-zA-Z-]{0,62}\.)([0-9a-zA-Z-]{1,63}\.)*[0-9a-zA-Z]{1,63})|(([0-9a-fA-F]{0,4}:){0,6}(([0-9a-fA-F]{0,4}:[0-9a-fA-F]{0,4})|(((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}))). (Note: Additional constraints might exist)
  id
    description:
      - The id of the RadiusIdentitySource<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  limit
    description:
      - An integer representing the maximum amount of objects to return. If not specified, the maximum amount is 10
  name
    description:
      - The name of the RADIUS Identity Source
  offset
    description:
      - An integer representing the index of the first requested object. Index starts from 0. If not specified, the returned objects will start from index 0
  serverAuthenticationPort
    description:
      - The optional RADIUS identity source UDP port to be used for authentication of users. The allowed range of ports is 1-65535. If you do not specify a value, the default is port 1646<br>Field level constraints: must be between 1 and 65535 (inclusive). (Note: Additional constraints might exist)
  serverSecretKey
    description:
      - The shared secret used for secure communications between the system and the RADIUS identity source
  sort
    description:
      - The field used to sort the requested object list
  timeout
    description:
      - The optional length of time (in seconds) that the system waits for a RADIUS identity source to respond. If you do not specify a value, the default is 10 seconds<br>Field level constraints: must be between 1 and 300 (inclusive). (Note: Additional constraints might exist)
  type
    description:
      - radiusidentitysource
  version
    description:
      - The version of the RadiusIdentitySource
"""

EXAMPLES = """
- name: Fetch RadiusIdentitySource with a given name
  ftd_radius_identity_source:
    operation: "getRadiusIdentitySourceByName"
    name: "Ansible RadiusIdentitySource"

- name: Create a RadiusIdentitySource
  ftd_radius_identity_source:
    operation: 'addRadiusIdentitySource'
    description: "From Ansible with love"
    name: "Ansible RadiusIdentitySource"
    type: "radiusidentitysource"
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


class RadiusIdentitySourceResource(object):

    def __init__(self, conn):
        self._conn = conn

    def addRadiusIdentitySource(self, params):
        body_params = dict_subset(params, ['capabilities', 'description', 'host', 'id', 'name', 'serverAuthenticationPort', 'serverSecretKey', 'timeout', 'type', 'version'])

        return self._conn.send_request(
            url_path='/object/radiusidentitysources',
            http_method='POST',
            body_params=body_params,
        )

    def deleteRadiusIdentitySource(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/object/radiusidentitysources/{objId}',
            http_method='DELETE',
            path_params=path_params,
        )

    def editRadiusIdentitySource(self, params):
        path_params = dict_subset(params, ['objId'])
        body_params = dict_subset(params, ['capabilities', 'description', 'host', 'id', 'name', 'serverAuthenticationPort', 'serverSecretKey', 'timeout', 'type', 'version'])

        return self._conn.send_request(
            url_path='/object/radiusidentitysources/{objId}',
            http_method='PUT',
            body_params=body_params,
            path_params=path_params,
        )

    def getRadiusIdentitySource(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/object/radiusidentitysources/{objId}',
            http_method='GET',
            path_params=path_params,
        )

    def getRadiusIdentitySourceList(self, params):
        query_params = dict_subset(params, ['filter', 'limit', 'offset', 'sort'])

        return self._conn.send_request(
            url_path='/object/radiusidentitysources',
            http_method='GET',
            query_params=query_params,
        )

    def getRadiusIdentitySourceByName(self, params):
        search_params = params.copy()
        search_params['filter'] = 'name:%s' % params['name']
        item_generator = iterate_over_pageable_resource(self.getRadiusIdentitySourceList, search_params)
        return next(item for item in item_generator if item['name'] == params['name'])

    def upsertRadiusIdentitySource(self, params):
        def is_duplicate_name_error(err):
            err_msg = to_text(err.read())
            return err.code == 422 and "Validation failed due to a duplicate name" in err_msg

        try:
            return self.addRadiusIdentitySource(params)
        except HTTPError as e:
            if is_duplicate_name_error(e):
                existing_object = self.getRadiusIdentitySourceByName(params)
                params = copy_identity_properties(existing_object, params)
                return self.editRadiusIdentitySource(params)
            else:
                raise e

    def editRadiusIdentitySourceByName(self, params):
        existing_object = self.getRadiusIdentitySourceByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.editRadiusIdentitySource(params)

    def deleteRadiusIdentitySourceByName(self, params):
        existing_object = self.getRadiusIdentitySourceByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.deleteRadiusIdentitySource(params)


def main():
    fields = dict(
        operation=dict(type='str', default='upsertRadiusIdentitySource', choices=['addRadiusIdentitySource', 'deleteRadiusIdentitySource', 'editRadiusIdentitySource', 'getRadiusIdentitySource', 'getRadiusIdentitySourceList', 'getRadiusIdentitySourceByName', 'upsertRadiusIdentitySource', 'editRadiusIdentitySourceByName', 'deleteRadiusIdentitySourceByName']),
        register_as=dict(type='str'),

        capabilities=dict(type='list'),
        description=dict(type='str'),
        filter=dict(type='str'),
        host=dict(type='str'),
        id=dict(type='str'),
        limit=dict(type='int'),
        name=dict(type='str'),
        objId=dict(type='str'),
        offset=dict(type='int'),
        serverAuthenticationPort=dict(type='int'),
        serverSecretKey=dict(type='str'),
        sort=dict(type='str'),
        timeout=dict(type='int'),
        type=dict(type='str'),
        version=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=fields)
    params = module.params

    try:
        conn = Connection(module._socket_path)
        resource = RadiusIdentitySourceResource(conn)

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
