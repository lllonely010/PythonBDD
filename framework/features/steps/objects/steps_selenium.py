from behave import given, when, step, then # pylint: disable=no-name-in-module
from .src.ui import SeleniumObject # pylint: disable=relative-beyond-top-level
import json
import logging
from ..general.src.helper import check_for_substitute # pylint: disable=relative-beyond-top-level
import uuid


@given("we prepare a new selenium session called {session_name} with {config} configuration")
def prepare_new_selenium_session(context, session_name, config):
    session_name = check_for_substitute(context, session_name)
    config = check_for_substitute(context, config)
    context.test_objects[session_name] = SeleniumObject(session_name, config)

@when("we navigate selenium to {url} using {session_name}")
def navigate_to_url(context, url, session_name):
    url = check_for_substitute(context, url)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].get(url)

@when("we switch to window index {window_index} using selenium {session_name}")
def switch_to_window(context, window_index, session_name):
    session_name = check_for_substitute(context, session_name)

    context.test_objects[session_name].switch_to_window(window_index)

@given("we name {selector} iframe using selenium {session_name} the name {text}")
def name_iframe(context, selector, session_name, text):
    text = check_for_substitute(context, text)
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].set_name(selector, text)

@given("we switch to the iframe {frame_name} in {session_name} object")
def switch_to(context, frame_name, session_name):
    session_name = check_for_substitute(context, session_name)
    frame_name = check_for_substitute(context, frame_name)
    context.test_objects[session_name].switch_to_frame(frame_name)

@given("we wait {duration} seconds for url to be {url} in selenium {session_name}")
def wait_url_change(context, duration, url, session_name):
    duration = check_for_substitute(context, duration)
    url = check_for_substitute(context, url)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].wait_url_change(duration, url)

@when("we type into {selector} using selenium {session_name} the text {text}")
def type_into_selector(context, selector, session_name, text):
    text = check_for_substitute(context, text)
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].type_into(selector, text)

@when("we click on {selector} using selenium {session_name}")
def click_on_selector(context, selector, session_name):
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].click(selector)

@when("we close the browser using selenium {session_name}")
def close_the_browser(context, session_name):
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].close()
    
@when("we hover over on {selector} using selenium {session_name}")
def hover_over_on_selector(context, selector, session_name):
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].hover_over(selector)

@then("we capture a screenshot of {session_name} selenium session named {filename}")
def capture_screenshot(context, session_name, filename):
    filename = check_for_substitute(context, filename)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].capture_screenshot_to_file(filename)
    context.last_screenshot_id = context.test_objects[session_name].upload_screenshot(filename)

@then("we capture a wireframe of {session_name} selenium session named {filename}")
def capture_wireframe(context, session_name, filename):
    filename = check_for_substitute(context, filename)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].capture_wireframe_to_file(filename)

@then("we check {selector} has data_attr_value {get_data_attr_value} using selenium {session_name}")
def check_d_a_value(context, selector, get_data_attr_value, session_name):
    get_data_attr_value = check_for_substitute(context, get_data_attr_value)
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, selector)
    context.test_objects[session_name].check_data_attr_value(selector, get_data_attr_value)

@then("we check {selector} disabled is {disabled} using selenium {session_name}")
def check_is_disabled(context, selector, disabled, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, selector)

    is_disabled = context.test_objects[session_name].is_disabled(selector)

    if disabled == "True":
        assert is_disabled != False, f"element {selector} is not disabled"
    elif disabled == "False":
        assert is_disabled != True, f"element {selector} is disabled"
    else:
        assert False

@given("we prepare a new element from {session_name} with called {element_name} using {selector} selector")
def capture_element(context, element_name, session_name, selector):
    element_name = check_for_substitute(context, element_name)
    selector = check_for_substitute(context, selector)
    context.test_objects[session_name].populate_element_object(element_name, selector)

@when("we verify text {element_text} is present in element {element_selector} with element attribute {element_attribute} in session {session_name}")
def compare_text(context, element_selector, element_text, session_name, element_attribute):
    element_text = check_for_substitute(context, element_text)
    selector = check_for_substitute(context, element_selector)
    assert context.test_objects[session_name].compare_text(element_text, selector, element_attribute), f"element {selector} text is displayed incorrectly"

@when("we select {value} from {selector} using selenium {session_name} session")
def selenium_select(context, value, selector, session_name):
    session_name = check_for_substitute(context, session_name)
    value = check_for_substitute(context, value)
    selector = check_for_substitute(context, selector)
    context.test_objects[session_name].select_value(value, selector)

@when("we {acceptordecline} native alert pop up in the selenium {session_name} session")
def selenium_deal_with_native_alert(context, acceptordecline, session_name):
    acceptordecline = check_for_substitute(context, acceptordecline)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].dismiss_native_popup(acceptordecline) 
    
@then("we check that the text in the element {selector} contains the text {text} using the selenium {session_name}")
def selenium_group_check_for_text(context, selector, text, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, selector)
    text = check_for_substitute(context, text)
    session_uuid = str(uuid.uuid4())

    context.execute_steps(f"""
        Given we prepare a new element from {session_name} with called {session_uuid} using {selector} selector
        Then assert that {text} will be in object({session_name}.{session_uuid}.text) as expected
    """)

@when("we scroll to element {selector} using selenium {session_name}")
def scroll_to_element(context, selector, session_name):
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].scroll_to_selected_element(selector)

@when("we wait for the selenium element {element} to be present in the {session_name} object")
def wait_for_element(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    context.test_objects[session_name].wait_for_element(element)

@then("we check that the text in the element {selector} equals to the text {text} using the selenium {session_name}")
def selenium_group_check_for_text_compare(context, selector, text, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, selector)
    text = check_for_substitute(context, text)
    session_uuid = str(uuid.uuid4())

    context.execute_steps(f"""
        Given we prepare a new element from {session_name} with called {session_uuid} using {selector} selector
        Then assert that {text} will be equal to object({session_name}.{session_uuid}.text) as expected
    """)

@then("we check if {element} element is not present using selenium {session_name}")
def we_check_if_element_is_not_present(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, element)
    assert not context.test_objects[session_name].find_no_element(selector), f"element {selector} is present"
    context.lastappiumobjectid = session_name

@then("we check that the value in the element {selector} equals to {value} using the selenium {session_name}")
def selenium_group_check_for_value_compare(context, selector, value, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, selector)
    value = check_for_substitute(context, value)
    session_uuid = str(uuid.uuid4())

    context.execute_steps(f"""
        Given we prepare a new element from {session_name} with called {session_uuid} using {selector} selector
        Then assert that {value} will be equal to object({session_name}.{session_uuid}.value) as expected
    """)

@when("we clear the element {selector} using selenium {session_name}")
def clear_the_selector(context, selector, session_name):
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].clear_text(selector)