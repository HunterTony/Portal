from . import new
from . import post


def init(app):
    @app.route("/tools/password_generator/new")
    def tools_password_generator_new():
        return new.do()

    @app.route("/tools/password_generator/post", methods=["POST"])
    def tools_password_generator_post():
        return post.do()