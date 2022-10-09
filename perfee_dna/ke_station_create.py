# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json

_DEFAULT_CONFIG_FILE = '../config.json'


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


def create_ke_address():
    region_id = 6
    dna_common_db.region.delete_one({"id": region_id})
    dna_common_db.state.delete_many({"regionId": region_id})
    dna_common_db.city.delete_many({"regionId": region_id})
    dna_common_db.area.delete_many({"regionId": region_id})
    dna_common_db.region.insert_one(
        {
            "id": region_id,
            "callingCode": "254",
            "code": "KE",
            "name": "Kenya",
            "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/6.png",
            "currencyId": 404,
            "currencySymbol": "KSh",
            "currencyConversion": 113.6,
            "language": "en",
            "timeZone": "Africa/Nairobi",
            "currency": "KES",
            "index": region_id,
            "minAppVersion": 1,
            "userAddressInteractionMethod": 1
        }
    )
    state_id, city_id, area_id = 0, 0, 0
    for it in dna_common_db.state.find().sort([("id", -1)]).limit(1):
        state_id = it["id"] + 100
    for it in dna_common_db.city.find().sort([("id", -1)]).limit(1):
        city_id = it["id"] + 1000
    for it in dna_common_db.area.find().sort([("id", -1)]).limit(1):
        area_id = it["id"] + 10000

    for state in quark_common_db.State.find({"regionCode": "KE"}):
        state_id += 1
        dna_common_db.state.insert_one(
            {
                "id": state_id,
                "regionId": region_id,
                "index": state_id,
                "name": state["name"],
                "minAppVersion": 40,
                "enabled": True,
                "visible": True
            }
        )
        for city in quark_common_db.City.find({"stateId": state["_id"]}):
            city_id += 1
            dna_common_db.city.insert_one(
                {
                    "id": city_id,
                    "index": city_id,
                    "name": city["name"],
                    "minAppVersion": 40,
                    "stateId": state_id,
                    "regionId": region_id,
                    "enabled": True,
                    "visible": True
                }
            )
            for area in quark_common_db.Area.find({"cityId": city["_id"]}):
                area_id += 1
                dna_common_db.area.insert_one(
                    {
                        "id": area_id,
                        "index": area_id,
                        "name": area["name"],
                        "minAppVersion": 40,
                        "stateId": state_id,
                        "regionId": region_id,
                        "cityId": city_id,
                        "supportCod": False,
                        "postage": 1000,
                        "enabled": True,
                        "visible": True,
                        "ett": 7
                    }
                )


def add_promotion_parameter(region_id):
    dna_promotion_db.parameter.delete_many({"regionId": region_id})
    parameter_id = 0
    index = 1
    for it in dna_promotion_db.parameter.find().sort([("id", -1)]).limit(1):
        parameter_id = it["id"] + 100
    for it in dna_promotion_db.parameter.find({"regionId": 1}):
        it.pop("_id")
        it["id"] = parameter_id
        it["regionId"] = region_id
        it["index"] = index
        dna_promotion_db.parameter.insert_one(it)
        parameter_id += 1
        index += 1


def add_order_parameter(region_id):
    dna_order_db.parameter.delete_many({"regionId": region_id})
    parameter_id = 0
    index = 1
    for it in dna_order_db.parameter.find().sort([("id", -1)]).limit(1):
        parameter_id = it["id"] + 100
    for it in dna_order_db.parameter.find({"regionId": 1}):
        if it["name"] in ["ORDER_ONLINE_ENABLE", "ORDER_ONLINE_BKASH_ENABLE",
                          "MAXIMUM_SINGLE_FEE_BKASH", "MAXIMUM_SINGLE_FEE_SSL",
                          "PAY_GATEWAY_FEE_RATE_BKASH", "PAY_GATEWAY_FEE_RATE_SSL"]:
            continue
        it.pop("_id")
        it["id"] = parameter_id
        it["regionId"] = region_id
        it["index"] = index
        dna_order_db.parameter.insert_one(it)
        parameter_id += 1
        index += 1


def add_member_parameter(region_id):
    dna_member_db.parameter.delete_many({"regionId": region_id})
    parameter_id = 0
    for it in dna_member_db.parameter.find().sort([("id", -1)]).limit(1):
        parameter_id = it["id"] + 100
    for it in dna_member_db.parameter.find({"regionId": 1}):
        it.pop("_id")
        it["id"] = parameter_id
        it["regionId"] = region_id
        dna_member_db.parameter.insert_one(it)
        parameter_id += 1


def add_goods_parameter(region_id):
    dna_goods_db.Parameter.delete_many({"regionId": region_id})
    parameter_id = 0
    for it in dna_goods_db.Parameter.find().sort([("id", -1)]).limit(1):
        parameter_id = it["id"] + 100
    for it in dna_goods_db.Parameter.find({"regionId": 1}):
        it.pop("_id")
        it["id"] = parameter_id
        it["regionId"] = region_id
        dna_goods_db.Parameter.insert_one(it)
        parameter_id += 1


def add_common_parameter(region_id):
    dna_common_db.parameter.delete_many({"regionId": region_id})
    parameter_id = 0
    for it in dna_common_db.parameter.find().sort([("id", -1)]).limit(1):
        parameter_id = it["id"] + 100
    for it in dna_common_db.parameter.find({"regionId": 1}):
        it.pop("_id")
        it["id"] = parameter_id
        it["regionId"] = region_id
        dna_common_db.parameter.insert_one(it)
        parameter_id += 1


def add_seller_parameter(region_id):
    dna_seller_db.FaultAndPunishmentConfig.delete_many({"regionId": region_id})
    parameter_id = 0
    for it in dna_seller_db.FaultAndPunishmentConfig.find().sort(
            [("_id", -1)]).limit(1):
        parameter_id = it["_id"] + 100
    for it in dna_seller_db.FaultAndPunishmentConfig.find({"regionId": 1}):
        it["_id"] = parameter_id
        it["regionId"] = region_id
        dna_seller_db.FaultAndPunishmentConfig.insert_one(it)
        parameter_id += 1


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("ke_address.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    dna_common_db = get_db(config, env, "Common")
    dna_promotion_db = get_db(config, env, "Promotion")
    dna_order_db = get_db(config, env, "Order")
    dna_member_db = get_db(config, env, "Member")
    dna_goods_db = get_db(config, env, "Goods")
    dna_seller_db = get_db(config, env, "Seller")
    quark_common_db = get_db(config, env, "QuarkCommon")

    create_ke_address()
    add_common_parameter(6)
    add_promotion_parameter(6)
    add_order_parameter(6)
    add_member_parameter(6)
    add_goods_parameter(6)
    add_seller_parameter(6)

    print("---------------------------success-------------------------------")

