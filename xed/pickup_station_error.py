# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta
from openpyxl import load_workbook


_DEFAULT_CONFIG_FILE = '../kili_config.json'
_SOUTHX_CONFIG_FILE = '../config.json'
DATA_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}

X_DB_URL = {
    "dev": "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongodb-paas-service/admin?replicaSet=rs0",
	"test": "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@159.138.90.30:30734/admin",
    "prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@mongodb-paas-service/admin?replicaSet=rs0"
}


K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://root:IdrCgVpHzv@mongo-mongodb-headless.os:27017/admin?replicaSet=rs0&retrywrites=false",
    "prd": "mongodb://sk2:Gmbz8i63mtswuMKz8Lk92zNM7UxwO5Txz1@ebes-db.cmxtf8qiglae.eu-central-1.docdb.amazonaws.com:27017/admin?replicaSet=rs0&retrywrites=false"
}


UTC_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
LOCAL_FORMAT = '%Y-%m-%d %H:%M:%S'


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


def get_db(uri, env, database):
    client = pymongo.MongoClient(uri[env])
    db = '%s%s' % (env, database)
    return client[db]


def utc2local(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime(LOCAL_FORMAT)


def get_deep_start_id(deep):
    if deep in [0, 1, 2, 3]:
        return int(1000 * 10 ** ((deep - 1) * 3))
    elif deep > 3:
        return int(1000 * 10 ** (1+deep))


def convert_time(date_time_str):
    if date_time_str:
        return datetime.strptime(date_time_str, DATA_TIME_FORMAT)
    return None


def convert_time_str(date_time):
    if date_time:
        return date_time.strftime(DATA_TIME_FORMAT)
    return None


def strip_string_name(name):
    if not name:
        return
    name = name.strip()
    split_names = [s.capitalize() if "-" not in s else s for s in name.split(" ")]
    split_names = list(filter(None, split_names))
    name = " ".join(split_names)
    return name


def pull_pickup_station(file_route, from_seller=False):
    wb_obj = load_workbook(file_route, data_only=True)
    ks_sheet = wb_obj.get_sheet_by_name("KS&ward")
    total_count = 0
    for row in list(ks_sheet.iter_rows(min_row=434, max_row=621)):
        total_count += 1
        county, sub_county, area = strip_string_name(
            row[0].value), strip_string_name(row[1].value), strip_string_name(
            row[2].value)
        shop_id = strip_string_name(row[4].value)
        if not shop_id or not shop_id.isdigit():
            continue
        shop_id = int(shop_id)
        # address, shop_id, shop_name = row[3].value, row[4].value, row[5].value
        res_county = bee_common_db.Areas.find_one({"deep": 1, "name": county})
        if not res_county:
            continue
        res_sub_county = bee_common_db.Areas.find_one(
            {"deep": 2, "name": sub_county, "parentId": res_county["_id"]})
        if not res_sub_county:
            continue
        res_area = bee_common_db.Areas.find_one(
            {"deep": 3, "name": area, "parentId": res_sub_county["_id"]})
        if not res_area:
            continue
        station = bee_common_db.PickupStation.find_one_and_update(
            {"sourceStationId": shop_id},
            {"$pull": {"leafAreaIds": res_area["_id"]}})
        if not station:
            continue
        bee_common_db.Areas.update_one(
            {"_id": res_area["_id"]},
            {"$pull": {"pickupIds": shop_id}})
        if from_seller is True:
            member_db.address.update_many(
                {"addressType": 2, "pickupStationId": shop_id},
                {"$set": {"status": 2}})
        print("update success area=%s,sourceStationId=%s,line=%s" % (
            area, shop_id, total_count))
    print("loop count=%s" % total_count)


def push_pickup_station(file_route):
    wb_obj = load_workbook(file_route, data_only=True)
    ks_sheet = wb_obj.get_sheet_by_name("KS&ward")
    total_count = 0
    for row in list(ks_sheet.iter_rows(min_row=3, max_row=432)):
        total_count += 1
        county, sub_county, area = strip_string_name(
            row[0].value), strip_string_name(row[1].value), strip_string_name(
            row[2].value)
        shop_id = strip_string_name(row[4].value)
        if not shop_id or not shop_id.isdigit():
            continue
        shop_id = int(shop_id)
        # address, shop_id, shop_name = row[3].value, row[4].value, row[5].value
        res_county = bee_common_db.Areas.find_one({"deep": 1, "name": county})
        if not res_county:
            continue
        res_sub_county = bee_common_db.Areas.find_one(
            {"deep": 2, "name": sub_county, "parentId": res_county["_id"]})
        if not res_sub_county:
            continue
        area_dict = bee_common_db.Areas.find_one(
            {"deep": 3, "name": area, "parentId": res_sub_county["_id"]})
        if area_dict:
            station = bee_common_db.PickupStation.find_one_and_update(
                {"sourceStationId": shop_id},
                {"$addToSet": {"leafAreaIds": area_dict["_id"]}})
            if not station:
                continue
            bee_common_db.Areas.update_one(
                {"_id": area_dict["_id"]},
                {"$addToSet": {"pickupIds": shop_id}})
        if row[6].value:
            for it in row[6].value.split(","):
                it = strip_string_name(it)
                if it:
                    res_area = bee_common_db.Areas.find_one(
                        {"deep": 3, "name": it, "parentId": res_sub_county["_id"]})
                    if not res_area:
                        continue
                    station = bee_common_db.PickupStation.find_one_and_update(
                        {"sourceStationId": shop_id},
                        {"$addToSet": {"leafAreaIds": res_area["_id"]}})
                    if not station:
                        continue
                    bee_common_db.Areas.update_one(
                        {"_id": res_area["_id"]},
                        {"$addToSet": {"pickupIds": shop_id}})
                    print(
                        "update pickup area=%s,sourceStationId=%s,line=%s" % (
                            it, shop_id, total_count))


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")

    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env, source = sys.argv[1], sys.argv[2]
    # config = load_config(_DEFAULT_CONFIG_FILE, env)
    # southx_config = load_config(_SOUTHX_CONFIG_FILE, env)
    if env == "prd":
        url = X_DB_URL
    else:
        url = K_DB_URL
    if source == "xed":
        bee_common_db = get_db(url, env, "BeeCommon")
        from_seller = False
        member_db = {}
    else:
        bee_common_db = get_db(url, env, "Common")
        from_seller = True
        member_db = get_db(url, env, "Member")

    pull_pickup_station("./address Update V6.xlsx", from_seller=from_seller)
    push_pickup_station("./address Update V6.xlsx")




