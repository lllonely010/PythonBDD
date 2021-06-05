Feature: Phonixx:api:status
    Background:
        Given we store {"uri": "https://phonixx.preprod.parkmobile.nl/api/status"} in the context
        Given we prepare a new api session called test


    @api @wip
    @feature.customer.status
    Scenario: Check that status format is OK
        When we perform a GET against context(uri)?format=json using payload of None using test
        Then assert that 200 will be equal to object(test.statuscode) as expected
        Then assert that OK will be equal to object(test.data.message) as expected
        Then assert that Ok will be equal to object(test.data.status) as expected