#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
# import html
import pickle
# from Crypto.Cipher import PKCS1_v1_5
# from Crypto.Hash import SHA256
# from Crypto.PublicKey import RSA
# from urllib.parse import unquote
import base64


login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_pd = "z3gxd5ft"
# store_id = "9200003025708"
# store_pd = "r2s9kace"

search_trade_api = "https://pt01.mul-pay.jp/payment/SearchTradeMulti.idPass"
pay_pay_entry_tran_api = "https://pt01.mul-pay.jp/payment/EntryTranPaypay.json"
pay_pay_exec_tran_api = "https://pt01.mul-pay.jp/payment/ExecTranPaypay.json"
pay_pay_start_api = "https://pt01.mul-pay.jp/payment/PaypayStart.idPass"
pay_pay_sales_api = "https://pt01.mul-pay.jp/payment/PaypaySales.json"
pay_pay_cancel_return_api = \
    "https://pt01.mul-pay.jp/payment/PaypayCancelReturn.json"
# search_trade_api = "https://p01.mul-pay.jp/payment/SearchTradeMulti.idPass"
# pay_pay_entry_tran_api = "https://p01.mul-pay.jp/payment/EntryTranPaypay.json"
# pay_pay_exec_tran_api = "https://p01.mul-pay.jp/payment/ExecTranPaypay.json"
# pay_pay_start_api = "https://p01.mul-pay.jp/payment/PaypayStart.idPass"
# pay_pay_sales_api = "https://p01.mul-pay.jp/payment/PaypaySales.json"
# pay_pay_cancel_return_api = \
#     "https://p01.mul-pay.jp/payment/PaypayCancelReturn.json"
ret_url = "https://m-test.otoku-world.com/payment/gmo/result"

request_header = {"Content-Type": "application/json", "charset": "UTF-8"}

GEN_HTML = "test.html"
PUBLIC_KEY = '''
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlhKDXlWw4tu2JrbFITYUDT82BH2W8rLZ9OMFifrYIjO8fz12EsP+Xo+I/xUeh1ctTjGOIQYzZHYacWQ+xjNE5NSF5Beilcn2It0ST8EuQEb0NpRcm7BnYgVP7vYROXUFHiyrOUlPopSW4o+31IKwmO7VtTmq4iHZspMF/25YahIbOJfFF0uMAdIJYRxpYwIS5LWQB0zMT1G70tIGU6yIe3ciN7Le7phljZFidnM+EVSaauela9U8uL00WxTFudpybEwpDTX4zYoE5Cd1DWhZt4pSeKpqEiBMzK/siF1tkPBFifU+VH0e8L8+3n6/v52NwMnhPkoeHdDyLgl1tJnWJwIDAQAB
    '''
PUBLIC_HASH = "59e3e2708cdd699bfc9d3e8029350b4704c43591b52992f428190ee069cebcc1"


def request_get_api(url, args):
    res = requests.get(url=url, params=args, timeout=30).json()
    print(res)

    if res.get("APIConnect") != "DONE":
        print("error  message=%s" % res.get("errorReason"))

    return res


def get_md5_key(arg):
    m_hash = hashlib.md5()
    m_hash.update(arg.encode("utf-8"))
    return m_hash.hexdigest()


def request_post_api(url, args):
    res = requests.post(
        url=url, headers=request_header, json=args, timeout=30).json()
    print(res)

    return res


def pay_pay_entry_tran(order_id, amount, tax=0, job_cd="CAPTURE"):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "orderID": order_id,
        "jobCd": job_cd,
        "amount": str(amount)
    }
    if tax:
        data["tax"] = str(tax)

    return request_post_api(pay_pay_entry_tran_api, data)
    """
    {'accessID': 'a77d16e7b831924d1b843f83681ade00',
    'accessPass': '728761a681830ad8889b577a4f0502f1'}
    [{'errCode': 'E01', 'errInfo': 'E01020008'}]
    """


