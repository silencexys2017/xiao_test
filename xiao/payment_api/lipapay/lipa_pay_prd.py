#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
from urllib.parse import unquote
from copy import deepcopy


order_checkout_url = "https://www.lipapay.com/api/excashier.html"
query_transaction_url = "https://www.lipapay.com/api/queryExcashierOrder.htm"
cancel_order_url = "https://www.lipapay.com/api/cancelOrder.htm"
wallet_info_url = "https://pay.kilimall.com/balance/api/getWalletInfo.htm"
# merchant_id = "LP1645525242888"  # supply
merchant_id = "LP1652932882829"  # lite
# sign_key = "Yx0qb3wWzzG1Je5W97jGTf54bjCZOVgL"
sign_key = "Jd41ybDMvbCfatLo0EyUAZp2SvPU1p6E"
notify_url = "https://uomnify.perfee.com/api/payment/lipapay/webhook"
return_url = "https://uomnify.perfee.com/api/payment/lipapay/callback"
sa = "eyIkYXBwX3ZlcnNpb24iOiI0LjQuMC5EIiwiJGxpYiI6IkFuZHJvaWQiLCIkbGliX3ZlcnNpb24iOiI0LjQuNSIsIiRtYW51ZmFjdHVyZXIiOiJIVUFXRUkiLCIkbW9kZWwiOiJITUEtQUwwMCIsIiRvcyI6IkFuZHJvaWQiLCIkb3NfdmVyc2lvbiI6IjUuMS4xIiwiJHNjcmVlbl9oZWlnaHQiOjE5MjAsIiRzY3JlZW5fd2lkdGgiOjEwODAsIiR3aWZpIjp0cnVlLCIkbmV0d29ya190eXBlIjoiV0lGSSIsIiRjYXJyaWVyIjoiXHU0ZTJkXHU1NmZkXHU3OWZiXHU1MmE4IiwiJGlzX2ZpcnN0X2RheSI6dHJ1ZSwiJGFwcF9pZCI6Im5ldC5raWxpbWFsbC5zaG9wIiwiJHRpbWV6b25lX29mZnNldCI6LTQ4MCwiJGRldmljZV9pZCI6ImI4ZTk0Y2RjOTYyMzIxZWEiLCIkYXBwX25hbWUiOiJLaWxpbWFsbChEKSIsImFwcF9tYXJrZXQiOiJERVYiLCJjbGllbnRfbmFtZSI6ImFuZHJvaWRfYnV5ZXIiLCJwbGF0Zm9ybV90eXBlIjoiQW5kcm9pZCIsImFub255bW91c0lkIjoiYjhlOTRjZGM5NjIzMjFlYSIsImFkanVzdGlkIjoiY2NhYmQ5MmU1YjdlMDY3Nzg0OTNlNjY0ZDZkOGUwYjQiLCIkaXAiOiIxNjAuMjAuNTUuNjYifQ=="
channels = ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

Headers = {
    # "Authorization": "Bearer",
    "Content-Type": "application/x-www-form-urlencoded"
}


def get_signature(data_dict):
    sorted_keys = sorted(data_dict)
    plain_text = ""
    for key in sorted_keys:
        if data_dict[key] is None or key in ["version", "sign"]:
            continue
        value = str(data_dict[key])
        plain_text = plain_text + str(key) + "=" + value + "&"
    plain_text = plain_text[:-1] + sign_key
    print(plain_text)
    m_hash = hashlib.md5()
    m_hash.update(plain_text.encode("utf-8"))
    return m_hash.hexdigest()


def get_signature(data_dict):
    sorted_keys = sorted(data_dict)
    plain_text = ""
    for key in sorted_keys:
        if data_dict[key] in [None, ""] or key \
                in ["version", "sign", "countryCode"]:
            continue
        plain_text = plain_text + str(key) + "=" + str(data_dict[key]) + "&"
    plain_text = plain_text[:-1] + sign_key
    m_hash = hashlib.md5()
    m_hash.update(plain_text.encode("utf-8"))
    return m_hash.hexdigest()


def save_html(file_content):
    with open("lipa_payment" + ".html", "wb") as f:
        f.write(file_content)


