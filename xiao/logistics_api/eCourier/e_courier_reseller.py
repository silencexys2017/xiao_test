#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

env = "sandbox"
API_KEY = "9eSx"
API_SECRET = "4Y1B4"
USER_ID = "F2901"
Content_type = "application/json"
base_url = "https://staging.ecourier.com.bd/api"
# base_url = "https://backoffice.ecourier.com.bd/api"


HEADERS = {
            "API-SECRET": API_SECRET,
            "API-KEY": API_KEY,
            "USER-ID": USER_ID,
            "Content-Type": Content_type
        }


def place_order(
        product_id=None, number_of_items=None, actual_product_price=None,
        parcel_detail=None, pick_contact_person=None, pick_division=None,
        ep_name=None, recipient_division=None, recipient_district=None,
        comments=None):
    data = {
        "ep_id": 1,  # Mandatory, (Unique eCommerce Partner ID)
        "pick_district": "Dhaka",
        "pick_thana": "Gulshan",  # ?
        "pick_union": "Gulshan-2",
        "pick_address": "test",
        "pick_mobile": "01306415251",
        "pick_hub": 18488,  # Mandatory, Integer (Your child branch ID)???
        "recipient_name": "xiao",
        "recipient_mobile": "1991234002",
        # "recipient_district": "Dhaka",
        "recipient_city": "Dhaka",
        "recipient_area": "Baridhara",
        "recipient_thana": "Gulshan",  # Default ?
        "recipient_union": "1212",   # Default ?
        "recipient_address": "test",
        "package_code": "#2443",
        "product_price": 120,  # pay_method=MPAY, price=0,
        "payment_method": "COD",  # Str (COD, MPAY, POS, CCRD)
        "product_id": product_id,
        "special_instruction": "so=847328"
    }
    if ep_name:
        data["ep_name"] = ep_name
    if pick_contact_person:
        data["pick_contact_person"] = pick_contact_person
    if pick_division:
        data["pick_division"] = pick_division
    if recipient_division:
        data["recipient_division"] = recipient_division
    if recipient_district:
        data["recipient_district"] = recipient_district
    if product_id:
        data["order_code"] = product_id
    if number_of_items:
        data["number_of_items"] = number_of_items  # int, Default 1
    if actual_product_price:
        data["actual_product_price"] = actual_product_price  # int,Default 0
    if parcel_detail:
        data["parcel_detail"] = parcel_detail
    if comments:
        data["comments"] = comments

    url = base_url + "/order-place-reseller"
    result = requests.post(url, json=data, headers=HEADERS, timeout=150).json()
    if result.get("response_code") != 200:
        print("place_order fail")

    return result


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
    "success": false,
    "response_code": 200,
    "query_data": "No data found"
    }"""


def child_parcel_tracking(ecr):
    body = {"ecr": ecr}
    url = base_url + "/track-child"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if result.get("response_code") != 200:
        print("parcel_tracking_query fail")

    return result


def get_packages():
    body = {}
    url = base_url + "/packages"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    # if result.get("response_code") != 200:
    #     print("get_packages fail")

    return json.dumps(result)
    """
    [
    {
        "package_name": "50tk_INSIDE_DHK",
        "package_code": "#2443",
        "shipping_charge": 50,
        "hour": 24,
        "weight": "Up To 500gm",
        "weightrange": "0-500",
        "delivery_time": "Next Day(24hr)",
        "coverage_id": "Inside Dhaka",
        "package_type": "General Package",
        "start_time": "00:00:00",
        "end_time": "23:59:59",
        "coverage": "Inside Dhaka"
    }]
    """


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
    """{'success': False, 'message': 'Order not Canceled'}"""


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

    return json.dumps(result)
    # [{"name": "Bagherhat", "value": "Bagherhat"},]


def get_thana_list(city="Dhaka"):
    body = {
        "city": city
    }

    url = base_url + "/thana-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])

    return json.dumps(result)
    """{
    "success": true,
    "message": [
        {
            "name": "Ashulia",
            "value": "Ashulia"
        }]}"""


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
    """{
    "success": true,
    "message": [
        {
            "name": "Enam Medical",
            "value": "Enam Medical"
        }
    ]
    }"""


def get_post_code_list(city, thana):
    body = {
        "city": city,
        "thana": thana
    }
    url = base_url + "/postcode-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    print(result)
    # if type(result) is not list:
    #     if result.get("errors"):
    #         print(result["errors"])
    #
    # return json.dumps(result)


def get_branch_list():
    body = {}
    url = base_url + "/branch-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])

    return result
    """[
    {
        "name": "Dhanmondi Hub",
        "value": 18488
    }]"""


def label_print(ecr):
    body = {
        "tracking": ecr
    }
    url = base_url + "/label-print"
    result = requests.post(url, json=body, headers=HEADERS, timeout=60)
    print(result.headers)
    print(result.status_code)
    print(result.content.decode("utf8"))
    result = result.json()
    if result.get("success") in [False, None]:
        if result.get("errors"):
            print(result["errors"])

    return result


parcel_detail = '[{"product_name":"Men Casual (Elbow Patch) Blazer-Blue",' \
                '"quantity":1},{"product_name":"Men Casual(Elbow Patch) ' \
                'Blazer -Blue","quantity":1}]'

if __name__ == "__main__":
    # res = place_order(
    #     product_id="F90001", number_of_items=None, actual_product_price=None,
    #     parcel_detail=None, pick_contact_person=None, pick_division=None,
    #     ep_name=None, recipient_division=None, recipient_district="test",
    #     comments="Test")
    # ECR39694162051120  really reseller: ECR57936086101120
    # ECR74595033101120
    res = parcel_tracking(product_id=None, ecr="ECR30847532101120")
    # res = child_parcel_tracking(ecr="ECR19593784101120")
    # res = get_packages()
    # res = cancel_order("ECR19593784101120", "make a mistake")
    # res = fraud_alert_check("01306415251")
    # res = get_city_list()
    # res = get_thana_list("Dhaka")
    # res = get_post_code_list("Dhaka", "Ashulia")
    # res = get_area_list_by_post_code(1349)
    # res = get_branch_list() # ECR89207706101120
    # res = label_print(ecr="ECR19593784101120")
    print(res)

