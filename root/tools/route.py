from . import create_agent_link
from . import password_generator
from . import setup_workstation


def init(app):
    create_agent_link.route.init(app)
    password_generator.route.init(app)
    setup_workstation.route.init(app)
