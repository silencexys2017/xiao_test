#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

# USERNAME = "sandboxTokenizedUser02"
# PASSWORD = "sandboxTokenizedUser02@12345"
# APP_KEY = "4f6o0cjiki2rfm34kfdadl1eqq"
# APP_SECRET = "2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b"

USERNAME = "sandboxTokenizedUser01"
PASSWORD = "sandboxTokenizedUser12345"
APP_KEY = "7epj60ddf7id0chhcm3vkejtab"
APP_SECRET = "18mvi27h9l38dtdv110rq5g603blk0fhh5hg46gfb27cp2rbs66f"

AGREE_CALLBACK_URL = "https://api-dev.perfee.com/partner/pay/bkash/" \
                     "agreement-callback?platform=%s&billId=%s&token=%s"
PAY_CALLBACK_URL = "https://api-dev.perfee.com/partner/pay/bkash/" \
                   "payment-callback?platform=%s&billId=%s&token=%s"
GRANT_TOKEN_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
                  "checkout/token/grant"
REFRESH_TOKEN_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
                    "checkout/token/refresh"
CREATE_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/create"
EXECUTE_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
              "checkout/execute"
QUERY_PAYMENT_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                    "tokenized/checkout/payment/status"
QUERY_AGREEMENT_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                      "tokenized/checkout/agreement/status"
CANCEL_AGREEMENT_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                       "tokenized/checkout/agreement/cancel"
search_transaction_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                         "tokenized/checkout/general/searchTransaction"
refund_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/payment/refund"

refund_status_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/payment/refund/status"

PERFEE_URL = "https://m-dev.perfee.com/bkash-payment?billId=%s" \
             "&agreementStatus=%s&customerMsisdn=%s"

# bkash测试账号：01770618575，短信验证码: 123456， PIN: 12121

id_token = "eyJraWQiOiJvTVJzNU9ZY0wrUnRXQ2o3ZEJtdlc5VDBEcytrckw5M1NzY0VqUzlERXVzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiJlODNlMDkwMC1jY2ZmLTQzYTctODhiNy0wNjE5NDJkMTVmOTYiLCJhdWQiOiI0ZjZvMGNqaWtpMnJmbTM0a2ZkYWRsMWVxcSIsImV2ZW50X2lkIjoiY2RhZjI3NDYtYjBiMy00MWM4LWE4ZWMtNzNhNmU0NTNhYWRjIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDIzMjk1MTQsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV9yYTNuUFkzSlMiLCJjb2duaXRvOnVzZXJuYW1lIjoic2FuZGJveFRva2VuaXplZFVzZXIwMiIsImV4cCI6MTYwMjMzMzExNCwiaWF0IjoxNjAyMzI5NTE0fQ.vBm1AFfDE0dP1emgWWIisl8nLxrAdmb3jOXJ1yVo0ulyQ1jhAEokceOUpgYXL-F9Yx1yNSpGemPgUXPnROaFpTpq9nJB5VEV97vRkO9c-gd30vjgrT7-Z5ZBgDh9HHu7WxISA1iRUTbYe0Dgm8kdHWX9VEFWebgSMeQtbPgqjqzABPjpEWR2rTRHLkImQS3BwfXNrVdNPq2IdmcqPQ0PAoPTpRTus9XZdKLStnolyAx_CYXmmS7C-YCCL_bkEtdeg6PWvcmVesK0YpXBQslQTFyUWdqd_DVz0LQ1_X4mtxN30FLZnnrcXT2pGmR5bkCZ1qoDwvDiXLk06eLUHWJI6w"


def request_post_api(url, token, args):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': token,
        'X-APP-Key': APP_KEY
    }

    res = requests.post(
        url=url, headers=headers, json=args, timeout=30).json()
    print(res)
    code = int(res['statusCode'])
    message = res['statusMessage']

    if code != 0:
        print("bkash_error  message=%s,code=%s" % (message, code))
        raise Exception(message)

    return res


def grant_token():
    url = GRANT_TOKEN_API
    headers = {
        'username': USERNAME,
        'password': PASSWORD
    }
    data = {
        'app_key': APP_KEY,
        'app_secret': APP_SECRET
    }

    res = requests.post(
        url=url, headers=headers, json=data, timeout=30).json()
    code = int(res['statusCode'])
    message = res['statusMessage']

    if code != 0:
        print("bkash_error  message=%s,code=%s" % (message, code))
        raise Exception(message)
    print(res)

    return res


def refresh_token(refresh_token):
    url = REFRESH_TOKEN_API
    headers = {
        'username': USERNAME,
        'password': PASSWORD
    }

    data = {
        'app_key': APP_KEY,
        'app_secret': APP_SECRET,
        'refresh_token': refresh_token
    }

    res = requests.post(url=url, headers=headers, json=data, timeout=30).json()
    code = int(res['statusCode'])
    message = res['statusMessage']

    if code != 0:
        print("bkash_error  message=%s,code=%s" % (message, code))
        raise Exception(message)

    return res


def create_agreement(bill_id, payer_reference, platform, token, per_token):
    args = {
        'mode': '0000',
        'payerReference': payer_reference,
        'callbackURL': AGREE_CALLBACK_URL % (platform, bill_id, per_token)
    }

    return request_post_api(CREATE_API, token, args)


def cancel_agreement(agreement_id, token):
    args = {
        'agreementID': agreement_id
    }
    # {"statusCode":"0000","agreementStatus":"Cancelled"}
    return request_post_api(CANCEL_AGREEMENT_API, token, args)


def query_agreement_status(agreement_id, token):
    args = {
        'agreementID': agreement_id
    }
    return request_post_api(QUERY_AGREEMENT_API, token, args)


