import random

from libs import exception


def de_vowel_password(password, options):
    return "".join([char for char in list(password) if char not in "aeiou"])

def duplicate_password(password, options):
    if("duplicate-frequency" not in options):
        frequency = 3
    else:
        try:
            frequency = int(options["duplicate-frequency"])
        except ValueError:
            raise exception.PasswordGeneratorError("Invalid value supplied for duplicate frequency")

    duplicated_password = []
    for index, char in enumerate(password):
        duplicated_password.append(char)
        if(index % frequency == 0):
            duplicated_password.append(char)

    return "".join(duplicated_password)

def intersperse_password(password, options):
    if("intersperse-frequency" not in options):
        frequency = 3
    else:
        try:
            frequency = int(options["intersperse-frequency"])
        except KeyError:
            raise exception.PasswordGeneratorError("Invalid value supplied for intersperse frequency")

    if("intersperse-characters" not in options):
        characters = string.punctuation
    else:
        characters = options["intersperse-characters"]

    interspersed_password = []
    for index, char in enumerate(password):
        interspersed_password.append(char)
        if(index % frequency == 0):
            interspersed_password.append(random.choice(characters))

    return "".join(interspersed_password)

def leetspeak_password(password, options):
    leetspeak_map = { "a": "4", "e": "3", "g": "6", "i": "1", "o": "0", "s": "5", "t": "7", }

    leetspeaked_password = []
    for char in password:
        if(char in leetspeak_map):
            leetspeaked_password.append(leetspeak_map[char])
        else:
            leetspeaked_password.append(char)

    return "".join(leetspeaked_password)

def reverse_password(password, options):
    return password[::-1]


def apply(password, options):
    option_map = {
        "de-vowel":               de_vowel_password,
        "duplicate":              duplicate_password,
        "intersperse":            intersperse_password,
        "leetspeak":              leetspeak_password,
        "reverse":                reverse_password,
    }

    for option in options:
        try:
            password = option_map[option](password, options)
        except KeyError:
            pass

    return password