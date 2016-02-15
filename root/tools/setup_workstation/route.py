from . import new
from . import site_select_ajax
from . import post

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
