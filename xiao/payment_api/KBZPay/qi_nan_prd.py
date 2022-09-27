#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import uuid
import hashlib
from requests.adapters import HTTPAdapter
from urllib.parse import quote

from urllib3.util.ssl_ import create_urllib3_context


APP_ID = "kp71752c8d405e4a19b0327e2cfeb643"
APP_KEY = "5e5d338abcf1c5c03687c25739ce4f73"
MERCHANT_CODE = "200112"
USER_NAME = "Mr Zhang Junfei"
"PWAAPP, PAY_BY_QRCODE,APPH5,MICROPAY,QRCODE_H5, MINIAPP"
PW_TRADE_TYPE = "PWAAPP"
QR_TRADE_TYPE = "PAY_BY_QRCODE"
APP_H5 = "APPH5"
TRANS_CURRENCY = "MMK"
ORG_PORTAL_URL = "https://159.138.20.58:31002/payment/orglogin.action"
PRE_CREATE_URL = "https://api.kbzpay.com/payment/gateway/precreate"
PWA_URL = "https://wap.kbzpay.com/pgw/pwa/#/"
ORDER_QUERY_URL = "https://api.kbzpay.com/payment/gateway/queryorder"
REFUND_URL = "https://api.kbzpay.com:8008/payment/gateway/refund"
ORDER_CLOSE_URL = "https://api.kbzpay.com/payment/gateway/closeorder"
QUERY_REFUND_API = "https://api.kbzpay.com/payment/gateway/queryrefund"
IPN_LISTENER = "https://api.perfee.com/payment/kbzpay/ipn"
referer_url = "https://m.perfee.com/payment/kbzpay/pay"
return_url = "https://m.perfee.com/payment/kbzpay/callback"
app_cube_callback_success_url = ""
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
        if key in ["sign", "sign_type", "refund_info", "qrCode"] or not value:
            continue
        # if is_refund:
        #     if key not in REFUND_SIGN_FIELDS:
        #         continue
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


def sign_order_info(prepay_id, merch_code, appid, timestamp, nonce_str):
    order_info = {
        "prepay_id": prepay_id,
        "merch_code": merch_code,
        "appid": appid,
        "timestamp": timestamp,
        "nonce_str": nonce_str
    }
    re_li = []
    for key, value in order_info.items():
        re_li.append(str(key) + "=" + str(value))
    re_li.sort()
    res_string = ""
    for it in re_li:
        res_string = res_string + it + "&"
    string_sign = res_string + "key=" + APP_KEY
    hash_obj = hashlib.sha256()
    hash_obj.update(string_sign.encode('utf-8'))
    return res_string + "sign=" + hash_obj.hexdigest().upper()


def request_post_api(url, common_params, biz_content, with_ssl=False):
    dict_merged = dict(biz_content, **common_params)
    res_sign, res_string = verify_signature(dict_merged)
    common_params["sign_type"] = "SHA256"
    common_params["sign"] = res_sign
    common_params["biz_content"] = biz_content
    headers = {"Content-Type": "application/json"}
    params = {"Request": common_params}
    if with_ssl:
        session = requests.Session()
        session.mount(url, SSLAdapter(
            "ssl_certificate/uat_merchserver_cert.pem",
            "./ssl_certificate/uat_merchserver_key.pem",
            "Aa123456", "./ssl_certificate/UAT_CA_PGW.crt"))
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
        merch_order_id, total_amount, trans_currency, trade_type, title=None,
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
        "version": "1.0"
    }

    biz_content = {
        "merch_order_id": merch_order_id,
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "trade_type": trade_type,
        "total_amount": total_amount,
        "trans_currency": trans_currency,
    }
    if title:
        biz_content["title"] = title  # Offering name.
    if timeout_express:
        biz_content["timeout_express"] = timeout_express  # 多长时间支付失效min
    if callback_info:
        biz_content["callback_info"] = quote(str(callback_info))
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
        biz_content["business_param"] = quote(str(business_param))
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

    return request_post_api(QUERY_REFUND_API, common_params, biz_content)


def query_refund(merch_order_id=None, refund_request_no=None, sub_type=None,
                 sub_identifier_type=None, sub_identifier=None):
    unique_key = str(uuid.uuid1()).replace("-", "")
    if len(unique_key) > 32:
        unique_key = unique_key[:32]
    common_params = {
        "timestamp": str(int(time.time())),
        "method": "kbz.payment.queryrefund",
        "nonce_str": unique_key,
        "version": "1.0"
    }

    biz_content = {
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "merch_order_id": merch_order_id
    }
    if refund_request_no:
        biz_content["refund_request_no"] = refund_request_no
    if sub_type:
        biz_content["sub_type"] = sub_type
    if sub_identifier_type:
        biz_content["sub_identifier_type"] = sub_identifier_type
    if sub_identifier:
        biz_content["sub_identifier"] = sub_identifier

    return request_post_api(QUERY_REFUND_API, common_params, biz_content)


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
        merch_order_id, refund_request_no, refund_amount=None,
        is_last_refund=None, refund_reason=None):
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
        "merch_order_id": str(merch_order_id),
        "merch_code": MERCHANT_CODE,
        "appid": APP_ID,
        "refund_request_no": str(refund_request_no)
    }
    if refund_amount:
        biz_content["refund_amount"] = str(refund_amount)
    if is_last_refund:
        biz_content["is_last_refund"] = is_last_refund
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
    #     merch_order_id="TEST913", total_amount="100", trans_currency="MMK",
    #     trade_type="PAY_BY_QRCODE", title=None, timeout_express=None,
    #     callback_info="36", operator_id=None, store_id=None, terminal_id=None,
    #     business_param=None)

    # res = get_complete_pwa_url(response.get("Response"))
    res = query_order(
        merch_order_id="124191", mm_order_id=None,
        refund_request_no="")  # "86844"  "01002091070008232787" "483"
    # res = query_refund(merch_order_id="124191")
    # res = close_order("TEST911")
    # res = refund_order(
    #     "102562", refund_request_no="4697", refund_amount="1",
    #     refund_reason='CancelOrder')
    # sign_order_info(
    #     "KBZ00c25d94271b4d950ec748fdaf20c81d2b154042384", "200001",
    #     "kp419a753459284f72aa76d2ae9d6057", "1535165303",
    #     "5K8264ILTKCH16CQ2502SI8ZNMTM67VS")
    print(res)
