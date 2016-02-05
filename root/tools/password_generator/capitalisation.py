import random


def capital_all(password):
    return password.upper()

def capital_none(password):
    return password.lower()

def capital_random(password):
    capitaled_password = []
    for char in password:
        if(random.randint(0, 1)):
            capitaled_password.append(char.upper())
        else:
            capitaled_password.append(char.lower())

    return "".join(capitaled_password)

def capital_title(password):
    return password.title()


def apply(password, options):
    option_map = {
        "all":    capital_all,
        "none":   capital_none,
        "random": capital_random,
        "title":  capital_title,
    }

    if("capital" not in options):
        capital = "none"
    else:
        capital = options["capital"]

    try:
        password = option_map[capital](password)
    except KeyError:
        pass

    return password