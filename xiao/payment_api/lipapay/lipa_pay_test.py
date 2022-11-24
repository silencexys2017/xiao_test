#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import json
import copy


# get_wallet_info_api = "http://walletdemo45.net.kili.co/api/getWalletInfo.htm"
get_wallet_info_api = "https://lipapay-wallet.kilitest.com/api/getWalletInfo.htm"
update_wallet_phone_api = "https://lipapay-wallet.kilitest.com/api/user/updateBindPhoneNo.html"
wallet_payment_api = "https://lipapay-cashier.kilitest.com/api/walletPayment.htm"
# order_checkout_url = "http://demo45.net.kili.co/api/excashier.html"
sdk_checkout_url = "https://lipapay-cashier.kilitest.com/v2/user/sdkSubmitPayment"
# sdk_checkout_url = "https://pay.kilimall.com/cashier/v2/user/sdkSubmitPayment"
order_checkout_url = "https://lipapay-cashier.kilitest.com/v2/app/excashierCreateOrder"
# query_transaction_url = "http://demo45.net.kili.co/api/queryExcashierOrder.htm"
query_transaction_url = "https://lipapay-cashier.kilitest.com/api/queryExcashierOrder.htm"
cancel_order_url = "https://lipapay-cashier.kilitest.com/api/cancelOrder.htm"
refund_order_url = "https://lipapay-cashier.kilitest.com/api/orderRefund.htm"
merchant_id = "2016051112014649173095"
# merchant_id = "kilimall-ke"
password = "1234567890"
# sign_key = "He4AXjdOmq1G2YH3RKVSS4kqU5VFa4aK"
wallet_key = "Lx0PuHxEOcIzaQbo"
# sign_key = "Gw416RCMO8tD5MSUg5dok5uQGvR3rPpx"
notify_url = "https://uomnify-test.perfee.com/api/payment/lipapay/webhook"
return_url = "https://uomnify-test.perfee.com/api/payment/lipapay/callback"
refund_notify_url = "https://uomnify-test.perfee.com/api/payment/lipapay/refund"
channels = ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

Headers = {
    # "Authorization": "Bearer",
    "Content-Type": "application/x-www-form-urlencoded"
}


def get_signature(data_dict, ignore_country_code=True):
    sorted_keys = sorted(data_dict)
    plain_text = ""
    for key in sorted_keys:
        # if data_dict[key] is None or key in ["version", "sign"]:
        #     continue
        if data_dict[key] in [None, ""] or key in ["version", "sign"]:
            continue
        if key == "countryCode" and ignore_country_code is True:
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
        "version": "1.4",
        "buyerId": None
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
    response_url = response_url[:-1]
    result = requests.post(
        url=order_checkout_url, headers=Headers, params=data,
        allow_redirects=False)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    print("result.status_code=%r" % result.status_code)
    print("result.url=%r" % result.url)
    print("result.reason=%r" % result.reason)
    print("result.history=%r" % result.history)
    # result.encoding = "utf-8"
    save_html(result.text)
    response = result.json()
    print(response)
    return response, result.url


