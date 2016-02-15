import flask

from libs import package


def do():
    return flask.render_template("/tools/package_manager/view.html", packages=package.get_all())
