from behave import step, then, when  # pylint: disable=no-name-in-module
import json
from .src.helper import check_for_substitute, merge_context  # pylint: disable=relative-beyond-top-level
import logging
import decimal
import time
import os
import re
import os.path
from datetime import datetime
from dateutil.parser import parse as date_parse

@then("assert that {look_for} will {notbe} equal to {look_in} as expected")
def then_look_for_will_notbe_equal_look_in(context, look_for, notbe, look_in):
    look_for = check_for_substitute(context, look_for)
    look_in = check_for_substitute(context, look_in)

    # temp hack to allow to check for decimals
    try:
        look_for = decimal.Decimal(look_for)
        look_in = decimal.Decimal(look_in)
    except:
        pass

    if "not" in notbe:
        assert look_for != look_in, f"{look_for} is not equal to {look_in}"
    else:
        assert look_for == look_in, f"{look_for} is equal to {look_in}"


@then("assert that {compare} will be {lessmore} than {to} as expected")
def then_compare_will_be_lessmore_than_to(context, compare, lessmore, to):
    compare = decimal.Decimal(check_for_substitute(context, compare))
    to = decimal.Decimal(check_for_substitute(context, to))
    if lessmore == "more":
        assert compare > to, f"{compare} is not more than {to}"
    else:
        assert compare < to, f"{compare} is not less than {to}"


@then("assert that {look_for} will {notbe} in {look_in} as expected")
def then_look_for_will_notbe_in_look_in(context, notbe, look_for, look_in):
    """Then assert that {look_for} will {notbe} in {look_in}
    Check for something in something else, if it doesn't find a match, an assertion will be triggered

    Parameters:
        context: Behave contextual object
        look_for (str): A string that you're going to search for
        notbe (str): To be or not to be, that is the question
        look_in (str): The string that you'll search in
    """
    check_list_all = False

    if ".ALL." in look_in:
        check_list_all = True

    look_for = check_for_substitute(context, look_for)
    look_in = check_for_substitute(context, look_in)

    logging.debug(f"|{look_for}|")
    logging.debug(f"|{look_in}|")
    if check_list_all:
        data_list = json.loads(look_in)
        for l in data_list:
            if "not" in notbe:
                assert look_for != str(l), f"{l} was equal to {look_for}"
            else:
                assert look_for == str(l), f"{l} was not equal to {look_for}"
    else:
        if "not" in notbe:
            assert look_for not in look_in, f"{look_for} is in {look_in}"
        else:
            assert look_for in look_in, f"{look_for} is not in {look_in}"


@then("assert that {test} is within {margin}% of {outof} as expected")
def compare_marginal(context, test, margin, outof):
    test = decimal.Decimal(check_for_substitute(context, test))
    margin = decimal.Decimal(check_for_substitute(context, margin))
    outof = decimal.Decimal(check_for_substitute(context, outof))

    upper_margin = ((outof / 100) * (100 + margin))
    lower_margin = ((outof / 100) * (100 - margin))
    logging.debug(f"upper_margin {upper_margin}")
    logging.debug(f"test         {test}")
    logging.debug(f"outof        {outof}")
    logging.debug(f"lower_margin {lower_margin}")
    logging.debug(f"total margin {upper_margin - lower_margin}")

    assert test <= upper_margin, "more than upper margin"
    assert test >= lower_margin, "less than lower margin"


@then("assert that time {time} is within {start_time} and {end_time} as expected")
def compare_datetime(context, time, start_time, end_time):
    time = datetime.utcfromtimestamp(date_parse(check_for_substitute(context, time)).timestamp())
    start_time = datetime.utcfromtimestamp(date_parse(check_for_substitute(context, start_time)).timestamp())
    end_time = datetime.utcfromtimestamp(date_parse(check_for_substitute(context, end_time)).timestamp())
    assert time <= end_time, "time is out of end time limit"
    assert time >= start_time, "time is out of start time limit"
