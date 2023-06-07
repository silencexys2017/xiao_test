# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta


_DEFAULT_CONFIG_FILE = '../kili_config.json'
_SOUTHX_CONFIG_FILE = '../config.json'
DATA_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}


K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://sk2:Qmvz84mtswuMJz8Kk90zBM7UbdW@ebes-db.cluster-cvxmlpsy4xpw.eu-central-1.docdb.amazonaws.com:27017/admin?authSource=admin",
    # "prd": "mongodb://sk2:Gmbz8i63mtswuMKz8Lk92zNM7UxwO5Txz1@ebes-db.cmxtf8qiglae.eu-central-1.docdb.amazonaws.com:27017/admin?replicaSet=rs0&retrywrites=false"
    "prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@mongodb-paas-service:27017/?replicaSet=rs0&authSource=admin"
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


def import_ke_address(
        ke_json, region_id, region_code, deep_1_start_id, deep_2_start_id,
        deep_3_start_id, utc_now):
    mall_sub_county = ke_json["mallSubCounty"]
    shop_area_map = {}
    for state, s_item in ke_json.items():
        if state in ["notMatchTown", "notMatchWard", "mallSubCounty"]:
            continue
        deep_1_start_id += 1
        code = region_code + "1" + str(deep_1_start_id)
        data_1 = {
            "_id": deep_1_start_id,
            "areaType": 1,
            "name": state,
            "code": code,
            "postcode": None,
            "parentId": region_id,
            "sort": deep_1_start_id,
            "deep": 1,
            "regionCode": region_code,
            "isSupportToDoor": False,
            "isLeaf": False,
            "state": 1,
            "pickupIds": [],
            "lastUpdatedUserId": 1,
            "lastUpdatedTime": utc_now,
            "supportCod": False
        }
        bee_common_db.Areas.insert_one(data_1)

        for city, c_item in s_item.items():
            deep_2_start_id += 1
            code = region_code + "2" + str(deep_2_start_id)
            if mall_sub_county.get(state+";"+city):
                area_type = 2
            else:
                area_type = 1
            data_2 = {
                "_id": deep_2_start_id,
                "areaType": area_type,
                "name": city,
                "code": code,
                "postcode": None,
                "parentId": deep_1_start_id,
                "sort": deep_2_start_id,
                "deep": 2,
                "regionCode": region_code,
                "isSupportToDoor": False,
                "isLeaf": False,
                "state": 1,
                "pickupIds": [],
                "lastUpdatedUserId": 1,
                "lastUpdatedTime": utc_now,
                "supportCod": False
            }
            bee_common_db.Areas.insert_one(data_2)
            for area, a_item in c_item.items():
                deep_3_start_id += 1
                code = region_code + "3" + str(deep_3_start_id)
                data_3 = {
                    "_id": deep_3_start_id,
                    "areaType": a_item["type"],
                    "name": area,
                    "code": code,
                    "postcode": None,
                    "parentId": deep_2_start_id,
                    "sort": deep_3_start_id,
                    "deep": 3,
                    "regionCode": region_code,
                    "isSupportToDoor": a_item["supportDoor"],
                    "isLeaf": True,
                    "state": 1,
                    "pickupIds": a_item["shopIds"],
                    "lastUpdatedUserId": 1,
                    "lastUpdatedTime": utc_now,
                    "supportCod": False
                }
                for s_id in a_item["shopIds"]:
                    if shop_area_map.get(s_id):
                        shop_area_map[s_id].append(deep_3_start_id)
                    else:
                        shop_area_map[s_id] = [deep_3_start_id]
                bee_common_db.Areas.insert_one(data_3)
                kk_ad = a_item["kiLiAddress"]
                ct = bee_common_db.LogisticsAddress.find_one_and_update(
                    {"name": kk_ad[0], "deep": 1},
                    {"$addToSet": {"areaIds": deep_1_start_id}})
                if ct:
                    bee_common_db.LogisticsAddress.update_one(
                        {"parentId": ct["_id"], "name": kk_ad[1]},
                        {"$addToSet": {
                            "leafAreaIds": deep_3_start_id,
                            "areaIds": {
                                "$each": [deep_2_start_id, deep_3_start_id]}}}
                    )
    with open("shop_area_map.json", 'w', encoding="utf-8") as write_f:
        write_f.write(json.dumps(shop_area_map, indent=4, ensure_ascii=False))


