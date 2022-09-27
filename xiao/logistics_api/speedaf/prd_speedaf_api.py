#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import time
import hashlib
from pyDes import des, CBC, PAD_PKCS5

import base64

# app_code = "TT660041"
# secret_key = "9tLIDTfB"
# customer_code = "860046"
platform_source = "QINANXINXI"
app_code = "880024"
secret_key = "cs3d7791"
customer_code = "2340024"
prd_cn_customer_code = "860095"
des_iv = 0x12, 0x34, 0x56, 0x78, 0x90, 0xAB, 0xCD, 0xEF

place_order_api = "https://apis.speedaf.com/open-api/express/order/createOrder"
print_order_api = "https://apis.speedaf.com/open-api/express/order/print"
query_track_api = "https://apis.speedaf.com/open-api/express/track/query"
cancel_order_api = "https://apis.speedaf.com/open-api/express/order/cancelOrder"
subscribe_track_api = "https://apis.speedaf.com/open-api/express/track/subscribe"
get_areas_api = "https://apis.speedaf.com/open-api/common/area/getArea"
get_area_tree_api = "https://apis.speedaf.com/open-api/common/area/getAreaTree"

notify_url = "https://openapi.xedelivery.cn/express/speedaf/track/callback"
place_order_url = ""
inquiry_url = ""

params = {
    "appCode": app_code,
    "timestamp": int(time.time())
}

headers = {
            "Content-Type": "application/json",
            "X-Forwarded-For":  "114.119.188.180"
            # "X-Forwarded-For": "159.138.90.156"
        }
proxies = {'http': '47.241.40.42'}


def hashlib_md5(data):
    return hashlib.md5(data.encode(encoding='utf-8')).hexdigest()


