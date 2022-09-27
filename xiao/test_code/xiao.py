import json
from math import ceil
from decimal import Decimal, ROUND_UP
from functools import wraps
import hashlib


def currency_converter(
        amount, exchange_rate=1, currency_code="USD"):
    original_amount = Decimal(str(exchange_rate)) * Decimal(str(amount))
    if currency_code in ["USD"]:
        return float(original_amount.quantize(Decimal('0.00'), ROUND_UP))
        # return float("%.2f" % float(ceil(float(original_amount * 100))/100))
    return ceil(float(original_amount))


def multiplication_operation(number_1, number_2):
    return float(Decimal(str(number_1)) * Decimal(str(number_2)))


def division_operation(dividend, divisor):
    return float(Decimal(str(dividend))/Decimal(str(divisor)))


def _ratio_split_integer(split_num, each_ratio):
    # each_ratio: for example {1: float(1) / 5, 2: float(2) / 5}
    split_list = [int(round(float(item) * split_num)) for item in
                  each_ratio.values()]
    amount = sum(split_list)
    rest_num = abs(split_num - amount)
    index = 0
    number = 0
    if split_num < amount:
        for num in split_list:
            if num == 0:
                index += 1
                continue
            num = num - 1
            split_list[index] = num
            index += 1
            number += 1
            if number == rest_num:
                break
    elif split_num > amount:
        for num in split_list:
            num = num + 1
            split_list[index] = num
            index += 1
            if index == rest_num:
                break
    return dict(zip(each_ratio.keys(), split_list))


def _get_postage_info(grouped_sku_dict, address):
    group_postage = {}
    if not address or not address.id:
        for key, skus in grouped_sku_dict.items():
            group_postage[key] = 0
            for sku in skus:
                sku.postage = 0
        return grouped_sku_dict


def hmac_hashlib():
    import hmac
    import hashlib
    import json
    from urllib.parse import urlencode

    params = {'event': 'charge.success',
              'data': {'id': 1624123033, 'domain': 'test', 'status': 'success',
                       'reference': '840', 'amount': 785, 'message': None,
                       'gateway_response': 'Successful',
                       'paid_at': '2022-02-15T02:39:22.000Z',
                       'created_at': '2022-02-15T02:39:09.000Z',
                       'channel': 'card', 'currency': 'NGN',
                       'ip_address': '175.9.141.245', 'metadata': '',
                       'log': {'start_time': 1644892754, 'time_spent': 8,
                               'attempts': 1, 'errors': 0, 'success': False,
                               'mobile': False, 'input': [], 'history': [
                               {'type': 'action',
                                'message': 'Attempted to pay with card',
                                'time': 8}]}, 'fees': 12, 'fees_split': None,
                       'authorization': {
                           'authorization_code': 'AUTH_tpiscsmsu5',
                           'bin': '408408', 'last4': '4081', 'exp_month': '12',
                           'exp_year': '2030', 'channel': 'card',
                           'card_type': 'visa ', 'bank': 'TEST BANK',
                           'country_code': 'NG', 'brand': 'visa',
                           'reusable': True,
                           'signature': 'SIG_Zt450J9ivGcysI46uimj',
                           'account_name': None},
                       'customer': {'id': 69698862, 'first_name': None,
                                    'last_name': None,
                                    'email': '3078639052@qq.com',
                                    'customer_code': 'CUS_ymzfgcl0tdnr20n',
                                    'phone': None, 'metadata': None,
                                    'risk_action': 'default',
                                    'international_format_phone': None},
                       'plan': {}, 'subaccount': {}, 'split': {},
                       'order_id': None, 'paidAt': '2022-02-15T02:39:22.000Z',
                       'requested_amount': 785, 'pos_transaction_data': None,
                       'source': {'source': 'merchant_api', 'identifier': None,
                                  'event_type': 'api'}, 'fees_breakdown': None},
              'order': None, 'business_name': 'xiao test'}
    del params['event']
    param_b = urlencode(params).encode('utf-8')
    # param_b = json.dumps(params).encode(encoding="utf-8")
    # param_b = str(params).encode("utf-8")
    # params = params.encode('utf-8')
    secret_key = "sk_test_db2e6d4e2ecdabfda816787fff97ad7f8b89387c"
    public_key = "pk_test_1128700716ae14243c0b56ca08be1edfce8aff67"
    res = hmac.new(secret_key.encode(encoding="utf-8"),
                   param_b, hashlib.sha512).hexdigest()


def deduction_value_currency_converter(
        deduction_value, before_exchange_rate, later_exchange_rate,
        currency_code):
    if not isinstance(deduction_value, (int, float, str)):
        return 0
    original_postage = Decimal(str(deduction_value)) / Decimal(
        str(before_exchange_rate)) * Decimal(str(later_exchange_rate))
    if currency_code in ["USD"]:
        return float(original_postage.quantize(Decimal('0.0'), ROUND_UP))
    print(original_postage)
    print(ceil(float(original_postage)))
    return (original_postage / 10).quantize(Decimal('0'), ROUND_UP) * 10


