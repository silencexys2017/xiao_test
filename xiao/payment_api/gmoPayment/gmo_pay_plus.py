#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
# from urllib.parse import unquote
from datetime import datetime, timedelta

login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_name = "OTOKU WORLD Co.，Ltd."
store_pd = "z3gxd5ft"
DOMAIN_URL = "https://p01.mul-pay.jp"
PRE_CREATE_URL = "https://pt01.mul-pay.jp/payment/GetLinkplusUrlPayment.json"  # post
site_id = "tsite00041368"
site_pd = "2xzq35wr"
site_name = "OTOKU WORLD Co.，Ltd."
config_id = "perfeetest123"
company_name = "OTOKU WORLD株式会社"
contact_phone = "03-6427-1681"
contact_interval = "09:00-18:00"

RET_URL = "https://m-test.otoku-world.com/payment/gmo/result?billId=21"
RET_URL = "https://api-test.otoku-world.com/payment/gmo/result"
# RET_URL = "https://api-test.otoku-world.com/payment/gmo/ipn"
CANCEL_URL = "https://api-dev.perfee.com/partner/pay/gmo/callback?billId=%d"
QUERY_API = "https://pt01.mul-pay.jp/payment/SearchTradeMulti.idPass"
GEN_HTML = "test.html"


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


def request_post_api(url, args):
    headers = {"Content-Type": "application/json", "charset": "UTF-8"}

    res = requests.post(url=url, headers=headers, json=args, timeout=30).json()

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def pre_create(
        config_id, order_id, amount, tax, is_guide_email=None,
        is_thank_email=None, send_mail_address=None, customer_name=None,
        template_no=None, bcc_send_mail_address=None,
        from_send_mail_address=None, from_send_mail_name=None,
        client_field1=None, client_field2=None, client_field3=None,
        overview=None, detail=None, pay_methods=None, ret_url=None,
        job_cd="CAPTURE", method="1", pay_times=None, td_flag="0",
        member_id=None, sec_code_required_flag="1", tds2_type="3",
        cvs_name=None, cvs_phone=None, cvs_interval=None, customer_kana=None,
        tel_no=None):
    utc_now = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
    data = {
        "configid": config_id,
    }
    geturlparam = {
        "ShopID": store_id,
        "ShopPass": store_pd
    }
    if is_guide_email or is_thank_email:
        if is_guide_email:
            geturlparam["GuideMailSendFlag"] = is_guide_email  # 0 默认， 1
        if is_thank_email:
            geturlparam["ThanksMailSendFlag"] = is_thank_email  # 0 默认，1
        geturlparam["SendMailAddress"] = send_mail_address
        geturlparam["CustomerName"] = customer_name
        geturlparam["TemplateNo"] = template_no
    if bcc_send_mail_address:
        geturlparam["BccSendMailAddress"] = bcc_send_mail_address
    if from_send_mail_address:
        geturlparam["FromSendMailAddress"] = from_send_mail_address
    if from_send_mail_name:
        geturlparam["FromSendMailName"] = from_send_mail_name
    data["geturlparam"] = geturlparam
    transaction = {
        "OrderID": order_id,
        "Amount": amount
    }
    if tax:
        transaction["Tax"] = tax
    if client_field1:
        transaction["ClientField1"] = client_field1
    if client_field2:
        transaction["ClientField2"] = client_field2
    if client_field3:
        transaction["ClientField3"] = client_field3
    if overview:  #
        transaction["Overview"] = overview
    if detail:
        transaction["Detail"] = detail
    if pay_methods:
        transaction["PayMethods"] = pay_methods
    if ret_url:
        transaction["RetUrl"] = ret_url
    data["transaction"] = transaction
    customer = {}
    if send_mail_address:
        customer["MailAddress"] = send_mail_address
    if send_mail_address:
        customer["ConfirmMailAddress"] = send_mail_address
    if customer_name:
        customer["CustomerName"] = customer_name
    if customer_kana:
        customer["CustomerKana"] = customer_kana
    if tel_no:
        customer["TelNo"] = tel_no
    if customer:
        data["customer"] = customer
    displaysetting = {"ColorPattern": "nature_01", "blue_01Lang": "ja"}
    if displaysetting:
        data["displaysetting"] = displaysetting
    credit = {}
    if job_cd:
        credit["JobCd"] = job_cd
    if method:
        credit["Method"] = method
    if pay_times:
        credit["PayTimes"] = pay_times
    if td_flag:
        credit["TdFlag"] = td_flag
    if member_id:
        credit["MemberID"] = member_id
    if sec_code_required_flag:
        credit["SecCodeRequiredFlag"] = sec_code_required_flag
    if tds2_type:
        credit["Tds2Type"] = tds2_type
    if credit:
        data["credit"] = credit
    cvs = {}

    if cvs_name:
        cvs["ReceiptsDisp11"] = cvs_name
    if cvs_phone:
        cvs["ReceiptsDisp12"] = cvs_phone
    if cvs_interval:
        cvs["ReceiptsDisp13"] = cvs_interval
    if cvs:
        data["cvs"] = cvs
    print(data)

    return request_post_api(PRE_CREATE_URL, data)


def query_order_status(order_id, pay_type="3"):
    data = {
        "ShopID": store_id,
        "ShopPass": store_pd,
        "OrderID": order_id,
        "PayType": pay_type
    }

    res = requests.post(url=QUERY_API, params=data, timeout=30)
    res_di = {}
    for it in res.text.split("&"):
        item = it.split("=")
        res_di[item[0]] = item[1]
    print(res_di)

    return res


if __name__ == "__main__":
    res = pre_create(
        config_id=config_id, order_id="23893434", amount="100", tax="0",
        is_guide_email=None, is_thank_email=None,
        send_mail_address="xiaoyongsheng@perfee.com",
        customer_name="xiao", customer_kana="yongsheng", tel_no="0435235235",
        template_no=None, bcc_send_mail_address=None,
        from_send_mail_address=None, from_send_mail_name=None,
        client_field1="34324", client_field2=None, client_field3=None,
        overview=None, detail=None, pay_methods=["credit", "cvs"],
        ret_url=RET_URL, job_cd="CAPTURE", method="1", pay_times=None,
        td_flag="0", member_id=None, sec_code_required_flag="1", tds2_type="3",
        cvs_name=company_name, cvs_phone=contact_phone,
        cvs_interval=contact_interval)
    print(res.get("LinkUrl"))
    # res = query_refund_status(refund_ref_id="5f80174f8d440")
    # verify_ipn_notify(res_str)
    # res = query_order_status(order_id="10268", pay_type="3")
    # print res
