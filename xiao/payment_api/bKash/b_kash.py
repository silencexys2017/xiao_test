#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
"""
"username": "PERFEEONLINESHOP",
"password": "pE@1fi5NLt4D8C",
"app_key": "46ep1363qr0q9u58lld2usidko",
"app_secret": "ju4olme7t8lh70c9arar99i4hukq2qdr4n0g2vs57tji8i0o02d",
"ipn_listener": "https://api.perfee.com/partner/pay/bkash/ipn",
"perfee_url": "https://m.perfee.com/bkash-payment?billId=%s&agreementStatus=%s&customerMsisdn=%s",
"pay_callback_url": "https://api.perfee.com/partner/pay/bkash/payment-callback?platform=%s&billId=%s&token=%s",
"agree_callback_url": "https://api.perfee.com/partner/pay/bkash/agreement-callback?platform=%s&billId=%s&token=%s",
"execute_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute",
"grant_token_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant",
"refresh_token_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh",
"query_payment_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status",
"create_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create",
"query_agreement_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/status",
"cancel_agreement_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/agreement/cancel",
"search_transaction_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/general/searchTransaction",
"refund_api": "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/refund"
"""
# USERNAME = "sandboxTokenizedUser02"
# PASSWORD = "sandboxTokenizedUser02@12345"
# APP_KEY = "4f6o0cjiki2rfm34kfdadl1eqq"
# APP_SECRET = "2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b"

USERNAME = "PERFEEONLINESHOP"
PASSWORD = "pE@1fi5NLt4D8C"
APP_KEY = "46ep1363qr0q9u58lld2usidko"
APP_SECRET = "ju4olme7t8lh70c9arar99i4hukq2qdr4n0g2vs57tji8i0o02d"

AGREE_CALLBACK_URL = "https://api-dev.perfee.com/partner/pay/bkash/" \
                     "agreement-callback?platform=%s&billId=%s&token=%s"
PAY_CALLBACK_URL = "https://api-dev.perfee.com/partner/pay/bkash/" \
                   "payment-callback?platform=%s&billId=%s&token=%s"
GRANT_TOKEN_API = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"
REFRESH_TOKEN_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
                    "checkout/token/refresh"
CREATE_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/create"
EXECUTE_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
              "checkout/execute"
QUERY_PAYMENT_API = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status"
QUERY_AGREEMENT_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                      "tokenized/checkout/agreement/status"
CANCEL_AGREEMENT_API = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                       "tokenized/checkout/agreement/cancel"
search_transaction_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/" \
                         "tokenized/checkout/general/searchTransaction"
search_transaction_api = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/general/searchTransaction"
refund_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/payment/refund"

refund_status_api = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/" \
             "checkout/payment/refund/status"

PERFEE_URL = "https://m-dev.perfee.com/bkash-payment?billId=%s" \
             "&agreementStatus=%s&customerMsisdn=%s"

# bkash测试账号：01770618575，短信验证码: 123456， PIN: 12121