def create_tokenized_payment(
        agreement_id, amount, currency, bill_id, merchant_invoice_number,
        platform, token, per_token):
    args = {
        'mode': '0001',
        'agreementID': agreement_id,
        'amount': amount,
        'currency': currency,
        'intent': "sale",
        'merchantInvoiceNumber': merchant_invoice_number,
        'callbackURL': PAY_CALLBACK_URL % (platform, bill_id, per_token)
    }

    return request_post_api(CREATE_API, token, args)


def create_payment_without_agreement(
        amount, currency, bill_id, merchant_invoice_number, payer_reference,
        platform, token, per_token):
    args = {
        'mode': '0011',
        'payerReference': payer_reference,
        'amount': amount,
        'currency': currency,
        'intent': "sale",
        'merchantInvoiceNumber': merchant_invoice_number,
        'callbackURL': PAY_CALLBACK_URL % (platform, bill_id, per_token)
    }

    return request_post_api(CREATE_API, token, args)


def execute_payment(payment_id, token):
    args = {
        'paymentID': payment_id
    }
    return request_post_api(EXECUTE_API, token, args)


def query_payment_status(payment_id, token):
    args = {
        'paymentID': payment_id
    }
    return request_post_api(QUERY_PAYMENT_API, token, args)


def search_transaction(trx_id, token):
    args = {
        'trxID': trx_id
    }
    return request_post_api(search_transaction_api, token, args)


def refund_transaction(payment_id, trx_id, token, amount, reason, sku=None):
    args = {
        'paymentID': payment_id,
        'trxID': trx_id,
        'amount': amount,
        'reason': reason,
        'sku': sku
    }

    return request_post_api(refund_api, token, args)


def query_refund_status(payment_id, trx_id, token):
    args = {
        'paymentID': payment_id,
        'trxID': trx_id
    }
    return request_post_api(refund_api, token, args)


def get_perfee_url():
    return PERFEE_URL


if __name__ == "__main__":
    # id_token = grant_token().get("id_token")
    id_token = "eyJraWQiOiJvTVJzNU9ZY0wrUnRXQ2o3ZEJtdlc5VDBEcytrckw5M1NzY0VqUzlERXVzPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIwZTVjOGU4Ni0xMTQzLTQyNjEtOTJkYy02MTQwMTNhMmNkYTAiLCJhdWQiOiI2cDdhcWVzZmljZTAxazltNWdxZTJhMGlhaCIsImV2ZW50X2lkIjoiOWY4NmZlNmEtZWM0Mi00NjBkLWI2NWMtNGE3NzRjYzc0YzA3IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NDY5ODk5MDcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV9yYTNuUFkzSlMiLCJjb2duaXRvOnVzZXJuYW1lIjoic2FuZGJveFRva2VuaXplZFVzZXIwMSIsImV4cCI6MTY0Njk5MzUwNywiaWF0IjoxNjQ2OTg5OTA3fQ.x-hDejbB-HcNBOnNuZg9f9tQTAl1MiZX6dwSicOf55hHNJ4Lv-FKa9DLHaHcrluz1MLYrr2N2Pr4U1-yNAMDgVZREhMQs0Eqvb8NdggDKkhBHsetm21IvsdmitZGeMyQpWVVaMUv7cDASGp2j8_DkmpNUcmE1Bd032i3xs9Cs4VSXMimvKyWxTFhUcPLW6115GjREeJLoXunfoqifhYs_zwP9bA1dXP5izoDQBfBcQqjxBrEvw8rphF0i2HqBIaKV-nPSeQnFIGnlp93hYo74ihBN9rF1J_EI8MTAdy5BwjXaAQxY3ilHaIYLdBeYvP493Ovq6rDQRt9ipngeEpPLA"
    print(id_token)

    # res = create_agreement(
    #     bill_id=1, payer_reference="342343", platform="web", token=id_token,
    #     per_token="432423")
    # payment_id = res.get("paymentID")

    # res = execute_payment("TR0011YZ1598431437675", id_token)
    # agreement_id = res.get("agreementID")

    # res = query_agreement_status(
    #     "TokenizedMerchant01MFD2W6N1595318329543", id_token)

    # res = cancel_agreement(
    #     "TokenizedMerchant01MFD2W6N1595318329543", id_token)

    # res = create_tokenized_payment(
    #     "TokenizedMerchant0210TSKC61596700937675", 100, "BDT", 1, "B12020",
    #     "web", id_token, "343423")

    res = create_payment_without_agreement(
        "200.00", "BDT", 2, "B1894334", "0137994348", "web", id_token, "48382")

    # res = execute_payment("TR0011YZ1598431437675", id_token)
    # trxID = '7GL1029CPN'
    # paymentID = 'TR0001NL1595325165379'
    # {"_id": 88693, "paymentId": "TR0011XT1599792897123"} 'verificationStatus': 'Incomplete'
    # {"_id": 88694, "paymentId": "TR00114B1599793003053"}
    # {"_id": 88777, "paymentId": "TR0011CV1599885266993"} 'verificationStatus': 'Complete' 'transactionStatus': 'Initiated'
    # {"_id": 88780, "paymentId": "TR0011SB1599886511378"}  Complete
    # {"_id": 88783, "paymentId": "TR0011HX1599886940093"}  Incomplete
    # {"_id": 88784, "paymentId": "TR0011XA1599887092670"}   Complete

    # res = query_payment_status("TR00117O1602329319554", id_token)

    # res = search_transaction("7JA8733V86", id_token)

    # res = refund_transaction(
    #     "TR0011YZ1598431437675", '7HQ602B9PY', id_token, "100", "CancelOrder",
    #     "skuId=80004838")

    # res = query_refund_status("TR0011YZ1598431437675", '7HQ602B9PY', id_token)

    print(res)