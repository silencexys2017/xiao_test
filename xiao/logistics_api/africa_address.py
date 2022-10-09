# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from speedaf.speedaf_api import get_area_tree

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = '../../config.json'
# REGION_CODES = ["GH", "UG", "KE", "NG", "MA", "EG"]
REGION_CODES = ["NG", "KE", "UG"]

MAP_REGION_XED = {
    "NG": {
            "_id": 7,
            "callingCode": "234",
            "code": "NG",
            "name": "Nigeria",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/NG.png",
            "currency": "NGN",
            "currencyId": 566,
            "currencySymbol": "₦",
            "currencyConversion": 418.09,
            "language": "en",
            "timeZone": "Africa/Lagos",
            "index": 10
        },
    "GH": {
            "_id": 8,
            "callingCode": "233",
            "code": "GH",
            "name": "Ghana",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/GH.png",
            "currency": "GHS",
            "currencyId": 936,
            "currencySymbol": "GH₵",
            "currencyConversion": 6.42,
            "language": "en",
            "timeZone": "Africa/Accra",
            "index": 7
        },
    "UG": {
            "_id": 9,
            "callingCode": "256",
            "code": "UG",
            "name": "Uganda",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/UG.png",
            "currency": "UGS",
            "currencyId": 800,
            "currencySymbol": "USh",
            "currencyConversion": 3541.20,
            "language": "en",
            "timeZone": "Africa/Kampala",
            "index": 8
        },
    "KE": {
            "_id": 10,
            "callingCode": "254",
            "code": "KE",
            "name": "Kenya",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/KE.png",
            "currency": "KES",
            "currencyId": 404,
            "currencySymbol": "KSh",
            "currencyConversion": 113.60,
            "language": "en",
            "timeZone": "Africa/Nairobi",
            "index": 9
        },
    "MA": {
            "_id": 11,
            "callingCode": "212",
            "code": "MA",
            "name": "Morocco",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/MA.png",
            "currency": "MAD",
            "currencyId": 504,
            "currencySymbol": "DH.",
            "currencyConversion": 9.27,
            "language": "ar",
            "timeZone": "Africa/Casablanca",
            "index": 11
        },
    "EG": {
            "_id": 12,
            "callingCode": "20",
            "code": "EG",
            "name": "Egypt",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/EG.png",
            "currency": "EGP",
            "currencyId": 818,
            "currencySymbol": "LF.",
            "currencyConversion": 15.71,
            "language": "ar",
            "timeZone": "Africa/Cairo",
            "index": 12
        }
}

MAP_REGION_POSTAGE = {
    "NG": {
                "_id": 3,
                "regionCode": "NG",
                "regionZh": "尼日利亚",
                "status": True,
                "postage": 100,
                "regionEn": "Nigeria",
                "isDiscountPostage": False,
                "localDeliveryDays": "2-5",
                "minOrderAmount": 1000,
                "transnationalDeliveryDays": "5-20"
            },
    "KE": {
                "_id": 4,
                "regionCode": "KE",
                "regionZh": "肯尼亚",
                "status": True,
                "postage": 100,
                "regionEn": "Kenya",
                "isDiscountPostage": False,
                "localDeliveryDays": "2-5",
                "minOrderAmount": 1000,
                "transnationalDeliveryDays": "5-20"
            },
    "UG": {
                "_id": 5,
                "regionCode": "UG",
                "regionZh": "乌干达",
                "status": True,
                "postage": 100,
                "regionEn": "Uganda",
                "isDiscountPostage": False,
                "localDeliveryDays": "2-5",
                "minOrderAmount": 1000,
                "transnationalDeliveryDays": "5-20"
            }
}

MAP_REGION_UO = {
    "NG": {
            "code": "NG", "callingCode": "234", "name": "Nigeria",
            "intro": "A great country", "flag": "NG.png", "currency": "NGN",
            "currencyId": "566", "currencySymbol": "₦",
            "currencyConversion": 1, "language": "en",
            "timeZone": "Africa/Lagos", "timeZoneUTC": 1, "index": 6,
            "minAppVersion": 1, "userAddressInteractionMethod": 1,
            "enabled": True},
    "KE": {
            "code": "KE", "callingCode": "254", "name": "Kenya",
            "intro": "A great country", "flag": "KE.png", "currency": "KES",
            "currencyId": "404", "currencySymbol": "KSh",
            "currencyConversion": 1, "language": "en",
            "timeZone": "Africa/Nairobi", "timeZoneUTC": 3, "index": 6,
            "minAppVersion": 1, "userAddressInteractionMethod": 1,
            "enabled": True},
    "UG": {
            "code": "UG", "callingCode": "256", "name": "Uganda",
            "intro": "A great country", "flag": "UG.png", "currency": "UGS",
            "currencyId": "800", "currencySymbol": "USh",
            "currencyConversion": 1, "language": "en",
            "timeZone": "Africa/Kampala", "timeZoneUTC": 3, "index": 6,
            "minAppVersion": 1, "userAddressInteractionMethod": 1,
            "enabled": True},
}

