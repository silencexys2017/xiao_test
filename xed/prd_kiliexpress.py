#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import hashlib
from datetime import datetime


merchant_no = "Xedelivery"
merchant_key = "Ih55t85cdMz7iXWiGLhv1X1i5YjX0srp"
account = "business-xedelivery-user"
password = "6nizFUDkwv39SGIscXaj8pAdWMZbQOCh"
test_network_id = "718864912"

base_url = "https://gw.kiliexpress.com"
sign_in_api = "/uac/v1/auth/ability/sign-in"
place_order_api = "/oms/omsExpress/v1.2/createOrder"
get_express_bill_api = "/oms/oms/expressBillPrintData"
get_express_order_info_api = "/oms/omsExpress/v1.0/getExpressOrderInfo"
cancel_order_api = "/oms/omsExpress/v1.0/cancelOrder"
waybill_state_notify_api = "/oms/express/notify/waybillStatus"
waybill_track_notify_api = "/oms/waybill_notify"
get_tracking_api = "/tracking/getTrackingInfos/v3/{}"
get_area_tree_api = "/network/baseArea/availableAreaTree"
get_pick_up_station_api = "/network/network/business/base/getPickupStationList"
prd_express_bill_url = "https://admin.kiliexpress.com/#/pickup/expressSheet100mm?merchantOrderNos={你们的订单号}"
test_express_bill_url = "http://admin.kiliexpress.cn/#/pickup/expressSheet100mm?merchantOrderNos={你们的订单号}"
notify_url = "https://openapi.xedelivery.cn/express/kiliexpress/track/callback"
headers = {"Content-Type": "application/json",
           "Authorization": ""}
auth_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsInN1YiI6IjMyMDMiLCJuYmYiOjE2ODYxMDY0NjksInN1YnMiOnsiVUFDIjoiMzIwMyIsIlNZUy1YRURFTElWRVJZIjoiMzIwMyJ9LCJzY29wZXMiOltdLCJleHAiOjE2ODYxOTI4NjksImlhdCI6MTY4NjEwNjQ2OSwianRpIjoiZjg2Mzk0YjctZWU3OC00MzRmLTk3ZTUtOTc1MjBjYmRhOTMyIn0.-BLi78HYFgiX0SXY3Ej9LG69CSU2kmNa4D0wFjAfvmw"

def hashlib_md5(data):
    return hashlib.md5(data.encode(encoding='utf-8')).hexdigest()


