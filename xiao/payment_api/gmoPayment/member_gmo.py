#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
import pickle
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64


login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_pd = "z3gxd5ft"
site_id = "tsite00041368"
site_pd = "2xzq35wr"

get_token_api = "https://pt01.mul-pay.jp/ext/api/credit/getToken"
traded_card_api = "https://pt01.mul-pay.jp/payment/TradedCard.json"
save_member_api = "https://pt01.mul-pay.jp/payment/SaveMember.json"
update_member_api = "https://pt01.mul-pay.jp/payment/UpdateMember.json"
search_member_api = "https://pt01.mul-pay.jp/payment/SearchMember.json"
delete_member_api = "https://pt01.mul-pay.jp/payment/DeleteMember.json"
save_card_api = "https://pt01.mul-pay.jp/payment/SaveCard.json"
search_card_api = "https://pt01.mul-pay.jp/payment/SearchCard.json"
search_card_detail_api = "https://pt01.mul-pay.jp/payment/SearchCardDetail.json"
delete_card_api = "https://pt01.mul-pay.jp/payment/DeleteCard.json"

request_header = {"Content-Type": "application/json", "charset": "UTF-8"}
token_header = {"Content-Type": "application/x-www-form-urlencoded",
                "charset": "UTF-8"}

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


def request_post_api(url, args):
    # res = requests.post(
    #     url=url, headers=request_header, json=args, timeout=30).text
    # print(res)
    res = requests.post(
        url=url, headers=request_header, json=args, timeout=30).json()
    print(res)

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def save_member(member_id, member_name=None):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id)
    }
    if member_name:
        data["memberName"] = member_name
    return request_post_api(save_member_api, data)


def update_member(member_id, member_name=None):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id)
    }
    if member_name:
        data["memberName"] = member_name
    return request_post_api(update_member_api, data)


def search_member(member_id):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id)
    }
    return request_post_api(search_member_api, data)


def delete_member(member_id):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id)
    }
    return request_post_api(delete_member_api, data)


def save_or_update_card(member_id, token, card_seq=None, card_pass=None):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id),
        "token": token
    }
    if card_seq:  # when update
        data["CardSeq"] = card_seq
    if card_pass:
        data["CardPass"] = card_pass
    return request_post_api(save_card_api, data)


def traded_card(order_id, member_id, card_seq=None):
    data = {
        "shopID": store_id,
        "shopPass": store_pd,
        "orderID": str(order_id),
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id)
    }
    if card_seq:
        data["cardSeq"] = card_seq
    return request_post_api(traded_card_api, data)


def search_card(member_id, card_seq=None):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id),
        "token": token
    }
    if card_seq:
        data["cardSeq"] = card_seq
    return request_post_api(search_card_api, data)

"""
[{
'cardSeq': '0', 
'holderName': None, 
'cardName': None, 
'cardNo': '*************111', 
'deleteFlag': '0', 
'expire': '2212', 
'defaultFlag': '0'}, 
{
'cardSeq': '1', 
'holderName': None, 
'cardName': None, 
'cardNo': '*************111', 
'deleteFlag': '0', 
'expire': '2204', 
'defaultFlag': '0'
}]
"""


def search_card_detail(
        card_no=None, token=None, order_id=None, member_id=None):
    data = {
        "shopID": store_id,
        "shopPass": store_pd
    }
    if order_id:
        data["orderID"] = str(order_id)
    if card_no:
        data["cardNo"] = card_no
    if token:
        data["token"] = token
    if member_id:
        data["siteID"] = site_id
        data["sitePass"] = site_pd
        data["memberID"] = str(member_id)

    return request_post_api(search_card_detail_api, data)


def delete_card(member_id, card_seq):
    data = {
        "siteID": site_id,
        "sitePass": site_pd,
        "memberID": str(member_id),
        "cardSeq": card_seq
    }

    return request_post_api(delete_card_api, data)


def encrypt_with_rsa(key, plain_text):
    cipher_pub_obj = PKCS1_v1_5.new(RSA.importKey(base64.b64decode(key)))
    return base64.b64encode(
        cipher_pub_obj.encrypt(plain_text)).decode()


def get_token(
        card_no, expire, token_number="1", security_code=None,
        holder_name=None):
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
    res = requests.post(
        url=get_token_api, headers=token_header, params=data, timeout=30).json()
    print(res)


if __name__ == "__main__":
    # res = get_token(
    #     card_no="5111111111111111", expire="2212", security_code="112")
    token = "147c336f56d7f41edca475868a0d3c05edc8ed33274f1e7e71e53d30e1fecaad"
    # res = save_member(member_id=3, member_name="silence")
    # update_member(member_id=2, member_name="silence")
    # search_member(member_id=2)
    # delete_member(member_id=2)
    # save_or_update_card(member_id=110, card_pass="3141", token=token)
    # traded_card(order_id="10279", member_id=3)
    search_card(member_id=110, card_seq="")
    # search_card_detail(
    #     card_no="", token=None, order_id=None, member_id=110)
    # delete_card(member_id=110, card_seq="0")
    # print(res)



