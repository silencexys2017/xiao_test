#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import pickle
from zeep import Client
import os
import base64
import xmltodict
import hashlib

env = "sandbox"
API_KEY = "9eSx"
API_SECRET = "4Y1B4"
USER_ID = "F2901"
Content_type = "application/json"
place_order_url = "http://asp4.cj-soft.co.jp/SWebServiceComm/services/" \
                  "CommService/uploadData"
wsdl_url = "https://asp4.cj-soft.co.jp/SWebServiceComm/services/CommService?" \
           "wsdl"
inquiry_url = "https://tracking.sagawa-sgx.com/sgx/xmltrack.asp"
status_url = "https://tracking.sagawa-sgx.com/sgl/xmlstatuscode.asp"
print_label = "http://118.242.34.94:8240/SWebserviceRS/services/t/print"
print_label_url = "https://asp4.cj-soft.co.jp/SWebserviceRS/services/t/print"
print_call_back_url = "https://dnx-test.perfee.com/api/sagawa/label"
local_inquiry_api = "https://k2k.sagawa-exp.co.jp/cgi-api/xml.acgi"  # ?oku01=111111111112&key=99999&incode=EUC-JP&outcode=UTF-8
HEADERS = {
            "Content-Type": "text/xml",
            "SOAPAction": "http://ws.com",
            "charset": "utf-8"
        }

ship_xml = """
<?xml version="1.0" encoding="utf-8"?>

<DATA>
  <ADDRESS>
    <BOXID>test8989</BOXID>
    <SHIPDATE>2020/12/24</SHIPDATE>
    <KANA>xiao</KANA>
    <POSTAL>0600000</POSTAL>
    <JPADDRESS1>東京都品川区勝島１－１－１</JPADDRESS1>
    <JPADDRESS2>test2</JPADDRESS2>
    <CONTEL>0438432345</CONTEL>
    <KBN>TEST4286</KBN>
    <SHINADAI>4000</SHINADAI>
    <TTLAMOUNT>4500</TTLAMOUNT>
    <TESURYO>500</TESURYO>
    <CODFLG>1</CODFLG>
    <WGT>2</WGT>
    <SHITEIBI>2020/12/26</SHITEIBI>
    <SHITEIJIKAN>1200</SHITEIJIKAN>
    <TRACKINGNO>test0000001</TRACKINGNO>
    <BIKO>test</BIKO>
  </ADDRESS>
  <ITEM>
    <ITEMCD>432532532</ITEMCD>
    <ITEMNAME>test xiao</ITEMNAME>
    <PIECE>2</PIECE>
    <ORIGIN>JP</ORIGIN>
    <UNITPRICE>1000</UNITPRICE>
  </ITEM>
  <ITEM>
    <ITEMCD>432532542</ITEMCD>
    <ITEMNAME>test 222</ITEMNAME>
    <PIECE>2</PIECE>
    <ORIGIN>JP</ORIGIN>
    <UNITPRICE>1000</UNITPRICE>
  </ITEM>
</DATA>
"""


def json_to_xml(json_str):
    xml_str = ""
    xml_str = xmltodict.unparse(json_str, encoding='utf-8')
    return xml_str
    # except Exception:
    #     xml_str = xmltodict.unparse({'request': json_str}, encoding='utf-8')
    # finally:
    #     return xml_str


