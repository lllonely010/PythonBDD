from behave import step, then, when # pylint: disable=no-name-in-module
import json
from .src.helper import check_for_substitute, merge_context # pylint: disable=relative-beyond-top-level
import logging
import decimal
import time
import os
import re
import os.path


@step("we store {json_to_store} in the context")
def step_we_store_json_in_the_context(context, json_to_store):
    """Given/When/Then we store {json_to_store} in the context
    Updates the json stored in the context, with the provided changes

    Parameters:
        context: Behave contextual object
        json_to_store (str): A string that represents the json to store

    """
    json_to_store = check_for_substitute(context, json_to_store)
    context.context = merge_context(context.context, json.loads(json_to_store))

@step("we remove {json_to_remove} from the context")
def step_we_remove_json_from_the_context(context, json_to_remove):
    """Given/When/Then we remove {json_to_remove} from the context
    Removes a key from the context.

    Parameters:
        context: Behave contextual object
        json_to_remove (str): A string that represents the json to remove

    """
    json_to_remove = json.loads(check_for_substitute(context, json_to_remove))
    for key in json_to_remove:
        del context.context[key]

@step("we store {value} as {key} as a simple value")
def store_a_simple_value(context, value, key):
    value = check_for_substitute(context, value)
    key = check_for_substitute(context, key)
    context.simple_values[key] = value


@step("we store table as {table_name}")
def store_a_table(context, table_name):
    table_name = check_for_substitute(context, table_name)
    context.test_objects[table_name] = context.table
