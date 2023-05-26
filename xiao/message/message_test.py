import requests
import uuid
from requests.auth import HTTPBasicAuth
send_url = "https://gw.kilitest.com/nmdc/v1/send_message"
account = "kili_lite"
password = "Asvg9eyDjWcls9B4pKMUVsbI8"


def send_sms_api(
        msg_id: str, template_code: str, calling_code: str,
        national_number: str, region_code: str,
        msg_type: str, message: str):
    headers = {"content-type": "application/json"}

    data = {
        "apiRequest": [
            {
                "type": ["sms"],
                "msgId": msg_id,
                "templateCode": template_code,
                "areaCode": calling_code,
                "nationalNumber": national_number,
                "siteCode": region_code,
                "smsParams": {msg_type: str(message)}
            }
        ]
    }
    res = requests.post(
        url=send_url, json=data, headers=headers,
        verify=False, auth=HTTPBasicAuth(account, password))
    print(str(res.status_code).startswith("5"))
    resp_sms = res.json()
    print(resp_sms)
    res.raise_for_status()
"""{'status': 400, 'message': 'Template Kilimall_lite_welcome_member_email does not configure channel type : sms'}"""

config = {"message_api": {
          "sendUrl": "https://gw.kilitest.com/nmdc/v1/send_message",
          "account": "kili_lite",
          "password": "Asvg9eyDjWcls9B4pKMUVsbI8"
         }}


class CommunicationApi(object):
    def __init__(self):
        msg_config = config["message_api"]
        self.headers = {"content-type": "application/json"}
        self.send_url = msg_config["sendUrl"]
        self.account = msg_config["account"]
        self.password = msg_config["password"]

    def send_msg(self, a):
        print(self.send_url, a)


def try_do():
    try:
        raise Exception("xiao")
        return 2
    except Exception as e:
        print("lai")
        raise e
    finally:
        print("lklkl")


if __name__ == "__main__":
    # send_sms_api(str(uuid.uuid1()), "Kilimall_lite_welcome_member_email",
    #              "080", "17693438342", "CN", "1", "test")
    try_do()
