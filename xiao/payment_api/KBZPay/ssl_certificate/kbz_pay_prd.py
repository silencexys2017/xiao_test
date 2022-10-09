#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import uuid
import hashlib
from requests.adapters import HTTPAdapter
import json
from urllib3.util.ssl_ import create_urllib3_context

# APP_ID = "kp5893721e986349ebad28c0cd50d971"
# APP_KEY = "a34904b818bfc5f1f9c8296a35839b59"
# MERCHANT_CODE = "200121"
# USER_NAME = "20012101"

APP_ID = "kp71752c8d405e4a19b0327e2cfeb643"
APP_KEY = "5e5d338abcf1c5c03687c25739ce4f73"
MERCHANT_CODE = "200112"
USER_NAME = "Mr Zhang Junfei"


TRADE_TYPE = "PWAAPP"
TRANS_CURRENCY = "MMK"
ORG_PORTAL_URL = "https://159.138.20.58:31002/payment/orglogin.action"
PRE_CREATE_URL = "http://api.kbzpay.com/payment/gateway/uat/precreate"
PWA_URL = "https://static.kbzpay.com/pgw/uat/pwa/#/?"
ORDER_QUERY_URL = "http://api.kbzpay.com/payment/gateway/uat/queryorder"
REFUND_URL = "https://api.kbzpay.com:18008/payment/gateway/refund"
ORDER_CLOSE_URL = "https://api.kbzpay.com/payment/gateway/uat/closeorder"
REFUND_SIGN_FIELDS = ["result", "code", "msg", "merch_order_id", "merch_code",
                      "refund_amount", "nonce_str"]

response_test = {
        "Response": {
            "result": "SUCCESS",
            "code": "0",
            "msg": "success",
            "merch_order_id": "10001",
            "prepay_id": "KBZ007f54898139dbcb1151e46517500c63d5154525506",
            "nonce_str": "4821B565F1194D75A1B8F04391A9BD43",
            "sign_type": "SHA256",
            "sign": "C26977DEF1F6796D705AA1E0C5AA4F9F8B756C477DF16806231D5E368420DFDF"
        }
    }


class SSLAdapter(HTTPAdapter):
    def __init__(
            self, cert_file, key_file, password=None, crt_file=None, *args,
            **kwargs):
        self._cert_file = cert_file
        self._key_file = key_file
        self._password = password
        self._crt_file = crt_file
        super(self.__class__, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs):
        context = create_urllib3_context()
        context.load_cert_chain(
            certfile=self._cert_file, keyfile=self._key_file,
            password=self._password)
        context.load_verify_locations(self._crt_file)
        kwargs['ssl_context'] = context


def verify_signature(response, with_key=True, is_upper=True, is_refund=False):
    re_li = []
    for key, value in response.items():
        if key in ["sign", "sign_type", "refund_info"] or not value:
            continue
        if is_refund:
            if key not in REFUND_SIGN_FIELDS:
                continue
        re_li.append(str(key) + "=" + str(value))
    re_li.sort()
    res_string = ""
    for it in re_li:
        res_string = res_string + it + "&"
    if with_key:
        string_sign = res_string + "key=" + APP_KEY
    else:
        string_sign = res_string[:-1]
    res_hash_obj = hashlib.sha256()
    res_hash_obj.update(string_sign.encode('utf-8'))
    if is_upper:
        res_sign = res_hash_obj.hexdigest().upper()
    else:
        res_sign = res_hash_obj.hexdigest()
    return res_sign, res_string[:-1]


def request_post_api(url, common_params, biz_content, with_ssl=False):
    dict_merged = dict(biz_content, **common_params)
    res_sign, res_string = verify_signature(dict_merged)
    common_params["sign_type"] = "SHA256"
    common_params["sign"] = res_sign
    common_params["biz_content"] = biz_content
    headers = {"Content-Type": "application/json"}
    params = {"Request": common_params}
    print(params)
    print(url)
    print(headers)
    if with_ssl:
        # res = requests.post(
        #     url, data=params, cert=(
        #         'CA_PGW.crt',
        #         'merchserver_key_200112.pem'), verify=False)
        session = requests.Session()
        session.mount(url, SSLAdapter(
            "merchserver_cert_200112.pem", "merchserver_key_200112.pem",
            password="Mk200112", crt_file="CA_PGW.crt"))
        res = session.post(url=url, headers=headers, json=params).json()
    else:
        res = requests.post(
            url=url, headers=headers, json=params, timeout=30).json()
    print(res)
    response = res["Response"]

    if response["result"] != "SUCCESS" or response["code"] != "0":
        print("pwa_error  message=%s,code=%s" % (
            response['msg'], response['code']))
    if with_ssl:
        res_sign, res_string = verify_signature(response, is_refund=True)
    else:
        res_sign, res_string = verify_signature(response)
    if res_sign != response["sign"]:
        raise Exception("Sign verification failed")

    return res