MAP_CURRENCY = {
    "NG": {
            "code": "NGN", "currencyId": "566", "currencySymbol": "₦",
            "currencyConversion": 1, "isBase": False,
            "exchangeRateToBase": 418.09, "reservedDigits": 0, "index": 6,
            "enabled": False},
    "KE": {
            "code": "KES", "currencyId": "404", "currencySymbol": "KSh",
            "currencyConversion": 1, "isBase": False,
            "exchangeRateToBase": 113.60, "reservedDigits": 0, "index": 6,
            "enabled": False},
    "UG": {
            "code": "UGX", "currencyId": "566", "currencySymbol": "USh",
            "currencyConversion": 1, "isBase": False,
            "exchangeRateToBase": 3541.20, "reservedDigits": 0, "index": 6,
            "enabled": False},
}


def init_logging(filename):
    directory = os.path.dirname(filename)
    if directory != '' and not os.path.exists(directory):
        os.makedirs(directory)

    level = logging.INFO
    if os.environ.get('_DEBUG') == '1':
        level = logging.DEBUG
    fmt = '[%(asctime)s %(levelname)s | %(module)s %(funcName)s] %(message)s'
    logging.basicConfig(
        filename=filename, level=logging.DEBUG, format=fmt,
        datefmt="%Y-%M-%d %H:%M:%S")
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(fmt=fmt, datefmt="%H:%M:%S"))
    logging.getLogger().addHandler(console)


def load_config(filename, env):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config[env]


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def create_uomnify_addresses(data):
    region = quark_common_db.Region.find_one({"code": data["code"]})
    postage_region = quark_common_db.CountryPostage.find_one(
        {"regionCode": data["code"]})
    if not postage_region:
        region_postage_id = None
        for it in quark_common_db.CountryPostage.find().sort(
                [("_id", -1)]).limit(1):
            region_postage_id = it["_id"] + 1
        postage_country = MAP_REGION_POSTAGE[data["code"]]
        postage_country["_id"] = region_postage_id
        quark_common_db.CountryPostage.insert_one(postage_country)
    if not region:
        index = None
        for it in quark_common_db.Region.find().sort([("index", -1)]).limit(1):
            index = it["index"] + 1
        region = MAP_REGION_UO[data["code"]]
        region["index"] = index
        quark_common_db.Region.insert_one(region)
    currency = quark_common_db.Currency.find_one({"code": data["code"]})
    if not currency:
        index = None
        for it in quark_common_db.Currency.find().sort([("index", -1)]).limit(1):
            index = it["index"] + 1
        currency = MAP_CURRENCY[data["code"]]
        currency["index"] = index
        quark_common_db.Currency.insert_one(currency)
    quark_common_db.State.delete_many({"regionCode": region["code"]})
    quark_common_db.City.delete_many({"regionCode": region["code"]})
    quark_common_db.Area.delete_many({"regionCode": region["code"]})
    last_state_id = None
    for it in quark_common_db.State.find().sort([("_id", -1)]).limit(1):
        last_state_id = it["_id"]
    last_city_id = None
    for it in quark_common_db.City.find().sort([("_id", -1)]).limit(1):
        last_city_id = it["_id"]
    last_area_id = None
    for it in quark_common_db.Area.find().sort([("_id", -1)]).limit(1):
        last_area_id = it["_id"]
    for state in data.get("children"):
        if state["type"] != 1:
            logging.error("state data error")
            raise Exception("state data error")
        last_state_id += 1
        quark_common_db.State.insert_one(
            {
                "_id": last_state_id,
                "regionCode": region["code"],
                "parentCode": state["parentCode"],
                "code": state["code"],
                "name": state["name"],
                "enabled": True,
                "visible": True,
                "index": last_state_id,
                "postage": None,
                "minAppVersion": 1,
            })
        if not state.get("children"):
            logging.error("state not have children! state=%r" % state)
            continue
        for city in state["children"]:
            if city["type"] != 2:
                logging.error("city data error")
                raise Exception("city data error")
            last_city_id += 1
            quark_common_db.City.insert_one(
                {
                    "_id": last_city_id,
                    "name": city["name"],
                    "code": city["code"],
                    "regionCode": region["code"],
                    "stateId": last_state_id,
                    "parentCode": city["parentCode"],
                    "enabled": True,
                    "visible": True,
                    "index": last_city_id,
                    "postage": None,
                    "minAppVersion": 1,
                })
            for area in city["children"]:
                if area["type"] != 3:
                    logging.error("area data error")
                    raise Exception("area data error")
                last_area_id += 1
                quark_common_db.Area.insert_one(
                    {
                        "_id": last_area_id,
                        "name": area["name"],
                        "code": area["code"],
                        "regionCode": region["code"],
                        "stateId": last_state_id,
                        "cityId": last_city_id,
                        "parentCode": area["parentCode"],
                        "postage": 1,
                        "supportCod": True,
                        "enabled": True,
                        "visible": True,
                        "index": last_area_id,
                        "minAppVersion": 1,
                        "ett": 0
                    }
                )


