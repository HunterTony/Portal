import flask


def client_authed():
    if("authenticated" not in flask.session):
        return False

    if(not flask.session["authenticated"]):
        return False

    return True