def find_not_match_address():
    names_1, names_2, names_3 = [], [], []
    for it in bee_common_db.Areas.find({"regionCode": "KE", "deep": 3}):
        res = bee_common_db.LogisticsAddress.find_one(
            {"leafAreaIds": it["_id"]})
        if not res:
            name_2 = bee_common_db.Areas.find_one({"_id": it["parentId"]})
            name_1 = bee_common_db.Areas.find_one({"_id": name_2["parentId"]})
            names_3.append(it["name"])
            names_2.append(name_2["name"])
            names_1.append(name_1["name"])
            print(it["_id"])
    print("------------------------------------------------------------")
    for it in names_1:
        print(it)
    print("------------------------------------------------------------")
    for it in names_2:
        print(it)
    print("------------------------------------------------------------")
    for it in names_3:
        print(it)


def add_logistics_address():
    start_id = 0
    for it in bee_common_db.LogisticsAddress.find(
            {"deep": 2}).sort([("_id", -1)]).limit(1):
        start_id = it["_id"] + 1
    for area in bee_common_db.KiliArea.find({}):
        name = area["name"].strip()
        l_area = bee_common_db.LogisticsAddress.find_one(
            {"deep": 2, "name": name})
        if not l_area:
            print(area)
            city = bee_common_db.KiliCity.find_one({"id": area["parentId"]})
            l_city = bee_common_db.LogisticsAddress.find_one(
                {"deep": 1, "name": city["name"].strip()})
            if not l_city:
                print("not found count=%r" % city)
                continue
            data = {
                    "_id": start_id,
                    "regionCode": "KE",
                    "parentId": l_city["_id"],
                    "selfAreaId": area["id"],
                    "selfAreaCode": area["code"],
                    "providerId": "KiliExpress",
                    "name": name,
                    "deep": 2,
                    "isSupportToDoor": bool(area["supportToDoor"]),
                    "isSupportPickup": False,
                    "isLeaf": True,
                    "state": area["status"],
                    "areaIds": [],
                    "leafAreaIds": [],
                    "pickupIds": []
            }
            bee_common_db.LogisticsAddress.insert_one(data)
            print("add-town=%r" % data)
            start_id += 1


def verify_town_names():
    name_list = ["Baringo", "Tiaty", "Balambala", "Daadab", "Fafi", "Lagdera",
                 "Kindu Bay", "Kirinyaga", "Banissa", "Lafey", "Rahamu",
                 "Laisamis", "Horr", "Embu Town", "Thika", "Bamburi", "Kandara",
                 "Kanduyi", "Mathioya", "Wamba", "Samburu", "Galole", "Garsen",
                 "Tharaka", "Loima", "Turkana Town", "Vihiga Town", "Isiolo"]
    for name in name_list:
        res = bee_common_db.LogisticsAddress.find_one({"deep": 2, "name": name})
        if not res:
            print(name)