def retry_tool():
    def func_wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retry_times, result, exp = 0, {}, None
            while retry_times < 3:
                try:
                    result = func(*args, **kwargs)
                    break
                except Exception as exp:
                    retry_times += 1
            if retry_times == 3:
                print(kwargs["msg_body"])
            print(kwargs)
            return result
        return wrapper
    return func_wrapper


@retry_tool()
def ki_li_api_address_update(data, msg_body=None):
    print(data, msg_body)


if __name__ == "__main__":
    # res = currency_converter(0.54347824 * 92)
    # print(res)
    # sku_item = {8000: 34}
    # sku_postage = _ratio_split_integer(
    #     multiplication_operation(res, 100),
    #     {it: float(1) / len(sku_item) for it in sku_item.keys()})
    # print(sku_postage)
    # postage = division_operation(sku_postage.get(8000), 100)
    # print(postage)
    # res = deduction_value_currency_converter(11314, 92, 92, "BDT")
    # res = ki_li_api_address_update(4343, msg_body=343434)
    params = [{
        "networkBaseInfoVo": {
            "address":"Street one",
            "areaCode":"112548",
            "areaId":2003,
            "areaName":None,
            "businessName":"LIUYY",
            "businessTime": "12",
            "businessType": 2,
            "cityId": None,
            "cityName": None,
            "countryCode": "KE",
            "createdAt": 1645090138,
            "id": 718864910,
            "isSupportBigPackage": None,
            "latitude": 0.0,
            "longitude": 0.0,
            "parentId": 173,
            "pauseEndTime": 1627747200,
            "pauseStartTime": 1627747200,
            "pickingCode": "173-1",
            "remark": None,
            "stationCode": "301LiuYY",
            "stationDesc": "wqwq123",
            "stationDescRid": None,
            "stationLevel": "1",
            "stationName": "LiuYY",
            "stationNameRid": None,
            "stationScore": 1,
            "stationSize": "",
            "stationSubType": None,
            "stationType": 2,
            "status": 1,
            "supplierId": None,
            "updatedAt": 1655778676
        },
        "networkCoverageVoList": None,
        "networkStaffInfoVoList": [{
            "address": "湖南长沙岳麓区",
            "age": None,
            "createdAt": 1645090327,
            "email": "154878@qq.com",
            "firstName": "LIU",
            "gender": "0",
            "id": 42615,
            "identifyNo": "4305548755457878",
            "identifyType": 1,
            "lastName":"YY",
            "mobileNo":"13677395687",
            "parentId": None,
            "positionId": None,
            "stationId": 718864910,
            "status": None,
            "telephoneNo": "07310823548"
        }]
    }]
    params = [{"networkBaseInfoVo": {"address": "Joy 622 address over.  120001.0001   6210000003", "areaCode": "100109", "areaId": 304, "areaName": "Karen01011029", "businessName": None, "businessTime": "Mon-Fri\n09:00-18:00;Sat09:00-15:00", "businessType": 3, "cityId": 1, "cityName": "Nairobi_1", "countryCode": "KE", "createdAt": 1583387399, "id": 1000149, "isSupportBigPackage": None, "latitude": -0.1044620, "longitude": 34.7528711, "parentId": 304, "pauseEndTime": 1609027200, "pauseStartTime": 1608456058, "pickingCode": "3-402", "remark": "http://k.kili.co/rj9r", "stationCode": "3-402", "stationDesc": " AL IMRAN PLAZA 1st Floor Oginga Odinga street Kisumu222221  111", "stationDescRid": None, "stationLevel": "1", "stationName": "Joy 622-1120", "stationNameRid": None, "stationScore": None, "stationSize": "9", "stationSubType": None, "stationType": 2, "status": 1, "supplierId": None, "updatedAt": 1655798225}, "networkCoverageVoList": [{"areaCode": "100109", "areaName": "Karen01011029", "createdAt": 1655797149, "id": 5926, "remark": None, "stationId": 1000149, "status": 0, "updatedAt": 1655797149}], "networkStaffInfoVoList": [{"address": "", "age": None, "createdAt": 1637373885, "email": "", "firstName": "Joy", "gender": "1", "id": 42614, "identifyNo": "", "identifyType": None, "lastName": "1", "mobileNo": "13412341234", "parentId": None, "positionId": None, "stationId": 1000149, "status": None, "telephoneNo": ""}]}]
    params = json.dumps(params, separators=(',', ':'), ensure_ascii=False)
    print(params)
    sign_1 = hashlib.md5((params+"12345678").encode(
        encoding='utf-8')).hexdigest()
    print(sign_1)
    sign_2 = hashlib.md5((json.dumps(params) + "Ih55t85cdMz7iXWiGLhv1X1i5YjX0srp").encode(
        encoding='utf-8')).hexdigest()
    "b114826ade26fde648f47daf3ac6f06b"
    print("3c063786e09fcb4376c9328f3ddf1f81", "a46860a6929c57b6a2185749514fefb0")

    print(sign_2)

