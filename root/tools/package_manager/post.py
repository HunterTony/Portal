import flask
import json

from libs import render
from libs import exception
from libs import package


def do():
    applications = []
    for application in ["setup", "update"]:
        if(flask.request.form.get(application) is not None):
            applications.append(application)

    if(len(applications) == 0):
        return render.error("Package Manager Error", "No applications specified", "/tools/package_manager/new")

    try:
        eligibility = json.loads(flask.request.form["eligibility"])
    except json.decoder.JSONDecodeError:
        return render.error("Package Manager Error", "Invalid eligibility provided", "/tools/package_manager/new")

    new_package = {
        "name":         flask.request.form["name"].replace(" ", "_"),
        "description":  flask.request.form["description"],
        "applications": applications,
        "eligibility":  eligibility,
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
