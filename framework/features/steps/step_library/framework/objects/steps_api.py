from behave import given, when, step, then # pylint: disable=no-name-in-module
import json
import logging
import uuid
from .src.api import RequestObject # pylint: disable=relative-beyond-top-level
from ..general.src.helper import check_for_substitute # pylint: disable=relative-beyond-top-level


@step("we perform a {method} against {url} using payload of {data}")
def step_we_perform_a_method_against_url_using_payload_of_data(context, method, url, data):
    """Given perform a {method} against {url} using payload of {data}
    Grouping of steps that create a new api request

    Parameters:
        context: Behave contextual object
        method (str): The chosen method (POST, PUT, GET, etc)
        url (str): The full url that's to be called including schema (http://www.google.com/)
        data (str): Json in string from, to be sent as the payload, or None if not required

    Artifacts:
        A new api session named after a generated uuid, stored in context(lastRequestID)
    """
    session_name = str(uuid.uuid4())
    url = check_for_substitute(context, url)
    data = check_for_substitute(context, data)
    steps = f"Given we prepare a new api session called {session_name}\n"
    steps += f"When we perform a {method} against {url} using payload of {data} using {session_name}\n"
    context.context['lastRequestID'] = session_name
    context.execute_steps(steps)

@given("we prepare a new api session called {session}")
def given_we_prepare_a_new_api_session_called(context, session):
    """Given we prepare a new api session called {session}
    Creates a new api session and stores it in test objects

    Parameters:
        context: Behave contextual object
        session (str): The name to call the session

    Artifacts:
        A new api session named {session}
    """
    session = check_for_substitute(context, session)
    context.test_objects[session] = RequestObject(session)

@given("we force our http requests for {session} through the proxy {hostname}:{port}")
def step_adjust_proxy(context, session, hostname, port):
    session_name = check_for_substitute(context, session)
    hostname = check_for_substitute(context, hostname)
    port = check_for_substitute(context, port)
    context.test_objects[session_name].adjust_http_proxy(hostname, port)

@when("we perform a {method} against {url} using payload of {data} using {session}")
def step_we_perform_a_method_against_url_using_payload_of_data_using_session(context, method, url, data, session):
    """Given perform a {method} against {url} using payload of {data} using {session}
    Performs a call against a given url using a predefined session

    Parameters:
        context: Behave contextual object
        method (str): The chosen method (POST, PUT, GET, etc)
        url (str): The full url that's to be called including schema (http://www.google.com/)
        data (str): Json in string from, to be sent as the payload, or None if not required
        session (str): The session that's being interacted with
    """
    session_name = check_for_substitute(context, session)
    url = check_for_substitute(context, url)
    data = check_for_substitute(context, data)

    if data == "None":
        data = None

    context.test_objects[session_name].perform_request(method, url, data=data)

@when("we perform a {method} against {url} sending the file {file_path} using {session} with filename {filename}")
def step_we_perform_a_method_against_url_using_payload_of_file_using_session(context, method, url, filename, file_path, session):
    """Given perform a {method} against {url} using payload of {data} using {session}
    Performs a call against a given url using a predefined session

    Parameters:
        context: Behave contextual object
        method (str): The chosen method (POST, PUT, GET, etc)
        url (str): The full url that's to be called including schema (http://www.google.com/)
        data (str): Json in string from, to be sent as the payload, or None if not required
        session (str): The session that's being interacted with
    """
    session_name = check_for_substitute(context, session)
    url = check_for_substitute(context, url)
    file_path = check_for_substitute(context, file_path)
    filename = check_for_substitute(context,filename)

    context.test_objects[session_name].perform_request(method, url, filename, filepath=file_path)

@given("we add basicauth to {session} using username {username} and password {password}")
def given_we_add_basic_auth_to_session(context, session, username, password):
    """Given we add basicauth to {session_name} using username {username} and password {password}
    Adds basic auth to an API session

    Parameters:
        context: Behave contextual object
        session (str): The session that's being interacted with
        username (str): The desired username
        password (str): The desired password
    """
    session = check_for_substitute(context, session)
    username = check_for_substitute(context, username)
    password = check_for_substitute(context, password)
    context.test_objects[session].add_basic_auth(username, password)

@given('we set allow_redirects for {session} to {enabled}')
def given_set_redirects(context, session, enabled):
    if enabled == "True":
        context.test_objects[session].set_allow_redirects(True)
    else:
        context.test_objects[session].set_allow_redirects(False)
     

@given("we add a {headers} headers to {session}")
def given_we_add_a_headers_to_session_name(context, session, headers):
    """Given we add basicauth to {session_name} using username {username} and password {password}
    Adds one or more headers to an api session

    Parameters:
        context: Behave contextual object
        session (str): The session that's being interacted with
        headers (str): Json that descibes the headers
    """
    session = check_for_substitute(context, session)
    headers = check_for_substitute(context, headers)
    context.test_objects[session].add_headers(json.loads(headers))

@given("we enable retries on the session named {session}")
def given_we_set_retries_on(context, session):
    session = check_for_substitute(context, session)
    context.test_objects[session].set_retry_on()

@given("we add a {parameters} parameters to {session}")
def given_we_add_a_parameters_to_session_name(context, session, parameters):
    """Given we add basicauth to {session_name} using username {username} and password {password}
    Adds one or more headers to an api session

    Parameters:
        context: Behave contextual object
        session (str): The session that's being interacted with
        headers (str): Json that descibes the headers
    """
    session = check_for_substitute(context, session)
    parameters = check_for_substitute(context, parameters)
    context.test_objects[session].add_parameters(json.loads(parameters))
