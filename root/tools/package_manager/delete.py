import flask

from libs import package
from libs import exception
from libs import render


def do(package_name):
    try:
        package.delete(package_name)
    except exception.PackageError as error:
        return render.error("Package Manager Error", error, "/tools/package_manager")

    return render.success("Package Manager Success", "Package deleted", "/tools/package_manager")
