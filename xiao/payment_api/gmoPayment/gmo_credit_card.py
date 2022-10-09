#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
import pickle
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from urllib.parse import unquote
import base64


login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_pd = "z3gxd5ft"
site_id = "tsite00041368"
site_pd = "2xzq35wr"

GET_TOKEN_URL = "https://pt01.mul-pay.jp/ext/api/credit/getToken"
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


def request_post_api(url, args, headers=request_header):
    res = requests.post(
        url=url, headers=headers, json=args, timeout=30).json()
    print(res)

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def pre_create(order_id, amount, version=3, currency="JPY", job_cd="AUTH",
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
        "clientField1": client_field_1,
        "clientField2": "項目２",
        "clientField3": "項目３",
        "clientFieldFlag": "1"
    }
    if token_type:
        data["tokenType"] = token_type
    if token:
        data["token"] = token
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


def execute_member_payment(
        access_id, access_pass, order_id, member_id, card_seq,
        seq_mode="0", card_pass="", security_code=None, method="1",
        pay_times="", client_field_1="test"):
    data = {
        "accessID": access_id,
        "accessPass": access_pass,
        "orderID": order_id,
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id),
        "cardSeq": card_seq,
        "clientField1": client_field_1,
        "clientField2": "項目２",
        "clientField3": "項目３",
        "clientFieldFlag": "1"
    }
    if seq_mode:
        data["seqMode"] = seq_mode
    if card_pass:
        data["cardPass"] = card_pass
    if security_code:
        data["securityCode"] = security_code
    if method:
        data["method"] = method
    if pay_times:
        data["payTimes"] = pay_times

    return request_post_api(EXECUTE_URL, data)


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
    cipher_pub_obj = PKCS1_v1_5.new(RSA.importKey(base64.b64decode(key)))
    return base64.b64encode(
        cipher_pub_obj.encrypt(plain_text)).decode()


def get_token(
        card_no, expire, token_number="1", security_code=None, holder_name=None):
    header = {"Content-Type": "application/x-www-form-urlencoded",
              "charset": "UTF-8"}
    encrypted = {
        "cardNo": card_no,
        "expire": expire,
        "tokenNumber": token_number
    }
    if security_code:
        encrypted["securityCode"] = security_code
    if holder_name:
        encrypted["holderName"] = holder_name
    if token_number:
        encrypted["tokenNumber"] = token_number
    content_bytes = json.dumps(encrypted).encode("utf-8")
    rsa_str = encrypt_with_rsa(PUBLIC_KEY, content_bytes)
    data = {
        "Encrypted": rsa_str,
        "ShopID": store_id,
        "KeyHash": PUBLIC_HASH
    }
    return requests.post(
        url=GET_TOKEN_URL, headers=header, params=data, timeout=30).json()


if __name__ == "__main__":
    res = get_token(card_no="2111111111111111", expire="2212")
    # res = pre_create(order_id="test9346", amount=100, tax=0, job_cd="CAPTURE")
    token = "126c2d9a9381c91c34736e5500ada6a033a95a1c478f8207c5a0d8316ca45ff8"
    # res = execute_payment(
    #     access_id="df0d3137e6e0d3a04124c5b41f419a5f",
    #     access_pass="caf1978f305c4ea3dac150134c3430ff", order_id="test9342",
    #     card_no="", expire="", pin="", method="1", token=token)
    # res = execute_member_payment(
    #     access_id="79bddd15a5d15a48de1804eac347d7dc",
    #     access_pass="47c45844ad6587830961feb1e62c75e5", order_id="test9346",
    #     member_id="110", card_seq="2", seq_mode="0", card_pass="",
    #     security_code=None, method="1", pay_times="", client_field_1="test")
    # res = query_transaction_status(order_id="test9342")
    # res = update_transaction(
    #     access_id="df0d3137e6e0d3a04124c5b41f419a5f",
    #     access_pass="caf1978f305c4ea3dac150134c3430ff", job_cd="CANCEL",
    #     amount=None, tax=None, method=1, pay_times=1)
    # res = change_transaction(
    #     access_id="df0d3137e6e0d3a04124c5b41f419a5f",
    #     access_pass="caf1978f305c4ea3dac150134c3430ff", job_cd="CAPTURE",
    #     amount="70", tax="")
    # verify_ipn_notify(res_str)

    # 2012291812111111111111809657
    print(res)



