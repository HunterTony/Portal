import os
import time
import flask

import config
from root import route
from root import csrf
from root import error
from root import before
from libs import log

log.info("Initialising server")

os.environ["TZ"] = "UTC"
time.tzset()

### Init Flask ###
app = flask.Flask(__name__)

app.static_folder   = "../static/app/"
app.template_folder = "templates/"

app.secret_key  = config.flask.session_key
if(app.secret_key == "debug" and config.root.debug is not True):
    raise RuntimeError("Secret key not set in a production environment")

app.jinja_env.trim_blocks   = True
app.jinja_env.lstrip_blocks = True

app.host = config.network.host
app.port = config.network.port


### Init App ###
csrf.init(app)
error.init(app)
before.init(app)
route.init(app)


log.info("Server initialised")


### Debug ###
if(config.root.debug):
    log.warn("Debug mode is enabled")

    app.debug = True
    app.host = "127.0.0.1"
    app.port = 5000
    app.run()
