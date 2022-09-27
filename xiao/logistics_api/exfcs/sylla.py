#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json

region_api = "http://www.exfcs.com/sylla/api/country/list"
state_api = "http://www.exfcs.com/sylla/api/state/list"
city_api = "http://www.exfcs.com/sylla/api/city/list"
login_api = "http://www.exfcs.com/sylla/api/customer/login"
create_api = "http://www.exfcs.com/sylla/web/order/create"
order_count_api = "http://www.exfcs.com/sylla/web/myorder/count"
order_list_api = "http://www.exfcs.com/sylla/web/myorder/list"
order_detail_api = "http://www.exfcs.com/sylla/web/myorder/detail"
print_api = "http://www.exfcs.com/print/c/"
tracking_api = "http://www.exfcs.com/sylla/api/order/search"
# http://www.exfcs.com/print/c/{code}
UID = "PerFeeMM"
PWD = "PerFeeMM@2020"

COOKIE = "cust=t2cucL3bq2oLY/ar1EaT3BPgRaVVzx9Xa5pugEgIu+lM0TiavrIHAzOrmiB7q" \
         "ueWDOZ5eCCT3bCHy2/RiCvdVBuR+Gbh3ew8r0G6bBgmeDXhAE8hnXTi1Q2KaUmdlYvg" \
         "; path=/"


def get_regions():
    result = requests.get(region_api, headers={}, params={}).json()
    print(result)
    res = [
            {
                "id": 2,
                "country": "缅甸",
                "countryen": "Myanmar"
            }]


def get_states(country_id):
    param = {"country": country_id}
    result = requests.get(state_api, params=param).json()

    return result


def get_cities(state_id):
    param = {"state": state_id}
    result = requests.get(city_api, params=param).json()
    # print(result.get("data"))
    return result


def get_all_address():
    addresses = []
    for item in get_states(2).get("data"):
        city_li = []
        for it in get_cities(item["id"]).get("data"):
            city_li.append(
                {"city_id": it.get("id"), "city_name": it.get("cityen")})
        addresses.append(
            {"state_id": item.get("id"), "state_name": item.get("stateen"),
             "cities": city_li})
    print(addresses)


def get_token_login():
    body = {"uid": UID, "pwd": PWD}
    res = requests.post(login_api, params=body)

    return res.headers


