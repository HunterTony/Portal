from . import new
from . import site_select_ajax
from . import post
from . import action_download

from root import before


def init(app):
    @app.route("/tools/setup_workstation")
    def tools_setup_workstation():
        return new.do()

    @app.route("/tools/setup_workstation/site_select_ajax/<int:client_id>")
    def tools_setup_workstation_site_select_ajax(client_id):
        return site_select_ajax.do(client_id)

    @app.route("/tools/setup_workstation/post", methods=["POST"])
    def tools_setup_workstation_post():
        return post.do()

    before.auth_excluded_endpoints.append("tools_setup_workstation_action_download")
    @app.route("/tools/setup_workstation/action_download/<string:action_name>")
    def tools_setup_workstation_action_download(action_name):
        return action_download.do(action_name)
