import json
import logging
import time
import logging
import fnmatch
import string
import random
import os
from dateutil import tz  
from datetime import datetime
from PIL import Image, ImageChops
from .jsons import search_json, merge_json, merge_context,get_dotsearch
from .getters import get_abspath, get_length, get_parse_regex, get_readtxtfile, get_readxmlfile, get_simplevalue, get_config, get_context, get_object, get_persona 
from .modifiers import modify_datetimetotimestamp, modify_lowercase, modify_replace, modify_shorten, modify_uppercase, modify_calc, modify_time_format, get_next_month_first_date,modify_min_max_time,modify_character_length,modify_removeAllSpecialCharacters,modify_by_substitute
from .generate import generate_random_integer, generate


def search_and_load_config():
    start_time = time.time()
    config = {}
    pattern = "*.json"
    for root, dirs, files in os.walk("features/"): # pylint: disable=unused-variable
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                logging.debug(f"loading config: {os.path.join(root, name)}")
                f = open(os.path.join(root, name), "r")
                file_string = f.read()
                try:
                    new_config = json.loads(file_string)
                except Exception as e:
                    logging.error(f"loading {name} failed - {e}")
                    raise
                finally:
                    f.close()
                # for c in new_config:
                    # config[c] = new_config[c]
                config = merge_json(config, new_config)
    logging.debug(f"loading config complete took: {time.time()-start_time}s")
    return config

def check_for_substitute(context, str_in):
    function_names = {
        'config': get_config,
        'context': get_context,
        'object': get_object,
        'simplevalue': get_simplevalue,
        'personas': get_persona,
        'length': get_length,
        'dotsearch': get_dotsearch,
        'readxmlfile': get_readxmlfile,
        'readtxtfile': get_readtxtfile,
        'regex': get_parse_regex,
        'abspath': get_abspath,
        'shorten': modify_shorten,
        'reduce': modify_character_length,
        'lowercase': modify_lowercase,
        'uppercase': modify_uppercase,
        'replace': modify_replace,
        'remove_special_char': modify_removeAllSpecialCharacters,
        'substitute': modify_by_substitute,
        'datetimetotimestamp': modify_datetimetotimestamp,
        'time_format': modify_time_format,
        'next_month_first_date': get_next_month_first_date,
        'generate': get_generate,
        'randominteger': generate_random_integer,
        'randomstring': generate_random_string,
        'calc': modify_calc,
        'issorted':check_sorted,
        'utctolocal':convert_utc_local,
        'datedefined':modify_min_max_time
    }

    str_out = str_in

    for function_name in function_names:
        internal_functions_count = 0
        if f"{function_name}(" in str_in:
            function_start_location = str_in.rfind(f"{function_name}(")
            if function_name == "regex":
                function_end_location = str_in.find('")', str_in.rfind(f"{function_name}(")) + 2
            else:
                function_end_location = str_in.find(")", str_in.rfind(f"{function_name}(")) + 1
            function_contents = (str_in[function_start_location:function_end_location]).lstrip(function_name)
            for internal_function_name in function_names:
                internal_functions_count += function_contents.count(f"{internal_function_name}(")
            if (internal_functions_count == 0) and (len(function_contents) > 0):
                str_out = str_out.replace(f"{function_name}{function_contents}", function_names[function_name](context, chomp(function_contents.replace("$1234567890$", ")"))), 1)
                break
    
    remaining_functions_count = 0
    for function_name in function_names:
        remaining_functions_count += str_out.count(f"{function_name}(")

    if remaining_functions_count > 0:
        str_out = check_for_substitute(context, str_out)
    else:
        str_out = str_out.replace("$1234567890$", ")")

    return str_out

def chomp(string_to_chomp):
    return string_to_chomp.rstrip(")").lstrip("(")

def get_generate(context, item):
    if "," in item:
        (key_word, locale) = item.split(",")
    else:
        key_word = item
        locale = context.locale
    return generate(context, key_word, check_for_substitute(context, locale))

def generate_random_string(context,size):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(int(size)))

def convert_utc_local(context,date_converted):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Europe/Amsterdam')
    utc = datetime.strptime(date_converted, '%Y-%m-%dT%H:%M:%SZ')
    utc = utc.replace(tzinfo=from_zone)
    return utc.astimezone(to_zone).strftime('%Y-%m-%dT%H:%M:%S')

def compare(original, new, diff):
    new = Image.open(f"{os.getcwd()}/results/screenshots/{new}.png")
    original = Image.open(f"{os.getcwd()}/results/screenshots/{original}.png")
    img = ImageChops.difference(original, new).convert('RGB')
    img.save(f"{os.getcwd()}/results/screenshots/{diff}.png")
    pixels = img.getdata()
    black_thresh = 0
    nblack = 0
    for pixel in pixels:
        if sum(pixel) < black_thresh:
            nblack += 1
    return nblack

def check_sorted(context,item_to_be_checked):
    flag = False
    sort_list = []
    item_to_sort = json.loads(item_to_be_checked.split("#")[0])
    parameter = str(item_to_be_checked.split("#")[1])
    logging.debug(f'{item_to_sort}')
    for l in item_to_sort:
        if (isinstance(sort_list,str)):
            sort_list.append(l[parameter].lower())
        else:
            sort_list.append(l[parameter])
    if "ASC" in item_to_be_checked:
        if(sorted(sort_list, reverse=False)==sort_list):
            flag=True
    elif "DESC" in item_to_be_checked:
        if(sorted(sort_list, reverse=True)==sort_list):
            flag=True
    else:
        logging.error(f'order {item_to_be_checked.split("#")[2]} not supported')
    return str(flag)