def create_addresses(data):
    region = bee_common_db.Region.find_one({"code": data["code"]})
    bee_common_db.State.delete_many({"regionId": region["_id"]})
    bee_common_db.City.delete_many({"regionId": region["_id"]})
    bee_common_db.Area.delete_many({"regionId": region["_id"]})
    last_state_id = None
    for it in bee_common_db.State.find().sort([("_id", -1)]).limit(1):
        last_state_id = it["_id"]
    last_city_id = None
    for it in bee_common_db.City.find().sort([("_id", -1)]).limit(1):
        last_city_id = it["_id"]
    last_area_id = None
    for it in bee_common_db.Area.find().sort([("_id", -1)]).limit(1):
        last_area_id = it["_id"]
    if not data.get("children"):
        logging.error("region data error, 缺少下级数据 data=%r" % data)
    for state in data.get("children"):
        if state["type"] != 1:
            logging.error("state data error")
            raise Exception("state data error")
        last_state_id += 1
        bee_common_db.State.insert_one(
            {
                "_id": last_state_id,
                "regionId": region["_id"],
                "parentCode": state["parentCode"],
                "code": state["code"],
                "name": state["name"],
                "enabled": True,
                "visible": True,
                "index": last_state_id,
            })
        if not state.get("children"):
            logging.error("state not have children! state=%r" % state)
            continue
        for city in state.get("children"):
            if city["type"] != 2:
                logging.error("city data error")
                raise Exception("city data error")
            last_city_id += 1
            bee_common_db.City.insert_one(
                {
                    "_id": last_city_id,
                    "name": city["name"],
                    "code": city["code"],
                    "regionId": region["_id"],
                    "stateId": last_state_id,
                    "parentCode": city["parentCode"],
                    "enabled": True,
                    "visible": True,
                    "index": last_city_id
                })
            if not city.get("children"):
                logging.error("city not have children! city=%r" % city)
            for area in city["children"]:
                if area["type"] != 3:
                    logging.error("area data error")
                    raise Exception("area data error")
                last_area_id += 1
                bee_common_db.Area.insert_one(
                    {
                        "_id": last_area_id,
                        "name": area["name"],
                        "code": area["code"],
                        "regionId": region["_id"],
                        "stateId": last_state_id,
                        "cityId": last_city_id,
                        "parentCode": area["parentCode"],
                        "postage": 500,
                        "postcode": None,
                        "supportCod": True,
                        "enabled": True,
                        "visible": True,
                        "index": last_area_id
                    }
                )


def create_africa_region(region_code):
    bee_common_db.Region.delete_one({"code": region_code})
    region_id = None
    for it in bee_common_db.Region.find().sort([("_id", -1)]).limit(1):
        region_id = it["_id"] + 1
    region = MAP_REGION_XED[region_code]
    region["index"] = region_id
    region["_id"] = region_id
    bee_common_db.Region.insert_one(region)


def add_transport_corridor():
    start_id = 10
    for it in bee_logistics_db.TransportCorridor.find().sort(
            [("_id", -1)]).limit(1):
        start_id = it["_id"] + 1

    bee_logistics_db.TransportCorridor.insert_one(
        {
            "_id": start_id,
            "providerId": "speedaf",
            "providerLocation": "易递-speedAf",
            "providerName": "speedAf",
            "contactName": "Harunur Roshid",
            "contactPhone": "01840566762",
            "type": 2,
            "terminalRegionIds": [
                7, 8, 9
            ],
            "state": 1,
            "targetRegionIds": [
                7, 8, 9
            ],
            "supportAssortments": [
                1,
                2,
                3,
                4,
                5,
                6
            ],
            "index": 6,
            "terminalType": {
                "1": 1
            }
        }
    )


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    bee_common_db = get_db(config, env, "BeeCommon")
    quark_common_db = get_db(config, env, "QuarkCommon")
    bee_logistics_db = get_db(config, env, "BeeLogistics")

    for region_code in REGION_CODES:
        # if region_code != "KE":
        #     continue
        create_africa_region(region_code)
        data = get_area_tree(region_code, env)
        create_addresses(json.loads(data))
        create_uomnify_addresses(json.loads(data))
        logging.info("region %s is complete!" % region_code)
        # exit()
        # raise Exception("test")
    add_transport_corridor()

    print("---------------------------success-------------------------------")

