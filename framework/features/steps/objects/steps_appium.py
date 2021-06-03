from behave import given, when, step, then  # pylint: disable=no-name-in-module
from .src.ui import AppiumObject  # pylint: disable=relative-beyond-top-level
import logging
from _datetime import datetime
from ..general.src.helper import check_for_substitute  # pylint: disable=relative-beyond-top-level
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ExpectedConditions
from selenium.webdriver.common.by import By
from pytz import timezone 

@given("we prepare a new appium session called {session_name} with {config} configuration with {driver_provider} driver provider")
def prepare_new_appium_session(context, session_name, config, driver_provider):
    session_name = check_for_substitute(context, session_name)
    config = check_for_substitute(context, config)
    driver_provider = check_for_substitute(context, driver_provider)
    context.test_objects[session_name] = AppiumObject(session_name, config, driver_provider)
    context.execute_steps(f"""
       When we change environment for parkmobile android execution {session_name} session
    """)
    context.lastappiumobjectid = session_name

@when("we type into {selector} using appium {session_name} the text {text}")
def type_into_selector(context, selector, session_name, text):
    text = check_for_substitute(context, text)
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].type_into(selector, text)
    context.lastappiumobjectid = session_name

@when("we set value for {selector} using appium {session_name} the text {text}")
def set_value_into_selector(context, selector, session_name, text):
    text = check_for_substitute(context, text)
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].set_value_into(selector, text)
    context.lastappiumobjectid = session_name

@when("we set value {value} for PickerWheel on ios using appium {session_name}")
def set_value_into_pickerwheel(context, session_name, value):
    driver = context.test_objects[session_name].get_driver()
    value = check_for_substitute(context, value)
    session_name = check_for_substitute(context, session_name)
    logging.info(f"Entering {value} value in PickerWheel")
    driver.find_element_by_xpath("//XCUIElementTypePickerWheel").send_keys(value)
    driver.find_element_by_xpath("//XCUIElementTypeButton[@name='Done']").click()
    context.lastappiumobjectid = session_name

@when("we click on {selector} using appium {session_name}")
def click_on_selector(context, selector, session_name):
    selector = check_for_substitute(context, selector)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].click(selector)
    context.lastappiumobjectid = session_name

@then("we capture a screenshot of {session_name} appium session named {filename}")
def capture_screenshot(context, session_name, filename):
    filename = check_for_substitute(context, filename)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].capture_screenshot_to_file(filename)
    context.lastappiumobjectid = session_name

@then("we capture a wireframe of {session_name} appium session named {filename}")
def capture_wireframe(context, session_name, filename):
    filename = check_for_substitute(context, filename)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].capture_wireframe_to_file(filename)
    context.lastappiumobjectid = session_name

@given("we set the geolocation of {session_name} appium session to long:{long}, lat:{lat}")
def set_geolocation(context, session_name, long, lat):
    long = check_for_substitute(context, long)
    lat = check_for_substitute(context, lat)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].set_geo_location(long, lat)
    context.lastappiumobjectid = session_name

@then("we dump the source from {session_name} appium session to the console")
def dump_source(context, session_name):
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].dump_source()
    context.lastappiumobjectid = session_name

