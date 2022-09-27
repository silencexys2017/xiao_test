#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time

env = "sandbox"
# API_KEY = "9eSx"
# API_SECRET = "4Y1B4"
# USER_ID = "F2901"

API_KEY = "jizL"
API_SECRET = "zv1cl"
USER_ID = "G4546"

Content_type = "application/json"
# base_url = "https://staging.ecourier.com.bd/api"
base_url = "https://backoffice.ecourier.com.bd/api"
place_order_url = ""
inquiry_url = ""


HEADERS = {
            "API-SECRET": API_SECRET,
            "API-KEY": API_KEY,
            "USER-ID": USER_ID,
            "Content-Type": Content_type
        }


def place_order(
        recipient_name="xiao", recipient_mobile="1991234001",
        recipient_city="Dhaka", recipient_area="Dhaka",
        recipient_address="LuGu", package_code="#2443", product_price=100,
        payment_method="COD", recipient_thana=None, recipient_zip=None,
        product_id=None, comments=None, number_of_item=None,
        actual_product_price=None, parcel_type=None,
        requested_delivery_time=None, pick_hub=None, pick_address=None,
        delivery_hour=None, recipient_landmark=None, special_instruction=None):
    data = {
        "recipient_name": recipient_name,
        "recipient_mobile": recipient_mobile,
        "recipient_city": recipient_city,
        "recipient_area": recipient_area,
        "recipient_thana": recipient_thana,  # 新增
        "recipient_address": recipient_address,
        "package_code": package_code,
        "product_price": product_price,  # pay_method=MPAY, price=0,
        "payment_method": payment_method,
        # Integer(Cash on Delivery-1, Others-2) or Str (COD, MPAY, POS, CCRD)
        "recipient_zip": recipient_zip  # 新增
    }
    if product_id:
        data["product_id"] = product_id
    if comments:
        data["comments"] = comments
    if number_of_item:
        data["number_of_item"] = number_of_item
    if actual_product_price:
        data["actual_product_price"] = actual_product_price
    if parcel_type:
        data["parcel_type"] = parcel_type
    if requested_delivery_time:
        data["requested_delivery_time"] = requested_delivery_time
    if pick_hub:
        data["pick_hub"] = pick_hub
    if pick_address:
        data["pick_address"] = pick_address  # Optional,Default 0
    if delivery_hour:
        data["delivery_hour"] = delivery_hour
    if recipient_landmark:
        data["recipient_landmark"] = recipient_landmark
    if special_instruction:
        data["special_instruction"] = special_instruction

    url = base_url + "/order-place"
    result = requests.post(url, json=data, headers=HEADERS, timeout=150)
    print(result.status_code)
    if result.status_code == 200:
        print("dkfkdkf")
    result = result.json()
    if result.get("response_code") != 200:
        print("place_order fail")

    return result

    """{
    "success": true,
    "errors": [],
    "response_code": 200,
    "message": "Order Submitted",
    "ID": "ECR36145394240920"
    },
    {
    "success": false,
    "response_code": 400,
    "errors": [
        "recipient_zip Parameter either missing or not set correctly. "
    ]
    }"""


def parcel_tracking(product_id=None, ecr=None):
    body = {}
    if product_id:
        body["product_id"] = product_id
    if ecr:
        body["ecr"] = ecr

    url = base_url + "/track"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if result.get("response_code") != 200:
        print("parcel_tracking_query fail")

    return result
    """{
    "success": true,
    "response_code": 200,
    "query_data": {
        "REFID": "ECR36145394240920",
        "company": "PerfeeBD",
        "product_id": "",
        "r_name": "xiao",
        "r_mobile": "1991234001",
        "r_address": "LuGu, Area: Dhaka, District: Dhaka, Thana: Dhaka(8216)",
        "r_area": "Dhaka",
        "r_type": "BOX",
        "r_time": "2020-09-24 09:48:01",
        "paymentmethod": null,
        "paymentclear": "Not yet cleared",
        "r_timing": "Next Day(24hr)",
        "r_coverage": "Inside Dhaka",
        "r_weight": "Up To 500gm",
        "product_price": "100",
        "collected_amount": 0,
        "shipping_price": 50,
        "cod": 0,
        "status": [
            {
                "status": "Initiated",
                "time": "2020-03-11T22:51:06.000000Z",
                "comment": ""
            }
        ]
    }
    }"""