def place_order(
        token, order_type, country_code, platform_biz_type, merchant_no,
        merchant_order_no, order_amount, goods_list, consignee_name,
        consignee_mobile, consignee_country, consignee_province, consignee_city,
        consignee_area_code, consignee_address, consignee_network_id,
        shipper_country, consignee_email=None, consignee_postcode=None,
        shipper_name=None, shipper_mobile=None, shipper_email=None,
        shipper_province=None, shipper_city=None, shipper_area_code=None,
        shipper_address=None, shipper_network_id=None, shipper_postcode=None,
        buyer_id=None, seller_id=None, home_delivery=None, notify_url=None,
        warehouse=None):
    data = {
      "orderType": order_type,   # 订单类型（FB：仓配类FBK订单,ES：快递类Express订单,CB：跨境类CrossBorder订单）
      "countryCode": country_code,
      "platformBizType": platform_biz_type,  # 销售SO 售后RO 调拨AO
      "merchantNo": merchant_no,   # 商户注册时的商户码(如：kilimall)
      "merchantOrderNo": merchant_order_no,
      "orderAmount": order_amount,
      "shipperForm": {
        "shipperName": shipper_name,
        "shipperMobile": shipper_mobile,
        "shipperEmail": shipper_email,
        "shipperCountry": shipper_country,
        "shipperProvince": shipper_province,
        "shipperCity": shipper_city,
        "shipperAreaCode": shipper_area_code,
        "shipperAddress": shipper_address,
        "networkId": shipper_network_id,  # 发货网点ID
        "shipperPostcode": shipper_postcode
      },
      "receiveForm": {
        "consigneeName": consignee_name,
        "consigneeMobile": consignee_mobile,
        "consigneeEmail": consignee_email,
        "consigneeCountry": consignee_country,
        "consigneeProvince": consignee_province,
        "consigneeCity": consignee_city,
        "consigneeAreaCode": consignee_area_code,  # 收货方地区code
        "consigneeAddress": consignee_address,
        "networkId": consignee_network_id,  # 收货网点
        "consigneePostcode": consignee_postcode
      },
      "buyerId": buyer_id,
      "sellerId": seller_id,
      "homeDelivery": home_delivery,  # 是否送货上门（0为自取，1为送货上门，默认0）
      "notifyUrl": notify_url,  # 通知地址
      "warehouse": warehouse   # 仓库编码
    }
    items = []
    for item in goods_list:
        items.append(
            {
                "goodsName": item["goodsName"],
                "goodsCount": item["goodsCount"],
                "goodsUnit": item.get("goodsUnit"),
                "skuId": item["skuId"],
                "storeId": item.get("storeId"),
                "goodsWeight": item.get("goodsWeight"),
                "goodsAmount": item.get("goodsAmount"),
                "currency": item.get("currency"),
                "goodsVolume": item.get("goodsVolume"),
                "remark": item.get("remark"),
                "isBattery": item.get("isBattery"),
                "isPoison": item.get("isPoison"),  # 是否有毒
                "isFragile": item.get("isFragile"),  # 是否易碎
                "hsCode": item.get("hsCode"),  # 海关编码
                "tradeName": item.get("tradeName"),
                "ssAttribute": item.get("ssAttribute")
            }
        )
    data["goodsList"] = items
    data["sign"] = hashlib_md5(json.dumps(data)+merchant_key)
    headers["Authorization"] = token
    result = requests.post(
        base_url+place_order_api, json=data, headers=headers, timeout=60)
    print(result.status_code)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def get_express_bill(token, merchant_order_no):
    headers["Authorization"] = token
    params = {"merchantOrderNos": merchant_order_no}
    result = requests.get(
        base_url + get_express_bill_api, params=params, headers=headers,
        timeout=60)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def get_express_order_info(
        token, logistics_order_no, merchant_order_no, merchant_no,
        waybill_no=None):
    params = {
        "logisticsOrderNo": logistics_order_no,
        "merchantOrderNo": merchant_order_no,
        "merchantNo": merchant_no
    }
    if waybill_no:
        params["waybillNo"] = waybill_no
    headers["Authorization"] = token
    result = requests.get(
        base_url + get_express_order_info_api, params=params, headers=headers,
        timeout=60)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def cancel_order(order_no, merchant_no, waybill_no=None, remark=None,
                 merchant_order_no=None):
    data = {
        "orderNo": order_no,
        "merchantNo": merchant_no,
        "notifyUrl": notify_url
    }
    if waybill_no:
        data["waybillNo"] = waybill_no
    if remark:
        data["remark"] = remark
    if merchant_order_no:
        data["merchantOrderNo"] = merchant_order_no
    result = requests.post(
        base_url + cancel_order_api, json=data, headers=headers, timeout=60)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def waybill_state_notify(waybill_no, status, business_type="SO", remark=None):
    data = {
      "waybillNo": waybill_no,
      "status": status,  # 0创建 15到达国内分拨中心 20到达分拨中心 25到达自提点 30已发货 40有问题 60拒收 65被第三方退回 50用户签收 90取消
      "businessType": business_type
    }
    if remark:
        data["remark"] = remark
    result = requests.post(
        base_url + waybill_state_notify_api, json=data, headers=headers)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def waybill_track_notify(order_no):
    data = {
        "logisticsOrderNo": order_no
    }
    result = requests.post(
        base_url + waybill_track_notify_api, data=data, headers=headers)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def tracks_format_conversion(data):
    tracks = []
    for waybill in data.get("waybillList") or []:
        for node in waybill.get("nodeInfos") or []:
            for track in node.get("trackingInfo") or []:
                tracks.append({
                    "createdAt": datetime.utcfromtimestamp(
                        float(track["trackingTime"])/1000),
                    "description": track["tracking"],
                    "operator": "DLS.Operator.SYSTEM",
                    "operateCode": "DLS.OperateCode.IN_DELIVERING",
                    "operatorId": -1})
    return tracks