def create_order(
        fruname, frcityid, fraddress, frmob, touname, tocityid, toaddress,
        tomob, itemdescs, itemweight, fremail=None, toemail=None,
        currencyid=1, insured=False, insuredprice=0, paytype=0, payment=1,
        cod=False, codamount=0, remark="PerFee Test"):
    headers = {"cookie": COOKIE}
    data = {
        "fruname": fruname,
        "frcityid": frcityid,
        "fraddress": fraddress,
        "frmob": frmob,
        "touname": touname,
        "tocityid": tocityid,
        "toaddress": toaddress,
        "tomob": tomob,
        "itemdescs": itemdescs,
        "itemweight": itemweight
    }
    if fremail:
        data["fremail"] = fremail
    if toemail:
        data["toemail"] = toemail
    if currencyid:
        data["currencyid"] = currencyid
    if type(insured) is bool:
        data["insured"] = insured
    if insuredprice:
        data["insuredprice"] = insuredprice
    if paytype:
        data["paytype"] = paytype
    if payment:
        data["payment"] = payment
    if type(cod) is bool:
        data["cod"] = cod
    if codamount:
        data["codamount"] = codamount
    if remark:
        data["remark"] = remark

    result = requests.post(create_api, headers=headers, params=data).json()
    return result
    """
    {
        "status": 0,
        "ts": 1598607585410,
        "data": {
            "id": 0,
            "code": "8a266433d649959af27c9653d665e76d",
            "sn": "FS570202244111MY",
            "rectp": 0,
            "status": 100,
            "issued": false,
            "custuid": "PerFeeMM",
            "custuno": "FC00572",
            "cdate": 1598607586433,
            "fraddr": "679d415d0d498d4330f79d810c719734",
            "fremail": "xiaoyongsheng@perfee.com",
            "fruname": "PerFee",
            "frcityid": 1,
            "frcityname": "瑞丽",
            "frcitynameen": "Ruili",
            "frstateid": 1,
            "frstatename": "云南省",
            "frstatenameen": "Yunnan Province",
            "frcountryid": 1,
            "frcountryname": "中国",
            "frcountrynameen": "China",
            "frcorp": "",
            "frmob": "18684799196",
            "fraddress": "Ruili",
            "toaddr": "af3bf72603a3f167865987510e45fe4f",
            "toemail": "xiaoyongsheng@perfee.com",
            "touname": "David",
            "tocityid": 68,
            "tocityname": "ရန်ကုန်မြို့",
            "tocitynameen": "Yangon City",
            "tostateid": 16,
            "tostatename": "ရန်ကုန်တိုင်း",
            "tostatenameen": "Yangon Region",
            "tocountryid": 2,
            "tocountryname": "缅甸",
            "tocountrynameen": "Myanmar",
            "tocorp": "",
            "tomob": "0943179788",
            "toaddress": "NO.131st street",
            "redirectcityid": 0,
            "redirectstateid": 0,
            "redirectcountryid": 0,
            "redirectfee": 0,
            "redirecttype": 0,
            "descr": "gift2",
            "qty": 0,
            "weight": 0.18,
            "length": 0,
            "width": 0,
            "height": 0,
            "pkg": false,
            "pkgdescs": "",
            "cod": false,
            "codamount": 0,
            "codfeerate": 0,
            "codfee": 0,
            "insured": false,
            "insuredprice": 0,
            "insuredfee": 0,
            "paytype": 0,
            "payment": 1,
            "remark": "PerFee Test, 请删除",
            "transfer": false,
            "transsn": "",
            "transcorp": "",
            "fee": 0,
            "currencyid": 1,
            "cuid": "",
            "cts": 1598607586433,
            "ets": 0,
            "luid": "",
            "lts": 1598607586433,
            "feediscount": 0,
            "pkgchangebox": false,
            "pkgchangeboxfee": 0,
            "pkgfirm": false,
            "pkgfirmfee": 0,
            "prservice": false,
            "prserviceamount": 0,
            "prservicefee": 0,
            "spot": false,
            "spotamount": 0,
            "spotfee": 0,
            "thirdfreight": false,
            "thirdfreightfee": 0,
            "thirdfreightservicefee": 0,
            "thirdcompanyid": 0,
            "countgoods": false,
            "countgoodsfee": 0,
            "photogoods": false,
            "photogoodsfee": 0,
            "smsnotice": false,
            "smsnoticefee": 0,
            "transferfee": 0,
            "transferservicefee": 0,
            "expedite": false,
            "expeditefee": 0,
            "transportbatchid": 0,
            "ologs": []
        }
    }
    """


def get_order_count():
    headers = {"cookie": COOKIE}
    param = {}
    result = requests.get(order_count_api, headers=headers, params=param)

    # {"status": 0, "ts": 1598594815882, "data": 2}
    return result.json()


