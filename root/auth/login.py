import flask
import smtplib
import socket

import config
from libs import exception
from libs import render

from . import check


def validate_post(username, password):
    if(username is None or password is None):
        raise exception.AuthError("Invalid value supplied for username or password")

    if(len(username) == 0 or len(username) > 1024 or len(password) == 0 or len(password) > 1024):
        raise exception.AuthError("Invalid value supplied for username or password")


def validate_credentials(username, password):
    try:
        with smtplib.SMTP(config.auth.smtp_host, config.auth.smtp_port) as smtp:
            try:
                smtp.ehlo()
                smtp.starttls()
                smtp.login(username, password)
                smtp.quit()
            except smtplib.SMTPAuthenticationError as error:
                raise exception.AuthError("Invalid credentials supplied.".format(error))
    except (smtplib.SMTPConnectError, smtplib.SMTPHeloError, smtplib.SMTPException, socket.timeout, socket.gaierror) as error:
        raise exception.AuthError("Failed to connect to server: '{0}'".format(error))


def do():
    username = flask.request.form["username"]
    password = flask.request.form["password"]

    if(check.client_authed()):
        return render.error("Auth Error", "Client is already logged in.")

    try:
        validate_post(username, password)
    except exception.AuthError as error:
        return flask.render_template("/auth/redirect.html", error=error)

    try:
        validate_credentials(username, password)
    except exception.AuthError as error:
        return flask.render_template("/auth/redirect.html", error=error)

    flask.session["username"] = username
    flask.session["authenticated"] = True

    if("auth_return_url" in flask.session):
        return_url = flask.session["auth_return_url"]
        del flask.session["auth_return_url"]
    else:
        return_url = "/"

    return render.success("Auth Success", "Authentication successful.", return_url)