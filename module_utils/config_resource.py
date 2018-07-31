from ansible.module_utils._text import to_text
from ansible.module_utils.six.moves.urllib.error import HTTPError

IGNORED_FIELDS = ['id', 'version', 'isSystemDefined', 'links']


class BaseConfigObjectResource(object):
    def __init__(self, conn):
        self._conn = conn
        self.config_changed = False

    def get_object_by_name(self, url_path, name, path_params=None):
        result = self._conn.send_request(url_path=url_path, http_method='GET', path_params=path_params,
                                         query_params={'filter': 'name:%s' % name})
        return next((i for i in result['items'] if i['name'] == name), None)

    def add_object(self, url_path, body_params, path_params=None, query_params=None):
        if body_params.get('name') is None:
            raise Exception('New object cannot be added without name. The name field is mandatory for new objects.')
        existing_obj = self.get_object_by_name(url_path, body_params['name'], path_params)

        if not existing_obj:
            return self._send_modifying_request(url_path=url_path, http_method='POST', body_params=body_params,
                                                path_params=path_params, query_params=query_params)
        elif equal_objects(existing_obj, body_params):
            return existing_obj
        else:
            raise Exception('Cannot add new object. An object with the same name but different parameters already exists.')

    def delete_object(self, url_path, path_params):
        def is_invalid_uuid_error(err):
            err_msg = to_text(err.read())
            return err.code == 422 and "Validation failed due to an invalid UUID" in err_msg

        try:
            return self._send_modifying_request(url_path=url_path, http_method='DELETE', path_params=path_params)
        except HTTPError as e:
            if is_invalid_uuid_error(e):
                return {'response': 'Referenced object does not exist'}
            else:
                raise e

    def update_object(self, url_path, body_params, path_params):
        existing_object = self._conn.send_request(url_path=url_path, http_method='GET', path_params=path_params)

        if not existing_object:
            raise ValueError('Referenced object does not exist')
        elif equal_objects(existing_object, body_params):
            return existing_object
        else:
            return self._send_modifying_request(url_path=url_path, http_method='PUT', body_params=body_params,
                                                path_params=path_params)

    def _send_modifying_request(self, url_path, http_method, body_params=None, path_params=None, query_params=None):
        response = self._conn.send_request(url_path=url_path, http_method=http_method, body_params=body_params,
                                           path_params=path_params, query_params=query_params)
        self.config_changed = True
        return response


def equal_objects(dict1, dict2):
    if type(dict1) is not dict or type(dict2) is not dict:
        raise ValueError("Arguments must be dictionaries")

    dict1 = dict((k, dict1[k]) for k in dict1.keys() if k not in IGNORED_FIELDS and dict1[k])
    dict2 = dict((k, dict2[k]) for k in dict2.keys() if k not in IGNORED_FIELDS and dict2[k])

    if len(dict1) != len(dict2):
        return False

    for key, value1 in dict1.items():
        if key not in dict2:
            return False

        value2 = dict2[key]

        if type(value1) != type(value2):
            return False

        equal_values = value1 == value2 if type(value1) != dict else equal_objects(value1, value2)
        if not equal_values:
            return False

    return True