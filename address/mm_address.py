# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from exfcs import get_all_address

_DEFAULT_LOG_FILE = 'app.log'
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


def delete_myanmar_address():
    mm = common_db.region.find_one({"name" : "Myanmar"})
    common_db.state.delete_many({"regionId": mm["id"]})
    common_db.city.delete_many({"regionId": mm["id"]})
    common_db.area.delete_many({"regionId": mm["id"]})


def delete_ex_fcs_address_mapping():
    order_db.ExfcsAddressMapping.delete_many({})


def create_myanmar_address(data_li):
    mm = common_db.region.find_one({"name": "Myanmar"})
    last_state_id = None
    for it in common_db.state.find().sort([("id", -1)]).limit(1):
        last_state_id = it["id"]
    last_city_id = None
    for it in common_db.city.find().sort([("id", -1)]).limit(1):
        last_city_id = it["id"]
    last_area_id = None
    for it in common_db.area.find().sort([("id", -1)]).limit(1):
        last_area_id = it["id"]
    for item in data_li:
        last_state_id += 1
        common_db.state.insert_one(
            {
                "id": last_state_id,
                "regionId": mm["id"],
                "index": last_state_id,
                "name": item["state_name"],
                "minAppVersion": 40,
                "enabled": True,
                "visible": True
            })
        muse_count = 0
        for it in item["cities"]:
            last_city_id += 1
            if it["city_name"] == "Muse":
                muse_count += 1
                if muse_count > 1:
                    continue
            common_db.city.insert_one(
                {
                    "index": last_city_id,
                    "name": it["city_name"],
                    "minAppVersion": 40,
                    "stateId": last_state_id,
                    "regionId": mm["id"],
                    "id": last_city_id,
                    "enabled": True,
                    "visible": True
                })

            order_db.ExfcsAddressMapping.insert_one(
                {
                    "regionId": mm["id"],
                    "cityId": it["city_id"],
                    "stateId": item["state_id"],
                    "pfCityId": last_city_id,
                    "stateName": item["state_name"],
                    "cityName": it["city_name"]
                })
            last_area_id += 1
            common_db.area.insert_one(
                {
                    "postage": 500,
                    "index": last_area_id,
                    "name": it["city_name"],
                    "minAppVersion": 40,
                    "stateId": last_state_id,
                    "regionId": mm["id"],
                    "cityId": last_city_id,
                    "supportCod": True,
                    "id": last_area_id,
                    "enabled": True,
                    "visible": True,
                    "ett": 7
                }
            )


def insert_china_map_address():
    order_db.ExfcsAddressMapping.insert_one(
        {
            "regionId": 2,
            "cityId": 1,
            "stateId": 1,
            "cityName": "Ruili",
            "stateName": "Yunnan Province",
            "pfCityId": 430
        })


def update_pf_mm_area():
    postage_di = {
        1500: ["Yangon City", "Yangon Zone 2"],
        2000: ["Bago", "Epost"],
        3500: ["Myitkyina", "Lashio", "Mawlamyine", "Sagaing", "Monywa",
               "Sagaing Zone 2"],
        2500: ["Taunggyi", "Muse", "Taunggyi ATY", "Naypyitaw",
               "Naypyitaw Zone 2", "Moegok", "Kyauksel", "Pyin Oo Lwin",
               "Mandalay", "Mandalay Zone 2"]}
    for k, v in postage_di.items():
        common_db.area.update_many(
            {"regionId": 3, "name": {"$in": v}}, {"$set": {"postage": k}})


def update_area_name(area_ids):
    for area in common_db.area.find({"id": {"$in": area_ids}}):
        common_db.area.update_one(
            {"id": area["id"]}, {"$set": {"name": area["name"] + " City"}})

    for area in bee_common_db.Area.find({"_id": {"$in": area_ids}}):
        bee_common_db.Area.update_one(
            {"_id": area["_id"]}, {"$set": {"name": area["name"] + " City"}})

    for area in quark_common_db.Area.find({"_id": {"$in": area_ids}}):
        quark_common_db.Area.update_one(
            {"_id": area["_id"]}, {"$set": {"name": area["name"] + " City"}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    common_db = get_db(config, env, "Common")
    member_db = get_db(config, env, "member")
    bee_common_db = get_db(config, env, "BeeCommon")
    quark_common_db = get_db(config, env, "QuarkCommon")

    # data = get_all_address()
    update_area_name([21006, 21007, 21009, 21011, 21015, 21021])
    # delete_myanmar_address()
    # delete_ex_fcs_address_mapping()
    # create_myanmar_address(data)
    # insert_china_map_address()
    # update_pf_mm_area()

    print("---------------------------success-------------------------------")

