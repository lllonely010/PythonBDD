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
        "emailmailinator": generate_mailinatoremail,
        "otherlocale": generate_otherlocale,
        "phonenumber": generate_phonenumber,
        "intphonenumber": generate_int_phonenumber,
        "boolean": generate_boolean,
        "gender": generate_gender,
        "iban": generate_iban,
        "vrn": generate_vrn,
        "vrn_chomped": generate_vrn_chomped,
        "serial": generate_serial,
        "firstname": generate_firstname,
        "lastname": generate_lastname,
        "street": generate_street,
        "streetnumber": generate_streetnumber,
        "city": generate_city,
        "zipcode": generate_zipcode,
        "emptystring": generate_emptystring,
        "mobileCountryPrefix": generate_mobileCountryPrefix,
        "vatno": generate_vatno,
        "extendedvatno": generate_extendedvatno,
        "countrycode": generate_countrycode,
        "supplierid": generate_supplierid,
        "dateofbirth": generate_date_of_birth,
        "now": generate_now,
        "locale": generate_locale,
        "product": generate_product,
        "apptype": generate_app_product_type,
        "validzone": generate_validzone,
        "validIVR": generate_validIVR,
        "validIVRzone1": generate_validIVRzone1,
        "validIVRExtendedzone2": generate_validIVRExtendedzone2,
        "uuid": generate_uuid,
        "random_number": generate_random_number,
        "longitude": generate_longitude,
        "latitude": generate_latitude,
        "app_package": generate_app_package,
        "password": generate_password,
        "operator_id": generate_valid_operator_id,
        "poi_id": generate_valid_poi_id,
        "validoffstreetpoi" : generate_validoffstreetpoi,
        "validonstreetpoi" : generate_validonstreetpoi,
        "zone_code": generate_valid_zone_code,
        "opening_hours": generate_opening_hours_id,
        "platform_type": generate_app_platform_type,
        "appium_driver_provider": generate_appium_driver_provider,
        "membership_type": generate_membership_type,
        "transactioncost": generate_transactioncost,
        "membership_type_value": generate_membership_type_value,
        "shortcode": generate_shortcode,
        "networkoperator" : generate_networkoperator,
        "membership_group_type_value": generate_membership_group_type_value
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

def generate_longitude(context):
    return {
        "de-DE": "52.505450",
        "de-AT": "48.213599",
        "de-CH": "47.335981",
        "fr-FR": "48.854404",
        "fr-CH": "47.552593",
        "en-GB": "51.267268",
        "nl-BE": "50.823581",
        "nl-NL": "52.326422"
    }[context.generator_locale]

def generate_membership_type_value(context):
    return {
        "private_transactional": "Transactional",
    }[context.membership_type]

def generate_membership_group_type_value(context):
    return {
        "private_transactional": "None",
    }[context.membership_type]

def generate_latitude(context):
    return {
        "nl-NL": "4.951878"
    }[context.generator_locale]

def generate_validzone(context):
    test_data = {

        "nl-NL": ["10004","36350"]
    }
    random_index = context.fake.random.randint(1, len(test_data[context.generator_locale])) - 1
    return test_data[context.generator_locale][random_index]

def generate_validoffstreetpoi(context):
    return str(71923)

def generate_validonstreetpoi(context):
    return str(70206)

def generate_supplierid(context):
    return {
        "parkmobile": {
            "nl-NL": "20",
        }
    }[context.product][context.generator_locale]

def generate_countrycode(context):
    return {
        "nl-NL": "NL",
    }[context.generator_locale]

def generate_extendedvatno(context):
    vat_codes = {
        "de-CH": "CHE-123.456.788 TVA"
    }
    if context.generator_locale in vat_codes:
        return vat_codes[context.generator_locale]
    else:
        return "UNKNOWN"

def generate_vatno(context):
    return {
        "nl-NL": "NL234567876B01"
    }[context.generator_locale]

def generate_iban(context):
    options = {
        "nl-NL": "NL36TEST0236169114"
    }
    return Faker().numerify(text=options[context.generator_locale]) # pylint: disable=no-member

def generate_phonenumber(context):
    options = {
        "nl-NL": "065#######"
    }
    return Faker().numerify(text=options[context.generator_locale]) # pylint: disable=no-member



def generate_int_phonenumber(context):
    options = {
        "nl-NL": "+3165#######"
    }
    return Faker().numerify(text=options[context.generator_locale]) # pylint: disable=no-member

def generate_mobileCountryPrefix(context):
    return {
        "nl-NL": 31
    }[context.generator_locale]

def generate_otherlocale(context):
    locale_lookup = {
        "nl-NL": "nl_NL"
    }
    temp_locale = {}
    for p_locale in locale_lookup:
        if p_locale != context.generator_locale:
            temp_locale[p_locale] = locale_lookup[p_locale]
    return list(temp_locale.keys())[random.randint(0, len(temp_locale)-1)]

def generate_password(context):
    return ''.join(random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=10))

