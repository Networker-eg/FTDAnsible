#!/usr/bin/python

# Copyright (c) 2018 Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: ftd_configuration
short_description: Manages ConfigEntity objects on Cisco FTD devices over REST API.
version_added: "2.7"
author: "Cisco Systems, Inc."
options:
  operation:
    description:
      - The name of the operation to execute. Commonly, the operation starts with 'add', 'edit', 'get'
       or 'delete' verbs, but can have an arbitrary name too. 
    required: true
  data:
    description:
      - Key-value pairs that should be sent as body parameters in a REST API call
  query_params:
    description:
      - Key-value pairs that should be sent as query parameters in a REST API call.
  path_params:
    description:
      - Key-value pairs that should be sent as path parameters in a REST API call.
  register_as:
    description:
      - Specifies Ansible fact name that is used to register received response from the FTD device.
"""

EXAMPLES = """
- name: Create a network object
  ftd_configuration:
    operation: "addNetworkObject"
    data:
      name: "Ansible-network-host"
      description: "From Ansible with love"
      subType: "HOST"
      value: "192.168.2.0"
      dnsResolution: "IPV4_AND_IPV6"
      type: "networkobject"
      isSystemDefined: false
    register_as: "hostNetwork"

- name: Delete the network object
  ftd_configuration:
    operation: "deleteNetworkObject"
    path_params:
      objId: "{{ hostNetwork['id'] }}"
"""

RETURN = """
response:
  description: HTTP response returned from the API call.
  returned: success
  type: dict
"""
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.connection import Connection

# TODO: remove import workarounds when module_utils are moved to the Ansible core
try:
    from ansible.module_utils.config_resource import BaseConfigObjectResource
    from ansible.module_utils.http import HTTPMethod
    from ansible.module_utils.misc import construct_ansible_facts, ConfigurationError
    from ansible.module_utils.fdm_swagger_client import OperationField
except (ImportError, ModuleNotFoundError):
    from module_utils.config_resource import BaseConfigObjectResource
    from module_utils.http import HTTPMethod
    from module_utils.misc import construct_ansible_facts, ConfigurationError
    from module_utils.fdm_swagger_client import OperationField


def is_add_operation(operation_name, operation_spec):
    # Some endpoints have non-CRUD operations, so checking operation name is required in addition to the HTTP method
    return operation_name.startswith('add') and operation_spec[OperationField.METHOD] == HTTPMethod.POST


def is_edit_operation(operation_name, operation_spec):
    # Some endpoints have non-CRUD operations, so checking operation name is required in addition to the HTTP method
    return operation_name.startswith('edit') and operation_spec[OperationField.METHOD] == HTTPMethod.PUT


def is_delete_operation(operation_name, operation_spec):
    # Some endpoints have non-CRUD operations, so checking operation name is required in addition to the HTTP method
    return operation_name.startswith('delete') and operation_spec[OperationField.METHOD] == HTTPMethod.DELETE


def main():
    fields = dict(
        operation=dict(type='str', required=True),
        data=dict(type='dict'),
        query_params=dict(type='dict'),
        path_params=dict(type='dict'),
        register_as=dict(type='str')
    )
    module = AnsibleModule(argument_spec=fields)
    params = module.params
    connection = Connection(module._socket_path)

    op_name = params['operation']
    op_spec = connection.get_operation_spec(op_name)
    if op_spec is None:
        module.fail_json(msg='Invalid operation name provided: %s' % op_name)

    data, query_params, path_params = params['data'], params['query_params'], params['path_params']
    # TODO: implement validation for input parameters

    resource = BaseConfigObjectResource(connection)

    try:
        if is_add_operation(op_name, op_spec):
            resp = resource.add_object(op_spec[OperationField.URL], data, path_params, query_params)
        elif is_edit_operation(op_name, op_spec):
            resp = resource.edit_object(op_spec[OperationField.URL], data, path_params, query_params)
        elif is_delete_operation(op_name, op_spec):
            resp = resource.delete_object(op_spec[OperationField.URL], path_params)
        else:
            resp = resource.send_request(op_spec[OperationField.URL], op_spec[OperationField.METHOD], data, path_params,
                                         query_params)

        module.exit_json(changed=resource.config_changed, response=resp,
                         ansible_facts=construct_ansible_facts(resp, module.params))
    except ConfigurationError as e:
        module.fail_json(msg='Failed to execute %s operation because of the configuration error: %s' % (op_name, e))


if __name__ == '__main__':
    main()