def checkout_order(
        amount, currency, merchant_id, merchant_order_no, expiration_time,
        source_type, goods_list, email=None, mobile=None, seller_id=None,
        seller_account=None, buyer_id=None, buyer_account=None,
        customer_ip=None, channels=None, payment_method=None, country_code=None,
        remark=None, use_installment=None, custom_field_1=None,
        custom_field_2=None, custom_field_3=None):
    data = {
        "signType": "MD5",
        "merchantId": merchant_id,
        "notifyUrl": notify_url,
        "returnUrl": return_url,
        "merchantOrderNo": merchant_order_no,
        "amount": amount,
        "expirationTime": expiration_time,
        "sourceType": source_type,
        "currency": currency,
        "countryCode": country_code,
        "version": "1.4"
    }
    if remark:
        data["remark"] = remark
    if email:
        data["email"] = email
    if mobile:
        data["mobile"] = mobile
    if seller_id:
        data["sellerId"] = seller_id
    if seller_account:
        data["sellerAccount"] = seller_account
    if buyer_id:
        data["buyerId"] = buyer_id
    if buyer_account:
        data["buyerAccount"] = buyer_account
    if customer_ip:
        data["customerIP"] = customer_ip
    if channels:
        data["channels"] = channels
    if payment_method:
        data["paymentMethod"] = payment_method
    if use_installment in [False, True]:
        data["useInstallment"] = use_installment
    if custom_field_1:
        data["p1"] = custom_field_1
    if custom_field_2:
        data["p2"] = custom_field_2
    if custom_field_3:
        data["p3"] = custom_field_3

    response_data = deepcopy(data)
    goods_index = 0
    for goods in goods_list:
        pre_name = "goods[" + str(goods_index) + "]."
        data[pre_name + "goodsId"] = goods["goodsId"][:32] if goods["goodsId"] \
            else None
        data[pre_name + "goodsName"] = goods["goodsName"][:60] if \
            goods["goodsName"] else "goods"
        data[pre_name + "goodsQuantity"] = goods["goodsQuantity"]
        data[pre_name + "goodsPrice"] = str(float(goods["goodsPrice"]) * 100)
        data[pre_name + "goodsInfo"] = goods["goodsInfo"][:2000] if \
            goods["goodsInfo"] else None
        data[pre_name + "goodsType"] = goods["goodsType"]
        data[pre_name + "goodsUrl"] = goods["goodsUrl"]
        goods_index += 1
    response_data["sign"] = get_signature(data)
    data["sign"] = response_data["sign"]
    if response_data["sign"] == "cdc33f8e923a0cade4b7da67da49da35":
        print("e3434334")

    goods_li = []
    for goods in goods_list:
        goods_li.append(
            {
                "goodsId": goods["goodsId"][:32] if goods["goodsId"] else None,
                "goodsName": goods["goodsName"][:60] if goods["goodsName"] else
                "goods",
                "goodsQuantity": goods["goodsQuantity"],
                "goodsPrice": str(float(goods["goodsPrice"]) * 100),
                "goodsInfo": goods["goodsInfo"][:2000] if goods["goodsInfo"]
                else None,
                "goodsType": goods["goodsType"],
                "goodsUrl": goods["goodsUrl"]
            }
        )
    response_data["goods"] = goods_li
    response_data["url"] = order_checkout_url
    # return response_data
    result = requests.post(
        url=order_checkout_url, headers=Headers, params=data)
    # if str(result.status_code).startswith("5"):
    #     raise Exception("Request method not recognised or implemented.")
    print(result.url)
    print(result.reason)
    print(result.history)
    # result.encoding = "utf-8"
    response = {}
    # if payment_method == "OF":
    response = result.json()
    return response, result.url


def query_transaction(order_no):
    params = {
        "merchantId": merchant_id,
        "signType": "MD5",
        "merchantOrderNo": order_no
    }
    params["sign"] = get_signature(params)
    result = requests.post(
        url=query_transaction_url, data=params, timeout=30)
    print(result.text)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def cancel_order(order_no, amount):
    params = {
        "merchantId": merchant_id,
        "signType": "MD5",
        "merchantOrderNo": order_no,
        "amount": amount
    }
    params["sign"] = get_signature(params)
    print(params)
    print(cancel_order_url)
    result = requests.post(
        url=cancel_order_url, data=params, timeout=30)
    print(result.status_code)
    print(result.text)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    # response = result.json()
    # if response.get("status") is False:
    #     raise Exception(response.get("message"))
    # return response

def get_wallet_info(account_id, phone=None):
    data = {
        "merchantId": merchant_id,
        "merchantUserId": account_id,
        "currencyCode": "KES",
        "countryCode": "KE",
        "signType": "MD5"
    }
    if phone:
        data["phoneNo"] = phone
    data["sign"] = get_signature(data)
    print(data["sign"])

    result = requests.post(url=wallet_info_url, data=data, timeout=30,
                           verify=False)
    print(result.status_code)
    print(result.json())


if __name__ == "__main__":
    goods_list = [
        {
            "goodsUrl": "https://image.kilimall.com/kenya/shop/store/goods/5824/2022/06/1655026020011e27ae0340f994d4bb326a871e04bcf3a.jpg",
            "goodsId": "17659800",
            "goodsQuantity": "1",
            "goodsInfo": "White,M,100%polyester",
            "goodsName": "2 PCS 2 in 1 Men Clothes TShirts",
            "goodsPrice": "69900.0",
            "goodsType": 1
        },
        {
            "goodsUrl": "https://image.kilimall.com/kenya/shop/store/goods/5872/2020/11/5872_06577545305282980.jpg",
            "goodsId": "15502161",
            "goodsQuantity": "1",
            "goodsInfo": "Black",
            "goodsName": "JC Y30 Bluetooth Earphones Wirel",
            "goodsPrice": "45900.0",
            "goodsType": 1
        }

    ]
    # res = checkout_order(
    #     amount=18200, currency="KES", merchant_id=merchant_id,
    #     merchant_order_no="P12022022600013",
    #     expiration_time="172800", source_type="B", goods_list=goods_list,
    #     email='9991234036@perfeetest.com',  mobile='13052262256',
    #     seller_id="", seller_account="", buyer_id="2",
    #     buyer_account="9**********", customer_ip='172.16.1.49', channels="",
    #     payment_method="AP", custom_field_1="1029", custom_field_2=None,
    #     custom_field_3=None, country_code="KE", remark="",
    #     use_installment=None)
    # res = query_transaction(order_no="a3ec84bd-6ff2-11ed-a008-b6d47b14f78f")
    # res = cancel_order(order_no="4WHDJ2UNAEQQF349", amount="2")
    # res = get_wallet_info(100007985)  # 11166703
    data = {'amount': '200', 'merchantId': 'LP1652932882829', 'merchantOrderNo': '2696f414-f51e-11ed-a751-0255ac10003a', 'orderId': 'K2305180149009409715', 'orgTransId': 'WAA-31243429-31243430', 'p1': '100011497', 'paymentChannel': 'wallet', 'paymentMethod': 'SDK_V1', 'sign': '7c977bf1789e657b376a1709c7efe37b', 'signType': 'MD5', 'status': 'SUCCESS'}
    res = get_signature(data)
    print(res==data.get("sign"))
    print(res)