def generate_serial(context):
    return ''.join(
        [random.choice(string.ascii_letters + string.digits) for n in range(6)]
    ).upper()

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

def generate_vrn(context):
    return_item = context.fake.license_plate() # pylint: disable=no-member
    if "Ö" in return_item:
        context.generate_requests["vrn"] = context.generate_requests["vrn"] + 1
        return_item = generate(context, "vrn", context.generator_locale)
    return return_item

def generate_vrn_chomped(context):   
    return generate_vrn(context).replace("-", "").replace(" ", "")

def generate_email(context):
    return generate_fakeemail(context)

def generate_fakeemail(context):
    return f"testli_{generate(context, 'serial', context.generator_locale)}@fake.com"

def generate_mailinatoremail(context):
    return f"testli_{generate(context, 'serial', context.generator_locale)}@parknow.m8r.co"

def generate_date_of_birth(context):
    return (datetime.datetime.now() - relativedelta(years=random.randint(18, 80))).strftime(u"%Y-%m-%dT00:00:00Z")

def generate_locale(context):
    return context.locale

def generate_product(context):
    return context.product

def generate_app_product_type(context):
    return context.app_product_type

def generate_app_package(context):
    return context.app_package

def generate_app_platform_type(context):
    return context.app_platform_type

def generate_appium_driver_provider(context):
    return context.appium_driver_provider

def generate_membership_type(context):
    return context.membership_type

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

def generate_valid_operator_id(provider_id=None):
    """Generates the valid operator id for the existing provider
    Options for substitutions are:
      - config(): returns string from configurations json
      - context(): returns string from contextual json
      - generate(): generates a new string based on the variable provided
      - object(): returns a string from an test object
    Parameters:
        provider_id (str): Defaults to None, but will be changed and used when the test data storage is created
    Returns:
        String: The existing operator id
    """
    return str(98765)

def generate_valid_poi_id(zone_code=None):
    """Generates the valid POI id for the existing zone_code
    Options for substitutions are:
      - config(): returns string from configurations json
      - context(): returns string from contextual json
      - generate(): generates a new string based on the variable provided
      - object(): returns a string from an test object
    Parameters:
        zone_code (str): Defaults to None, but will be changed and used when the test data storage is created
    Returns:
        String: The existing POI id
    """
    return str(98765)

def generate_valid_zone_code(operator_id=None):
    """Generates the valid zone code for the existing operator id
    Options for substitutions are:
      - config(): returns string from configurations json
      - context(): returns string from contextual json
      - generate(): generates a new string based on the variable provided
      - object(): returns a string from an test object
    Parameters:
        operator_id (str): Defaults to None, but will be changed and used when the test data storage is created
    Returns:
        String: The existing zone_code
    """
    return str(98765)

def generate_opening_hours_id(poi_id=None):
    """Generates the valid zone code for the existing POI
    Options for substitutions are:
      - config(): returns string from configurations json
      - context(): returns string from contextual json
      - generate(): generates a new string based on the variable provided
      - object(): returns a string from an test object
    Parameters:
        poi_id (str): Defaults to None, but will be changed and used when the test data storage is created
    Returns:
        String: The opening hours id for the POI
    """
    return str(27)

def generate_transactioncost(context):
    return {
        "parkmobile": {
            "private_transactional":{
                "nl-BE": "0.30",
                "nl-NL": "0.30"
            }
        }

    }[context.product][context.membership_type][context.generator_locale]

def generate_validIVRzone1(context):
    test_data = {
        "nl-NL": ["9200"]
    }
    random_index = context.fake.random.randint(1, len(test_data[context.generator_locale])) - 1
    return test_data[context.generator_locale][random_index]

def generate_validIVRExtendedzone2(context):
    test_data = {
        "nl-NL": ["1910"]
    }
    random_index = context.fake.random.randint(1, len(test_data[context.generator_locale])) - 1
    return test_data[context.generator_locale][random_index]   

def generate_validIVR(context):
    test_data = {
        "parkmobile":{
            "nl-NL": ["207990000"]
        },        
    }
    random_index = context.fake.random.randint(1, len(test_data[context.product][context.generator_locale])) - 1
    return test_data[context.product][context.generator_locale][random_index]
    
def generate_shortcode(context):
    test_data = {
        "parkmobile":{
            "nl-NL": ["4111"],
            "nl-BE": ["4810"]
        },
         "parknow":{
            "de-DE": ["82555"]      
        },
         "parkline":{
            "nl-NL": ["4111"]      
        },
    }
    random_index = context.fake.random.randint(1, len(test_data[context.product][context.generator_locale])) - 1
    return test_data[context.product][context.generator_locale][random_index]


def generate_networkoperator(context):
    test_data = {
        "parkmobile":{
            "nl-NL": ["pm"],
        }
    }
    random_index = context.fake.random.randint(1, len(test_data[context.product][context.generator_locale])) - 1
    return test_data[context.product][context.generator_locale][random_index]



