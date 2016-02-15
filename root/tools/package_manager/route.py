from . import view
from . import new
from . import post
from . import edit
from . import delete


def init(app):
    @app.route("/tools/package_manager")
    def tools_package_manager():
        return view.do()

    @app.route("/tools/package_manager/new")
    def tools_package_manager_new():
        return new.do()

    @app.route("/tools/package_manager/post", methods=["POST"])
    def tools_package_manager_post():
        return post.do()

    @app.route("/tools/package_manager/<string:package_name>/edit")
    def tools_package_manager_edit(package_name):
        return edit.do(package_name)

    @app.route("/tools/package_manager/<string:package_name>/delete", methods=["POST"])
    def tools_package_manager_delete(package_name):
        return delete.do(package_name)
