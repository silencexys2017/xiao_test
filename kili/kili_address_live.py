# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta
from pymongo import ReturnDocument

_DEFAULT_CONFIG_FILE = '../kili_config.json'
_SOUTHX_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}

X_DB_URL = {
    "dev": "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongodb-paas-service/admin?replicaSet=rs0",
	"test": "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@159.138.90.30:30734/admin",
	"prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@159.138.90.30:30734/admin?authSource=admin"
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
    client = pymongo.MongoClient(uri[env], retryWrites=False)
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


def add_kili_ke_address(area_list):
    common_db.Areas.delete_many({})
    for it in area_list:
        if it["regionCode"] == "KE":
            if it["deep"] == 0:
                it["_id"] = 6
            elif it["deep"] == 1:
                it["parentId"] = 6
        it["lastUpdatedTime"] = convert_time(it["lastUpdatedTime"])
        common_db.Areas.insert_one(it)


def update_kili_ke_address(area_list):
    for it in area_list:
        if it["regionCode"] == "KE" and it["deep"] == 3:
            area = common_db.Areas.find_one({"_id": it["_id"]})
            print(area["pickupIds"])
            if not area:
                common_db.Areas.insert_one(it)
            else:
                res = common_db.Areas.find_one_and_update(
                    {"_id": it["_id"]},
                    {"$set": {"pickupIds": it["pickupIds"]}},
                    return_document=True)
                print(res["pickupIds"])


def add_kili_region_config():
    # common_db.RegionConfig.delete_many({})
    common_db.region.update_one(
        {"code": "CN"}, {"$set": {
            "addressLevel": 2, "addressNameMap": {"1": "State", "2": "City"}}})
    common_db.region.update_one(
        {"code": "KE"}, {"$set": {
            "addressLevel": 3, "addressNameMap": {
                "1": "County", "2": "Subcounty/Town", "3": "Area(ward)"}}})
    """
    common_db.RegionConfig.insert_many(
        [
            {
                "_id": 2,
                "callingCode": "86",
                "code": "CN",
                "name": "China",
                "intro": "A great country",
                "flag": "https://perfee-sys.obs.ap-southeast-3.myhuaweicloud.com/country-flags/2.png",
                "currencyId": 156,
                "currencySymbol": "¥",
                "currencyConversion": 1,
                "language": "zh",
                "timeZone": "Asia/Shanghai",
                "currency": "CNY",
                "index": 2,
                "minAppVersion": 1,
                "userAddressInteractionMethod": 1,
                "addressLevel": 2,
                "addressNameMap": {"1": "state", "2": "city"}
            },
            {
                "_id": 6,
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
                "index": 6,
                "minAppVersion": 1,
                "userAddressInteractionMethod": 1,
                "addressLevel": 3,
                "addressNameMap": {"1": "county", "2": "subcounty", "3": "ward"}
            }
        ]
    )
    """


def add_kili_pickup_station(station_list):
    common_db.PickupStation.delete_many({})
    for it in station_list:
        common_db.PickupStation.insert_one(it)


def update_kili_pickup_station(station_list):
    for it in station_list:
        res = common_db.PickupStation.find_one(
            {"sourceStationId": it["sourceStationId"]})
        if res:
            print(res["leafAreaIds"])
        if not res:
            common_db.PickupStation.insert_one(it)
        else:
            res = common_db.PickupStation.find_one_and_update(
                {"sourceStationId": it["sourceStationId"]},
                {"$set": {"leafAreaIds": it["leafAreaIds"]}},
                return_document=True
            )
            if res:
                print(res["leafAreaIds"])


def update_user_address():
    for it in member_db.address.find():
        if it.get("addressType") is None:
            state_name, city_name, area_name = it["state"], it["city"], it["area"]
        else:
            names = []
            for val in it["areaNames"].values():
                for name in val.values():
                    names.append(name)
            state_name, city_name, area_name = names

        state = common_db.Areas.find_one(
            {"name": state_name, "deep": 1})
        if not state:
            member_db.address.update_one(
                {"id": it["id"]}, {"$set": {"status": 2}})
            continue
        city = common_db.Areas.find_one(
            {"name": city_name, "deep": 2, "parentId": state["_id"]})
        if not city:
            member_db.address.update_one(
                {"id": it["id"]}, {"$set": {"status": 2}})
            continue
        area = common_db.Areas.find_one(
            {"name": area_name, "deep": 3, "parentId": city["_id"]})
        if not area:
            member_db.address.update_one(
                {"id": it["id"]}, {"$set": {"status": 2}})
            continue
        member_db.address.update_one(
            {"id": it["id"]},
            {"$set": {
                "pickupStationId": None,
                "familyName": it["name"],
                "givenName": it["name"],
                "regionCode": "KE",
                "addressType": 1,
                "pickupStationAddress": None,
                "postcode": it.get("postcode"),
                "isSelected": it.get("isSelected"),
                "status": 1,
                "areaIds": [area["_id"], city["_id"], state["_id"]],
                "areaNames": {
                        "1": {str(state["_id"]): state["name"]},
                        "2": {str(city["_id"]): city["name"]},
                        "3": {str(area["_id"]): area["name"]}
                },

            }}
        )


def convert_time(date_time_str):
    if date_time_str:
        return datetime.strptime(date_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return None


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]

    # config = load_config(_DEFAULT_CONFIG_FILE, env)
    # southx_config = load_config(_SOUTHX_CONFIG_FILE, env)
    common_db = get_db(K_DB_URL, env, "Common")
    # bee_common_db = get_db(X_DB_URL, env, "BeeCommon")
    member_db = get_db(K_DB_URL, env, "Member")
    with open("../xed/ki_li_data.json", 'r', encoding="utf-8") as f:
        ki_li_data = json.load(f)
    # add_kili_ke_address(ki_li_data["areas"])
    # print("add_kili_ke_address success")
    # add_kili_region_config()
    # print("add_kili_region_config success")
    # add_kili_pickup_station(ki_li_data["stations"])
    # print("add_kili_pickup_station success")
    # update_user_address()
    # print("update_user_address success")

    # update_kili_ke_address(ki_li_data["areas"])
    # print("update_kili_ke_address success")
    update_kili_pickup_station(ki_li_data["stations"])
    print("update_kili_pickup_station success")