def pay_pay_exec_tran(
        access_id, access_pass, order_id, ret_utl, client_field1=None,
        client_field2=None, client_field3=None, payment_term_sec=None):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "retURL": ret_utl
    }
    if client_field1:
        data["clientField1"] = client_field1
    if client_field2:
        data["clientField2"] = client_field2
    if client_field3:
        data["clientField3"] = client_field3
    if payment_term_sec:
        data["paymentTermSec"] = payment_term_sec

    return request_post_api(pay_pay_exec_tran_api, data)

    """
    {
    "accessID": "c12d417b0bd7627276ab7224fe714ecd",
    "token": "2ac99a371f0ede96284e8479805fe4073b2cacee1a305c8e72e2bcc0571cb0d5",
    "startURL": "https://pt01.mul-pay.jp/payment/PaypayStart.idPass",
    "startLimitDate": "20210421152513"
    }
    [{'errCode': 'E01', 'errInfo': 'E01050004'}, 
    {'errCode': 'M01', 'errInfo': 'M01004014'}]
    """


def search_trade(order_id, pay_type="45"):
    data = {
        "ShopID": store_id,
        "ShopPass": store_pd,
        "OrderID": order_id,
        "PayType": pay_type
    }

    res = requests.post(url=search_trade_api, params=data, timeout=30)
    res_di = {}
    for it in res.text.split("&"):
        item = it.split("=")
        res_di[item[0]] = item[1]
    print(res_di)

    return res


def pay_pay_start(access_id, token):
    data = {
        "AccessID": access_id,
        "Token": token
    }
    res = requests.post(
        url=pay_pay_start_api, params=data, timeout=30)
    print(res.text)
    # html
    return res


def pay_pay_sales(order_id, amount, access_id, access_pass, tax=""):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "amount": str(amount)
    }
    if tax:
        data["tax"] = tax
    return request_post_api(pay_pay_sales_api, data)


def pay_pay_cancel_return(
        access_id, access_pass, order_id, cancel_amount, cancel_tax):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "cancelAmount": cancel_amount
    }
    if cancel_tax:
        data["cancelTax"] = cancel_tax

    return request_post_api(pay_pay_cancel_return_api, data)

    """{
    "accessID": "1ac5d8d0e63bbe40ffe61d128cf67db9",
    "accessPass": "12978a3d44d2b88dc6a5918d1d528bfe",
    "forward": "2a99662",
    "approve": "0000000",
    "tranID": "2012172112111111111111804067",
    "tranDate": "20201217213639"
    }"""


if __name__ == "__main__":
    res = pay_pay_entry_tran(
        order_id="test9339100", amount=120, tax=0, job_cd="CAPTURE")
    # {'accessID': '5c0fda750370f4b0af9e95909f0118b3',
    # 'accessPass': 'ab13368c6ffb1b4d64388d57813b0473'}
    # res = pay_pay_exec_tran(
    #     access_id="5c0fda750370f4b0af9e95909f0118b3",
    #     access_pass="ab13368c6ffb1b4d64388d57813b0473", order_id="test93390",
    #     ret_utl=ret_url, client_field1="", client_field2="", client_field3="",
    #     payment_term_sec="86400")
    # res = pay_pay_start(
    #     access_id="2d9745655a4f14b35b9799e2f59872d4",
    #     token="dfb81b3f6ffbbf0dcd00f867c25f52ffe620c280de0e5c5d59cede0540660db1")
    # res = search_trade(order_id="test93391", pay_type="45")
    # pay_pay_sales(
    #     order_id="df", amount="100", access_id="", access_pass="", tax="")
    # res = pay_pay_cancel_return(
    #     access_id="5c0fda750370f4b0af9e95909f0118b3",
    #     access_pass="ab13368c6ffb1b4d64388d57813b0473", order_id="test93390",
    #     cancel_amount="10", cancel_tax="")

    # verify_ipn_notify(res_str)

    # 2012291812111111111111809657
    print(res)



