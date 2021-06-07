import random
import datetime
import string
import logging
from dateutil.relativedelta import relativedelta
import operator
from faker import Faker
from faker.providers import address, automotive, person
import uuid

def generate(context, item, locale):
    locale_lookup = {
        "nl-NL": "nl_NL"
    }

    
    generators = {
        "email": generate_email,
        "emailfake": generate_fakeemail,
        "boolean": generate_boolean,
        "gender": generate_gender,
        "firstname": generate_firstname,
        "lastname": generate_lastname,
        "street": generate_street,
        "streetnumber": generate_streetnumber,
        "city": generate_city,
        "zipcode": generate_zipcode,
        "emptystring": generate_emptystring,
        "dateofbirth": generate_date_of_birth,
        "now": generate_now,
        "uuid": generate_uuid,
        "random_number": generate_random_number,
        "password": generate_password
    }
    
    context.fake = Faker(locale_lookup[locale])
    context.fake.add_provider(address)
    context.fake.add_provider(automotive)
    context.fake.add_provider(person)
    context.generator_locale = locale

    if item not in context.generate_requests:
        context.generate_requests[item] = 0
    else:
        context.generate_requests[item] += 1
    context.fake.seed(int(context.seed) + context.generate_requests[item])

    if "now" in item:
        return str(generators["now"](context, item))
    else:
        return str(generators[item](context))

def generate_now(context, requested_time):
    return generate_timestamp(requested_time).strftime("%Y-%m-%dT%H:%M:%SZ")

def generate_phonenumber(context):
    options = {
        "nl-NL": "065#######"
    }
    return Faker().numerify(text=options[context.generator_locale]) # pylint: disable=no-member

def generate_password(context):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=10))

def generate_firstname(context):
    return context.fake.first_name() # pylint: disable=no-member

def generate_lastname(context):
    return context.fake.last_name() # pylint: disable=no-member

def generate_street(context):
    return context.fake.street_name() # pylint: disable=no-member

def generate_streetnumber(context):
    return context.fake.building_number() # pylint: disable=no-member

def generate_city(context):
    return context.fake.city() # pylint: disable=no-member

def generate_zipcode(context):
    return context.fake.postcode() # pylint: disable=no-member

def generate_emptystring(context):
    return ""

def generate_boolean(context):
    return Faker().boolean() # pylint: disable=no-member

def generate_gender(context):
    if Faker().boolean(): # pylint: disable=no-member
        return "female"
    else:
        return "male"

def generate_email(context):
    return generate_fakeemail(context)

def generate_fakeemail(context):
    return f"testli_{generate(context, 'serial', context.generator_locale)}@fake.com"

def generate_date_of_birth(context):
    return (datetime.datetime.now() - relativedelta(years=random.randint(18, 80))).strftime(u"%Y-%m-%dT00:00:00Z")

def generate_uuid(context):
    return uuid.uuid4()

def generate_random_number(context):
    return context.fake.random.randint(1,999999)

def generate_random_integer(context, from_to):
    return random_integer(from_to)

def random_integer(string_to_process):
    (lower, upper) = string_to_process.split(",")
    fake = Faker("de_DE")
    return str(fake.random.randint(int(lower), int(upper)))

def generate_timestamp(date_requested):
    d = None
    ops = {"+": operator.add, "-": operator.sub}
    if date_requested == "now":
        d = datetime.datetime.utcnow()
    else:
        if date_requested[3] in ops:
            m = date_requested[date_requested.find(date_requested[3]) + 1:-1]
            date_type = date_requested[-1]
            if date_type == u"s":
                d = ops[date_requested[3]](datetime.datetime.utcnow(), datetime.timedelta(seconds=int(m)))
            elif date_type == u"m":
                d = ops[date_requested[3]](datetime.datetime.utcnow(), datetime.timedelta(minutes=int(m)))
            elif date_type == u"h":
                d = ops[date_requested[3]](datetime.datetime.utcnow(), datetime.timedelta(hours=int(m)))
            elif date_type == u"d":
                d = ops[date_requested[3]](datetime.datetime.utcnow(), datetime.timedelta(days=int(m)))
            elif date_type == u"w":
                d = ops[date_requested[3]](datetime.datetime.utcnow(), datetime.timedelta(weeks=int(m)))
        else:
            logging.error(f"operator {date_requested[3]} not supported")
    return d
    
def generate_unique_email(length=None):
    """Generates a new email address

    Options for substitutions are:
      - config(): returns string from configurations json
      - context(): returns string from contextual json
      - generate(): generates a new string based on the variable provided
      - object(): returns a string from an test object

    Parameters:
        length (str): Defaults to None, but will extend a generated address to length
    Returns:
        String: The new fancy email address testli_[timestamp]@blah.com
    """
    email = u"testli_%s@fake.com" % str(datetime.datetime.now().strftime(u"%m%d%H%M%S").rstrip(u"000"))

    if length is not None:
        random_value = ""
        if int(length) > len(email):
            length_diff = int(length) - len(email)
            random_value = ''.join(
                [random.choice(string.ascii_letters + string.digits) for n in range(length_diff)]
            )
        email = random_value + email
    return email