def new_checkout_order(
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

    sign_data = copy.deepcopy(data)
    goods_index = 0
    for goods in goods_list:
        pre_name = "goods[" + str(goods_index) + "]."
        sign_data[pre_name + "goodsId"] = goods.get("goodsId")[:32]
        sign_data[pre_name + "goodsName"] = goods.get("goodsName")[:60]
        sign_data[pre_name + "goodsQuantity"] = goods.get("goodsQuantity")
        sign_data[pre_name + "goodsPrice"] = goods.get("goodsPrice")
        sign_data[pre_name + "goodsInfo"] = goods.get("goodsInfo")[:2000]
        sign_data[pre_name + "goodsType"] = goods.get("goodsType")
        sign_data[pre_name + "goodsUrl"] = goods.get("goodsUrl")
        goods_index += 1

    data["sign"] = get_signature(sign_data)
    goods_li = []
    for goods in goods_list:
        goods_li.append(
            {
                "goodsId": goods.get("goodsId")[:32],
                "goodsName": goods.get("goodsName")[:60],
                "goodsQuantity": goods.get("goodsQuantity"),
                "goodsPrice": goods.get("goodsPrice"),
                "goodsType": goods.get("goodsType"),
                "goodsUrl": goods.get("goodsUrl"),
                "goodsInfo": goods.get("goodsInfo")[:2000]
            }
        )
    data["goods"] = goods_li

    result = requests.post(url=order_checkout_url, json=data, verify=False)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    print("result.status_code=%r" % result.status_code)
    print("result.context=%r" % result.text)
    print("result.reason=%r" % result.reason)
    print(result.request.body)
    response = result.json()
    print(response)
    return response, result.url


def sdk_checkout_order(
        amount, currency, merchant_id, merchant_order_no, expiration_time,
        channel_code, goods_list, email=None, mobile=None, seller_id=None,
        seller_account=None, buyer_id=None, buyer_account=None,
        remark=None, custom_field_1=None, custom_field_2=None,
        custom_field_3=None, password=None):
    data = {
            "signType": "MD5",
            "merchantOrderNo": str(merchant_order_no),
            "merchantId": merchant_id,
            "amount": int(amount * 100),
            "currency": currency,
            "channelCode": channel_code,
            "sellerId": seller_id,
            "mobile": mobile,
            "email": email,
            "version": "1.4",
            "notifyUrl": "https://mall-api.kilitest.com/api/payment/lipapay/webhook",
            "returnUrl": return_url,
            "firstName": "",
            "lastName": "",
            "password": password,
            "sellerAccount": seller_account,
            "buyerId": buyer_id,
            "buyerAccount": buyer_account,
            "expirationTime": expiration_time,
            "remark": remark,
            "p1": custom_field_1,
            "p2": custom_field_2,
            "p3": custom_field_3
        }
    sign_data = copy.deepcopy(data)
    goods_index = 0
    for goods in goods_list:
        pre_name = "goods[" + str(goods_index) + "]."
        sign_data[pre_name + "goodsId"] = goods.get("goodsId")[:32]
        sign_data[pre_name + "goodsName"] = goods.get("goodsName")[:60]
        sign_data[pre_name + "goodsQuantity"] = goods.get("goodsQuantity")
        sign_data[pre_name + "goodsPrice"] = goods.get("goodsPrice")
        sign_data[pre_name + "goodsInfo"] = goods.get("goodsInfo")[:2000]
        sign_data[pre_name + "goodsType"] = goods.get("goodsType")
        sign_data[pre_name + "goodsUrl"] = goods.get("goodsUrl")
        goods_index += 1

    data["sign"] = get_signature(sign_data)
    goods_li = []
    for goods in goods_list:
        goods_li.append(
            {
                "id": "",
                "requestId": "",
                "goodsId": goods.get("goodsId")[:32],
                "goodsName": goods.get("goodsName")[:60],
                "goodsQuantity": goods.get("goodsQuantity"),
                "goodsPrice": goods.get("goodsPrice"),
                "goodsType": goods.get("goodsType"),
                "goodsUrl": goods.get("goodsUrl"),
                "goodsInfo": goods.get("goodsInfo")[:2000],
                "createTime": None
            }
        )
    data["goods"] = goods_li

    response_url = order_checkout_url + "?"
    for k, v in data.items():
        if v in [True, False] or v:
            response_url = response_url + str(k) + "=" + str(v) + "&"
    response_url = response_url[:-1]

    result = requests.post(url=sdk_checkout_url,  json=data, verify=False)
    print(json.dumps(result.json()))
    print(json.loads(result.request.body))
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    print("result.url=%r" % result.url)
    # result.encoding = "utf-8"
    response = {}
    save_html(result.text)
    if channel_code != "OL":
        response = result.json()
    else:
        res_url = response_url
    print(response)
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


def get_wallet_info(merchant_user_id, currency_code, country_code,
                    phone_no=None):
    params = {
        "merchantId": merchant_id,
        "signType": "MD5",
        "merchantUserId": merchant_user_id,
        "currencyCode": currency_code,
        "countryCode": country_code
    }
    if phone_no:
        params["phoneNo"] = phone_no
    params["sign"] = get_signature(params, ignore_country_code=False)
    result = requests.post(
        url=get_wallet_info_api, data=params, timeout=30)
    print(result.status_code)
    print(result.request.url)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def update_wallet_phone(member_id, phone_no):
    params = {
        "merchantId": merchant_id,
        # "signType": "MD5",
        "memberId": member_id,
        "mobile": phone_no
    }
    params["sign"] = get_signature(params)
    result = requests.post(
        url=update_wallet_phone_api, json=params, timeout=30)
    print(result.status_code)
    print(result.request.body)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def wallet_payment(merchant_order_id, order_id, password):
    params = {
        "password": password,
        "signType": "MD5",
        "orderId": order_id,
        "merchantOrderId": merchant_order_id,
        "merchantId": merchant_id
    }
    params["sign"] = get_signature(params)
    result = requests.post(
        url=wallet_payment_api, data=params, timeout=30)
    print(result.status_code)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def encrypt(plain_text, kwargs={}):
    # 选择pkcs7补全
    pad_pkcs7 = pad(plain_text.encode('utf-8'), AES.block_size)
    encrypt_data = AES.new(
        wallet_key.encode('utf-8'), AES.MODE_ECB, **kwargs).encrypt(pad_pkcs7)
    return base64.b64encode(encrypt_data).decode("utf-8")

def encrypt_1(text):
    cipher = AES.new(wallet_key, AES.MODE_ECB)
    x = AES.block_size - (len(text) % AES.block_size)
    if x != 0:
        text = text + chr(x)*x
    msg = cipher.encrypt(text)
    return base64.b64encode(msg)


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
    # res = get_wallet_info(
    #     merchant_user_id=100101014, currency_code="KES", country_code="KE",
    #     phone_no="714456852")
    # res = update_wallet_phone(
    #     member_id="100100032", phone_no="254714456839")
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
    #  payment_method(OL[线上], OF[线下], AP[钱包], OP[m-pesa])
    # res = checkout_order(
    #     amount=60000, currency="KES", merchant_id=merchant_id,
    #     merchant_order_no="343435F6464258",
    #     expiration_time="1000000", source_type="B", goods_list=goods_list,
    #     email="",  mobile="254714456852",
    #     seller_id="33333333", seller_account="33333333", buyer_id="100100013",
    #     buyer_account="4444444", customer_ip="10.0.0.140", channels="!mkey010101",
    #     payment_method="OL", custom_field_1=None, custom_field_2=None,
    #     custom_field_3=None, country_code="KE", remark="",
    #     use_installment=False)

    # res = new_checkout_order(
    #     amount=60000, currency="KES", merchant_id=merchant_id,
    #     merchant_order_no="343435F3464252",
    #     expiration_time="1000000", source_type="B", goods_list=goods_list,
    #     email="34324@qq.com",  mobile="254714456852",
    #     seller_id="33333333", seller_account="33333333", buyer_id="100100013",
    #     buyer_account="4444444", customer_ip="10.0.0.140", channels="",
    #     payment_method="AP", custom_field_1="324324", custom_field_2=None,
    #     custom_field_3=None, country_code="", remark="3432432",
    #     use_installment=None)

    """wallet020101,mpesa020106,mpesa020105,ipay010102"""
    password_encrypt = encrypt("123456")
    print(password_encrypt)
    res = sdk_checkout_order(
        amount=60000, currency="KES", merchant_id=merchant_id,
        merchant_order_no="343432F32343232", expiration_time="1000000",
        channel_code="ipay010102", goods_list=goods_list,
        email="1159983582@qq.com", mobile="254714456852",
        seller_id="33333333", seller_account="33333333", buyer_id="100100013",
        buyer_account="4444444",
        custom_field_1=None, custom_field_2=None,
        custom_field_3=None,  remark="", password=password_encrypt
    )
    # password_encrypt = encrypt("123456")
    # res = wallet_payment(
    #     merchant_order_id="343435F3464254", order_id="K2210180724381326032",
    #     password=password_encrypt)
    # res = query_transaction(order_no="C120220426000015")
    # res = cancel_order(order_no="343435F3464253", amount="60001")
    # res = refund_order(
    #     merchant_refund_id="4", order_id="K2204220344557447114",
    #     merchant_order_id="C120220422000071", amount="34342", reason=None,
    #     p0=None, payment_trans_id=None, org_name=None, is_use_wallet="N")

    print(res)
