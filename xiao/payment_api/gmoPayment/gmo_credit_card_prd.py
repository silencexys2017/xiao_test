#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
# import html
import pickle
from Crypto.Cipher import PKCS1_OAEP, PKCS1_v1_5, DES3
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5 as aaabbb
# from urllib.parse import unquote
import base64


login_store_id = "ADMINISTRATOR"
login_store_password = "2020&otoku"
store_id = "9200003025708"
store_pd = "r2s9kace"
site_id = "tsite00041368"
site_pd = "2xzq35wr"

GET_TOKEN_URL = "https://p01.mul-pay.jp/ext/api/credit/getToken"
PRE_CREATE_URL = "https://pt01.mul-pay.jp/payment/EntryTran.json"
EXECUTE_URL = "https://pt01.mul-pay.jp/payment/ExecTran.json"
DS1_AUTH_URL = "https://pt01.mul-pay.jp/payment/SecureTran.json"
DS2_AUTH_URL = "https://pt01.mul-pay.jp/payment/SecureTran2.json"
UPDATE_PAY_URL = "https://pt01.mul-pay.jp/payment/AlterTran.json"
UPDATE_AMOUNT_URL = "https://pt01.mul-pay.jp/payment/ChangeTran.json"
QUERY_STATUS_URL = "https://pt01.mul-pay.jp/payment/SearchTrade.json"
RET_URL = "https://api-dev.perfee.com/partner/pay/gmo/payment-callback?"
CANCEL_URL = "https://api-dev.perfee.com/partner/pay/gmo/callback?billId=%d"
request_header = {"Content-Type": "application/json", "charset": "UTF-8"}

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


def verify_ipn_notify(params):
    data = unquote(params)
    param_di = {}
    for item in data.split("&"):
        it = item.split("=")
        param_di[it[0]] = it[1]
    print(param_di)
    param_di["store_passwd"] = get_md5_key(store_pd)
    verify_keys = param_di.get("verify_key").split(",")
    verify_keys.append("store_passwd")
    verify_keys.sort()
    new_params = ""
    for key in verify_keys:
        new_params = new_params + key + "=" + param_di[key] + "&"
    # new_params = new_params.replace("+", " ")
    print(new_params)
    md5_res = get_md5_key(new_params[:-1])
    print(md5_res)
    print(param_di["verify_sign"])


def request_post_api(url, args):
    res = requests.post(
        url=url, headers=request_header, json=args, timeout=30).json()
    print(res)

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def pre_create(order_id, amount, version=3, currency="JPY", job_cd=None,
               td_flag="0", item_code="0000990", tax=0):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "orderID": order_id,
        "jobCd": job_cd,
        "amount": amount
    }
    if tax:
        data["tax"] = tax
    if item_code:
        data["itemCode"] = item_code
    if version:
        data["version"] = version
    if td_flag:
        data.update({
            "tdFlag": "0",  # 设置是否使用3DS付款。
            "tdTenantName": "FerFee",
            "tds2Typ": 1})

    return request_post_api(PRE_CREATE_URL, data)
    """
    {'accessID': 'a77d16e7b831924d1b843f83681ade00',
    'accessPass': '728761a681830ad8889b577a4f0502f1'}
    [{'errCode': 'E01', 'errInfo': 'E01020008'}]
    """


def execute_payment(
        access_id, access_pass, order_id, card_no=None, expire=None,
        token_type="", token="", security_code=None, pin=None, version="3",
        method="", pay_times="", client_field_1="test"):
    data = {
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "cardNo": card_no,
        "expire": expire,
        "clientField1": client_field_1,
        "clientField2": "項目２",
        "clientField3": "項目３",
        "clientFieldFlag": "1"
    }
    if token_type:
        data["tokenType"] = token_type
    if token:
        data["token"] = "Lg9sRgo5nx6yfefJ51z8bj/1VdNFAaCZYWZ+qLKJyqWwBS7yYvxSiC0zeMVH+O4F"
    if card_no:
        data["cardNo"] = card_no
    if expire:
        data["expire"] = expire  # YYMM
    if security_code:
        data["securityCode"] = security_code
    if pin:
        data["pIN"] = pin
    if version:
        data["version"] = version
    if method:
        data["method"] = method  # 除“有效性检查”外，需要进行处理分类
    if pay_times:
        data["payTimes"] = pay_times  # method为2：分割时传

    return request_post_api(EXECUTE_URL, data)

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


def query_transaction_status(order_id):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "orderID": order_id,
        "useSiteMaskLevel": "0"
    }

    return request_post_api(QUERY_STATUS_URL, data)
    """
    {
    "orderID": "test003",
    "status": "CHECK",
    "processDate": "20201217195022",
    "jobCd": "CHECK",
    "accessID": "10d295999410d623b9f08aa07197805c",
    "accessPass": "9d3c6d1c5c69a8755719c3aeaaa40fe8",
    "itemCode": "0000990",
    "amount": "100",
    "tax": "10",
    "siteID": "",
    "memberID": "",
    "cardNo": "************1111",
    "expire": "2212",
    "method": "",
    "payTimes": "",
    "forward": "2a99662",
    "tranID": "2012171912111111111111801654",
    "approve": "0000000",
    "clientField1": "test",
    "clientField2": "項目２",
    "clientField3": "項目３"
    }
    [{'errCode': 'E01', 'errInfo': 'E01110002'}]
    """