def place_order(
        reference_no, ship_date, consignee_kana_1, consignee_postal_code,
        address_1, address_2, phone_number, control_code, item_total,
        total_amount, cod_charge, cod_flg, sku_items, weight=None,
        appointed_delivery_date=None, appoint_time_period=None,
        tracking_no=None, remark=None, freight=None):
    address = {
        "BOXID": reference_no,
        "SHIPDATE": ship_date,
        "KANA": consignee_kana_1,
        "POSTAL": consignee_postal_code,
        "JPADDRESS1": address_1,
        "JPADDRESS2": address_2,
        "CONTEL": phone_number,
        "KBN": control_code,
        "SHINADAI": item_total,
        "TTLAMOUNT": total_amount,
        "TESURYO": cod_charge,
        "CODFLG": cod_flg
    }
    if weight:
        address["WGT"] = weight
    if appointed_delivery_date:
        address["SHITEIBI"] = appointed_delivery_date
    if appoint_time_period:
        address["SHITEIJIKAN"] = appoint_time_period
    if tracking_no:
        address["TRACKINGNO"] = tracking_no
    if freight:
        address["SOURYO"] = freight
    if remark:
        address["BIKO"] = remark
    items = []
    for it in sku_items:
        items.append(
            {"ITEMCD": it["skuId"], "ITEMNAME": it["skuName"],
             "PIECE": it["count"], "ORIGIN": it["countryOrigin"],
             "UNITPRICE": it["price"]})
    data = {"DATA": {"ADDRESS": address, "ITEM": items}}
    ship_xml = json_to_xml(data)
    print(ship_xml)
    client = Client(wsdl_url)
    result = client.service.uploadData(handler=ship_xml)
    print(result)
    if result[:2] == "ok" and "|" in result:
        res_li = result[3:].split("|")
        res = {
            "status": res_li[0], "refNo": res_li[1], "routingCode1": res_li[3],
            "routingBarCode": res_li[2], "routingCode2": res_li[4],
            "trackingBarCode": res_li[5], "trackingNumber": res_li[6],
            "codYesNo": res_li[7]}
    else:
        res = {"code": 0, "errorInfo": result}
    print(result)
    return res

    """ok:38489291|TEST11|C7016404D|7016|404|Atest0000001A|test-0000-001|0"""


def parcel_tracking(declaration=None, ref=None, sagawa=None):
    body = {}
    if declaration:
        body["AWB"] = declaration
    if ref or sagawa:
        body["REF"] = ref or sagawa

    result = requests.get(inquiry_url, params=body, headers=HEADERS).text
    print(result)
    result = json.dumps(xmltodict.parse(result))

    return result
    """
    """


def local_parcel_tracking(ref=None, sagawa=None):
    body = {
        "oku01": ref,
        "key": "00044",
        "incode": "EUC-JP",
        "outcode": "UTF-8"
    }

    result = requests.get(local_inquiry_api, params=body, headers=HEADERS).text
    print(result)
    result = json.dumps(xmltodict.parse(result))
    print(result)


def get_and_match_address_zipcode(zipcode=None, addr=None):
    client = Client(wsdl_url)
    res = client.service.getAddr(zipcode=zipcode, addr=addr)
    res_li = res.split("|")
    error_info = ""
    code = 0
    if res_li[2] == "0":
        code = 0
    elif res_li[2] == "2":
        error_info = "Address does not exist."
        code = 1
    elif res_li[2] == "1":
        error_info = "Either zip code or address is incorrect."
        code = 1
    return {"errorInfo": error_info, "code": code, "zipCode": res_li[0],
            "address": res_li[1]}


def get_order_info(control_cd, tracking_no, reference):
    client = Client(wsdl_url)
    res = client.service.getOrdInfo(
        controlcd=control_cd, trackingno=tracking_no, reference=reference)
    print(res)
    return res


def get_match_track_info():  # Shift_JIS
    response = requests.get(status_url, headers=HEADERS)
    print(response.headers)
    print(response.encoding)
    response.encoding = 'cp932'
    result = response.text
    print(result)
    result = xmltodict.parse(result)
    status_code = {}
    for it in result["DATA"]["TRACK"]:
        status_code[it["STATUS"]] = {
            "en": it["ENGLISH"], "jp": it["JAPANESE"]}
    print(json.loads(json.dumps(status_code)))
    with open("status_code_map.json", "w") as f:
        json.dump(status_code, f)
    print(status_code)

    return result