def get_order_list(start, size, sn=None, touname=None):
    headers = {"cookie": COOKIE}
    param = {"start": start, "size": size}
    if sn:
        param["sn"] = sn
    if touname:
        param["touname"] = touname
    result = requests.get(order_list_api, headers=headers, params=param).json()
    return result
    """
        {
        "status": 0,
        "ts": 1598594885855,
        "data": [
            {
                "id": 418661,
                "code": "9ed0a4a8322c5b3e4efcbb98f13d66bb",
                "sn": "FS220203222494MY",
                "rectp": 0,
                "status": 100,
                "issued": false,
                "custuid": "PerFeeMM",
                "custuno": "FC00572",
                "cdate": 1597136045000,
                "fraddr": "999e877600f9fabd2421881bc5400751",
                "fremail": "xiaoyongsheng@perfee.com",
                "fruname": "PerFee",
                "frcityid": 1,
                "frcityname": "瑞丽",
                "frcitynameen": "Ruili",
                "frstateid": 1,
                "frstatename": "云南省",
                "frstatenameen": "Yunnan Province",
                "frcountryid": 1,
                "frcountryname": "中国",
                "frcountrynameen": "China",
                "frcorp": "",
                "frmob": "18684799196",
                "fraddress": "Ruili,",
                "toaddr": "17f928859fb5d9e840cd4db9d3d7b85c",
                "toemail": "xiaoyongsheng@perfee.com",
                "touname": "David",
                "tocityid": 68,
                "tocityname": "ရန်ကုန်မြို့",
                "tocitynameen": "Yangon City",
                "tostateid": 16,
                "tostatename": "ရန်ကုန်တိုင်း",
                "tostatenameen": "Yangon Region",
                "tocountryid": 2,
                "tocountryname": "缅甸",
                "tocountrynameen": "Myanmar",
                "tocorp": "",
                "tomob": "0943179788",
                "toaddress": "NO.131st street",
                "redirectcityid": 0,
                "redirectstateid": 0,
                "redirectcountryid": 0,
                "redirectfee": 0,
                "redirecttype": 0,
                "descr": "gift",
                "qty": 0,
                "weight": 0.18,
                "length": 0,
                "width": 0,
                "height": 0,
                "pkg": false,
                "pkgdescs": "",
                "cod": false,
                "codamount": 0,
                "codfeerate": 0,
                "codfee": 0,
                "insured": false,
                "insuredprice": 0,
                "insuredfee": 0,
                "paytype": 0,
                "payment": 1,
                "remark": "PerFee Test",
                "transfer": false,
                "transsn": "",
                "transcorp": "",
                "fee": 0,
                "currencyid": 1,
                "cuid": "",
                "cts": 1597136044632,
                "ets": 0,
                "luid": "",
                "lts": 1597136044632,
                "feediscount": 0,
                "pkgchangebox": false,
                "pkgchangeboxfee": 0,
                "pkgfirm": false,
                "pkgfirmfee": 0,
                "prservice": false,
                "prserviceamount": 0,
                "prservicefee": 0,
                "spot": false,
                "spotamount": 0,
                "spotfee": 0,
                "thirdfreight": false,
                "thirdfreightfee": 0,
                "thirdfreightservicefee": 0,
                "thirdcompanyid": 0,
                "countgoods": false,
                "countgoodsfee": 0,
                "photogoods": false,
                "photogoodsfee": 0,
                "smsnotice": false,
                "smsnoticefee": 0,
                "transferfee": 0,
                "transferservicefee": 0,
                "expedite": false,
                "expeditefee": 0,
                "transportbatchid": 0,
                "ologs": []
            }
        ]
    }
    """


