import flask

from libs import render
from libs import exception
from libs import package


def do():
    new_package = {
        "name":         flask.request.form["name"].replace(" ", "_"),
        "description":  flask.request.form["description"],
        "script":       flask.request.form["script"],
    }

    if(flask.request.form.get("edit_package") is not None):
        try:
            package.update(new_package)
        except exception.PackageError as error:
            return render.error("Package Manager Error", error, "/tools/package_manager")
    else:
        try:
            package.create(new_package)
        except exception.PackageError:
            return render.error("Package Manager Error", error, "/tools/package_manager")

    return render.success("Package Manager Success", "Package created", "/tools/package_manager")