def get_xml_to_dict():
    xml_test = """
    <TRACK>
        <INFO>
            <AWB>1234567890</AWB>
            <ORIGIN>PVG</ORIGIN>
            <DEST>HND</DEST>
            <LCLDATE>20150711</LCLDATE>
            <LCLTIME>1642</LCLTIME>
            <STATUS>TA</STATUS>
            <DETAIL>ARRIVED AT TRANSIT POINT</DETAIL>
            <COUNTRY>SHANGHAI, CHINA</COUNTRY>
            <SVC>EX</SVC>
            <LINKURL/>
            <LCLNBR/>
        </INFO>
        <INFO>
            <AWB>1234567890</AWB>
            <REF>567856785678</REF>
            <ORIGIN>PVG</ORIGIN>
            <DEST>HND</DEST>
            <LCLDATE>20150712</LCLDATE>
            <LCLTIME>0540</LCLTIME>
            <STATUS>OB</STATUS>
            <DETAIL>SSSHANJIN000</DETAIL>
            <COUNTRY>SHANGHAI, CHINA</COUNTRY>
            <SVC>EX</SVC>
            <LINKURL/>
            <LCLNBR/>
        </INFO>
        <LCLINFO>
            <AWB></AWB>
            <REF></REF>
            <ORIGIN></ORIGIN>
            <DEST></DEST>
            <LCLDATE></LCLDATE>
            <LCLTIME></LCLTIME>
            <STATUS></STATUS>
            <DETAIL></DETAIL>
            <COUNTRY>JAPAN</COUNTRY>
            <SVC></SVC>
            <LINKURL></LINKURL>
            <LCLNBR></LCLNBR>
        </LCLINFO>
    </TRACK>
    """
    res = json.dumps(xmltodict.parse(xml_test))
    print(res)


def md5(str):
    m = hashlib.md5()
    m.update(str.encode("utf8"))
    return m.hexdigest()


def print_label(order_keys, sch_type="1"):
    order = {
        "schtype": sch_type,  # 1.HAWB#，2.REF#，3.运单号
        "orderkey": order_keys
    }
    print(order)
    order_base = base64.b64encode(json.dumps(order).encode("utf-8")).decode(
        "utf-8")
    print(order_base)
    sign = md5("TEST4286" + json.dumps(order) + print_call_back_url)
    print(sign)
    data = {
        "compcd": "TEST4286",
        "orderData": order_base,
        "callbackUrl": print_call_back_url,
        "sign": sign
    }

    result = requests.post(print_label_url, data=data).json()
    print(result)
    return result


def hua_wei_obs_link():
    url = "https://seller-export-dev.obs.ap-southeast-3.myhuaweicloud.com/" \
          "monthly-clearing-dnx/5d92e708-5a2e-11eb-bcb8-02550a0a00ae.xlsx"
    result = requests.get(url)
    print(result.status_code)


if __name__ == "__main__":
    sku_items = [
        {"skuId": "90000000891", "skuName": "マスク 不織布 カラー 50枚 +1枚 13色 "
                                            "新色入荷 大人用マスク 不織布マスク カラーマスク ピンク ハニー グレー 家庭用 花粉 風邪 ウィルス ホコリ 3層フィルター マスク",
         "countryOrigin": "JP",
         "count": "2", "price": "478"}
    ]
    # TEST4286
    address_1 = "埼玉県" + "北足立郡伊奈町" + "大針"
    control_code = "TEST4286"
    # control_code = "4286"
    # control_code = "00044"
    res = place_order(
        reference_no="F12021040100009", ship_date="2021/04/29",
        consignee_kana_1="齋藤 博美",
        consignee_postal_code="3620803", address_1=address_1,
        address_2="429", phone_number="09084601386",
        control_code=control_code,  item_total="956", total_amount="1551",
        cod_charge="0", cod_flg="0", sku_items=sku_items, weight="0.5",
        appointed_delivery_date="", appoint_time_period="", tracking_no="",
        remark="soId: 230, shipPackageCode: F120210407000001")
    # res = get_and_match_address_zipcode(zipcode="1400002", addr="")
    # ECR36145394240920
    # res = parcel_tracking(declaration="", ref="352423965003", sagawa="")
    # local_parcel_tracking(ref="359725232020")
    # res = get_packages()
    # res = get_order_info(
    #     control_cd="TEST4286", tracking_no="358438213416", reference="")
    # res = cancel_order("ECR68099762291020", "make a mistake")
    # res = get_match_track_info()
    # get_xml_to_dict() "200002467840" 200002467733
    # res = print_label(['200002470360'], sch_type="1")
    # hua_wei_obs_link()

    # print(res)

