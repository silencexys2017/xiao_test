# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta

_DEFAULT_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}


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


def utc2local(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime('%Y-%m-%d %H:%M:%S')


def update_error_address_logistics_orders(start_time):
    for it in bee_logistics_db.LogisticsOrder.find(
            {"userType": 1, "createdAt": {"$gt": start_time}}).sort([("_id", 1)]):
        if it["recipient"]["areaId"] == "None":
            res = it["recipient"]
            region_code = bee_common_db.Region.find_one(
                {"_id": it["regionId"]})["code"]
            state = bee_common_db.Areas.find_one(
                {"regionCode": region_code, "deep": 1, "name": res["state"]})
            if not state:
                print("not find state,order=%s,regionId=%s" % (
                    it["orderNo"], it["regionId"]))
                continue
            city = bee_common_db.Areas.find_one(
                {"regionCode": region_code, "deep": 2, "name": res["city"]})
            if not city:
                print("not find city,order=%s,regionId=%s" % (
                    it["orderNo"], it["regionId"]))
                continue

            area = bee_common_db.Areas.find_one(
                {"regionCode": region_code, "deep": 3, "name": res["area"]})
            if not area:
                print("not find area,order=%s,regionId=%s" % (
                    it["orderNo"], it["regionId"]))
                continue

            bee_logistics_db.LogisticsOrder.update_one(
                {"orderNo": it["orderNo"]}, {"$set": {
                    "recipient.areaId": str(area["_id"]),
                    "recipient.cityId": str(city["_id"])}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("xed-order-export.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    bee_logistics_db = get_db(config, env, "BeeLogistics")
    bee_common_db = get_db(config, env, "BeeCommon")

    start_time = datetime(2022, 6, 1)
    update_error_address_logistics_orders(start_time)



