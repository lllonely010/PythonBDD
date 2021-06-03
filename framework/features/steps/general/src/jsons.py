import decimal
import regex
import ast
import logging
import json
from datetime import datetime
from dotted.collection import DottedDict


def search_json(json_data, key):
    """Search for dot notation in json

    If ALL or ANY are included in the search path, then we will return a list of matching items.
    For example: with the data of:
      {"dogs": [
      {"name": "spot",
      "breed": "dalmatian"},
      {"name": "Daisy",
      "breed": "boomer"},
      {"name": "jack",
      "breed": "jack russel"},
      ]
      }
    Search terms, and their responses:
    dogs.1.breed = "boomer"
    dogs.2 = {"name": "jack", "breed": "jack russel"}
    dogs.ALL.name = ["spot", "Daisy", "jack"]
    dogs.ANY.name = ["spot", "Daisy", "jack"]
    dogs.ANY.name = ["spot", "Daisy", "jack"]

    Parameters:
        json_data (str): The json to be searched in
        key (str): The string to look for
    Returns:
        String: The new string with found values
    """
    if ".ALL." in key or ".ANY." in key:
        key = key.replace(".ANY.", ".ALL.")
        short_list = DottedDict(json_data)[key.split(".ALL.")[0]].to_python()
        collated_values = []
        for item in short_list:
            if type(item[key.split(".ALL.")[1]]) == datetime:
                collated_value = str(item[key.split(".ALL.")[1]])
            else:
                collated_value = item[key.split(".ALL.")[1]]
            collated_values.append(collated_value)
        found_value = json.dumps(collated_values)
    else:
        if type(DottedDict(json_data)[key]) in [str, int, bool, float, decimal.Decimal, datetime]:
            found_value = str(DottedDict(json_data)[key])
        elif callable(DottedDict(json_data)[key]):
            found_value = DottedDict(json_data)[key]()
        elif DottedDict(json_data)[key] == None:
            found_value = "None"
        else:
            found_value = json.dumps(DottedDict(json_data)[key].to_python(), sort_keys=True, default=str)
    return found_value


def merge_context(base_context, addition):
    """Merges one set of json into another

    Parameters:
        base_context (dict): The initial json to merge to
        addition (dict): The json that we want to add
        
    Returns:
        String (dict): The new json that we'll return
    """
    if len(base_context) > 0:
        for u_item in addition:
            if u_item not in base_context:
                base_context[u_item] = addition[u_item]
            else:
                if type(addition[u_item]) == dict:
                    base_context[u_item] = merge_context(base_context[u_item], addition[u_item])
                elif type(addition[u_item]) == list and type(base_context[u_item]) == list:
                    base_context[u_item] += addition[u_item]
                else:
                    base_context[u_item] = addition[u_item]
    else:
        base_context = addition
    return base_context


def merge_json(base_context, addition):
    """Merges one set of json into another

    Parameters:
        base_context (dict): The initial json to merge to
        addition (dict): The json that we want to add
    Returns:
        String (dict): The new json that we'll return
    """
    if len(base_context) > 0:
        for u_item in addition:
            if u_item not in base_context:
                base_context[u_item] = addition[u_item]
            else:
                if type(addition[u_item]) == dict:
                    base_context[u_item] = merge_json(base_context[u_item], addition[u_item])
                else:
                    base_context[u_item] = addition[u_item]
    else:
        base_context = addition
    return base_context

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def get_dotsearch(context, string_to_search):
    # rx = ast.literal_eval(regex.findall(r"(\[.*\])", string_to_search)[0])    
    rx = json.loads(regex.findall(r"(\[.*\])", string_to_search)[0])
    search_pattern = string_to_search.replace(regex.findall(r"(\[.*\], )", string_to_search)[0], "")
    search_key = search_pattern[:search_pattern.find(".")]
    # search_value = search_pattern[search_pattern.rfind(".") + 1:]
    search_value = search_pattern.lstrip(search_key)
    search_value = search_value.replace(".", "", 1)
    logging.debug(f"search_key: {search_key}")
    logging.debug(f"search_value: {search_value}")
    found_index = "NOTFOUND"
    for array_index, dict_struct in enumerate(rx):
        if search_key in dict_struct:
            found_value = search_json(dict_struct, search_key)
            if (found_value != "NOTFOUND") and (found_value == search_value):
                found_index = str(array_index)

    logging.debug(f"found_index: {found_index}")
            
    return found_index
