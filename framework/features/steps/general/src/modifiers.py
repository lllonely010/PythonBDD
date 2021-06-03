import datetime 
import regex
import time
import logging
from dateutil.parser import parse as date_parse
import ast
import operator as op
from dateutil import relativedelta
from datetime import datetime, timedelta
import re


operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


def eval_(node):
    if isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def modify_calc(context, value):
    result = str(eval_(ast.parse(value, mode='eval').body))
    return result

def modify_lowercase(context, value):
    return value.lower()

def modify_uppercase(context, value):
    return value.upper()

def modify_shorten(context, item_to_shorten):
    (string_to_shorten, start, end) = item_to_shorten.split(",")
    return string_to_shorten[int(start):len(string_to_shorten)-int(end)]

def modify_character_length(context, item_to_shorten):
    (string_to_shorten, length) = item_to_shorten.split(",")
    return string_to_shorten[0:int(length)]

def modify_time_format(context, string_to_process): 
    if ',' in string_to_process:
        time_string = string_to_process.split(',')[0]
        time_format = string_to_process.split(',')[1] 
    time_string = time_string.strip("Z")
    datetimeobject = datetime.strptime(time_string,'%Y-%m-%dT%H:%M:%S')
    return datetimeobject.strftime(time_format)

def get_next_month_first_date(context, string_to_process):
    today = datetime.date.today()
    next_month_first_date = today + relativedelta.relativedelta(months=1, day=1)
    return str(next_month_first_date.strftime("%d-%m-%Y"))

def modify_datetimetotimestamp(context, string_to_process):
    replacement = None
    isdayfirst = False
    time_string = string_to_process
    if ',' in string_to_process:
        time_string = string_to_process.split(',')[0]
        isdayfirst = string_to_process.split(',')[1] 

    if "Today" in time_string:
        time_string = time_string.replace("Today", datetime.today().strftime('%d/%m/%Y'))
    if "Yesterday" in time_string:
        time_string = time_string.replace("Yesterday", (datetime.utcnow() - timedelta(days=1)).strftime('%d/%m/%Y'))
    if "Tomorrow" in time_string:
        time_string = time_string.replace("Tomorrow", (datetime.utcnow() + timedelta(days=1)).strftime('%d/%m/%Y'))    
    if regex.findall(r"([APM]{2} - )", time_string):
        datetime_collection = time_string.split("-")
        time_string = f"{datetime_collection[1].strip()} {datetime_collection[0].strip()}"
        
    replacement = str(date_parse(time_string, dayfirst=isdayfirst).timestamp())
    logging.debug(f"converting {time_string} t0 {replacement}")
    return replacement

def modify_replace(context, string_to_process):
    original_string = string_to_process[1:string_to_process.find('",')]
    return eval(f'"{original_string}".replace({string_to_process[string_to_process.find(", ")+1:]})')

def modify_by_substitute(replace_from, replace_with, string_to_process):
    replaced_string = None
    replaced_string = re.sub(replace_from, replace_with, string_to_process)
    return str(replaced_string)

def modify_removeAllSpecialCharacters(context, string_to_process):
    replaced_string_with_no_spl_char = modify_by_substitute('[^a-zA-Z0-9 \n\.]', '', string_to_process)
    return str(replaced_string_with_no_spl_char)

def modify_min_max_time(context,definedTime):
    if ',' in definedTime:
        time_string = definedTime.split(',')[0]
    dtr = datetime.strptime(time_string, '%Y-%m-%dT%H:%M:%SZ')
    if 'min' in definedTime:
        dtr = datetime.combine(dtr,datetime.min.time())
    elif 'max' in definedTime:
        dtr = datetime.combine(dtr,datetime.max.time())
    else:
        logging.error(f'value {definedTime.split(",")[1]} not supported')
    return dtr.strftime('%Y-%m-%dT%H:%M:%SZ')