#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import hashlib
from urllib.parse import unquote

store_id = "perfe5c0df8f018ea2"
store_password = "perfe5c0df8f018ea2@ssl"
transaction_session_api = "https://sandbox.sslcommerz.com/gwprocess/v3/api.php"
validation_rest_api = "https://sandbox.sslcommerz.com/validator/api/" \
                      "validationserverAPI.php"
refund_query_rest_api = "https://sandbox.sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php"
transaction_query_api = "https://sandbox.sslcommerz.com/validator/api/merchantTransIDvalidationAPI.php"
res_str = "amount=330.00&bank_tran_id=20100982342Wj5aH2KpRp7z78u&base_fair=0.00&card_brand=VISA&card_issuer=STANDARD CHARTERED BANK&card_issuer_country=Bangladesh&card_issuer_country_code=BD&card_no=421481XXXXXX4177&card_type=VISA-Dutch Bangla&currency=BDT&currency_amount=330.00&currency_rate=1.0000&currency_type=BDT&risk_level=0&risk_title=Safe&status=VALID&store_amount=321.75&store_id=perfe5c0df8f018ea2&tran_date=2020-10-09 08%3A23%3A37&tran_id=2eca5973-09d6-11eb-a2b0-02550a0a00b7&val_id=20100982342sYLSgGjMh4eNZAW&value_a=86887&value_b=&value_c=&value_d=&verify_sign=34dff68d643e8270cc3f331be280b5c5&verify_sign_sha2=42f36b0d2efc41790265b9bc61ba2f0872bb756d51944936c1442696b24ec429&verify_key=amount%2Cbank_tran_id%2Cbase_fair%2Ccard_brand%2Ccard_issuer%2Ccard_issuer_country%2Ccard_issuer_country_code%2Ccard_no%2Ccard_type%2Ccurrency%2Ccurrency_amount%2Ccurrency_rate%2Ccurrency_type%2Crisk_level%2Crisk_title%2Cstatus%2Cstore_amount%2Cstore_id%2Ctran_date%2Ctran_id%2Cval_id%2Cvalue_a%2Cvalue_b%2Cvalue_c%2Cvalue_d"


def request_get_api(url, args):
    res = requests.get(url=url, params=args, timeout=30)
    print(res.content)
    print(res.text)
    res = res.json()
    print(res)

    if res.get("APIConnect") != "DONE":
        print("error  message=%s" % res.get("errorReason"))

    return res


def refund_transaction(
        bank_tran_id, refund_amount, refund_remarks, refe_id=None):
    args = {
        "bank_tran_id": bank_tran_id,
        "store_id": store_id,
        "store_passwd": store_password,
        "refund_amount": refund_amount,
        "refund_remarks": refund_remarks,
        "format": "json"
    }
    if refe_id:
        args["refe_id"] = refe_id

    return request_get_api(refund_query_rest_api, args)


def query_refund_status(refund_ref_id):
    args = {
        "refund_ref_id": refund_ref_id,
        "store_id": store_id,
        "store_passwd": store_password
    }
    return request_get_api(refund_query_rest_api, args)


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
    param_di["store_passwd"] = get_md5_key(store_password)
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


def query_transaction_by_transaction_id(tran_id):
    args = {
        "tran_id": tran_id,
        "store_id": store_id,
        "store_passwd": store_password
    }
    return request_get_api(transaction_query_api, args)


if __name__ == "__main__":
    # res = refund_transaction(
    #     bank_tran_id="20100982342Wj5aH2KpRp7z78u", refund_amount="1",  # 330
    #     refund_remarks="refund", refe_id=None)  # 5f80085ea3da6, 5f800dcb56965,
    # 5f8015165d1c4, 5f80174f8d440
    res = query_transaction_by_transaction_id(
        tran_id="7f6b6bfa-4931-11ec-ade3-0255ac100050")
    # res = query_refund_status(refund_ref_id="5f80174f8d440")
    # verify_ipn_notify(res_str)
    print(res)