def update_transaction(
        access_id, access_pass, job_cd=None, amount=None, tax=None, method=None,
        pay_times=None):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "accessID": access_id,
        "accessPass": access_pass,
        "version": 3
    }
    if job_cd:
        data["jobCd"] = job_cd
    if amount:
        data["amount"] = amount
    if tax:
        data["tax"] = tax
    if method:
        data["method"] = method
    if pay_times:
        data["payTimes"] = pay_times

    return request_post_api(UPDATE_PAY_URL, data)

    """{
    "accessID": "1ac5d8d0e63bbe40ffe61d128cf67db9",
    "accessPass": "12978a3d44d2b88dc6a5918d1d528bfe",
    "forward": "2a99662",
    "approve": "0000000",
    "tranID": "2012172112111111111111804067",
    "tranDate": "20201217213639"
    }"""


def change_transaction(
        access_id, access_pass, job_cd=None, amount=None, tax=None):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "accessID": access_id,
        "accessPass": access_pass,
        "version": 3
    }
    if job_cd:
        data["jobCd"] = job_cd
    if amount:
        data["amount"] = amount
    if tax:
        data["tax"] = tax

    return request_post_api(UPDATE_AMOUNT_URL, data)
    """
    {
    "accessID": "b9630e51ce7bf2b3c61a57babd14a74a",
    "accessPass": "8a4d758347bfee89a855b4dfecbfaab1",
    "forward": "2a99662",
    "approve": " 001071",
    "tranID": "2012172112111111111111800019",
    "tranDate": "20201217214132"
   }"""


def encrypt_with_rsa(key, plain_text):
    # public_key = RSA.importKey(base64.b64decode(key))
    # cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    cipher_pub_obj = PKCS1_v1_5.new(RSA.importKey(base64.b64decode(key)))
    return base64.b64encode(cipher_pub_obj.encrypt(plain_text.encode())).decode()
    return base64.b64encode(cipher.encrypt(plain_text.encode())).decode()


def get_token(
        card_no, expire, token_number="1", security_code=None, holder_name=None):
    header = {"Content-Type": "application/x-www-form-urlencoded",
              "charset": "UTF-8"}
    encrypted = {
        "cardNo": card_no,
        "expire": expire,
        "securityCode": security_code,
        "tokenNumber": token_number,
    }
    if security_code:
        encrypted["securityCode"] = security_code
    if holder_name:
        encrypted["holderName"] = holder_name
    if token_number:
        encrypted["tokenNumber"] = token_number

    content_bytes = json.dumps(encrypted).encode("utf-8")
    rsa_str = encrypt_with_rsa(PUBLIC_KEY, content_bytes)

    # rsa_str = "hmvZos1IHsE0UgEJmVoxEEcgQ6sb/wwrqpk6s0m8gVQNC2756jdFNh92j2TehNf01CSTIeUjHEvIJP9ySIqcAxdmpkooDaswMwkjLrJ9YyCbZH62SBatY5bRhWRR/Q7dUyBWlh+yXAwmckMA6LEADhYBEehHK5jFKgf5MgFHo5Css6JaANndMkJessk0VTbiMhmKgZ0dlPGmLoz6T16mDZwvleqpi/bi2ViSxtZovkFQuJHyYvftQjnTNCdod+c1RvdMoW+5g/uG14loDXbo8FYeq6VDWN49rym2ScRpVPBb1cEmNrNACXeV40nd0eQ1K+0QzFNuqeSfPgi9D3Y3Ew=="
    # rsa_str = "RUcrW3J4QbNyDC3WBmAeZCbC/sRR7YS9M9Cm+9s5NkJe7baPLQtU6NOXwzcIZYZz0C33hTyb+oVhLu/JGxf7vVH5Aih9HjGA5SC0bXK/i3jymJNl+z3R6qRBCy7HMbmeGAt8lQro0dTBld1VqgKNhk9hubwZl8IW4CBI0CTBeR1DzvGayuOxkAHibfUJNraCQEnkxXr5ElLSIrE5obuwtUMdfbVK6A5NDgps7hq1wZsVDpPaM3Ef4r7fn34nYKtNZ19bo4G9lcUZEAZHZHYkhMeCqZIs1KG2p+v/+8Zp1tFOb7XZyZH/M5EUTliZXEjLx/I1MXg7TT+pATg8mP+lmA=="
    data = {
        "Encrypted": rsa_str,
        "ShopID": store_id,
        "KeyHash": PUBLIC_HASH
    }
    return requests.post(
        url=GET_TOKEN_URL, headers=header, params=data, timeout=30).json()


if __name__ == "__main__":
    # res = get_token(
    #     card_no="4392260041492461", expire="2411", security_code="573")
    res = pre_create(order_id="test90", amount=100, tax=10, job_cd="AUTH")
    # res = execute_payment(
    #     access_id="f2e8203d65336be91f2f03afc9dd3f9b",
    #     access_pass="4f9f155b6407ca8dcf55662155fc9dd7", order_id="test999",
    #     card_no="4123450131003312", expire="2212", pin="", method="1")
    # res = query_transaction_status(order_id="test09999")
    # res = update_transaction(
    #     access_id="8c702ce66e2a6aa6011d5078f2d44c1e",
    #     access_pass="ca84f4f60d7a9cde31741306013a7659", job_cd="VOID",
    #     amount=None, tax=None, method=1, pay_times=1)
    # res = change_transaction(
    #     access_id="f2e8203d65336be91f2f03afc9dd3f9b",
    #     access_pass="4f9f155b6407ca8dcf55662155fc9dd7", job_cd="CAPTURE",
    #     amount="80", tax="")
    # verify_ipn_notify(res_str)

    # 2012291812111111111111809657
    print(res)



