#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

region_api = "http://www.exfcs.com/sylla/api/country/list"
state_api = "http://www.exfcs.com/sylla/api/state/list"
city_api = "http://www.exfcs.com/sylla/api/city/list"
login_api = "http://www.exfcs.com/sylla/api/customer/login"
create_api = "http://www.exfcs.com/sylla/web/order/create"
order_count_api = "http://www.exfcs.com/sylla/web/myorder/count"
order_list_api = "http://www.exfcs.com/sylla/web/myorder/list"
order_detail_api = "http://www.exfcs.com/sylla/web/myorder/detail"
print_api = "http://www.exfcs.com/print/c/"

UID = "PerFeeMM"
PWD = "PerFeeMM@2020"

COOKIE = "cust=/WyuLfNqeWJo4+KzD7rOCFb4Xoklmu1dqgNQS2iOZ/PEAkqwvAB2I0GSkDp" \
         "h4rTUjDw2Doy++stT2+EXwVOHVvhDO8HUG8QrSdV60VyPdcBAH1vesRgY57fztFN" \
         "H2E/f; path=/"


def get_regions():
    result = requests.get(region_api).json()
    print(result)
    res = [
            {
                "id": 1,
                "country": "中国",
                "countryen": "China"
            },
            {
                "id": 4,
                "country": "新加坡",
                "countryen": "Singapore"
            },
            {
                "id": 2,
                "country": "缅甸",
                "countryen": "Myanmar"
            },
            {
                "id": 3,
                "country": "越南",
                "countryen": "Vietnam"
            }]


def get_states(country_id):
    param = {"country": country_id}
    result = requests.get(state_api, params=param).json()

    return result


def get_cities(state_id):
    param = {"state": state_id}
    result = requests.get(city_api, params=param).json()
    # print(result.get("data"))
    return result


def get_all_address():
    addresses = []
    for item in get_states(2).get("data"):
        city_li = []
        for it in get_cities(item["id"]).get("data"):
            city_li.append(
                {"city_id": it.get("id"), "city_name": it.get("cityen")})
        addresses.append(
            {"state_id": item.get("id"), "state_name": item.get("stateen"),
             "cities": city_li})
    return addresses


def get_token_login():
    body = {"uid": UID, "pwd": PWD}
    res = requests.post(login_api, params=body)

    return res.headers


def create_order(
        fruname, frcityid, fraddress, frmob, touname, tocityid, toaddress,
        tomob, itemdescs, itemweight, fremail=None, toemail=None,
        currencyid=1, insured=False, insuredprice=0, paytype=0, payment=1,
        cod=False, codamount=0, remark="PerFee Test"):
    headers = {"cookie": COOKIE}
    data = {
        "fruname": fruname,
        "frcityid": frcityid,
        "fraddress": fraddress,
        "frmob": frmob,
        "touname": touname,
        "tocityid": tocityid,
        "toaddress": toaddress,
        "tomob": tomob,
        "itemdescs": itemdescs,
        "itemweight": itemweight
    }
    if fremail:
        data["fremail"] = fremail
    if toemail:
        data["toemail"] = toemail
    if currencyid:
        data["currencyid"] = currencyid
    if type(insured) is bool:
        data["insured"] = insured
    if insuredprice:
        data["insuredprice"] = insuredprice
    if paytype:
        data["paytype"] = paytype
    if payment:
        data["payment"] = payment
    if type(cod) is bool:
        data["cod"] = cod
    if codamount:
        data["codamount"] = codamount
    if remark:
        data["remark"] = remark

    result = requests.post(create_api, headers=headers, params=data).json()
    return result


def get_order_count():
    headers = {"cookie": COOKIE}
    param = {}
    result = requests.get(order_count_api, headers=headers, params=param)

    # print(result.get("data"))
    return result.json()


def get_order_list(start, size, sn=None, touname=None):
    headers = {"cookie": COOKIE}
    param = {"start": start, "size": size}
    if sn:
        param["sn"] = sn
    if touname:
        param["touname"] = touname
    result = requests.get(order_list_api, headers=headers, params=param).json()
    return result


def get_order_detail(code):
    headers = {"cookie": COOKIE}
    param = {"code": code}
    result = requests.get(
        order_detail_api, headers=headers, params=param).json()
    return result


def print_code(code):
    param = {"code": code}
    result = requests.get(print_api, params=param)
    print(result.text)
    return result


if __name__ == "__main__":
    # get_regions()
    # res = get_states(1)
    # res = get_cities(1)
    res = get_all_address()


    # res = get_token_login()
    # COOKIE = res.get("Set-Cookie")
    # print(COOKIE)

    # res = create_order(
    #     fruname="PerFee", frcityid=1, fraddress="Ruili,", frmob="18684799196",
    #     touname="David", tocityid=68, toaddress="NO.131st street",
    #     tomob="0943179788", itemdescs="gift", itemweight=0.18,
    #     fremail="xiaoyongsheng@perfee.com", toemail="xiaoyongsheng@perfee.com",
    #     currencyid=1, insured=False, insuredprice=0, paytype=0, payment=1,
    #     cod=False, codamount=0, remark="PerFee Test")

    # res = get_order_count()

    # res = get_order_list(start=0, size=2, sn=None, touname=None)

    # res = get_order_detail(code="9ed0a4a8322c5b3e4efcbb98f13d66bb")

    # print_code(code="9ed0a4a8322c5b3e4efcbb98f13d66bb")

    print(json.dumps(res))

