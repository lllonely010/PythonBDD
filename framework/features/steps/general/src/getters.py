import ast
import regex
import logging
import json
import os
from .jsons import is_json
from .jsons import search_json


def get_context(context, dot_notation):
    return search_json(context.context, dot_notation)


def get_config(context, dot_notation):
    return search_json(context.configuration, dot_notation)


def get_persona(context, dot_notation):
    return search_json(context.personas, dot_notation)


def get_object(context, dot_notation):
    object_key = dot_notation[:dot_notation.find('.')]
    return_value = str(search_json(
        context.test_objects[object_key].object_data, dot_notation)).replace(")", "$1234567890$")
    return return_value

def get_abspath(context, string_to_process):
    return os.path.abspath(string_to_process)

def get_parse_regex(context, string_to_process):
    s = regex.findall(r"\"(.*?)\", \"(.*)\"",
                      string_to_process, regex.DOTALL)[0]
    (regex_pattern, string_to_search) = s
    # (regex_pattern, string_to_search) = string_to_process.split(',')
    # regex_pattern = regex_pattern.strip()[1:]
    # string_to_search = string_to_search.strip()[1:-1]
    found_strings = regex.findall(regex_pattern, string_to_search)
    if len(found_strings) == 1:
        return found_strings[0]
    else:
        return json.dumps(found_strings)


def get_readxmlfile(context, filepath):
    f = open(filepath, "r")
    s = ""
    for line in f.readlines():
        s += line.strip()
    f.close
    return s


def get_readtxtfile(context, filepath):
    f = open(filepath, "r")
    s = f.read()
    f.close
    return s


def get_simplevalue(context, key_word):
    return context.simple_values[key_word]


def get_length(context, string_to_measure):
    string_to_measure = str(string_to_measure)

    try:
        value = json.loads(string_to_measure)
        if type(value) not in [dict, list]:
            value = str(value)
    except:
        value = str(string_to_measure)

    return str(len(value))


