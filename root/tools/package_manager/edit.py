import flask
import json

from libs import package
from libs import exception
from libs import render


def do(package_name):
    try:
        old_package = package.get(package_name)
    except exception.PackageError as error:
        return render.error("Package Manager Error", error, "/tools/package_manager")

    return flask.render_template("/tools/package_manager/new.html", edit_package=True, name=old_package["name"], description=old_package["description"], applications=old_package["applications"], eligibility=json.dumps(old_package["eligibility"]), script=old_package["script"])
