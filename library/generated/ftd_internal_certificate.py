#!/usr/bin/python

# Copyright (c) 2018 Cisco Systems, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'network'}

DOCUMENTATION = """
---
module: ftd_internal_certificate
short_description: Manages InternalCertificate objects on Cisco FTD devices
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
  cert
    description:
      - PEM formatted X.509v3 certificate.
  certType
    description:
      - An mandatory enum value that specifies the type of internal certificate. Values can be one of the following. <br> UPLOAD - Certificate is already defined and certificate and private string will be uploaded. <br> SELFSIGNED - Generate an internal certificate using the provided values. <br>
  filter
    description:
      - The criteria used to filter the models you are requesting. It should have the following format: {field}{operator}{value}[;{field}{operator}{value}]. Supported operators are: "!"(not equals), ":"(equals), "<"(null), "~"(similar), ">"(null). Supported fields are: "name".
  id
    description:
      - A unique string identifier assigned by the system when the object is created. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete (or reference) an existing object.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  isSystemDefined
    description:
      - A boolean value, TRUE and FALSE (the default). The TRUE value indicates that certificate is created by system and cannot be deleted. FALSE indicates that the certificate can be deleted.
  issuerCommonName
    description:
      - Common Name, typically product name/brand, of the Authority (issuer) that signed and issued the certificate.  This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  issuerCountry
    description:
      - An ISO3166 two character country code of the Authority (issuer) that signed and issued the certificate.  This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  issuerLocality
    description:
      - Locality, city name, of the Authority (issuer) that signed and issued the certificate. This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  issuerOrganization
    description:
      - Organization, company name, of the Authority (issuer) that signed and issued the certificate. This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  issuerOrganizationUnit
    description:
      - The Organization Unit, division or unit, of the Authority (issuer) that signed and issued the certificate. This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  issuerState
    description:
      - State or the province of the Authority (issuer) that signed and issued the certificate. This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  limit
    description:
      - An integer representing the maximum amount of objects to return. If not specified, the maximum amount is 10
  name
    description:
      - A mandatory UTF string containing the name for the certificate. The string can be up to 128 characters. The name is used in the configuration as an object name only, it is not part of the certificate itself.
  offset
    description:
      - An integer representing the index of the first requested object. Index starts from 0. If not specified, the returned objects will start from index 0
  passPhrase
    description:
      - Password used for encrypted private key. Encrypted keys are not supported yet.
  privateKey
    description:
      - PEM formatted private key. Only unencrypted keys are supported.
  sort
    description:
      - The field used to sort the requested object list
  subjectCommonName
    description:
      - An Unicode alphanumeric string containing the Common Name, typically product name/brand, of the entity (subject) being certified or authenticated in the given certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectCountry
    description:
      - An ISO3166 two character country code of the Authority (issuer) that signed and issued the certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectDistinguishedName
    description:
      - A DN (Distinguished Name) defining the entity (subject) being certified or authenticated in the given certificate. For a root certificate the issuer and subject will be the same DN.  This is automatically extracted from the uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectLocality
    description:
      - An Unicode alphanumeric string containing the locality, city name, of the entity (subject) being certified or authenticated in the given certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectOrganization
    description:
      - An Unicode alphanumeric string containing the organization, company name, of the entity (subject) being certified or authenticated in the given certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectOrganizationUnit
    description:
      - An Unicode alphanumeric string containing the Organization Unit, division or unit, of the entity (subject) being certified or authenticated in the given certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  subjectState
    description:
      - An Unicode alphanumeric string containing the state or the province of the entity (subject) being certified or authenticated in the given certificate. This is mandatory input value for Self-Signed certificate and extracted from an uploaded certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  type
    description:
      - A UTF8 string, all letters lower-case, that represents the class-type. This corresponds to the class name.
  validityEndDate
    description:
      - This is set to five years in UTC format from the current date for Self-Signed certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  validityStartDate
    description:
      - This is current date in UTC format for Self-Signed certificate.<br>Field level constraints: must match pattern ^((?!;).)*$. (Note: Additional constraints might exist)
  version
    description:
      - A unique string version assigned by the system when the object is created or modified. No assumption can be made on the format or content of this identifier. The identifier must be provided whenever attempting to modify/delete an existing object. As the version will change every time the object is modified, the value provided in this identifier must match exactly what is present in the system or the request will be rejected.
"""