def get_order_detail(code):
    headers = {"cookie": COOKIE}
    param = {"code": code}
    result = requests.get(
        order_detail_api, headers=headers, params=param).json()
    return result
    """
        {
        "status": 0,
        "ts": 1598595754897,
        "data": {
            "id": 404808,
            "code": "fa310085e63be6edb1b50924fc6e781f",
            "sn": "FC100373521MY",
            "rectp": 2,
            "status": 500,
            "issued": false,
            "custuid": "PerFeeMM",
            "custuno": "FC00572",
            "cdate": 1594969292000,
            "fraddr": "64950ef456863dcab4ea2ae74d8c3243",
            "fremail": "michel.wu@perfee.com",
            "fruname": "PerFee",
            "frcityid": 1,
            "frcityname": "瑞丽",
            "frcitynameen": "Ruili",
            "frstateid": 1,
            "frstatename": "云南省",
            "frstatenameen": "Yunnan Province",
            "frcountryid": 1,
            "frcountryname": "中国",
            "frcountrynameen": "China",
            "frcorp": "",
            "frmob": "18684799196",
            "fraddress": "Ruili,",
            "toaddr": "bb588abf44f070ebde362765dbdff8e8",
            "toemail": "",
            "touname": "U SAN MYINT AUNG",
            "tocityid": 68,
            "tocityname": "ရန်ကုန်မြို့",
            "tocitynameen": "Yangon City",
            "tostateid": 16,
            "tostatename": "ရန်ကုန်တိုင်း",
            "tostatenameen": "Yangon Region",
            "tocountryid": 2,
            "tocountryname": "缅甸",
            "tocountrynameen": "Myanmar",
            "tocorp": "",
            "tomob": "0943179788",
            "toaddress": "NO.13thuta 1st street ward 4 south okkalapa township",
            "redirectcityid": 0,
            "redirectstateid": 0,
            "redirectcountryid": 0,
            "redirectfee": 0,
            "redirecttype": 0,
            "descr": "口罩*1",
            "qty": 0,
            "weight": 0.18,
            "length": 0,
            "width": 0,
            "height": 0,
            "pkg": false,
            "pkgdescs": "",
            "cod": false,
            "codamount": 0,
            "codfeerate": 0,
            "codfee": 0,
            "insured": false,
            "insuredprice": 0,
            "insuredfee": 0,
            "paytype": 0,
            "payment": 1,
            "remark": "",
            "transfer": false,
            "transsn": "",
            "transcorp": "",
            "fee": 1500,
            "currencyid": 1,
            "frsite": "f9a652f7629fe83a467f7253903e77cc",
            "frsitename": "瑞丽公司",
            "frsitenameen": "Ruili Branch",
            "tosite": "03bfd96d32e502449d30474004d72739",
            "tositename": "49 Street Branch",
            "tositenameen": "49 Street Branch",
            "csite": "03bfd96d32e502449d30474004d72739",
            "csitename": "49 Street Branch",
            "csitenameen": "49 Street Branch",
            "nextsite": "03bfd96d32e502449d30474004d72739",
            "nextsitename": "49 Street Branch",
            "nextsitenameen": "49 Street Branch",
            "delivereruid": "thutaaung",
            "deliverername": "Thu Ta Aung 1",
            "deliverertel": "09696569809",
            "cuid": "李青青",
            "cts": 1594969291522,
            "ets": 0,
            "luid": "thutaaung",
            "lts": 1595381017738,
            "feediscount": 0,
            "pkgchangebox": false,
            "pkgchangeboxfee": 0,
            "pkgfirm": false,
            "pkgfirmfee": 0,
            "prservice": false,
            "prserviceamount": 0,
            "prservicefee": 0,
            "spot": false,
            "spotamount": 0,
            "spotfee": 0,
            "thirdfreight": false,
            "thirdfreightfee": 0,
            "thirdfreightservicefee": 0,
            "thirdcompanyid": 0,
            "countgoods": false,
            "countgoodsfee": 0,
            "photogoods": false,
            "photogoodsfee": 0,
            "smsnotice": false,
            "smsnoticefee": 0,
            "transferfee": 0,
            "transferservicefee": 0,
            "expedite": false,
            "expeditefee": 0,
            "transportbatchid": 10000018193,
            "ologs": [
                {
                    "id": 3750188,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 200,
                    "descs": "Arrived at Ruili Branch",
                    "frsite": "f9a652f7629fe83a467f7253903e77cc",
                    "frsitename": "瑞丽公司",
                    "frsitenameen": "Ruili Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "李青青",
                    "name": "李青青",
                    "ts": 1594969308452
                },
                {
                    "id": 3750191,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 215,
                    "descs": "Sorted, Next Location:  49 Street Branch ",
                    "frsite": "f9a652f7629fe83a467f7253903e77cc",
                    "frsitename": "瑞丽公司",
                    "frsitenameen": "Ruili Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "李青青",
                    "name": "李青青",
                    "ts": 1594969322616
                },
                {
                    "id": 3750192,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 220,
                    "descs": "Taken-out of Warehouse, to be Transported",
                    "frsite": "f9a652f7629fe83a467f7253903e77cc",
                    "frsitename": "瑞丽公司",
                    "frsitenameen": "Ruili Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "李青青",
                    "name": "李青青",
                    "ts": 1594969327883
                },
                {
                    "id": 3750193,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 300,
                    "descs": "Being Transported from Ruili Branch  to  49 Street Branch ",
                    "frsite": "f9a652f7629fe83a467f7253903e77cc",
                    "frsitename": "瑞丽公司",
                    "frsitenameen": "Ruili Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "李青青",
                    "name": "李青青",
                    "ts": 1594969348352
                },
                {
                    "id": 3762958,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 200,
                    "descs": "Arrived at 49 Street Branch",
                    "frsite": "03bfd96d32e502449d30474004d72739",
                    "frsitename": "49 Street Branch",
                    "frsitenameen": "49 Street Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "yelinaung",
                    "name": "Ye Lin Aung",
                    "ts": 1595223700291
                },
                {
                    "id": 3772038,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 215,
                    "descs": "Sorted, Will be Delivered",
                    "frsite": "03bfd96d32e502449d30474004d72739",
                    "frsitename": "49 Street Branch",
                    "frsitenameen": "49 Street Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "htaykhinemoe",
                    "name": "Htay Khine Moe",
                    "ts": 1595320632843
                },
                {
                    "id": 3772485,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 400,
                    "descs": "Out For Delivery, Deliverer: Thu Ta Aung 1(09696569809)",
                    "frsite": "03bfd96d32e502449d30474004d72739",
                    "frsitename": "49 Street Branch",
                    "frsitenameen": "49 Street Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "htaykhinemoe",
                    "name": "Htay Khine Moe",
                    "ts": 1595323947237
                },
                {
                    "id": 3774496,
                    "code": "fa310085e63be6edb1b50924fc6e781f",
                    "sn": "FC100373521MY",
                    "status": 500,
                    "descs": "Delivered, Consignee: u san nyint aung",
                    "frsite": "03bfd96d32e502449d30474004d72739",
                    "frsitename": "49 Street Branch",
                    "frsitenameen": "49 Street Branch",
                    "tosite": "03bfd96d32e502449d30474004d72739",
                    "tositename": "49 Street Branch",
                    "tositenameen": "49 Street Branch",
                    "uid": "thutaaung",
                    "name": "Thu Ta Aung 1",
                    "ts": 1595381017745
                }
            ]
        }
    }
    """