def get_packages():
    body = {}
    url = base_url + "/packages"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    # if result.get("response_code") != 200:
    #     print("get_packages fail")

    return json.dumps(result)


def cancel_order(ecr, comment):
    body = {
        "tracking": ecr,
        "comment": comment
    }

    url = base_url + "/cancel-order"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if result.get("success") is not True:
        print("cancel_order fail")
        if result.get("errors"):
            print(result["errors"])

    return result


def fraud_alert_check(phone_number):
    body = {
        "number": phone_number
    }
    url = base_url + "/fraud-status-check"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if result.get("success") is not True:
        if result.get("errors"):
            print(result["errors"])

    return result


def get_city_list():
    body = {}
    url = base_url + "/city-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])

    return result


def retry_post_requests(params, url):
    retry_times = 0
    is_success = False
    result = {}
    while retry_times < 10 and not is_success:
        try:
            retry_times += 1
            result = requests.post(
                url, params=params, headers=HEADERS, timeout=150).json()
            is_success = True
        except json.decoder.JSONDecodeError as it:
            time.sleep(30)
            print("error info=%s, retry_times=%s" % (it, retry_times))
    if result.get("success") not in [True]:
        if url != "https://backoffice.ecourier.com.bd/api/area-list":
            print(params, url)
        result = {"message": []}
    return result


def get_thana_list(city="Dhaka"):
    body = {
        "city": city
    }

    url = base_url + "/thana-list"
    return retry_post_requests(body, url)


def get_area_list_by_post_code(postcode):
    body = {
        "postcode": postcode
    }

    url = base_url + "/area-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])

    return json.dumps(result)


def get_post_code_list(city, thana):
    body = {
        "city": city,
        "thana": thana
    }
    url = base_url + "/postcode-list"
    result = requests.post(url, params=body, headers=HEADERS, timeout=150).json()
    print(result)
    # if type(result) is not list:
    #     if result.get("errors"):
    #         print(result["errors"])
    #
    # return json.dumps(result)


# def get_branch_list():
#     body = {}
#     url = base_url + "/branch-list"
#     url = "https://pimg.perfee.com/caches/ecourier-branch-list.json"
#     print(HEADERS)
#     print(url)
#     result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
#     if type(result) is not list:
#         if result.get("errors"):
#             print(result["errors"])
#
#     return json.dumps(result)


def get_branch_list():
    body = {}
    url = "https://pimg.perfee.com/caches/ecourier-branch-list.json"
    print(HEADERS)
    print(url)
    result = requests.get("https://pimg.perfee.com/caches/ecourier-branch-list.json").json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])

    return json.dumps(result)


parcel_detail = '[{"product_name":"Men Casual (Elbow Patch) Blazer-Blue",' \
                '"quantity":1},{"product_name":"Men Casual(Elbow Patch) ' \
                'Blazer -Blue","quantity":1}]'

if __name__ == "__main__":
    # res = place_order(
    #     recipient_name="test", recipient_mobile="1991234001",
    #     recipient_city="Dhaka", recipient_area="Dhaka",
    #     recipient_address="test", package_code="#24432", product_price=100,
    #     payment_method="COD", recipient_thana="Dhaka", recipient_zip="8216",
    #     product_id=None, comments=None, number_of_item=None,
    #     actual_product_price=None, parcel_type=None,
    #     requested_delivery_time=None, pick_hub=None, pick_address=None,
    #     delivery_hour=None, recipient_landmark=None,
    #     special_instruction="t84328879")

    # ECR36145394240920
    res = parcel_tracking(product_id="", ecr="ECR24830969080122")
    # res = get_packages()
    # res = cancel_order("ECR68099762291020", "make a mistake")
    # res = fraud_alert_check("01306415251")  # 01306415251
    # res = get_city_list()
    # for it in get_city_list():
    #     res = get_thana_list(it.get("name"))
    #     print(res)
    # res = get_thana_list("Warehouse")
    # res = get_post_code_list("Dhaka", "Lalbag")
    # {'success': True, 'message': [{'name': '1211', 'value': '1211'}]}
    # res = get_area_list_by_post_code(4378)
    # res = get_branch_list()
    print(res)

