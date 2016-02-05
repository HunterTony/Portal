from . import new
from . import site_select_ajax
from . import post


def init(app):
    @app.route("/tools/create_agent_link")
    def tools_create_agent_link_new():
        return new.do()

    @app.route("/tools/create_agent_link/post", methods=["POST"])
    def tools_create_agent_link_post():
        return post.do()

    @app.route("/tools/create_agent_link/site_select_ajax/<int:client_id>")
    def tools_create_agent_link_site_select_ajax(client_id):
        return site_select_ajax.do(client_id)