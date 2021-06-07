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

def before_all(context):

    # this need to be extended to pull from environment variable
    context.system_under_test = ENVIRONMENT
    context.test_session = str(uuid.uuid4())
    context.session_id = context.test_session
    context.last_screenshot_id = "00000000-0000-0000-00000000000000000"
    

    if "session" in context.config.userdata:
        context.test_session = context.config.userdata["session"]
    
    context.configuration = search_and_load_config()
    context.lastappiumobjectid = None

    
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