def get_tracks(token, merchant_order_no=None, waybill_no=None):
    biz_order_no = merchant_order_no if merchant_order_no else waybill_no
    headers["Authorization"] = token
    result = requests.get(
        base_url + get_tracking_api.format(biz_order_no), headers=headers)
    print(result.url)
    print(result.status_code)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return tracks_format_conversion(res.get("data"))


def get_area_tree(token=None):
    headers["Authorization"] = token if token else auth_token
    result = requests.get(
        base_url + get_area_tree_api, headers=headers, timeout=60)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


def get_pick_up_stations(area_code, token=None):
    params = {"areaCode": area_code}
    headers["Authorization"] = token if token else auth_token
    result = requests.get(base_url + get_pick_up_station_api, params=params,
                          headers=headers, timeout=60)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res
    """
    {'code': 200, 'message': 'successful', 'data': [{'id': 248, 'supplierId': None, 'pickingCode': '1-37', 'address': 'OUTERRING ROAD, TUMAINI SUPERMAKET AT PIPELINE STAGE, ASHMI PLAZA GROUND FLOOR ROOM NO G13 SOFTPRO COMPUTER', 'areaCode': '100102', 'areaId': 294, 'businessTime': None, 'countryCode': 'KE', 'isSupportBigPackage': '1', 'latitude': None, 'longitude': None, 'businessType': 3, 'stationCode': None, 'stationName': 'EMBAKASI SOFTPRO KILISHOP', 'stationSize': None, 'businessName': None, 'pauseStartTime': 1608339874, 'pauseEndTime': 1609039874}]}
    """


def transport_created_order(token):
    return place_order(
        token, order_type="ES", country_code="KE", platform_biz_type="SO",
        merchant_no=merchant_no, merchant_order_no="test129",
        order_amount="100", consignee_name="xiao", consignee_mobile="884384834",
        consignee_country="Kenya", consignee_province="BUSIA",
        consignee_city="Butula", consignee_area_code="Elugulu",
        consignee_address="test address", consignee_network_id="",
        consignee_email=None, consignee_postcode="101001", shipper_name=None,
        shipper_mobile=None, shipper_email=None, shipper_country="KE",
        shipper_province=None, shipper_city=None, shipper_area_code=None,
        shipper_address=None, shipper_network_id=None, shipper_postcode=None,
        buyer_id=None, seller_id=None, home_delivery=1, notify_url=notify_url,
        warehouse=None,
        goods_list=[
            {
                "goodsName": "goods name test",
                "goodsCount": 2,
                "goodsUnit": "piece",
                "skuId": "890304343",
                "storeId": "34",
                "goodsWeight": "200",
                "goodsAmount": "200",
                "currency": "KES",
                "goodsVolume": "100",
                "remark": "remark test",
                "isBattery": None,
                "isPoison": 1,  # 是否有毒
                "isFragile": None,  # 是否易碎
                "hsCode": None,  # 海关编码
                "tradeName": "XiaoMi",
                "ssAttribute": None
            }
        ])


def sign_in():
    data = {
      "authType": "ACCOUNT",
      "accountAuth": {
        "account": account,
        "password": password,
        "captcha": ""
      },
      "workWechatAuth": {}
    }
    result = requests.post(
        base_url + sign_in_api, json=data, headers=headers)
    res = result.json()
    print(res)
    if res.get("code") != 200:
        raise Exception(res.get("error"))
    return res


if __name__ == "__main__":
    # res = sign_in()
    # res = transport_created_order(auth_token)
    # res = get_express_bill(auth_token, merchant_order_no="XD1000348566")
    # res = get_express_order_info(
    #     auth_token, logistics_order_no="", merchant_no=merchant_no,
    #     merchant_order_no="", waybill_no="KE313248870")
    # res = cancel_order(order_no="KEESSOXD6875178480", merchant_no=merchant_no,
    #                    waybill_no=None, remark=None, merchant_order_no=None)
    # res = waybill_state_notify(
    #     waybill_no="KE313248870", status=90, business_type="SO", remark=None)
    # res = waybill_track_notify(order_no="KEESSOSX2635426317")
    # res = get_tracks(
    #     auth_token, merchant_order_no="", waybill_no="KEESSOXD2125406577")
    # res = get_area_tree()
    res = get_pick_up_stations("100123")
    print(res)
