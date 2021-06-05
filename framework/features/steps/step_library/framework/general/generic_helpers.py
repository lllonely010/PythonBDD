from behave import step, then, when # pylint: disable=no-name-in-module
import json
from .src.helper import check_for_substitute, compare # pylint: disable=relative-beyond-top-level
import logging
import decimal
import time
import os
import re
import os.path


@then("wait for {seconds} seconds")
def wait_for(context, seconds):
    seconds = check_for_substitute(context, seconds)
    time.sleep(int(seconds))

@then("we need to implement this feature so for now it fails")
def force_fail(context):
    assert False==True, "Test Scenarion needs implementing"

@when("we log {thing_to_log}")
def when_we_log_thing_to_log(context, thing_to_log):
    """When we log {thing_to_log}
    Log something to the log file

    Parameters:
        context: Behave contextual object
        thing_to_log (str): The string to log
    """
    thing_to_log = check_for_substitute(context, thing_to_log)
    logging.info(thing_to_log)
    
@then("we generate a difference between image {one_image} and {two_image} saving as {diff_image}")
def imaging_diff_two_images(context, one_image, two_image, diff_image):
    one_image = check_for_substitute(context, one_image)
    two_image = check_for_substitute(context, two_image)
    diff_image = check_for_substitute(context, diff_image)
    print()
    print(compare(one_image, two_image, diff_image))
    print()

    