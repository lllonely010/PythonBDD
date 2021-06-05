import uuid
import os
import fnmatch
import json
import logging
import time
import sys
import random
import datetime
import requests
import subprocess
from steps.step_library.framework.general.src.helper import  search_and_load_config

ENVIRONMENT = "preprod"
VERSION = "0.0.5"

if "ENVIRONMENT_UNDER_TEST" in os.environ:
    ENVIRONMENT = os.environ["ENVIRONMENT_UNDER_TEST"]

log = logging.getLogger()
log.setLevel(logging.INFO)


def get_git_user():
    proc = subprocess.Popen("git config --list",
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            shell=True)
    std_out, std_err = proc.communicate()

    config_values = {}
    for value in std_out.decode('utf-8').split("\n"):
        config_values[value[0:value.find("=")]] = value[value.find("=")+1:]

    if "user.name" in config_values:
        user = config_values["user.name"]
    elif "user.email" in config_values:
        user = config_values["user.email"]
    else:
        user = "unknown"

    return user


def before_all(context):
    context.user = get_git_user()

    # this need to be extended to pull from environment variable
    context.system_under_test = ENVIRONMENT
    context.test_session = str(uuid.uuid4())
    context.session_id = context.test_session
    context.last_screenshot_id = "00000000-0000-0000-00000000000000000"
    

    if "session" in context.config.userdata:
        context.test_session = context.config.userdata["session"]
    
    context.configuration = search_and_load_config()
    context.lastappiumobjectid = None

    context.locale = "nl-NL",
    context.app_product_type = "parkmobile"
    context.membership_type = "private_transactional"

    if "membershiptype" in context.configuration["environment"]:
        context.membership_type = context.configuration["environment"]["membershiptype"]

    if "membershiptype" in context.config.userdata:
        context.membership_type = context.config.userdata["membershiptype"]

    if "MEMBERSHIP_TYPE" in os.environ:
        context.membership_type = os.environ["MEMBERSHIP_TYPE"]

    if "app_package" in context.configuration["environment"]:
        context.app_package = context.configuration["environment"]["app_package"]

    if "app_package" in context.config.userdata:
        context.app_package = context.config.userdata["app_package"]

    if "APP_PACKAGE" in os.environ:
        context.app_package = os.environ["APP_PACKAGE"]
    
    if "app_product_type" in context.configuration["environment"]:
        context.app_product_type = context.configuration["environment"]["app_product_type"]

    if "app_product_type" in context.config.userdata:
        context.app_product_type = context.config.userdata["app_product_type"]

    if "APP_PRODUCT_TYPE" in os.environ:
        context.app_product_type = os.environ["APP_PRODUCT_TYPE"]

    if "locale" in context.configuration["environment"]:
        context.locale = context.configuration["environment"]["locale"]

    if "locale" in context.config.userdata:
        context.locale = context.config.userdata["locale"]


    context.country = context.locale[-2:]

    context.product = context.config.userdata["product"]

    context.configuration["environment"]["locale"] = context.locale
    context.configuration["environment"]["country"] = context.country
    context.configuration["environment"]["product"] = context.product

    log.info(f"setting locale to {context.locale}")
    log.info(f"setting country to {context.country}")
    log.info(f"setting product to {context.product}")
    
def before_feature(context, feature):
    unique_scenarios = []
    for scenario in feature.scenarios:
        assert scenario.name not in unique_scenarios, f"Duplicate scenario name found in file: {scenario.filename}:{scenario.line} '{scenario.name}'"
        unique_scenarios.append(scenario.name)

    if "feature_id" in context.config.userdata:
        context.feature_id = context.config.userdata["feature_id"]
    else:
        context.feature_id = str(uuid.uuid4())



def before_scenario(context, scenario):
    context.scenario_id = str(uuid.uuid4())
    context.context = {}
    context.context["environment"] = context.system_under_test
    context.generate_requests = {}
    context.test_objects = {}
    context.personas = {}
    context.simple_values = {}

    if 'randomseed' in context.configuration['environment']:
        context.seed = context.configuration['environment']['randomseed']
    else:
        context.seed = random.randint(11111111, 99999999)


def after_scenario(context, scenario):
    for test_object in context.test_objects:
        if getattr(context.test_objects[test_object], "close", None):
            context.test_objects[test_object].close()
    for seed in context.generate_requests:
        context.generate_requests[seed] = 0


def before_step(context, step):
    context.last_screenshot_id = "00000000-0000-0000-00000000000000000"
    context.step_id = str(uuid.uuid4())

    # if step.location.filename == "<string>":
    #     print(f"- {step.step_type} {step.name}")