EXAMPLES = """
- name: Fetch InternalCertificate with a given name
  ftd_internal_certificate:
    operation: "getInternalCertificateByName"
    name: "Ansible InternalCertificate"

- name: Create a InternalCertificate
  ftd_internal_certificate:
    operation: 'addInternalCertificate'
    name: "Ansible InternalCertificate"
    type: "internalcertificate"
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


class InternalCertificateResource(object):

    def __init__(self, conn):
        self._conn = conn

    def addInternalCertificate(self, params):
        body_params = dict_subset(params, ['cert', 'certType', 'id', 'issuerCommonName', 'issuerCountry', 'issuerLocality', 'issuerOrganization', 'issuerOrganizationUnit', 'issuerState', 'isSystemDefined', 'name', 'passPhrase', 'privateKey', 'subjectCommonName', 'subjectCountry', 'subjectDistinguishedName', 'subjectLocality', 'subjectOrganization', 'subjectOrganizationUnit', 'subjectState', 'type', 'validityEndDate', 'validityStartDate', 'version'])

        return self._conn.send_request(
            url_path='/object/internalcertificates',
            http_method='POST',
            body_params=body_params,
        )

    def deleteInternalCertificate(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/object/internalcertificates/{objId}',
            http_method='DELETE',
            path_params=path_params,
        )

    def editInternalCertificate(self, params):
        path_params = dict_subset(params, ['objId'])
        body_params = dict_subset(params, ['cert', 'certType', 'id', 'issuerCommonName', 'issuerCountry', 'issuerLocality', 'issuerOrganization', 'issuerOrganizationUnit', 'issuerState', 'isSystemDefined', 'name', 'passPhrase', 'privateKey', 'subjectCommonName', 'subjectCountry', 'subjectDistinguishedName', 'subjectLocality', 'subjectOrganization', 'subjectOrganizationUnit', 'subjectState', 'type', 'validityEndDate', 'validityStartDate', 'version'])

        return self._conn.send_request(
            url_path='/object/internalcertificates/{objId}',
            http_method='PUT',
            body_params=body_params,
            path_params=path_params,
        )

    def getInternalCertificate(self, params):
        path_params = dict_subset(params, ['objId'])

        return self._conn.send_request(
            url_path='/object/internalcertificates/{objId}',
            http_method='GET',
            path_params=path_params,
        )

    def getInternalCertificateList(self, params):
        query_params = dict_subset(params, ['filter', 'limit', 'offset', 'sort'])

        return self._conn.send_request(
            url_path='/object/internalcertificates',
            http_method='GET',
            query_params=query_params,
        )

    def getInternalCertificateByName(self, params):
        search_params = params.copy()
        search_params['filter'] = 'name:%s' % params['name']
        item_generator = iterate_over_pageable_resource(self.getInternalCertificateList, search_params)
        return next(item for item in item_generator if item['name'] == params['name'])

    def upsertInternalCertificate(self, params):
        def is_duplicate_name_error(err):
            err_msg = to_text(err.read())
            return err.code == 422 and "Validation failed due to a duplicate name" in err_msg

        try:
            return self.addInternalCertificate(params)
        except HTTPError as e:
            if is_duplicate_name_error(e):
                existing_object = self.getInternalCertificateByName(params)
                params = copy_identity_properties(existing_object, params)
                return self.editInternalCertificate(params)
            else:
                raise e

    def editInternalCertificateByName(self, params):
        existing_object = self.getInternalCertificateByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.editInternalCertificate(params)

    def deleteInternalCertificateByName(self, params):
        existing_object = self.getInternalCertificateByName(params)
        params = copy_identity_properties(existing_object, params)
        return self.deleteInternalCertificate(params)


def main():
    fields = dict(
        operation=dict(type='str', default='upsertInternalCertificate', choices=['addInternalCertificate', 'deleteInternalCertificate', 'editInternalCertificate', 'getInternalCertificate', 'getInternalCertificateList', 'getInternalCertificateByName', 'upsertInternalCertificate', 'editInternalCertificateByName', 'deleteInternalCertificateByName']),
        register_as=dict(type='str'),

        cert=dict(type='str'),
        certType=dict(type='str'),
        filter=dict(type='str'),
        id=dict(type='str'),
        isSystemDefined=dict(type='bool'),
        issuerCommonName=dict(type='str'),
        issuerCountry=dict(type='str'),
        issuerLocality=dict(type='str'),
        issuerOrganization=dict(type='str'),
        issuerOrganizationUnit=dict(type='str'),
        issuerState=dict(type='str'),
        limit=dict(type='int'),
        name=dict(type='str'),
        objId=dict(type='str'),
        offset=dict(type='int'),
        passPhrase=dict(type='str'),
        privateKey=dict(type='str'),
        sort=dict(type='str'),
        subjectCommonName=dict(type='str'),
        subjectCountry=dict(type='str'),
        subjectDistinguishedName=dict(type='str'),
        subjectLocality=dict(type='str'),
        subjectOrganization=dict(type='str'),
        subjectOrganizationUnit=dict(type='str'),
        subjectState=dict(type='str'),
        type=dict(type='str'),
        validityEndDate=dict(type='str'),
        validityStartDate=dict(type='str'),
        version=dict(type='str'),
    )

    module = AnsibleModule(argument_spec=fields)
    params = module.params

    try:
        conn = Connection(module._socket_path)
        resource = InternalCertificateResource(conn)

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
