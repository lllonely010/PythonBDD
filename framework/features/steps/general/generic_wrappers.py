from behave import step, then, when, given # pylint: disable=no-name-in-module
import json
from .src.helper import check_for_substitute # pylint: disable=relative-beyond-top-level
import logging
import decimal
import time
import os
import re
import os.path


@then("if {value_a}=={value_b} do `{step_to_run}`")
def if_something_then_executestep(context, value_a, value_b, step_to_run):
    value_a = check_for_substitute(context, value_a)
    value_b = check_for_substitute(context, value_b)
    if value_a == value_b:
        logging.debug(f"running step {step_to_run}")
        context.execute_steps(step_to_run)


@then("if {value_a}!={value_b} do `{step_to_run}`")
def if_not_something_then_execute_step(context, value_a, value_b, step_to_run):
    value_a = check_for_substitute(context, value_a)
    value_b = check_for_substitute(context, value_b)
    if value_a != value_b:
        logging.debug(f"running step {step_to_run}")
        context.execute_steps(step_to_run)

@then("if {value_a}<{value_b} do `{step_to_run}`")
def if_something_less_than_something_execute_step(context, value_a, value_b, step_to_run):
    value_a = int(value_a)
    value_b = int(value_b)
    if value_a < value_b:
        logging.debug(f"running step {step_to_run}")
        context.execute_steps(step_to_run)

@then("if {value_a}>{value_b} do `{step_to_run}`")
def if_something_greater_than_something_execute_step(context, value_a, value_b, step_to_run):
    value_a = int(value_a)
    value_b = int(value_b)
    if value_a > value_b:
        logging.debug(f"running step {step_to_run}")
        context.execute_steps(step_to_run)

@given("if {condition} do `{step_to_run}`")
def if_condition(context, step_to_run, condition):
    condition = check_for_substitute(context, condition)
    condition = eval(condition)
    if bool(condition):
        logging.debug(f"running step {step_to_run}")
        context.execute_steps(step_to_run)

@when("we execute python code {python_code} and save it as {save_as_name}")
def execute_python_code(context, python_code, save_as_name):
    context.context[save_as_name] = eval(python_code)

@step("we retry {times} times, waiting for {seconds} seconds each time {step_to_run}")
def retry_steps(context, times, seconds, step_to_run):
    times = check_for_substitute(context, times)
    seconds = check_for_substitute(context, seconds)
    step_to_run = check_for_substitute(context, step_to_run)
    # steps_to_run = check_for_substitute(context, steps_to_run)
    success = False
    started_at = time.time()

    for a in range(0, int(times) - 1):
        try:
            context.execute_steps(step_to_run)
            success = True
            break
        except AssertionError as e:
            logging.debug(f"Retrying {a} of {times}, wait for {seconds}, total so far {time.time() - started_at}")
            time.sleep(int(seconds))
    if not success:
        context.execute_steps(step_to_run)

@when("we execute `{steps_to_execute}` multiple steps")
def execute_multiple_steps(context, steps_to_execute):
    step_def_list = steps_to_execute.split('<new_step>')
    for step_def in step_def_list:
        context.execute_steps(step_def)

@step("for each row in the table {table_name} execute {step_to_execute}")
def for_each_row_in_table_execute_steps(context, table_name, step_to_execute):
    for row in context.test_objects[table_name]:
        for header in context.test_objects[table_name].headings:
            value = check_for_substitute(context, row[header])
            context.simple_values[header] = value
        context.execute_steps(step_to_execute)

@step("for {start} to {end} do {step_to_execute}")
def for_loop_execute_steps(context, start, end, step_to_execute):
    start = int(check_for_substitute(context, start))
    end = int(check_for_substitute(context, end))

    for number in range(start, end):
        context.execute_steps(step_to_execute.replace("$COUNTER", str(number)))
