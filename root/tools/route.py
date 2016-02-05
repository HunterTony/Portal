from . import create_agent_link
from . import password_generator


def init(app):
    create_agent_link.route.init(app)
    password_generator.route.init(app)