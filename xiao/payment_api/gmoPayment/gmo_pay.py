#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import hashlib
import json
import base64
# import html
# from urllib.parse import unquote
from datetime import datetime

login_store_id = "ADMINISTRATOR"
login_store_password = "otoku2020?"
store_id = "tshop00047500"
store_name = "OTOKU WORLD Co.，Ltd."
store_pd = "z3gxd5ft"
site_id = "tsite00041368"
site_pd = "2xzq35wr"

RET_URL = "https://api-dev.perfee.com/partner/pay/gmo/payment-callback?billId=%d"
CANCEL_URL = "https://api-dev.perfee.com/partner/pay/gmo/callback?billId=%d"

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
    headers = {
        "Content-Type": "application/json", "charset": "UTF-8"
    }

    res = requests.post(url=url, headers=headers, params=args, timeout=30)
    print(res)
    f = open(GEN_HTML, 'w')
    f.write(res.text)
    f.close()
    # print(html.unescape(res))

    return res


def get_md5_value(str):
    my_md5 = hashlib.md5()
    my_md5.update(str.encode("utf8"))
    print(my_md5.hexdigest())
    return my_md5.hexdigest()


def pre_create(order_id, amount, tax, currency="JPY", member_id=None):
    utc_now = datetime.strftime(datetime.utcnow(), '%Y%m%d%H%M%S')
    data = {
        "ShopID": store_id,
        "OrderID": order_id,  # str
        "DateTime": utc_now,  # 格式: yyyyMMddhhmmss
        "RetURL": RET_URL,  # 付款完成结果发送到的会员商店的URL
        "CancelURL": CANCEL_URL,  # 取消付款时的网址
    }
    add_fields = {
        "Amount": amount,  # 请设置1日元或更多。 对于非日元付款，请设置为0.01或更高。 每种货币和每种付款方式的上限都不同
        "Tax": tax,  # “使用金额+税金运费”是总付款金额, 包括小数点的位数（至第二位）
        "Currency": currency,  # 默认: JPY
        "UserInfo": "pc",  # i：i-mode端末, e：EzWeb端末, sb：Softbank端末, pc：PC(默认)
        "RetryMax": 5,  # max: 5
        "SessionTimeout": 300,  # 这是从显示付款屏幕到进行付款所经过的时间的上限，当设置单位缩写为秒时，不会检查经过的时间。
        "Enc": "utf-8",  # 默认sjis
        "Lang": "en",  # 默认ja
        "Confirm": "0",  # 0：不显示1：显示, 默认0
        "TemplateNo": 1,  # 默认为1，一次链接付款仅可申请一个号码。 对于某笔交易，无法将付款页面用作数字1，将收据页面用作数字3。
        "ClientField1": "001"
    }
    credit_add = {
        "JobCd": "CHECK",  # CHECK：有效性检查, CAPTURE：立即销售, AUTH：临时销售
        "ItemCode": "0000990",  # 如果在卡付款中省略了产品代码，则将应用“ 0000990” *通常，将其忽略。 仅在与卡公司签订的合同中确定要使用的产品代码时，才进行设置。
    }
    pay_method = {
        "UseCredit": "1",  # 信用卡
        "UseCvs": "0",  # 便利付款
        "UseEdy": "0",  # 乐天Edy
        "UseSuica": "0",  # Suica移动支付
        "UsePayEasy": "0",  # Pay-easy
        "UsePayPal": "0",
        "UseAu": "0"
    }
    data.update(add_fields)
    data.update(credit_add)
    data.update(pay_method)
    goal_str = store_id + "|" + order_id + "|" + str(amount) + "|"
    if tax:
        goal_str += str(tax)
    goal_str += "|"
    currency_pay_method = ["UseMcp", "UsePayPal"]
    member_pay_method = ["UseCredit", "UseAu"]
    if currency:
        if pay_method.get("UsePayPal") or pay_method.get("UseMcp"):
            goal_str += (currency+"|")
    goal_str = goal_str + store_pd + "|" + utc_now
    data["ShopPassString"] = get_md5_value(goal_str)
    if pay_method.get("UseCredit") or pay_method.get("UseAu"):
        member_add = {
            "SiteID": site_id,  # 站点ID *会员ID付款所必需
            "MemberID": member_id,  # 会员编号*需要会员编号付款。
            "MemberPassString": None,  # 检查会员信息的字符串*会员ID支付必填
        }
        member_str = site_id+"|"+str(member_id)+"|"+site_pd+"|"+utc_now
        member_add["MemberPassString"] = get_md5_value(member_str)
        data.update(member_add)

    return request_post_api(DOMAIN_URL+PRE_CREATE_URL, data)


