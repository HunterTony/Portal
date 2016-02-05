import json

from libs import api
from libs import exception


def do(client_id):
    try:
        return json.dumps(api.remote_management.site.get_from_client_id(client_id))
    except exception.RemoteManagementError:
        return json.dumps([])