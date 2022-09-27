#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
from urllib.parse import unquote

order_checkout_url = "http://demo45.net.kili.co/api/excashier.html"
query_transaction_url = "https://demo45.net.kili.co/api/queryExcashierOrder.htm"
cancel_order_url = "http://demo45.net.kili.co/api/cancelOrder.htm"
refund_order_url = "http://demo45.net.kili.co/api/orderRefund.htm"
merchant_id = "2016051112014649173095"
# merchant_id = "kilimall-ke"
password = "1234567890"
sign_key = "He4AXjdOmq1G2YH3RKVSS4kqU5VFa4aK"
# sign_key = "Gw416RCMO8tD5MSUg5dok5uQGvR3rPpx"
notify_url = "https://uomnify-test.perfee.com/api/payment/lipapay/webhook"
return_url = "https://uomnify-test.perfee.com/api/payment/lipapay/callback"
refund_notify_url = "https://uomnify-test.perfee.com/api/payment/lipapay/refund"
channels = ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

Headers = {
    # "Authorization": "Bearer",
    "Content-Type": "application/x-www-form-urlencoded"
}


def get_signature(data_dict):
    sorted_keys = sorted(data_dict)
    plain_text = ""
    for key in sorted_keys:
        if data_dict[key] is None or key in ["version", "sign", "countryCode"]:
            continue
        value = str(data_dict[key])
        plain_text = plain_text + str(key) + "=" + value + "&"
    plain_text = plain_text[:-1] + sign_key
    print(plain_text)
    m_hash = hashlib.md5()
    m_hash.update(plain_text.encode("utf-8"))
    return m_hash.hexdigest()


def save_html(file_content):
    with open("lipa_payment" + ".html", "wb") as f:
        f.write(file_content.encode("utf8"))


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
    goods_index = 0
    for goods in goods_list:
        pre_name = "goods["+str(goods_index)+"]."
        data[pre_name + "goodsId"] = goods.get("goodsId")[:32]
        data[pre_name + "goodsName"] = goods.get("goodsName")[:60]
        data[pre_name + "goodsQuantity"] = goods.get("goodsQuantity")
        data[pre_name + "goodsPrice"] = goods.get("goodsPrice")
        data[pre_name + "goodsInfo"] = goods.get("goodsInfo")[:2000]
        data[pre_name + "goodsType"] = goods.get("goodsType")
        data[pre_name + "goodsUrl"] = goods.get("goodsUrl")
        goods_index += 1

    data["sign"] = get_signature(data)
    response_url = order_checkout_url + "?"
    for k, v in data.items():
        if v in [True, False] or v:
            response_url = response_url + str(k) + "=" + str(v) + "&"
    return response_url[:-1]
    # result = requests.post(
    #     url=order_checkout_url, headers=Headers, params=data,
    #     allow_redirects=False)
    # if str(result.status_code).startswith("5"):
    #     raise Exception("Request method not recognised or implemented.")
    # print(result.url)
    # print(result.reason)
    # print(result.history)
    # print(result.headers['Location'])
    # # result.encoding = "utf-8"
    # response = {}
    # save_html(result.text)
    # if payment_method == "OF":
    #     response = result.json()
    # return response, result.url


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


def refund_order(
        merchant_refund_id, order_id, merchant_order_id, amount, reason=None,
        p0=None, payment_trans_id=None, org_name=None, is_use_wallet="N"):
    params = {
        "merchantRefundId": merchant_refund_id,
        "orderId": order_id,
        "merchantOrderId": merchant_order_id,
        "merchantId": merchant_id,
        "amount": amount,
        "signType": "MD5",
        "isPriorityRefundWallet": is_use_wallet,
        "refundNotifyUrl": refund_notify_url,
    }
    if reason:
        params["reason"] = reason
    if p0:
        params["p0"] = p0
    if payment_trans_id:
        params["paymentTransId"] = payment_trans_id
    if org_name:
        params["orgName"] = org_name

    params["sign"] = get_signature(params)
    result = requests.post(
        url=refund_order_url, data=params, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    print(result)
    print(result.json())
    return result


if __name__ == "__main__":
    goods_list = [{
                "goodsId": "32423432",
                "goodsName": "goodsName test",
                "goodsQuantity": "1",
                "goodsPrice": "200",
                "goodsInfo": "tsete324324k",
                "goodsType": "1",
                "goodsUrl": "https://www.kilitest.com/item-900429.html"
            }]
    # res = checkout_order(
    #     amount=60000, currency="KES", merchant_id=merchant_id,
    #     merchant_order_no="343435F3464217",
    #     expiration_time="1000000", source_type="B", goods_list=goods_list,
    #     email="",  mobile="",
    #     seller_id="33333333", seller_account="33333333", buyer_id="4444444",
    #     buyer_account="4444444", customer_ip="10.0.0.140", channels="",
    #     payment_method="OL", custom_field_1=None, custom_field_2=None,
    #     custom_field_3=None, country_code="KE", remark="",
    #     use_installment=False)
    res = query_transaction(order_no="C120220426000015")
    # res = cancel_order(order_no="C120220427000047", amount="23")
    # res = refund_order(
    #     merchant_refund_id="4", order_id="K2204220344557447114",
    #     merchant_order_id="C120220422000071", amount="34342", reason=None,
    #     p0=None, payment_trans_id=None, org_name=None, is_use_wallet="N")

    print(res)