def print_code(code):
    param = {"code": code}
    result = requests.get(print_api, params=param)
    print(result.text)
    return result


def query_tracking(sn):
    param = {"sn": sn}
    result = requests.get(tracking_api, params=param).json()
    return result
    """
    {
        "status": 0,
        "ts": 1598682606406,
        "data": {
            "FC100373521MY": [
                {
                    "descs": "Arrived at Ruili Branch",
                    "ts": 1594969308452
                },
                {
                    "descs": "Sorted, Next Location:  49 Street Branch ",
                    "ts": 1594969322616
                },
                {
                    "descs": "Taken-out of Warehouse, to be Transported",
                    "ts": 1594969327883
                },
                {
                    "descs": "Being Transported from Ruili Branch  to  49 Street Branch ",
                    "ts": 1594969348352
                },
                {
                    "descs": "Arrived at 49 Street Branch",
                    "ts": 1595223700291
                },
                {
                    "descs": "Sorted, Will be Delivered",
                    "ts": 1595320632843
                },
                {
                    "descs": "Out For Delivery, Deliverer: Thu Ta Aung 1(09696569809)",
                    "ts": 1595323947237
                },
                {
                    "descs": "Delivered, Consignee: u san nyint aung",
                    "ts": 1595381017745
                }
            ]
        }
    }
    """


if __name__ == "__main__":
    # get_regions()
    # res = get_states(2)
    # res = get_cities(19)
    # res = get_all_address()

    # res = get_token_login()
    # COOKIE = res.get("Set-Cookie")
    # print(COOKIE)
    # print(res)

    # res = create_order(
    #     fruname="PerFee", frcityid=1, fraddress="Ruili", frmob="18684799196",
    #     touname="David", tocityid=68, toaddress="NO.131st street",
    #     tomob="0943179788", itemdescs="gift2", itemweight=0.18,
    #     fremail="xiaoyongsheng@perfee.com", toemail="xiaoyongsheng@perfee.com",
    #     currencyid=1, insured=False, insuredprice=0, paytype=0, payment=1,
    #     cod=False, codamount=0, remark="PerFee Test, 请删除")

    # res = get_order_count()

    # res = get_order_list(start=0, size=2, sn="FC100373521MY", touname=None)

    # res = get_order_detail(code="9ed0a4a8322c5b3e4efcbb98f13d66bb")

    res = query_tracking(sn="FS980222052971MY")

    # print_code(code="9ed0a4a8322c5b3e4efcbb98f13d66bb")

    print(json.dumps(res))