def reset_test():
    checking_dict = {
        "optionalPayGateways": [4, 5, 6],
        "defaultPayGateway": 4,
        "amount": 1000,
        "tax": 0,
        "billId": 1,
        "creditCard": {},
        "cvs": {
            "convenience": ["", ""],
            "customerName": "xiao",
            "customerKana": "永胜",
            "telNo": "01454353535"
        },
        "payPay": {}
    }
    param = {"transactionresult": {"AccessID": None, "AccessPass": None,
                           "OrderID": "4685", "Result": "PAYSTART",
                           "Processdate": "2021/04/05 12:23:09",
                           "ErrCode": None, "ErrInfo": None, "Paymethod": None}}
    param = json.dumps(param)
    b = base64.encodestring(param.encode("utf-8"))
    print(b)
    c = base64.decodestring(b)
    get_md5_value(b)


def base_64_test():
    goal_str = "eyJ0cmFuc2FjdGlvbnJlc3VsdCI6eyJBY2Nlc3NJRCI6ImFkYTJmNGU1ZDAzMmU4ZWI5OGE3M2Y1ZDQ4NjM5OGRjIiwiQWNjZXNzUGFzcyI6IjI1YThmZjlmMzZlNWFlNWQ5NDU3MmFlNjE2OWNhNTBkIiwiT3JkZXJJRCI6IjQ2ODUiLCJSZXN1bHQiOiJQQVlTVUNDRVNTIiwiUHJvY2Vzc2RhdGUiOiIyMDIxLzA0LzA1IDE2OjIyOjMyIiwiRXJyQ29kZSI6bnVsbCwiRXJySW5mbyI6bnVsbCwiUGF5bWV0aG9kIjoiY3JlZGl0In0sImNyZWRpdCI6eyJTdGF0dXMiOiJDQVBUVVJFIiwiRm9yd2FyZCI6IjJhOTk2NjIiLCJNZXRob2QiOiIxIiwiUGF5VGltZXMiOm51bGwsIlRyYW5JRCI6IjIxMDQwNTE2MDQxMTExMTExMTExMTE4MDY0NzUiLCJBcHByb3ZlIjoiMDcwNDkwOSIsIlRyYW5EYXRlIjoiMjAyMTA0MDUxNjIyMzMifX0=.2433e7ebc773e96a74daeb630d0aef14da524c6749fef952fc9357388e925a4f"
    goal_str = goal_str.split(".")[0]
    goal_str = base64.decodestring(goal_str.encode("utf-8"))
    print (json.loads(goal_str))


def get_base_64_decode(url):
    goal_str = ""
    for item in url.split("&"):
        if "params=" in item:
            goal_str = item[7:]
    print goal_str
    goal_str = base64.decodestring(goal_str.encode("utf-8"))
    a = json.loads(goal_str)
    print(a)


def get_gmo_cvs_result(bill_id, params):
    param = {
        "convenience": {
            "id": params.get("convenience"),
            "value": "DEF_PAY.GMO_CVS_MAP.get(params))"},
        "confNo": params.get("confNo"),
        "receiptNo": params.get("receiptNo"),
        "paymentTerm": params.get("paymentTerm"),
        "tranDate": params.get("tranDate"),
        "barCodeUrl": "GMO_BAR_CODE_URL%s%s" % (
            params.get("confNo"), params.get("receiptNo"))
    }
    base64_str = base64.encodestring(json.dumps(param).encode("utf-8"))
    return "https://m-test.otoku-world.com/payment/gmo/result?billId=%s" % \
           bill_id + "&params=%s" % base64_str


def test_update_dict():
    result = {"xiao": 234}
    res = {"code": 0, "data": {}}
    return res["data"].update(result)


if __name__ == "__main__":
    # res = pre_create(order_id="test001", amount=100, tax=10)
    # res = query_refund_status(refund_ref_id="5f80174f8d440")
    # verify_ipn_notify(res_str)
    # reset_test()
    # base_64_test()
    params = {
                "orderID": "186",
                "confNo": "12345",
                "tranDate": "20210510115352",
                "accessID": "9466ad0d205677dc771093910ed0f6b5",
                "checkString": "c97e8076f2df2ce8cd883248000c00a6",
                "convenience": "10002",
                "receiptNo": "FM0615232205",
                "accessPass": "a7edcb685be85e983dd1f250b55941a3",
                "paymentTerm": "20210513235959"
        }
    # res = get_gmo_cvs_result(bill_id=110, params=params)
    # print res
    # get_base_64_decode(res)
    print test_update_dict()

    # print(res)