def get_externalconfig(context, string_to_process):
    # This is a temporary solution before we have the ability to pull from the environment under test
    system_under_test = context.system_under_test
    data_config = {
        "test": {
            "phonixx_hostname_default": "parknow.test.parkmobile.nl",
            "phonixx_hostname_be": "be.test.parkmobile.nl",
            "phonixx_hostname_nluk": "phonixx.test.parkmobile.nl",
            "phonixx_hostname_pl": "parkline.test.parkmobile.nl",
            "phonixx_db_server": "10.168.134.252",
            "phonixx_db_database_pm_nluk": "Phonixx_NLUK",
            "phonixx_db_database_pn": "Phonixx_DE",
            "phonixx_db_database_pm_be": "Phonixx_BE",
            "phonixx_db_database_pl": "Phonixx_Parkline",
            "phonixx_db_username": "phonixx_de_Test",
            "phonixx_db_password": "Totoriina2!",
            "phonixx_db_username": "MONEY_DB_USR",
            "phonixx_db_password": "tdWbOQNjXNwb8aHCEYid",
            "consent_db_server": "test-parknow-consent-database.cluster-cpncfp6szzxd.eu-central-1.rds.amazonaws.com",
            "consent_db_name": "consentdb",
            "consent_db_username": "consent_srvc",
            "consent_db_password": "cyJ2ajJ1QWdVZaFRJKDQ",
            "consent_register_api_key": "ApiKey ConsentsRegisterApiKey",
            "consent_jwt_key": "ApiKey JwtGenerationKey",
            "consent_access_control_allow_origin_resp_header": "*",
            "manage_user_consents_by_id_key": "ApiKey ConsentsFullAccessApiKey",
            "consent_webapi": "webapi-consents.test.parknowportal.com",
            "rates_hostname": "rates.test.parknowportal.com",
            "rates_api_key":"PhonixxKey",
            "registrationbff_hostname": "registrationbff.test.parknowportal.com",
            "pr2adapter_hostname": "pr2adapter.test.parknowportal.com",
            "parkingrights_hostname": "parkingright.test.parknowportal.com",
            "inventory_hostname": "inventory.test.parknowportal.com",
            "inventory_apikey": "9db91b93b170bf310c8298f0f1fbcdaadc52ad96",
            "inventory_php_apikey": "9db91b93b170bf310c8298f0f1fbcdaadc52ad96",
            "inventory_forbidden_403_api_key": "ae3d89b2-7f93-4c25-a931-16b8586b0df4",
            "inventorySearch_hostname": "search.inventory.test.parknowportal.com",
            "inventory_db_server":"test-bloxx-inventory-database.cluster-cvvmvvr3besb.eu-central-1.rds.amazonaws.com",
            "inventory_db_database":"UIFTest",
            "inventory_zonesync_apikey":"5b0aa645-8319-4b9b-9c22-055e6bb4b108",
            "operator_hostname": "operator.test.parknowportal.com",
            "enforcementsearch_hostname": "enforcementsearch.test.parknowportal.com",
            "enforcementregister_hostname": "enforcementregister.test.parknowportal.com",
            "enforcementAdapter_hostname": "enforcement-adapters.test.parknowportal.com",
            "enforcementAdapter_external_hostname":"api.enforcement.test.parknowportal.com",
            "authentication_hostname": "authentication.test.parknowportal.com",
            "paris_enforcement_client_credentials": "WmFoeV9TR1RWX1BhcmlzOmI2MmUzMmZmLTY1NmEtNGVhNC1hYWQxLTRkODczYjMyZGU4NA==",
            "sangarHausen_enforcement_client_credentials": "U2FuZ2FySGF1c2VuQ2xpZW50SWQ6ZjAzYzQ2M2EtNzk5NC00ZDdmLTg5MjItNWQ4NGEzYzU5Mzdj",
            "sangerhausen_apikey":"ayushg",
            "enforcement_adapter_client_credentials": "dG91bG91c2U6dG91bG91c2U=",
            "enforcement_adapter_client_multiple_operators": "bmlvcnQtbGltb2dlczpuaW9ydC1saW1vZ2Vz",
            "orchestration_hostname": "orchestration.test.parknowportal.com",
            "tvvist_hostname": "tvvist.test.parknowportal.com",
            "reporting_hostname": "parkingrightreporting.test.parknowportal.com",
            "apiGateway_hostname": "bmwonline.test.parknowportal.com",
            "cale_hostname": "cale.test.parknowportal.com",
            "eligibilityService_hostname": "eligibility.test.parknowportal.com",
            "bloxx_api_key": "PhonixxKey",
            "cale_basic_auth": "Q2FsZTo3M2RhZTc3Ni03YWY2LTRmZTEtYjdhZi1jZTg3MGJkZTdhYmQ=",
            "bmw_api_gateway_auth": "Qm13T25saW5lQ0RQOkZCQzc1M0Q4LUIzRDQtNEVGQi04QjAzLUIwNUExQTQyNTQ0Ng==",
            "bmw_api_gateway_serviceAuth": "Qm13T25saW5lU2VydmljZUFjY291bnQ6RjYyMUY0NzAtOTczMS00QTI1LTgwRUYtNjdBNkY3QzVGNEI4",
            "reporting_external": "U0dSUzpkZWM1ZWM3MC0xZGYwLTQxM2ItOTUxZS03OGRmODU0ZDBmZTg=",
            "cale_api_key": "4fd15dc9-e10e-43e6-9a27-fbf7a0747206",
            "eligibility_api_key": "cc049b47-d46d-40f2-9b51-cbedc11cc7a2",
            "eligibility_api_key_toulouse": "7401630f-808b-43bc-93c3-aadb5acaa0cc",
            "mauticadapter_hostname": "mauticadapter.test.parknowportal.com",
            "phonixx_epms_username_financial_parkmobile_nl-BE": "be_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-BE": "be_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_nl-NL": "nl_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-NL": "nl_sa_tesion01",
            "phonixx_epms_username_financial_parkline_nl-NL": "pl_sf_tesion01",
            "phonixx_epms_username_admin_parkline_nl-NL": "pl_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_en-GB": "uk_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_en-GB": "uk_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-DE": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-DE": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-AT": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-AT": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_fr-FR": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_fr-FR": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-CH": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-CH": "pn_sa_tesion01",
            "phonixx_epms_password": "davinci",
            "tariffinfomanagement_hostname": "tariffinfo-mgmt.test.parknowportal.com",
            "tariffinfomanagement_db_server": "test-bic-tariffinfo-database.cluster-ro-csriosot6shw.eu-west-2.rds.amazonaws.com",
            "tariffinfomanagement_db_database": "TariffInfo",
            "tariffinfomanagement_db_username": "bloxx_tariffinfo_app",
            "tariffinfomanagement_db_password": "YE3AiTMjLJ0Rpd3eakC9",
            "tariffinfo_hostname": "tariffinfo.test.parknowportal.com",
            "tariffInfo_apikey":"ManagementKey",
            "tariffInfoWebApi_apikey":"ManagementKey",
            "adyen_notification_endpoint": "https://b81msvc9ek.execute-api.eu-central-1.amazonaws.com/Stage/notification",
            "adyen_authorization": "Basic VGVzdFVzZXI6RGF2aW5jaTE=",
            "registrationbff_api_key": "da2-y233qrpdvfbxfpi2um7ck74kza",
            "insight_hostname":"insight.test.parknowportal.com",
            "insightClient": "SW5zaWdodFRlc3Q6MmMwNTQwZjYtNmUyMi00YmNiLThmMGMtMjhlZTZjYzAxYjBj",
            "insightUserName": "sangeetha.rageswaran@parkmobile.com",
            "insightUserPassword": "Welcome123",
            "enforcementservice_db_server":"test-bloxx-enforcement-database.cluster-cvvmvvr3besb.eu-central-1.rds.amazonaws.com",
            "enforcementservice_db_database":"EnforcementService",
            "bloxx_db_username":"test_automation",
            "bloxx_db_password":"IgYCOIprViUfVcj1BDCc",
            "parknow_preprod": "accountpages.test.parknowportal.com",
            "parkmobile_for_business": "parkmobile.test.parknowportal.com",
            "adyen_iframe_pn": "parknow.test.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "adyen_iframe_nluk": "phonixx.test.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "gpa_iframe_landing": "parknow.test.parkmobile.nl/Epms/ClientPages/payment/GPA/landing.aspx",
            "x.api.key.parkmobile.nl":"22f9b5b2-3970-4cfb-b74c-73f94d64cd44",
            "enforcementmanagement_hostname":"enforcement-management.test.parknowportal.com",
            "x.api.key.enforcement.management":"e3a1521e-56a0-49da-a63a-4679c1092364",
            "x.api.key.orchestration.fr":"8237b715-c679-4bf9-a742-79f7104fab1e",
            "x.api.key.orchestration.be":"8f0c6811-db5e-46c0-8f3e-47ddebf37edf",
            "tvvist.authorization.header":"UGFyaXNUVlZJU1QwMTpmYmMxOWFiMi1jZmIwLTQzMzgtYjExNi0wZDdkYWEzMjNiYjI=",
            "pollution_hostname" : "pollution.test.parknowportal.com",
            "npr_hostname":"nprtariff.test.parknowportal.com",
            "ediciaUsername":"sa_Grenoble",
            "ediciaPassword":"davinci",
            "testapi_hostname":"testapi.test.parkmobile.nl",
            "x.api.key.testapi":"123456"
        },
        "sit": {
            "phonixx_hostname_default": "parknow.sit.parkmobile.nl",
            "phonixx_hostname_be": "be.sit.parkmobile.nl",
            "phonixx_hostname_nluk": "phonixx.sit.parkmobile.nl",
            "phonixx_hostname_pl": "parkline.sit.parkmobile.nl",
            "phonixx_db_server": "10.128.53.48",
            "phonixx_db_database_pm_nluk": "Phonixx_NLUK",
            "phonixx_db_database_pn": "Phonixx_DE",
            "phonixx_db_database_pm_be": "Phonixx_BE",
            "phonixx_db_database_pl": "Phonixx_Parkline",
            "phonixx_db_username": "testautomation",
            "phonixx_db_password": "5kO72zDEiu95WhKNO1k9",
            "consent_db_server": "sit-parknow-consent-database.cluster-c686azcjgfyq.eu-central-1.rds.amazonaws.com",
            "consent_db_name": "consentdb",
            "consent_db_username": "consent_srvc",
            "consent_db_password": "aqgIsoYpEVcdgNQzAvdK",
            "consent_register_api_key": "ApiKey 341e4157-a2ba-4236-9565-84677a3e5681",
            "consent_jwt_key": "ApiKey 6e297afc-162a-4960-9f0e-ea6efbe6a14d",
            "consent_access_control_allow_origin_resp_header": "https://consent.sit.parknowportal.com",
            "manage_user_consents_by_id_key": "ApiKey 2e83016e-a76a-4782-ae1d-4f280911741b",
            "consent_webapi": "webapi-consents.sit.parknowportal.com",
            "registrationbff_hostname": "registrationbff.sit.parknowportal.com",
            "rates_hostname": "rates.sit.parknowportal.com",
            "rates_api_key":"PhonixxKey",
            "pr2adapter_hostname": "pr2adapter.sit.parknowportal.com",
            "parkingrights_hostname": "parkingright.sit.parknowportal.com",
            "inventory_hostname": "inventory.sit.parknowportal.com",
            "inventory_apikey": "162d2ad7-46b7-4c31-96d7-e8d8ac449ced",
            "inventory_php_apikey": "CDC0B8B8986EFDC91629EA4092F03985A8814A56",
            "inventory_forbidden_403_api_key": "EligibilityKey",
            "inventorySearch_hostname": "search.inventory.sit.parknowportal.com",
            "inventory_db_server":"sit-bloxx-inventory-database.cluster-cft5njpzf6wn.eu-central-1.rds.amazonaws.com",
            "inventory_db_database":"UIFSit",
            "eligibilityService_hostname": "eligibility.sit.parknowportal.com",
            "eligibility_api_key": "6d062c2e-aa70-4461-b3f6-f25c9186432c",
            "eligibility_api_key_toulouse": "7401630f-808b-43bc-93c3-aadb5acaa0cc",
            "enforcementsearch_hostname": "enforcementsearch.sit.parknowportal.com",
            "enforcementregister_hostname": "enforcementregister.sit.parknowportal.com",
            "enforcementAdapter_hostname": "enforcement-adapters.sit.parknowportal.com",
            "enforcementAdapter_external_hostname":"api.enforcement.sit.parknowportal.com",
            "authentication_hostname": "authentication.sit.parknowportal.com",
            "cale_hostname": "cale.sit.parknowportal.com",
            "cale_basic_auth": "Q2FsZTplZDUxMmJlYy1iZmQyLTRhNGUtYjE2Zi1iMjY2MGQ2YjQ1ZGI=",
            "cale_api_key": "4fd15dc9-e10e-43e6-9a27-fbf7a0747206",
            "paris_enforcement_client_credentials": "QW50b25fU0dUVl9QYXJpczozMWZmMWJmMy00NGU2LTQ2N2QtOWQ3Yi0yYjY1Nzg5MWVkNGE=",
            "sangarHausen_enforcement_client_credentials": "U2FuZ2FySGF1c2VuQ2xpZW50SWQ6ODE2NmI5ODYtOTE5MS00ZTczLTljNGYtMmVmZWRkNGMzYTA1",
            "sangerhausen_apikey": "SangarHausenAPISIT",
            "enforcement_adapter_client_credentials": "dG91bG91c2U6dG91bG91c2U=",
            "enforcement_adapter_client_multiple_operators": "bmlvcnQtbGltb2dlczpuaW9ydC1saW1vZ2Vz",
            "reporting_external": "U0dSU1VBVDo0YjYyZjZjZS03MWI4LTQyNmYtOTVhYy1iZGJjMzM1YWZiOWE=",
            "orchestration_hostname": "orchestration.sit.parknowportal.com",
            "tvvist_hostname": "tvvist.sit.parknowportal.com",
            "reporting_hostname": "parkingrightreporting.sit.parknowportal.com",
            "apiGateway_hostname": "bmwonline.sit.parknowportal.com",
            "bloxx_api_key": "41caf45d-5a50-44c4-9f6d-a834d3f4d22a",
            "mauticadapter_hostname": "mauticadapter.sit.parknowportal.com",
            "phonixx_epms_username_financial_parkmobile_nl-BE": "be_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-BE": "be_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_nl-NL": "nl_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-NL": "nl_sa_tesion01",
            "phonixx_epms_username_financial_parkline_nl-NL": "pl_sf_tesion01",
            "phonixx_epms_username_admin_parkline_nl-NL": "pl_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_en-GB": "uk_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_en-GB": "uk_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-DE": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-DE": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-AT": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-AT": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_fr-FR": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_fr-FR": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-CH": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-CH": "pn_sa_tesion01",
            "phonixx_epms_password": "davinci",
            "tariffinfomanagement_hostname": "tariffinfo-mgmt.sit.parknowportal.com",
            "tariffinfomanagement_db_server": "sit-bic-tariffinfo-database.cluster-ro-csriosot6shw.eu-west-2.rds.amazonaws.com",
            "tariffinfomanagement_db_database": "TariffInfo",
            "tariffinfomanagement_db_username": "bloxx_tariffinfo_app",
            "tariffinfomanagement_db_password": "YE3AiTMjLJ0Rpd3eakC9",
            "tariffinfo_hostname": "tariffinfo.sit.parknowportal.com",
            "tariffInfo_apikey":"b78a7bbe-6ce7-47ac-8319-9f183a6c0852",
            "tariffInfoWebApi_apikey":"4341655b-e967-4c87-9f52-13a989d1a5f0",
            "adyen_notification_endpoint": "https://5nnp9h54ej.execute-api.eu-central-1.amazonaws.com/Stage/notification",
            "adyen_authorization": "Basic VGVzdFVzZXI6RGF2aW5jaTE=",
            "registrationbff_api_key": "da2-t7ncn3p6ujbftbdgudokad5spi",
            "insight_hostname":"insight.sit.parknowportal.com",
            "insightClient": "SW5zaWdodDpiZWY1NGRhMi05MGQzLTRjMGYtYjA0NC1kZmU4ZGM4",
            "insightUserName": "sangeetha.rageswaran@parkmobile.com",
            "insightUserPassword": "Welcome123",
            "enforcementservice_db_server":"sit-bloxx-enforcement-database.cluster-cft5njpzf6wn.eu-central-1.rds.amazonaws.com",
            "enforcementservice_db_database":"EnforcementService",
            "bloxx_db_username":"test_automation",
            "bloxx_db_password":"Belc6cFp2ke2RK1y0Erq",
            "parknow_preprod": "accountpages.sit.parknowportal.com",
            "parkmobile_for_business": "parkmobile.sit.parknowportal.com",
            "adyen_iframe_pn": "parknow.sit.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "adyen_iframe_nluk": "phonixx.sit.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "gpa_iframe_landing": "parknow.sit.parkmobile.nl/Epms/ClientPages/payment/GPA/landing.aspx",
            "x.api.key.parkmobile.nl":"52d09e10-210c-4ed2-b92d-9ce3dc2219be",
            "enforcementmanagement_hostname":"enforcement-management.sit.parknowportal.com",
            "x.api.key.enforcement.management":"af507712-6302-44e2-8d57-f49ce565ed1c",
            "x.api.key.orchestration.fr":"2c8bcd4d-c22b-4b89-873f-8850aeb7943c",
            "x.api.key.orchestration.be":"9a09d52f-c133-4968-ab0f-e13d2896bae3",
            "tvvist.authorization.header":"UGFyaXNUVlZJU1QwMTpmYmMxOWFiMi1jZmIwLTQzMzgtYjExNi0wZDdkYWEzMjNiYjI=",
            "pollution_hostname" : "pollution.sit.parknowportal.com",
            "npr_hostname":"nprtariff.sit.parknowportal.com",
            "ediciaUsername":"sa_Grenoble",
            "ediciaPassword":"davinci",
            "operator_hostname": "operator.sit.parknowportal.com",
            "testapi_hostname":"testapi.sit.parkmobile.nl",
            "x.api.key.testapi":"123456"
        },
        "preprod": {
            "phonixx_hostname_default": "parknow.preprod.parkmobile.nl",
            "phonixx_hostname_be": "be.preprod.parkmobile.nl",
            "phonixx_hostname_nluk": "phonixx.preprod.parkmobile.nl",
            "phonixx_hostname_pl": "parkline.preprod.parkmobile.nl",
            "phonixx_db_server": "10.50.21.110",
            # "phonixx_db_server": "10.50.23.197", This is the original A02. Use A01 10.50.21.110 in cases of QDBC driver Error
            "phonixx_db_database_pm_nluk": "Phonixx_NLUK",
            "phonixx_db_database_pn": "Phonixx_DE",
            "phonixx_db_database_pm_be": "Phonixx_BE",
            "phonixx_db_database_pl": "Phonixx_Parkline",
            "phonixx_db_username": "testautomation",
            "phonixx_db_password": "5kO72zDEiu95WhKNO1k9",
            "consent_db_server": "preprod-parknow-consent-database.cluster-cd9ces9cr9zy.eu-central-1.rds.amazonaws.com",
            "consent_db_name": "consentdb",
            "consent_db_username": "consent_srvc",
            "consent_db_password": "E3nGQB06ONYQjKRE9YkI",
            "consent_register_api_key": "ApiKey 75600b90-6ba2-4f72-bad1-5e013174766d",
            "consent_jwt_key": "ApiKey 75600b90-6ba2-4f72-bad1-5e013174766d",
            "consent_access_control_allow_origin_resp_header": "https://consent.preprod.parknowportal.com",
            "manage_user_consents_by_id_key": "ApiKey 75600b90-6ba2-4f72-bad1-5e013174766d",
            "consent_webapi": "webapi-consents.preprod.parknowportal.com",
            "registrationbff_hostname": "registrationbff.preprod.parknowportal.com",
            "rates_hostname": "rates.preprod.parknowportal.com",
            "rates_api_key":"PhonixxKey",
            "pr2adapter_hostname": "pr2adapter.preprod.parknowportal.com",
            "parkingrights_hostname": "parkingright.preprod.parknowportal.com",
            "inventory_hostname": "inventory.preprod.parknowportal.com",
            "inventory_apikey": "97b2d9e5-f439-485a-a26c-c9552dc50f1a",
            "inventory_php_apikey": "CDC0B8B8986EFDC91629EA4092F03985A8814A56",
            "inventory_forbidden_403_api_key": "EligibilityKey",
            "inventorySearch_hostname": "search.inventory.preprod.parknowportal.com",
            "inventory_db_server":"bloxx-inventory-preprod.cluster-csriosot6shw.eu-west-2.rds.amazonaws.com",
            "inventory_db_database":"UIFPreprod",
            "operator_hostname": "operator.preprod.parknowportal.com",
            "enforcementsearch_hostname": "enforcementsearch.preprod.parknowportal.com",
            "enforcementregister_hostname": "enforcementregister.preprod.parknowportal.com",
            "enforcementAdapter_hostname": "enforcement-adapters.preprod.parknowportal.com",
            "enforcementAdapter_external_hostname":"api.enforcement.preprod.parknowportal.com",
            "authentication_hostname": "authentication.preprod.parknowportal.com",
            "paris_enforcement_client_credentials": "QW50b25fU0dUVl9QYXJpczozMWZmMWJmMy00NGU2LTQ2N2QtOWQ3Yi0yYjY1Nzg5MWVkNGE=",
            "sangarHausen_enforcement_client_credentials": "U2FuZ2FySGF1c2VuQ2xpZW50SWQ6MWIzNWRlNmMtMDgyZi00MDBhLWExM2ItOTg4OTFkY2Q2OGVl",
            "sangerhausen_apikey": "SangarHausenAPIPreProd",
            "enforcement_adapter_client_credentials": "dG91bG91c2U6dG91bG91c2U=",
            "enforcement_adapter_client_multiple_operators": "bmlvcnQtbGltb2dlczpuaW9ydC1saW1vZ2Vz",
            "orchestration_hostname": "orchestration.preprod.parknowportal.com",
            "tvvist_hostname": "tvvist.preprod.parknowportal.com",
            "reporting_hostname": "parkingrightreporting.preprod.parknowportal.com",
            "apiGateway_hostname": "bmwonline.preprod.parknowportal.com",
            "cale_hostname": "cale.preprod.parknowportal.com",
            "eligibilityService_hostname": "eligibility.preprod.parknowportal.com",
            "bloxx_api_key": "41caf45d-5a50-44c4-9f6d-a834d3f4d22a",
            "cale_basic_auth": "Q2FsZTplZDUxMmJlYy1iZmQyLTRhNGUtYjE2Zi1iMjY2MGQ2YjQ1ZGI=",
            "bmw_api_gateway_auth": "Qm13T25saW5lQ0RQOkZCQzc1M0Q4LUIzRDQtNEVGQi04QjAzLUIwNUExQTQyNTQ0Ng==",
            "bmw_api_gateway_serviceAuth": "Qm13T25saW5lU2VydmljZUFjY291bnQ6RjYyMUY0NzAtOTczMS00QTI1LTgwRUYtNjdBNkY3QzVGNEI4",
            "bmw_parkopedia":"Qm13UGFya29wZWRpYVNlcnZpY2VBY2NvdW50OkJGRjdGRUI5LUVEMkQtNEU1NC1CRDIzLTE1OEREM0NBQkI1QQ==",
            "bmw_gps":"Qm13T25saW5lUGFya25vdzI6MjFCNUY3OTgtQkU1NS00MkJDLThBQTgtMDAyNUI5MDNEQzNC",
            "cale_api_key": "4fd15dc9-e10e-43e6-9a27-fbf7a0747206",
            "eligibility_api_key": "6d062c2e-aa70-4461-b3f6-f25c9186432c",
            "eligibility_api_key_toulouse": "7401630f-808b-43bc-93c3-aadb5acaa0cc",
            "reporting_external": "U0dSU1VBVDo0YjYyZjZjZS03MWI4LTQyNmYtOTVhYy1iZGJjMzM1YWZiOWE=",
            "mauticadapter_hostname": "mauticadapter.preprod.parknowportal.com",
            "phonixx_epms_username_financial_parkmobile_nl-BE": "be_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-BE": "be_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_nl-NL": "nl_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_nl-NL": "nl_sa_tesion01",
            "phonixx_epms_username_financial_parkline_nl-NL": "pl_sf_tesion01",
            "phonixx_epms_username_admin_parkline_nl-NL": "pl_sa_tesion01",
            "phonixx_epms_username_financial_parkmobile_en-GB": "uk_sf_tesion01",
            "phonixx_epms_username_admin_parkmobile_en-GB": "uk_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-DE": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-DE": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-AT": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-AT": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_fr-FR": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_fr-FR": "pn_sa_tesion01",
            "phonixx_epms_username_financial_parknow_de-CH": "pn_sf_tesion01",
            "phonixx_epms_username_admin_parknow_de-CH": "pn_sa_tesion01",
            "phonixx_epms_password": "davinci",
            "tariffinfomanagement_hostname": "tariffinfo-mgmt.preprod.parknowportal.com",
            "tariffinfomanagement_db_server": "preprod-bic-tariffinfo-database.cluster-ro-csriosot6shw.eu-west-2.rds.amazonaws.com",
            "tariffinfomanagement_db_database": "TariffInfo",
            "tariffinfomanagement_db_username": "bloxx_tariffinfo_app",
            "tariffinfomanagement_db_password": "YE3AiTMjLJ0Rpd3eakC9",
            "tariffinfo_hostname": "tariffinfo.preprod.parknowportal.com",
            "tariffInfo_apikey":"45d1bdfd-468e-4828-82f3-5c792ceb22a2",
            "tariffInfoWebApi_apikey":"4d9dd60b-47f9-4639-9095-64de4d6c781b",
            "adyen_notification_endpoint": "https://piq7m9931d.execute-api.eu-central-1.amazonaws.com/preprod/notification",
            "adyen_authorization": "Basic VGVzdFVzZXI6RGF2aW5jaTE=",
            "registrationbff_api_key": "da2-4brp5osvkzgkxdi7q6wers3xiu",
            "insight_hostname":"insight.preprod.parknowportal.com",
            "insightClient": "SW5zaWdodDpiZWY1NGRhMi05MGQzLTRjMGYtYjA0NC1kZmU4ZGM4",
            "insightUserName": "sangeetha.rageswaran@parkmobile.com",
            "insightUserPassword": "Welcome123",
            "enforcementservice_db_server":"bloxx-enforcement-preprod.cluster-csriosot6shw.eu-west-2.rds.amazonaws.com",
            "enforcementservice_db_database":"EnforcementService",
            "bloxx_db_username":"test_automation",
            "bloxx_db_password":"toVshrVGBe918Rboafkr",
            "parknow_preprod": "accountpages.preprod.parknowportal.com",
            "parkmobile_for_business": "parkmobile.preprod.parknowportal.com",
            "adyen_iframe_pn": "parknow.preprod.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "adyen_iframe_nluk": "phonixx.preprod.parkmobile.nl/Epms/ClientPages/payment/adyen/landing.aspx",
            "gpa_iframe_landing": "parknow.preprod.parkmobile.nl/Epms/ClientPages/payment/GPA/landing.aspx",
            "parknow_api_key":"e091ce05-3fa9-4323-b4fe-bf41a1066697",
            "x.api.key.parkmobile.nl":"52d09e10-210c-4ed2-b92d-9ce3dc2219be",
            "enforcementmanagement_hostname":"enforcement-management.preprod.parknowportal.com",
            "x.api.key.enforcement.management":"af507712-6302-44e2-8d57-f49ce565ed1c",
            "x.api.key.orchestration.fr":"2c8bcd4d-c22b-4b89-873f-8850aeb7943c", 
            "x.api.key.orchestration.be":"9a09d52f-c133-4968-ab0f-e13d2896bae3",
            "tvvist.authorization.header":"UGFyaXNUVlZJU1QwMTpmYmMxOWFiMi1jZmIwLTQzMzgtYjExNi0wZDdkYWEzMjNiYjI=",
            "pollution_hostname" : "pollution.preprod.parknowportal.com",
            "npr_hostname":"nprtariff.preprod.parknowportal.com",
            "nonPromoUsername":"test.nonpromo@parknow.com",
            "bmw_hostname":"customer-i.bmwgroup.com",
            "bmw_username_nl":"sangeetha.rageswaran@park-now.com",
            "bmw_password_nl":"davinci1234",
            "bmw_username_de":"sangeethark.ece@gmail.com",
            "bmw_password_de":"davinci123",
            "bmw_username_de_2":"parknow_dev_int_4@list.bmw.com",
            "bmw_password_de_2":"Parknow12#",
            "bmw_username_nl_2":"parknow_dev_pm_nl@list.bmw.com",
            "bmw_password_nl_2":"Parknow12#",
            "ediciaUsername":"sa_Grenoble",
            "ediciaPassword":"davinci",
            "testapi_hostname":"testapi.preprod.parkmobile.nl",
            "x.api.key.testapi":"ynVqJ3a7YXzQ7fLhDEx3"
        }
    }
    return_value = data_config[system_under_test][string_to_process]

    if "SYSTEM_TARGET" in os.environ:
        if is_json(os.environ["SYSTEM_TARGET"]):
            system_target = json.loads(os.environ["SYSTEM_TARGET"])
            if string_to_process in system_target:
                return_value = system_target[string_to_process]

    return return_value
