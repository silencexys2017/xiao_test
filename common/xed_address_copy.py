# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime

_DEFAULT_LOG_FILE = 'xed_address_copy.log'
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


def load_cities(filename):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def add_state_to_bee_common():
    for it in common_db.state.find({}).sort([("id", 1)]):
        if not bee_common_db.State.find_one({"_id": it["id"]}):
            bee_common_db.State.insert_one({
                "_id": it["id"],
                "regionId": it["regionId"],
                "name": it["name"],
                "index": it["index"],
                "enabled": it["enabled"],
                "visible": it["visible"]
            })


def add_city_to_bee_common():
    for it in common_db.city.find({}).sort([("id", 1)]):
        if not bee_common_db.City.find_one({"_id": it["id"]}):
            bee_common_db.City.insert_one(
                {
                    "_id": it["id"],
                    "name": it["name"],
                    "regionId": it["regionId"],
                    "stateId": it["stateId"],
                    "index": it["index"],
                    "enabled": it["enabled"],
                    "visible": it["visible"]
                })


def add_area_to_bee_common():
    for it in common_db.area.find({}).sort([("id", 1)]):
        if not bee_common_db.Area.find_one({"_id": it["id"]}):
            bee_common_db.Area.insert_one(
                {
                    "_id": it["id"],
                    "name": it["name"],
                    "regionId": it["regionId"],
                    "stateId": it["stateId"],
                    "cityId": it["cityId"],
                    "index": it["index"],
                    "enabled": it["enabled"],
                    "visible": it["visible"],
                    "postage": it.get("postage"),
                    "supportCod": it.get("supportCod"),
                    "postcode": it.get("postcode"),
                    "ett": it.get("ett")
                })


def add_area_mapping_to_bee_common():
    inc_id = 0
    for it in bee_common_db.AreaMapping.find({}).sort("_id", -1).limit(1):
        inc_id = it["_id"]
    for it in bee_common_db.Area.find({}).sort([("id", 1)]):
        if not bee_common_db.AreaMapping.find_one(
                {"xedAreaId": it["_id"], "regionId": it["regionId"]}):
            inc_id += 1
            bee_common_db.AddressMapping.insert_one(
                {
                    "_id": inc_id,
                    "userType": 2,
                    "regionId": it["regionId"],
                    "xedAreaId": it["_id"],
                    "otherAreaId": str(it["_id"])
                })


def add_xed_uonmify_address_mapping():
    inc_id = 0
    for it in bee_common_db.AddressMapping.find({}).sort([("_id", -1)]).limit(1):
        inc_id = it["_id"]
    for it in quark_common_db.Area.find({"regionCode": "KE"}).sort([("_id", 1)]):
        bee_area = bee_common_db.Area.find_one({"code": it["code"]})
        inc_id += 1
        bee_common_db.AddressMapping.insert_one(
            {
                "_id": inc_id,
                "userType": 2,
                "regionId": bee_area["regionId"],
                "xedAreaId": bee_area["_id"],
                "otherAreaId": str(it["_id"])
            })


def update_user_delivery_address():
    for it in bee_auth_db.StoreShippingAddress.find({}):
        store = bee_auth_db.Store.find_one({"_id": it.get("storeId")})
        if not store:
            print("error----------storeId=%s is not found in collection Store")
            # bee_auth_db.StoreShippingAddress.delete_one({"_id": it["_id"]})
            continue
        bee_auth_db.StoreShippingAddress.update_one({"_id": it["_id"]}, {
            "$set": {"addressType": 1, "userId": store["userId"],
                     "isDeleted": False}})
    address_id = 200
    for it in bee_auth_db.StoreShippingAddress.find({}).sort(
            [("_id", -1)]).limit(1):
        address_id = it["_id"] + 1

    bee_ids_db.ids.insert_one({"_id": "ShippingAddress", "seq": address_id})


def create_collection():
    bee_common_db.create_collection("State")
    bee_common_db.create_collection("City")
    bee_common_db.create_collection("Area")


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    common_db = get_db(config, env, "Common")
    bee_common_db = get_db(config, env, "BeeCommon")
    bee_auth_db = get_db(config, env, "BeeAuth")
    bee_ids_db = get_db(config, env, "BeeIds")
    quark_common_db = get_db(config, env, "QuarkCommon")
    # create_collection()
    """
    add_state_to_bee_common()
    print("----------add_state_to_bee_common success----------")
    add_city_to_bee_common()
    print("----------add_city_to_bee_common success----------")
    add_area_to_bee_common()
    print("----------add_area_to_bee_common success----------")
    update_user_delivery_address()
    print("----------update_user_delivery_address success----------")
    add_area_mapping_to_bee_common()
    print("----------add_area_mapping_to_bee_common success----------")
    """
    add_xed_uonmify_address_mapping()
