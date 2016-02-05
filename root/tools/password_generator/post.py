import flask
import string
import random

from libs import render
from libs import exception
from libs import data

from . import mutation
from . import capitalisation


def add_option(options, option):
    value = flask.request.form.get(option, None)
    if(value is not None and value != ""):
        options[option] = value


def prepare_source(options):
    if(options["base"] == "words"):
        if("dictionary" not in options):
            raise exception.PasswordGeneratorError("Words base selected but no dictionary supplied")

        if(options["dictionary"] not in data.dictionary.available):
            raise exception.PasswordGeneratorError("Invalid dictionary supplied")

        return data.dictionary.dictionaries[options["dictionary"]]
    elif(options["base"] == "characters"):
        return list(string.ascii_lowercase + string.digits + string.punctuation)
    else:
        raise exception.PasswordGeneratorError("Invalid base supplied")


def do():
    options = {}

    options["base"]        = flask.request.form["base"]
    options["base-length"] = int(flask.request.form["base-length"])

    for option in ["dictionary", "de-vowel", "duplicate", "duplicate-frequency", "intersperse", "intersperse-frequency", "intersperse-characters", "leetspeak", "reverse", "capital"]:
        
        add_option(options, option)

    try:
        source = prepare_source(options)

        passwords = []
        for i in range(0, 50):
            password = "".join(random.sample(source, options["base-length"]))

            password = mutation.apply(password, options)
            password = capitalisation.apply(password, options)

            passwords.append(password)
    except exception.PasswordGeneratorError as error:
        return render.error("Password Generator Error", error)

    return flask.render_template("/tools/password_generator/view.html", passwords=passwords)