def pre_create(
        merch_order_id, total_amount, trans_currency, title=None,
        timeout_express=None, callback_info=None, operator_id=None,
        store_id=None, terminal_id=None, business_param=None):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "notify_url": "https://api-test.perfee.com/payment/kbzpay/ipn",
        "method": "kbz.payment.precreate",
        "nonce_str": unique_key,
        "version": "3.0"
    }

    biz_content = {
        "merch_order_id": merch_order_id,
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "trade_type": TRADE_TYPE,
        # "trade_type": "PAY_BY_QRCODE",
        "total_amount": total_amount,
        "trans_currency": trans_currency,
    }
    if title:
        biz_content["title"] = title  # Offering name.
    if timeout_express:
        biz_content["timeout_express"] = timeout_express  # 多长时间支付失效min
    if callback_info:
        biz_content["callback_info"] = callback_info
        # Callback information, in URL encoding format.
    if operator_id:
        biz_content["operator_id"] = operator_id
        # Specifies a store operator ID
    if store_id:
        biz_content["store_id"] = store_id  # Specifies a Store ID
    if terminal_id:
        biz_content["terminal_id"] = terminal_id
        # Specifies a Terminal device ID
    if business_param:
        biz_content["business_param"] = business_param
        # Must be URL encoded format, should be agreed with KBZPay

    return request_post_api(PRE_CREATE_URL, common_params, biz_content)


def query_order(
        merch_order_id=None,  mm_order_id=None, refund_request_no=None):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "method": "kbz.payment.queryorder",
        "nonce_str": unique_key,
        "version": "3.0"
    }

    biz_content = {
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
    }
    if merch_order_id:
        biz_content["merch_order_id"] = merch_order_id
    if mm_order_id:
        biz_content["mm_order_id"] = mm_order_id
    if refund_request_no:
        biz_content["refund_request_no"] = refund_request_no

    return request_post_api(ORDER_QUERY_URL, common_params, biz_content)


def close_order(merch_order_id):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "method": "kbz.payment.closeorder",
        "nonce_str": unique_key,
        "version": "3.0"
    }

    biz_content = {
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "merch_order_id": merch_order_id
    }

    return request_post_api(ORDER_CLOSE_URL, common_params, biz_content)


def refund_order(
        merch_order_id, refund_request_no=None, refund_reason=None):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "method": "kbz.payment.refund",
        "nonce_str": unique_key,
        "version": "1.0"
    }

    biz_content = {
        "merch_order_id": merch_order_id,
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID
    }
    if refund_request_no:
        biz_content["refund_request_no"] = refund_request_no
        # Unique refund request ID generated by the merchant side.
    if refund_reason:
        biz_content["refund_reason"] = refund_reason

    return request_post_api(
        REFUND_URL, common_params, biz_content, with_ssl=True)
    """{
    "Response": {
        "result": "SUCCESS",
        "code": "0",
        "msg": "success",
        "merch_order_id": "86844",
        "merch_code": "200121",
        "trans_order_id": "31029Q09113301000118",
        "refund_status": "REFUND_SUCCESS",
        "refund_order_id": "30029Q09571301000118",
        "refund_amount": "10",
        "refund_currency": "MMK",
        "refund_time": "1601090833",
        "nonce_str": "D4E6282ECF7F4C85A260144A8A608AE1",
        "sign_type": "SHA256",
        "sign": "EAC1569565B304CA538908C8835F67E90C4C60B678FB48695A9BF6D8A6D5E8A8"
    }
    }"""


def get_complete_pwa_url(params):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "prepay_id": params.get("prepay_id"),
        # "nonce_str": unique_key,
        "nonce_str": params.get("nonce_str"),
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID
    }
    sign, res_string = verify_signature(
        common_params, with_key=True, is_upper=True)
    url = PWA_URL + res_string + "&sign=" + sign
    return url


if __name__ == "__main__":
    # res = pre_create(
    #     "1010", "100", "MMK", title=None, timeout_express=None,
    #     callback_info=None, operator_id=None, store_id=None,
    #     terminal_id=None, business_param=None)

    # res = verify_signature({
    #     "result": "SUCCESS",
    #     "code": "0",
    #     "msg": "success",
    #     "merch_order_id": "86837",
    #     "merch_code": "200121",
    #     # "trans_order_id": "31029M16261401000154",
    #     # "refund_status": "REFUND_SUCCESS",
    #     # "refund_order_id": "30029Q10432601000154",
    #     "refund_amount": "110",
    #     # "refund_currency": "MMK",
    #     # "refund_time": "1601093607",
    #     "nonce_str": "E37836CC5A1C468FBF9CDEC09A45EFD2",
    #     "sign_type": "SHA256",
    #     "sign": "5F540F52B1D103B19273076A7AC2F8E9EDFD6A1CCB5DC274023C1C07081B716F"
    # })

    # res = get_complete_pwa_url(response.get("Response"))
    # res = query_order(
    #     merch_order_id="86829", mm_order_id=None,
    #     refund_request_no="4843")  # "86844"  "01002091070008232787" "483"
    # res = close_order("86848")
    res = refund_order(
        "87083", refund_request_no="10", refund_reason=None)
    print(res)

