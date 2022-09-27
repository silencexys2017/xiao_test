#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
# import html
import pickle
# from urllib.parse import unquote
import base64


login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_name = "OTOKU WORLD Co.，Ltd."
store_pd = "z3gxd5ft"
DOMAIN_URL = "https://p01.mul-pay.jp"
# DOMAIN_URL = "https://stg.link.mul-pay.jp"
site_id = "tsite00041368"
site_pd = "2xzq35wr"
site_name = "OTOKU WORLD Co.，Ltd."

cvc_entry_tran_api = "https://pt01.mul-pay.jp/payment/EntryTranCvs.idPass"
cvs_exec_tran_api = "https://pt01.mul-pay.jp/payment/ExecTranCvs.idPass"
cvs_cancel_api = "https://pt01.mul-pay.jp/payment/CvsCancel.idPass"
HEADER = {"Content-Type": "application/json", "charset": "UTF-8"}
GEN_HTML = "test.html"
PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA14h4wtj9nR/tbAtozzNf62ZokR32bs2B+qhA8qjiHTZkd87sG0pJT1quSFP3TvIOO2nT+TVw7qZkDs0z81ZgeNfRm7cGHllihV44QrwmviIMZzEz7Gu878bKGwhqNoLq2wo8BFR3vLJFq7/BkQGJSOnDTTEfbRzWgUjD0lQgKvyl584FXWzZ80oDS9S5CWsWokx6WcJ4PWfvlrAV324gtZb3FQo8pbnWWxa8D86WuuF2wMUnlxgWefXq+7i4ExspXXnwczOy5Z/8lqnTre4ukvqQYy1E6CrE3SyvSLQbq+j5/JifQFK+wW+poBcNxpWn/3sK6sHcTmvJ8r/ffm2GXQIDAQAB"
PUBLIC_HASH = "989852a24fec9dc74299af2e841157d86b68f1cf09ec08f809cb44bcc19df52b"


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
    res = requests.post(url=url, params=args, timeout=30)
    print(res.content)
    print(res.text)

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def cvc_entry_tran(order_id, amount, version="3", tax="0"):
    data = {
        "ShopID": store_id,
        "ShopPass": store_pd,
        "OrderID": order_id,
        "Amount": amount
    }
    if tax:
        data["Tax"] = tax
    if version:
        data["Version"] = version

    return request_post_api(cvc_entry_tran_api, data)
    """
    {'accessID': 'a77d16e7b831924d1b843f83681ade00',
    'accessPass': '728761a681830ad8889b577a4f0502f1'}
    [{'errCode': 'E01', 'errInfo': 'E01020008'}]
    """


def cvs_exec_tran(
        access_id, access_pass, order_id, convenience, customer_name,
        customer_kana, tel_no, cvs_name, cvs_phone, cvs_period,
        payment_term_day=None, mail_address=None):
    data = {
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "Convenience": convenience,
        "CustomerName": customer_name,
        "CustomerKana": customer_kana,
        "TelNo": tel_no,
        "ReceiptsDisp11": cvs_name,
        "ReceiptsDisp12": cvs_phone,
        "ReceiptsDisp13": cvs_period,
    }
    if payment_term_day:
        data["PaymentTermDay"] = payment_term_day
    if mail_address:
        data["MailAddress"] = mail_address

    return request_post_api(cvs_exec_tran_api, data)

    """
    {
    "orderID": "test003",
    "forward": "2a99662",
    "method": "",
    "payTimes": "",
    "approve": "0000000",
    "tranID": "2012171912111111111111801654",
    "tranDate": "20201217195022",
    "checkString": "82f58995ae4357681d88876feb5827c1",
    "clientField1": "test",
    "clientField2": "項目２",
    "clientField3": "項目３",
    "acs": "0"
    }
    [{'errCode': 'E01', 'errInfo': 'E01050004'}, 
    {'errCode': 'M01', 'errInfo': 'M01004014'}]
    """


def pause_payment(access_id, order_id, access_pass=None):
    data = {
        "ShopID": store_id,
        "ShopPass": store_pd,
        "AccessID": access_id,
        "AccessPass": access_pass,
        "OrderID": order_id
    }
    res = requests.post(
        url=cvs_cancel_api, params=data, timeout=30)
    print(res.text)
    return res


if __name__ == "__main__":
    # res = cvc_entry_tran(order_id="test93890", amount="100", tax="10")
    res = cvs_exec_tran(
        access_id="de8a6ace65c331b36a22360ffb5a6a62",
        access_pass="5547db068a6b885190da5f9121dbc56e", order_id="test93890",
        convenience="10002", customer_name="xiao", customer_kana="sheng",
        tel_no="143848238", cvs_name="otoku world", cvs_phone="000004343",
        cvs_period="09:00-17:00", payment_term_day="0",
        mail_address="xiaoyongsheng@perfee.com")
    # verify_ipn_notify(res_str)
    # res = pause_payment(
    #     access_id="11aa976c91c9c1a6a49c24d8e085d559", order_id="3443",
    #     access_pass="0af3108b8a97e96c6d05ba7efadeff6b")


    # 2012291812111111111111809657
    print(res)



