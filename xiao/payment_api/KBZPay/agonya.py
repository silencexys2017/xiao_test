#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import uuid
import hashlib
from requests.adapters import HTTPAdapter
import json
from urllib3.util.ssl_ import create_urllib3_context

APP_ID = "kp5893721e986349ebad28c0cd50d971"
APP_KEY = "a34904b818bfc5f1f9c8296a35839b59"
MERCHANT_CODE = "200121"
TRADE_TYPE = "PWAAPP"
TRANS_CURRENCY = "MMK"
ORG_PORTAL_URL = "https://159.138.20.58:31002/payment/orglogin.action"
USER_NAME = "20012101"
PRE_CREATE_URL = "http://api.kbzpay.com/payment/gateway/uat/precreate"
PWA_URL = "https://static.kbzpay.com/pgw/uat/pwa/#/?"
ORDER_QUERY_URL = "http://api.kbzpay.com/payment/gateway/uat/queryorder"
REFUND_URL = "https://api.kbzpay.com:18008/payment/gateway/uat/refund"

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
    def __init__(self, certfile, keyfile, password=None, *args, **kwargs):
        self._certfile = certfile
        self._keyfile = keyfile
        self._password = password
        super(self.__class__, self).__init__(*args, **kwargs)

    def init_poolmanager(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).init_poolmanager(*args, **kwargs)

    def proxy_manager_for(self, *args, **kwargs):
        self._add_ssl_context(kwargs)
        return super(self.__class__, self).proxy_manager_for(*args, **kwargs)

    def _add_ssl_context(self, kwargs):
        context = create_urllib3_context()
        context.load_cert_chain(certfile=self._certfile,
                                keyfile=self._keyfile,
                                password=str(self._password))
        kwargs['ssl_context'] = context


def verify_signature(response):
    # 验签
    re_li = []
    for key, value in response.items():
        if key in ["sign", "sign_type"]:
            continue
        re_li.append(str(key) + "=" + str(value))
    re_li.sort()
    res_string = ""
    for it in re_li:
        res_string = res_string + it + "&"
    res_string = res_string + "key=" + APP_KEY
    res_hash_obj = hashlib.sha256()
    res_hash_obj.update(res_string.encode('utf-8'))
    res_sign = res_hash_obj.hexdigest().upper()
    return res_sign, res_string


def verify_ssl(url, params):
    session = requests.Session()
    session.mount('https://api.kbzpay.com:18008/', SSLAdapter(
        "./uat_merchserver_cert_200121.pem", "./uat_merchserver_key_200121.pem",
        "Aa123456"))
    response = session.post(url=url, json=json.dumps(params))

    print(response)
    return response


def request_post_api(url, common_params, biz_content, with_ssl=False):
    dict_merged = dict(biz_content, **common_params)
    res_sign, res_string = verify_signature(dict_merged)
    common_params["sign_type"] = "SHA256"
    common_params["sign"] = res_sign
    common_params["biz_content"] = biz_content
    params = {"Request": common_params}
    if with_ssl:
        # res = verify_ssl(url, params)
        # res = requests.post(
        #     url=url, json=params, timeout=30).json()
        res = requests.post(
            url=url, json=params, timeout=30,
            cert=("client.pem", "keys.pem")).json()
        # res = requests.post(
        #     url=url, json=params, timeout=30,
        #     cert=("uat_merchserver_cert_200121.pem",
        #           "uat_merchserver_key_200121.pem")).json()
        # res = requests.post(
        #     url=url, json=params, timeout=30, cert="UAT_CA_PGW.crt").json()
    else:
        res = requests.post(url=url, json=params, timeout=30).json()
    print(res)
    response = res["Response"]

    if response["result"] != "SUCCESS":
        print("pwa_error  message=%s,code=%s" % (
            response['msg'], response['code']))
        raise Exception(response['msg'])
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
        "notify_url": "https://m.agonya.com.mm/payment/kbzpay/ipn",
        "method": "kbz.payment.precreate",
        "nonce_str": unique_key,
        "version": "1.0"
    }

    biz_content = {
        "merch_order_id": merch_order_id,
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "trade_type": TRADE_TYPE,
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
        "notify_url": "https://m.agonya.com.mm/payment/kbzpay/ipn",
        "method": "kbz.payment.queryorder",
        "nonce_str": unique_key,
        "version": "1.0"
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


def get_complete_pwa_url(params):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "prepay_id": params.get("prepay_id"),
        "nonce_str": unique_key,
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
    }
    sign, res_string = verify_signature(common_params)
    url = PWA_URL + res_string + "&sign=" + sign
    return url


if __name__ == "__main__":
    # response = pre_create(
    #     "10002", "100", "MMK", title=None, timeout_express=None,
    #     callback_info=None, operator_id=None, store_id=None,
    #     terminal_id=None, business_param=None)

    # res = verify_signature(response_test.get("Response"))

    # res = get_complete_pwa_url(response.get("Response"))
    # res = query_order(
    #     merch_order_id="10001", mm_order_id=None, refund_request_no=None)

    res = refund_order(
        "10001", refund_request_no=None, refund_reason=None)
    print(res)



