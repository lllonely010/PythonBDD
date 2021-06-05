import ast
import regex
import logging
import json
import os
from .jsons import is_json
from .jsons import search_json


def get_context(context, dot_notation):
    return search_json(context.context, dot_notation)


def get_config(context, dot_notation):
    return search_json(context.configuration, dot_notation)


def get_persona(context, dot_notation):
    return search_json(context.personas, dot_notation)


def get_object(context, dot_notation):
    object_key = dot_notation[:dot_notation.find('.')]
    return_value = str(search_json(
        context.test_objects[object_key].object_data, dot_notation)).replace(")", "$1234567890$")
    return return_value

def get_abspath(context, string_to_process):
    return os.path.abspath(string_to_process)

def get_parse_regex(context, string_to_process):
    s = regex.findall(r"\"(.*?)\", \"(.*)\"",
                      string_to_process, regex.DOTALL)[0]
    (regex_pattern, string_to_search) = s
    # (regex_pattern, string_to_search) = string_to_process.split(',')
    # regex_pattern = regex_pattern.strip()[1:]
    # string_to_search = string_to_search.strip()[1:-1]
    found_strings = regex.findall(regex_pattern, string_to_search)
    if len(found_strings) == 1:
        return found_strings[0]
    else:
        return json.dumps(found_strings)


def get_readxmlfile(context, filepath):
    f = open(filepath, "r")
    s = ""
    for line in f.readlines():
        s += line.strip()
    f.close
    return s


def get_readtxtfile(context, filepath):
    f = open(filepath, "r")
    s = f.read()
    f.close
    return s


def get_simplevalue(context, key_word):
    return context.simple_values[key_word]


def get_length(context, string_to_measure):
    string_to_measure = str(string_to_measure)

    try:
        value = json.loads(string_to_measure)
        if type(value) not in [dict, list]:
            value = str(value)
    except:
        value = str(string_to_measure)

    return str(len(value))