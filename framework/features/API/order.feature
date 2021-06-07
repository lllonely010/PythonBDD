Feature: Verify order through API

    @api
    @utilities
    Scenario Outline: Order limit Negative scenarios 
        Given we store {"uri": "config(environment.mysystem.api)/order"} in the context
        Given we prepare a new api session called test
        Given we perform order request with card count <card_count> via api expect status code <status_code>
        When we log object(context(lastRequestID).data)
        Then if <status_code>==201 do `Then assert that <card_count> will be equal to object(context(lastRequestID).data.pendingApplicationsCount) as expected`
        Then if <status_code>==201 do `Then assert that <remaining_allowed_count> will be equal to object(context(lastRequestID).data.allowedStickersOrderCount) as expected`
        Then if <status_code>!=201 do `Then assert that 2029 will be equal to object(context(lastRequestID).data.pmErrorCode) as expected`
        Then if <status_code>!=201 do `Then assert that You have already ordered 10 stickers. If you need more please contact our customer service (test@est.com) will be equal to object(context(lastRequestID).data.pmErrorMessage) as expected`
        Examples:
            | card_count | status_code | remaining_allowed_count |
            | 8          | 201         | 2                       |
            | 11         | 400         |                         |
            | 10         | 201         | 0                       |
            | 15         | 400         |                         |

    @api
    @utilities
    @phonixx.system.medium
    @phonixx.sit.medium
    @parknow @de-DE @de-AT @business_pro @business_premium
    Scenario Outline: Business Sticker limit Negative scenarios -- Ordering all stickers at once (Business Pro, Business Premium)
        Given we store {"uri": "config(environment.mysystem.api)/order"} in the context
        Given we prepare a new api session called test
        Given we perform order request with card count <card_count> via api expect status code <status_code>
        When we log object(context(lastRequestID).data)
        Then if <status_code>==201 do `Then assert that <card_count> will be equal to object(context(lastRequestID).data.pendingApplicationsCount) as expected`
        Then if <status_code>==201 do `Then assert that <remaining_allowed_count> will be equal to object(context(lastRequestID).data.allowedStickersOrderCount) as expected`
        Then if <status_code>!=201 do `Then assert that 2029 will be equal to object(context(lastRequestID).data.pmErrorCode) as expected`
        Then if <status_code>!=201 do `Then assert that You have already ordered 15 stickers. If you need more please contact our customer service (test@test.com) will be equal to object(context(lastRequestID).data.pmErrorMessage) as expected`
        Examples:
            | card_count | status_code | remaining_allowed_count |
            | 14         | 201         | 1                       |
            | 16         | 400         |                         |
            | 15         | 201         | 0                       |
            | 20         | 400         |                         |