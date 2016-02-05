from . import password_generator


def init(app):
    password_generator.route.init(app)