id_token = "eyJraWQiOiJEWXd6RU9Fd3h5Q3lkRVwvUnJZU1BOcGk5MENBQkVBeHZ0bUs1QXQ4XC9oaVk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlZDM1ZWNmMS05ZWM3LTQyYmYtYmRhOC05ZWZmNjFhNTE2NDUiLCJhdWQiOiI0NmVwMTM2M3FyMHE5dTU4bGxkMnVzaWRrbyIsImV2ZW50X2lkIjoiMjE4NzA5NzQtOWZjZC00MGFjLWJlYjQtNjA4ZWY3ZWM0NjU1IiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2MDIzMjUwNjAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV9UM1ZLQ2cyaHkiLCJjb2duaXRvOnVzZXJuYW1lIjoiUEVSRkVFT05MSU5FU0hPUCIsImV4cCI6MTYwMjMyODY2MCwiaWF0IjoxNjAyMzI1MDYwfQ.cvAB_ENhTMvUsY27YOXZRllgcEg1KWwar7Q9OHFhGziHmVWsTQKx8kiBabH4M-9ZIeW1EXqtrgO7ufBYudqepuP-XAypcQcNufXc0j-6jKERYlNE8JFDxzUee8ivACeo1YY55mNveTElps7BpqYiru60W91Ocu9UiQA4t4wBKOsNdaugPyyKYbg3aegsNFwZcuiT135_WGmFR6anRZRWjua7zC79oNJFLgPSxXwpdOJ3wvzcDz3sKx-4raJVmIwxXkJwldAgjQ3bvaCt-qmFgUmfzx6DjcRZEYJt02Q-A2l25BQyFS3vRMUx_wTjyEuq6KJccw9NiPB-bi7HVKSsig"


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
    id_token = "eyJraWQiOiJEWXd6RU9Fd3h5Q3lkRVwvUnJZU1BOcGk5MENBQkVBeHZ0bUs1QXQ4XC9oaVk9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJlZDM1ZWNmMS05ZWM3LTQyYmYtYmRhOC05ZWZmNjFhNTE2NDUiLCJhdWQiOiJrNW1xNmJlaWs0aWR2ZDkxcDRmdGV0cHYzIiwiZXZlbnRfaWQiOiIxMDM3NzVlZC03NjUwLTQzOTMtYWY2Zi0xZjEzZGNiYTY4MGMiLCJ0b2tlbl91c2UiOiJpZCIsImF1dGhfdGltZSI6MTY1NDE1MzcyOSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoZWFzdC0xLmFtYXpvbmF3cy5jb21cL2FwLXNvdXRoZWFzdC0xX1QzVktDZzJoeSIsImNvZ25pdG86dXNlcm5hbWUiOiJQRVJGRUVPTkxJTkVTSE9QIiwiZXhwIjoxNjU0MTU3MzI5LCJpYXQiOjE2NTQxNTM3Mjl9.HavLS04rc7WE-pg4yEyBzPKul2d03qHjdp83xGgAs5j-ruSjTltsGU-QGfDVwqjDH8Zi5pP_a5qe00xmAOArl_FCTvl3y0aygZujVSOQJGcVirso5x82yIb6Z7zH2W1binws5ZpAGo1gV241ncVSxZ8UQ5Yum0t7bKKAp5uIUJVyHIc_k_-xXVLAz5caaZ4npSSyMrTuyoAGW2dfKqjJrUDrs5IKuAbCPWf5zVgeMwBZ3iWCR7LqpUq6hQ7FBmxbKDo2j4pz-1y2AolqWegBuPi4LwOkcDnllO6XD8x6hfk350hrxjiFzqM26nJ-Kb0izJVi0cthWT4r80kWojaxIA"
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

    # res = create_payment_without_agreement(
    #     "200.00", "BDT", 2, "B189434", "0137994348", "web", id_token, "48382")

    # res = execute_payment("TR0011YZ1598431437675", id_token)
    # trxID = '7GL1029CPN'
    # paymentID = 'TR0001NL1595325165379'
    # {"_id": 88693, "paymentId": "TR0011XT1599792897123"} 'verificationStatus': 'Incomplete'
    # {"_id": 88694, "paymentId": "TR00114B1599793003053"}
    # {"_id": 88777, "paymentId": "TR0011CV1599885266993"} 'verificationStatus': 'Complete' 'transactionStatus': 'Initiated'
    # {"_id": 88780, "paymentId": "TR0011SB1599886511378"}  Complete
    # {"_id": 88783, "paymentId": "TR0011HX1599886940093"}  Incomplete
    # {"_id": 88784, "paymentId": "TR0011XA1599887092670"}   Complete

    res = query_payment_status("TR0001301654091562654", id_token)

    # res = search_transaction("7JA8733V86", id_token)

    # res = refund_transaction(
    #     "TR0011YZ1598431437675", '7HQ602B9PY', id_token, "100", "CancelOrder",
    #     "skuId=80004838")

    # res = query_refund_status("TR0011YZ1598431437675", '7HQ602B9PY', id_token)

    # print(res)