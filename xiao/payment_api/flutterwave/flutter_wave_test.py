#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

public_key = "FLWPUBK_TEST-6b02b80c52963ab5f44bfc967da26046-X"
secret_key = "FLWSECK_TEST-04b54d064be49c42257b73b463845a45-X"
encryption_key = "FLWSECK_TESTa95de7baf762"
hash_secret = "uonmify31415926mall"

webhook_url = "https://uomnify-test.perfee.com/api/payment/flutterwave/webhook"
callback_url = "https://uomnify-test.perfee.com/api/payment/flutterwave/callback"
initiate_payment_api = "https://api.flutterwave.com/v3/payments"
get_all_transactions_api = "https://api.flutterwave.com/v3/transactions"
charges_url = "https://api.flutterwave.com/v3/charges"
verify_transaction_api = "https://api.flutterwave.com/v3/transactions/{}/verify"
verify_by_reference_api = "https://api.flutterwave.com/v3/transactions/verify_by_reference"
view_transaction_timeline_api = "https://api.flutterwave.com/v3/transactions/{}/events"
resend_transaction_webhook_api = "https://api.flutterwave.com/v3/transactions/{}/resend-hook"
initiate_transaction_refund_api = "https://api.flutterwave.com/v3/transactions/{}/refund"
get_transaction_refund_api = "https://api.flutterwave.com/v3/refunds/{}"
get_all_refunds_api = "https://api.flutterwave.com/v3/refunds"
get_transaction_fee_api = "https://api.flutterwave.com/v3/transactions/fee"
channels = ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

headers = {
    "Authorization": "Bearer %s" % secret_key,
    "Content-Type": "application/json",
    "Accept": "application/json"
}


def initialize_payment(
        tx_ref, amount, email, phone_number, customize_title,
        customize_description, customize_logo, customer_name=None,
        currency="NGN", payment_options="card", redirect_url=None,
        subaccounts=None, payment_plan=None, integrity_hash=None, metadata=None):
    redirect_url = redirect_url if redirect_url else callback_url
    data = {
        "tx_ref": tx_ref,
        "amount": amount,
        "currency": currency,
        "payment_options": payment_options,
        "redirect_url": redirect_url,
        "customer": {
            "email": email,
            "phonenumber": phone_number,
            "name": customer_name
        },
        "customizations": {
            "title": customize_title,
            "description": customize_description,
            "logo": customize_logo
        },
        "meta": {
            'consumer_id': 23,
            'consumer_mac': '92a3-912ba-1192a'
        }

    }
    if integrity_hash:
        data["integrity_hash"] = integrity_hash
    if payment_plan:
        data["payment_plan"] = payment_plan
    if subaccounts:
        data["subaccounts"] = subaccounts

    result = requests.post(
        url=initiate_payment_api, headers=headers, json=data, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response
    """
    {
    'status': 'success', 
    'message': 'Hosted Link', 
    'data': {
    'link': 'https://ravemodal-dev.herokuapp.com/v3/hosted/pay/826f6dc4918e46039a75'
    }}
    """


def verify_transaction(transaction_id):
    result = requests.get(
        url=verify_transaction_api.format(transaction_id), headers=headers,
        timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def verify_by_reference(tx_ref):
    data = {
        "tx_ref": tx_ref
    }
    result = requests.get(
        url=verify_by_reference_api, params=data, headers=headers,
        timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    print(response)
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def get_transactions(
        from_time=None, to_time=None, page=None, customer_email=None,
        status=None, tx_ref=None, customer_fullname=None, currency=None):
    data = {}
    if from_time:
        data["from"] = from_time
    if to_time:
        data["to"] = to_time
    if page:
        data["page"] = page
    if customer_email:
        data["customer_email"] = customer_email
    if status:
        data["status"] = status
    if tx_ref:
        data["tx_ref"] = tx_ref
    if customer_fullname:
        data["customer_fullname"] = customer_fullname
    if currency:
        data["currency"] = currency
    result = requests.get(
        url=get_all_transactions_api, params=data, headers=headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def view_transaction_timeline(tran_id):
    result = requests.get(
        url=view_transaction_timeline_api.format(tran_id),
        headers=headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def initiate_transaction_refund(transaction_id, amount=None):
    data = {}
    if amount:
        data["amount"] = amount
    result = requests.post(
        url=initiate_transaction_refund_api.format(transaction_id),
        params=data, headers=headers, timeout=30)

    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def get_refunds(refund_id=None, currency=None, from_time=None, to_time=None,
                status=None, flw_ref=None):
    data = {}
    if from_time:
        data["from"] = from_time
    if currency:
        data["currency"] = currency
    if to_time:
        data["to"] = to_time
    if status:
        data["status"] = status
    if refund_id:
        data["id"] = refund_id
    if flw_ref:
        data["flw_ref"] = flw_ref
    result = requests.get(
        url=get_all_refunds_api, params=data, headers=headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def get_transaction_refund(refund_id):
    result = requests.get(
        url=get_transaction_refund_api.format(refund_id), headers=headers,
        timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def resend_transaction_webhook(transaction_id, wait):
    data = {"wait": wait}
    result = requests.post(
        url=resend_transaction_webhook_api.format(transaction_id),
        params=data, headers=headers, timeout=30)

    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def get_transaction_fee(amount, currency, payment_type=None,
                        card_first6digits=None):
    data = {"amount": amount, "currency": currency}
    if payment_type:
        data["payment_type"] = payment_type
    if card_first6digits:
        data["card_first6digits"] = card_first6digits
    result = requests.get(
        url=get_transaction_fee_api, params=data, headers=headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") != "success":
        raise Exception(response.get("message"))
    return response


def get_quick_docs(url):
    split_list = url.split("v3")
    goal_url = split_list[0] + "v3/meta" + split_list[1]
    result = requests.post(url=goal_url, headers=headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    return response


if __name__ == "__main__":
    # res = initialize_payment(
    #     tx_ref="test114", amount="200", email="xiaoyongsheng@perfee.com",
    #     phone_number="", customer_name="xiao",
    #     customize_title="Uomnify Mall", customize_description="Well",
    #     customize_logo="https://uomnify-test.perfee.com/logosvg.svg",
    #     currency="NGN", payment_options="card", redirect_url=None,
    #     subaccounts=None, payment_plan=None, integrity_hash=None,
    #     metadata={"consumer_id": 110})
    # res = get_quick_docs(charges_url)
    # res = verify_transaction(transaction_id="xiao002")
    res = verify_by_reference(tx_ref="test114")
    # res = view_transaction_timeline(tran_id="3142592")
    # res = get_transactions(
    #     from_time=None, to_time=None, page=None, customer_email=None,
    #     status="successful", tx_ref="test111", customer_fullname=None,
    #     currency=None)
    # res = resend_transaction_webhook(transaction_id="3142592", wait="1")
    # res = initiate_transaction_refund(
    #     transaction_id=3142592, amount=5)
    # res = get_refunds(
    #     refund_id=None, currency=None, from_time=None, to_time=None,
    #     status=None, flw_ref="test111")
    # res = get_transaction_refund(refund_id="2484373")
    # res = get_transaction_fee(amount=100, currency="NGN", payment_type=None,
    #                           card_first6digits=None)
    print(res)
