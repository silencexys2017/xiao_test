#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

secret_key = "sk_test_db2e6d4e2ecdabfda816787fff97ad7f8b89387c"
public_key = "pk_test_1128700716ae14243c0b56ca08be1edfce8aff67"
callback_url = "https://uomnify-test.perfee.com/api/payment/paystack/callback"
webhook_url = "https://uomnify-test.perfee.com/api/payment/paystack/webhook"
initialize_api = "https://api.paystack.co/transaction/initialize"
verify_transaction_api = "https://api.paystack.co/transaction/verify/{}"
fetch_transaction_api = "https://api.paystack.co/transaction/{}"
view_transaction_timeline_api = "https://api.paystack.co/transaction/timeline/{}"
refund_api = "https://api.paystack.co/refund"

channels = ['card', 'bank', 'ussd', 'qr', 'mobile_money', 'bank_transfer']

Headers = {
    "Authorization": "Bearer %s" % secret_key,
    "Content-Type": "application/json"
}


def initialize_order(
        amount, email, currency=None, reference=None, callback_url=None,
        plan=None, invoice_limit=None, metadata=None, channels=None,
        split_code=None, subaccount=None, transaction_charge=None, bearer=None):
    data = {
        "amount": amount,
        "email": email,
        "currency": currency,
        "reference": reference,
        "callback_url": callback_url
    }
    if plan:
        data["plan"] = plan
    if invoice_limit:
        data["invoice_limit"] = invoice_limit
    if metadata:
        data["metadata"] = metadata
    if channels:
        data["channels"] = channels
    if split_code:
        data["split_code"] = split_code
    if subaccount:
        data["subaccount"] = subaccount
    if transaction_charge:
        data["transaction_charge"] = transaction_charge
    if bearer:
        data["bearer"] = bearer

    result = requests.post(
        url=initialize_api, headers=Headers, json=data, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response
    """
    {
        "status": true,
        "message": "Authorization URL created",
        "data": {
            "authorization_url": "https://checkout.paystack.com/32vokoovpvrkxf0",
            "access_code": "32vokoovpvrkxf0",
            "reference": "1zlvi8t2zl"
        }
    }
    """


def verify_transaction(reference):
    result = requests.get(
        url=verify_transaction_api.format(reference), headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def fetch_transaction(tran_id):
    result = requests.get(
        url=fetch_transaction_api.format(tran_id), headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def view_transaction_timeline(tran_id=None, reference=None):
    id_or_reference = None
    if tran_id:
        id_or_reference = tran_id
    elif reference:
        id_or_reference = reference
    result = requests.get(
        url=view_transaction_timeline_api.format(id_or_reference),
        headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def create_refund(transaction, amount=None, currency=None, customer_note=None,
                  merchant_note=None):
    data = {
        "transaction": transaction
    }
    if amount:
        data["amount"] = amount
    if currency:
        data["currency"] = currency
    if customer_note:
        data["customer_note"] = customer_note
    if merchant_note:
        data["merchant_note"] = merchant_note
    result = requests.post(
        url=refund_api, json=data, headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def list_refunds(reference, currency=None, from_time=None, to_time=None,
                 per_page=None, page_number=None):
    data = {
        "transaction": reference
    }
    if from_time:
        data["from"] = from_time
    if currency:
        data["currency"] = currency
    if to_time:
        data["to"] = to_time
    if per_page:
        data["perPage"] = per_page
    if page_number:
        data["page"] = page_number
    result = requests.get(
        url=refund_api, params=data, headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


def fetch_refund(refund_id):
    fetch_refund_api = refund_api + "/%s" % refund_id
    result = requests.get(
        url=fetch_refund_api, headers=Headers, timeout=30)
    if str(result.status_code).startswith("5"):
        raise Exception("Request method not recognised or implemented.")
    response = result.json()
    if response.get("status") is False:
        raise Exception(response.get("message"))
    return response


if __name__ == "__main__":
    res = initialize_order(
        200, "xiaoyongsheng@perfee.com", currency="NGN", reference="xiao005")
    # res = verify_transaction(reference="xiao002")
    # res = fetch_transaction(tran_id="1589098528")
    # res = view_transaction_timeline(tran_id="", reference="xiao")
    # res = create_refund(
    #     transaction=1581884298, amount=5, currency=None,
    #     customer_note=None, merchant_note=None)
    # res = list_refunds(1326836306, currency=None, from_time=None, to_time=None,
    #                    per_page=None, page_number=None)
    # res = fetch_refund(refund_id="2484373")
    print(res)
