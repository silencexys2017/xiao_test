import json
from dapr.clients import DaprClient


clearing_data = {
    "accAmount": 0,
    "accSummary": "string",
    "accType": "PAYABLE",
    "bizId": "string",
    "bizType": "CHARGE",
    "currency": "string",
    "inAccountId": "string",
    "merchantNo": "string",
    "outAccountId": "string",
    "remark": "string",
    "sign": "string",
    "signType": "string",
    "timestamp": 0
}

# with DaprClient() as client:
#     # Publish an event/message using Dapr PubSub
#     result = client.publish_event(
#         pubsub_name="pubrabbitmq",
#         # topic_name='clearing-message',
#         topic_name='message',
#         data=json.dumps(clearing_data),
#         data_content_type='application/json',
#     )
CONFIG_STORE_NAME = 'configredis'
CONFIG_KEY = 'configuration/psms-common-svc'

dapr_client = DaprClient(address="https://10.43.93.254:443")
configs = dapr_client.get_configuration(
                store_name=CONFIG_STORE_NAME, keys=[CONFIG_KEY]
            ).items.get(CONFIG_KEY).value
print(configs)