def update_logistics_address_area_id():
    data = [{1000031043: "Baringo",},{1000031044: "Baringo",},{1000031045: "Baringo",},{1000031046: "Baringo",},{1000031047: "Baringo",},{1000031048: "Baringo",},{1000031049: "Baringo",},{1000031050: "Baringo",},{1000031051: "Baringo",},{1000031065: "Tiaty",},{1000031066: "Tiaty",},{1000031067: "Tiaty",},{1000031068: "Tiaty",},{1000031069: "Tiaty",},{1000031070: "Tiaty",},{1000031071: "Tiaty",},{1000031208: "Balambala",},{1000031209: "Balambala",},{1000031210: "Balambala",},{1000031211: "Balambala",},{1000031212: "Balambala",},{1000031213: "Daadab",},{1000031214: "Daadab",},{1000031215: "Daadab",},{1000031216: "Daadab",},{1000031217: "Daadab",},{1000031218: "Daadab",},{1000031223: "Fafi",},{1000031224: "Fafi",},{1000031225: "Fafi",},{1000031226: "Fafi",},{1000031227: "Fafi",},{1000031228: "Fafi",},{1000031229: "Fafi",},{1000031230: "Fafi",},{1000031231: "Lagdera",},{1000031232: "Lagdera",},{1000031233: "Lagdera",},{1000031234: "Lagdera",},{1000031235: "Lagdera",},{1000031236: "Lagdera",},{1000031249: "Kindu Bay",},{1000031498: "Kirinyaga",},{1000031499: "Kirinyaga",},{1000031500: "Kirinyaga",},{1000031501: "Kirinyaga",},{1000031748: "Banissa",},{1000031749: "Banissa",},{1000031750: "Banissa",},{1000031751: "Banissa",},{1000031752: "Lafey",},{1000031753: "Lafey",},{1000031754: "Lafey",},{1000031760: "Rahamu",},{1000031761: "Rahamu",},{1000031762: "Rahamu",},{1000031763: "Rahamu",},{1000031777: "Laisamis",},{1000031778: "Laisamis",},{1000031779: "Laisamis",},{1000031780: "Laisamis",},{1000031788: "Horr",},{1000031789: "Horr",},{1000031790: "Horr",},{1000031791: "Horr",},{1000031792: "Horr",},{1000031822: "Embu Town",},{1000031825: "Thika",},{1000031892: "Bamburi",},{1000031928: "Kandara",},{1000031929: "Kandara",},{1000031930: "Kandara",},{1000031931: "Kandara",},{1000031932: "Kandara",},{1000031933: "Kandara",},{1000031947: "Kanduyi",},{1000031953: "Mathioya",},{1000031954: "Mathioya",},{1000031955: "Mathioya",},{1000032214: "Wamba",},{1000032215: "Wamba",},{1000032216: "Wamba",},{1000032217: "Wamba",},{1000032218: "Wamba",},{1000032219: "Samburu",},{1000032220: "Samburu",},{1000032221: "Samburu",},{1000032222: "Samburu",},{1000032223: "Samburu",},{1000032224: "Samburu",},{1000032278: "Galole",},{1000032279: "Galole",},{1000032280: "Galole",},{1000032281: "Galole",},{1000032282: "Garsen",},{1000032283: "Garsen",},{1000032284: "Garsen",},{1000032285: "Garsen",},{1000032286: "Garsen",},{1000032287: "Garsen",},{1000032298: "Tharaka",},{1000032299: "Tharaka",},{1000032300: "Tharaka",},{1000032301: "Tharaka",},{1000032302: "Tharaka",},{1000032322: "Loima",},{1000032323: "Loima",},{1000032324: "Loima",},{1000032325: "Loima",},{1000032334: "Turkana Town",},{1000032335: "Turkana Town",},{1000032336: "Turkana Town",},{1000032337: "Turkana Town",},{1000032386: "Vihiga Town",},{1000032387: "Vihiga Town",},{1000032408: "Vihiga Town",},{1000032409: "Vihiga Town",},{1000032410: "Vihiga Town",},{1000032411: "Vihiga Town",},{1000032412: "Vihiga Town",},{1000032413: "Vihiga Town",},{1000032418: "Isiolo",},{1000032419: "Isiolo",}]
    for it in data:
        for k, v in it.items():
            area = bee_common_db.Areas.find_one({"_id": k})
            if not area:
                print(area)
                continue
            bee_common_db.LogisticsAddress.update_one(
                {"deep": 2, "name": v},
                {"$addToSet": {"leafAreaIds": k,
                               "areaIds": {"$each": [k, area["parentId"]]}}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    bee_common_db = get_db(K_DB_URL, env, "BeeCommon")

    # 查找没有匹配到物流二级地址的fms的三级地址库
    find_not_match_address()


    # update_logistics_address_area_id()
    # print("create_kili_express_address success")