def des_encrypt(data):
    # secret_key = "12345678"
    k = des(secret_key, CBC, IV=des_iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(data)
    data = base64.b64encode(en).decode("utf-8")
    print(data)
    return data


def des_decrypt(data):
    # secret_key = "12345678"
    k = des(secret_key, CBC, des_iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(base64.b64decode(data)).decode("utf-8")
    return json.loads(de)


def get_area_tree(country_code, env="test"):
    data = json.dumps({"countryCode": country_code})
    timestamp = str(int(time.time()*1000))
    params["timestamp"] = timestamp
    body = {
      "data": data,
      "sign": hashlib_md5(timestamp+secret_key+data)
    }

    result = requests.post(
        get_area_tree_api, params=params, data=des_encrypt(json.dumps(body)),
        headers=headers, proxies=None, timeout=60)
    print(result.request.url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("get_area_tree fail")

    return json.dumps(result)


def get_areas(country_code, parent_code, type):
    data = json.dumps({
        "countryCode": country_code,
        "parentCode": parent_code,
        "type": type
    })
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }
    result = requests.post(
        get_areas_api, params=params, json=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.status_code)
    print(result.request.path_url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("get_areas fail")

    return result


def print_sheet(waybill_no_list, label_type):
    data = json.dumps({
        "waybillNoList": waybill_no_list, "labelType": label_type})
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }

    result = requests.post(
        print_order_api, params=params, data=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.request.url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("print_sheet fail")

    return result


def query_track(mail_no_list):
    data = json.dumps({"mailNoList": mail_no_list})
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }

    result = requests.post(
        query_track_api, params=params, data=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.request.url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("query_track fail")

    return result


def subscribe_track(mail_no, consumer_code):
    data = json.dumps({
        "mailNo": mail_no,
        "customerCode": consumer_code,
        "notifyUrl": notify_url
    })
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }

    result = requests.post(
        subscribe_track_api, params=params, data=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.request.url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("subscribe_track fail")

    return result


def cancel_order(orders):
    data = json.dumps([{
        "customerCode": order.get("customerCode"),
        "billCode": order.get("billCode"),
        "cancelReason": order.get("cancelReason"),
        "cancelBy": order.get("cancelBy"),
        "cancelTel": order.get("cancelTel")
    } for order in orders])
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }

    result = requests.post(
        cancel_order_api, params=params, data=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.request.url)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("cancel_order fail")

    return result


def place_order(
        accept_name, accept_address, accept_country_code, accept_province_name,
        accept_city_name, accept_district_name, send_name, send_address,
        send_mobile, send_country_code, send_province_name, send_city_name,
        send_district_name, parcel_weight, piece, goods_qty, parcel_type,
        delivery_type, transport_type, ship_type, pick_up_aging, pay_method,
        item_list, accept_post_code=None, accept_phone=None, accept_mobile=None,
        accept_email=None, accept_company_name=None, accept_country_name=None,
        accept_province_code=None, accept_city_code=None,
        accept_district_code=None, custom_order_no=None, send_company_name=None,
        send_post_code=None, send_phone=None, send_mail=None,
        send_country_name=None, send_province_code=None, send_city_code=None,
        send_district_code=None, parcel_length=None, parcel_width=None,
        parcel_high=None, parcel_volume=None, shipping_fee=None, cod_fee=None,
        insure_price=None, currency_type=None, small_code=None,
        packet_center_code=None, three_sections_code=None,
        pre_pick_up_time=None, remark=None):
    data = {
        "acceptAddress": accept_address,
        "acceptCityCode": accept_city_code,
        "acceptCityName": accept_city_name,
        "acceptCompanyName": accept_company_name,
        "acceptCountryCode": accept_country_code,
        "acceptCountryName": accept_country_name,
        "acceptDistrictCode": accept_district_code,
        "acceptDistrictName": accept_district_name,
        "acceptEmail": accept_email,
        "acceptMobile": accept_mobile,
        "acceptName": accept_name,
        "acceptPhone": accept_phone,
        "acceptPostCode": accept_post_code,
        "acceptProvinceCode": accept_province_code,
        "acceptProvinceName": accept_province_name,
        "currencyType": currency_type,
        "codFee": cod_fee,
        "customOrderNo": custom_order_no,
        "customerCode": customer_code,
        "parcelHigh": parcel_high,
        "parcelLength": parcel_length,
        "parcelVolume": parcel_volume,
        "parcelWeight": parcel_weight,
        "parcelWidth": parcel_width,
        "goodsQTY": goods_qty,
        "insurePrice": insure_price,
        "piece": piece,
        "remark": remark,
        "sendAddress": send_address,
        "sendCityCode": send_city_code,
        "sendCityName": send_city_name,
        "sendCompanyName": send_company_name,
        "sendCountryCode": send_country_code,
        "sendCountryName": send_country_name,
        "sendDistrictCode": send_district_code,
        "sendDistrictName": send_district_name,
        "sendMail": send_mail,
        "sendMobile": send_mobile,
        "sendName": send_name,
        "sendPhone": send_phone,
        "sendPostCode": send_post_code,
        "sendProvinceCode": send_province_code,
        "sendProvinceName": send_province_name,
        "shippingFee": shipping_fee,
        "deliveryType": delivery_type,
        "payMethod": pay_method,
        "parcelType": parcel_type,
        "shipType": ship_type,
        "transportType": transport_type,
        "pickUpAging": pick_up_aging,
        "prePickUpTime": pre_pick_up_time,
        "platformSource": platform_source,
        "smallCode": small_code,
        "threeSectionsCode": three_sections_code,
        "packetCenterCode": packet_center_code
    }
    items = []
    for item in item_list:
        items.append(
            {
                "battery": item["battery"],
                "blInsure": item["blInsure"],
                "dutyMoney": item.get("dutyMoney"),
                "goodsId": item.get("goodsId"),
                "goodsMaterial": item.get("goodsMaterial"),
                "goodsName": item["goodsName"],
                "goodsNameDialect": item.get("goodsNameDialect"),
                "goodsQTY": item["goodsQTY"],
                "goodsRemark": item.get("goodsRemark"),
                "goodsRule": item.get("goodsRule"),
                "goodsType": item["goodsType"],
                "goodsUnitPrice": item.get("goodsUnitPrice"),
                "goodsValue": item["goodsValue"],
                "goodsWeight": item.get("goodsWeight"),
                "goodsHigh": item.get("goodsHigh"),
                "goodsLength": item.get("goodsLength"),
                "goodsWidth": item.get("goodsWidth"),
                "goodsVolume": item.get("goodsVolume"),
                "makeCountry": item.get("makeCountry"),
                "salePath": item.get("salePath"),
                "sku": item["sku"],
                "unit": item.get("unit"),
                "currencyType": item.get("currencyType")
            }
        )
    data["itemList"] = items
    data = json.dumps(data)
    timestamp = str(int(time.time() * 1000))
    params["timestamp"] = timestamp
    body = {
        "data": data,
        "sign": hashlib_md5(timestamp + secret_key + data)
    }

    result = requests.post(
        place_order_api, params=params, json=des_encrypt(json.dumps(body)),
        headers=headers, timeout=60)
    print(result.status_code)
    result = result.json()
    if result.get("success"):
        result = des_decrypt(result["data"])
    else:
        print("place_order fail")

    return result


def transport_created_order():
    return place_order(
        accept_name="xiao", accept_address="#343street,200room",
        accept_country_code="NG", accept_province_name="test",
        accept_city_name="test", accept_district_name="test",
        send_name="she", send_address="YueLu", send_mobile="01379343",
        send_country_code="CN", send_province_name="湖南省",
        send_city_name="长沙市", send_district_name="岳麓区",
        parcel_weight="1.23", piece=1, goods_qty=3, parcel_type="PT01",
        delivery_type="DE01", transport_type="TT01", ship_type="ST01",
        pick_up_aging=1, pay_method="PA01",
        item_list=[{
            "battery": 0, "blInsure": 0, "dutyMoney": 1000, "goodsId": "19999",
            "goodsMaterial": "", "goodsName": "item mane",
            "goodsNameDialect": "item name", "goodsQTY": 2,
            "goodsRemark": "goodsRemark", "goodsRule": "goodsRule",
            "goodsType": "IT02", "goodsUnitPrice": 1, "goodsValue": 190,
            "goodsWeight": 1.45, "goodsHigh": 100, "goodsLength": 200,
            "goodsVolume": 1.52, "makeCountry": "makeCountry",
            "salePath": "salePath", "sku": "sku001", "unit": "",
            "goodsWidth": 200
            }],
        accept_post_code="acceptPostCode", accept_phone="999999",
        accept_mobile="1778922222",
        accept_email="123@Test.com", accept_company_name="Xiao COM",
        accept_country_name="Nigiera",
        accept_province_code=None, accept_city_code=None,
        accept_district_code="acceptDistrictName", custom_order_no="E3434",
        send_company_name=None,
        send_post_code="413405", send_phone="1764343435",
        send_mail="34324532.qq.com",
        send_country_name="China", send_province_code="41000",
        send_city_code=None, send_district_code=None,
        parcel_length=None, parcel_width=None,
        parcel_high=None, parcel_volume=None, shipping_fee=None, cod_fee=None,
        insure_price=None, currency_type=None, small_code=None,
        packet_center_code=None, three_sections_code=None,
        pre_pick_up_time=None, remark="32432432")


if __name__ == "__main__":
    # res = transport_created_order()
    # res = print_sheet(["47234208932022"], 1)
    # res = query_track(["47234208932022"])
    # res = subscribe_track("47234208932022", "860046")
    # res = cancel_order([
    #     {
    #         "customerCode": "860046",
    #         "billCode": "47234208932022",
    #         "cancelReason": "客户取消发货",
    #         "cancelBy": "xiao",
    #         "cancelTel": "1743843434"
    #     }
    # ])
    # res = get_areas(country_code="CN", parent_code=None, type=0)
    res = get_area_tree(country_code="KE")
    # res = des_encrypt("3432432")
    # body = json.dumps({
    #     "data": "123456",
    #     "sign": "905f4a332552cd980967b11e96ce7592"
    # })

    # res = des_encrypt(body)
    # res = des_decrypt(
    #     "VUfHje/5d11FQaNBFssotZ5JzR29I9tWUbApM+qcmhLLFdRHbn83VYmtyK5/xSoKlHytnHckQeSV+L9v4PsWbdpdrsCGM3jT")
    print(res)