@when("we wait for the element {element} to be present in the {session_name} object")
def wait_for_element(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    context.test_objects[session_name].wait_for_element(element)
    context.lastappiumobjectid = session_name

@when("we wait for the elements {element} to be present in the {session_name} object")
def wait_for_elements(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    context.test_objects[session_name].wait_for_elements(element)
    context.lastappiumobjectid = session_name

@when("we wait for the element {element} and click it in the {session_name} object")
def wait_for_element_and_click_it(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    context.test_objects[session_name].wait_for_element_and_click_it(element)
    context.lastappiumobjectid = session_name

@when("we wait for the element {element} to be enabled in the {session_name} object")
def wait_for_enabled_element(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    assert context.test_objects[session_name].wait_for_enabled_element(element), f"element {element} not enabled"
    context.lastappiumobjectid = session_name

@when("we wait for the random alert {element} to be enabled and click it in the {session_name} object")
def wait_for_random_element_and_click(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    element = check_for_substitute(context, element)
    context.test_objects[session_name].wait_for_random_elementAndClick(element)
    context.lastappiumobjectid = session_name

@then("we check for the element for the element {element} to be {condition} in the {session_name} object")
def we_check_for_enabled_element(context, element, condition, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, element)
    if condition == "enabled":
        assert context.test_objects[session_name].is_element_enabled(selector), f"element {selector} not enabled"
    elif condition == "disabled":
        assert not context.test_objects[session_name].is_element_enabled(selector), f"element {selector} not disabled"
    context.lastappiumobjectid = session_name

@when("we scroll form element {element_start} to {element_end} using appium {session_name}")
def scroll_to_element(context, element_start, element_end, session_name):
    selector_start = check_for_substitute(context, element_start)
    selector_end = check_for_substitute(context, element_end)
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].scroll_to_element(selector_start, selector_end)
    context.lastappiumobjectid = session_name

@when("we scroll from bottom to top using appium {session_name}")
def scroll_to_top(context, session_name):
    session_name = check_for_substitute(context, session_name)
    context.test_objects[session_name].sroll_to_top()
    context.lastappiumobjectid = session_name

@when("we increase time in {locator} date picker by {number_of} {hoursorminutes} in the {session_name} object")
def increase_time(context, locator, number_of, session_name, hoursorminutes):
    element = check_for_substitute(context, locator)
    timeunit_number = check_for_substitute(context, number_of)
    session_name = check_for_substitute(context, session_name)
    hoursorminutes = check_for_substitute(context, hoursorminutes)
    driver = context.test_objects[session_name].get_driver()
    logging.debug(f'Value of appium driver is {driver}')
    logging.debug(f'Value of element is {element.lstrip("xpath:")}')
    set_time = None
    local_timezone = timezone('Europe/Amsterdam')
    if hoursorminutes == "minutes":
        set_minutes = int(datetime.now(local_timezone).strftime("%M")) + int(timeunit_number)
        if set_minutes > 59:
            set_minutes = set_minutes - 60
        driver.find_element_by_xpath("//XCUIElementTypePickerWheel[3]").send_keys(set_minutes)
        if len(str(set_minutes)) == 1:
            set_minutes = "0" + str(set_minutes)
        set_time = datetime.now(local_timezone).strftime("%H") + ":" + str(set_minutes) 
    elif hoursorminutes == "hours":
        set_hours = int(datetime.now(local_timezone).strftime("%H")) + int(timeunit_number)
        if set_hours > 24:
            set_hours = set_hours - 24
        driver.find_element_by_xpath(
            "//XCUIElementTypePickerWheel[2]").send_keys(set_hours)
        if len(str(set_hours)) == 1:
            set_hours = "0" + str(set_hours)
        set_time = str(set_hours) + ":" + datetime.now(local_timezone).strftime("%M")
    context.get_time = set_time

@when("we hide keyboard using appium {session_name}")
def hide_keyboard(context, session_name):
    context.test_objects[session_name].hide_keyboard()
    context.lastappiumobjectid = session_name

@then("we check if {element} element is present using appium {session_name}")
def we_check_if_element_is_present(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, element)
    assert context.test_objects[session_name].wait_for_element(selector), f"element {selector} not present"
    context.lastappiumobjectid = session_name

@then("we check if {element} element is not present using appium {session_name}")
def we_check_if_element_is_not_present(context, element, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, element)
    assert not context.test_objects[session_name].find_no_element(selector), f"element {selector} is present"
    context.lastappiumobjectid = session_name

@then("we check if element text {elementtext} is present using appium {session_name}")
def we_check_if_element_text_is_present(context, elementtext, session_name):
    session_name = check_for_substitute(context, session_name)
    if (context.app_platform_type == 'android'):
        selector = check_for_substitute(context, f"xpath://android.widget.TextView[contains(@text,'{elementtext}')]")
    elif(context.app_platform_type == 'ios'):
        selector = check_for_substitute(context, f"xpath://XCUIElementTypeStaticText[contains(@value,'{elementtext}')]")  
    assert context.test_objects[session_name].wait_for_element(selector), f"element {selector} not present"
    context.lastappiumobjectid = session_name


@then("we verify element {element} attribute {element_attribute} attribute_text {element_text} is displayed using appium {session_name}")
def we_verify_element_text(context, element, element_attribute, element_text, session_name):
    session_name = check_for_substitute(context, session_name)
    selector = check_for_substitute(context, element)
    text = check_for_substitute(context, element_text)
    attribute = check_for_substitute(context, element_attribute)
    logging.info(f"session_name:{session_name} selector:{selector}text:{text}attribute:{attribute}")
    assert context.test_objects[session_name].compare_text_of_element(
        selector, attribute, text), f"element {selector} text is displayed incorrectly"
    context.lastappiumobjectid = session_name
