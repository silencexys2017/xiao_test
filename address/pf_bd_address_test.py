# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import requests
import time
import xlrd
from operator import itemgetter

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'

env = "prd"
API_KEY = "9eSx"
API_SECRET = "4Y1B4"
USER_ID = "F2901"
Content_type = "application/json"
base_url = "https://staging.ecourier.com.bd/api"
# base_url = "https://backoffice.ecourier.com.bd/api"
shut_down_areas = [
    {"cityId": 2, "name": {"$in": ["Demra", "Keraniganj Sadar"]}},
    {"cityId": 21, "name": {"$in": ["Kashem Cotton Mills", "Kashmipur"]}},
    {"cityId": 3, "name": {"$in": ["Faridpur Sadar"]}},
    {"cityId": 5, "name": {"$in": ["Gopalganj Sadar"]}},
    {"cityId": 10, "name": {"$in": ["Manikganj Sadar"]}},
    {"cityId": 16, "name": {"$in": ["Monohordi Hatirdia", "Monohordi Katabaria",
                                    "Narsingdi College"]}}]

shut_down_cities = [
    "Lakshimpur", "Chapai Nawabganj", "Naogaon", "Jhalakati",
    "Bogra", "Manikganj", "Sirajganj", "Lalmonirhat", "Natore",
    "Chattogram City", "Joypurhat", "Pabna", "Faridpur", "Pirojpur",
    "Gopalganj", "Gaibandha", "Bandarban", "Meherpur", "Bagherhat", "Rangmati",
    "Dinajpur", "Kurigram"
]

HEADERS = {
            "API-SECRET": API_SECRET,
            "API-KEY": API_KEY,
            "USER-ID": USER_ID,
            "Content-Type": Content_type
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


def load_cities(filename):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def get_city_list():
    body = {}
    url = base_url + "/city-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])
    return result
    # return json.dumps(result)


def retry_post_requests(params, url):
    error_info = []
    retry_times = 0
    is_success = False
    result = {}
    while retry_times < 10 and not is_success:
        try:
            retry_times += 1
            result = requests.post(
                url, params=params, headers=HEADERS, timeout=150).json()
            is_success = True
        except json.decoder.JSONDecodeError as it:
            time.sleep(30)
            print("error info=%s, retry_times=%s" % (it, retry_times))
    if result.get("success") not in [True]:
        if url != "https://backoffice.ecourier.com.bd/api/area-list":
            error_info.append((url, params, result.get("errors")))
        else:
            error_info.append(params.get("postcode"))
        result = {"message": []}
    return result


def get_thana_list(city):
    body = {
        "city": city
    }

    url = base_url + "/thana-list"
    return retry_post_requests(body, url)


def get_area_list_by_post_code(postcode):
    body = {
        "postcode": postcode
    }

    url = base_url + "/area-list"
    return retry_post_requests(body, url)


def get_post_code_list(city, thana):
    body = {
        "city": city,
        "thana": thana
    }
    url = base_url + "/postcode-list"
    return retry_post_requests(body, url)


def delete_e_courier_address():
    order_db.eCourierAddress.delete_many({"postCode": {"$exists": True}})


def insert_e_courier_address(data):
    order_db.eCourierAddress.insert_one(data)


def find_e_courier_change_address():
    ex_areas = []
    for it in order_db.eCourierAddressMapping.find():
        res = common_db.area.find_one({"name": it.get("area")})
        # res = order_db.eCourierAddress.find_one(
        #     {"city": it["city"], "area": it["area"],
        #      "thana": {"$exists": False}})
        if not res:
            ex_areas.append({"city": it["city"], "area": it["area"]})
    print(ex_areas)


def generate_e_courier_address(address, division):
    order_db.eCourierAddress.delete_many({})
    area_set = set()
    for key, value in address.items():
        for it in value:
            if it.get("area") in area_set:
                continue
            area_set.add(it.get("area"))
            order_db.eCourierAddress.insert_one({
                "division": division[key],
                "city": key, "thana": it.get("thana"),
                "area": it.get("area"), "postCode": it.get("postcode"),
                "payments": it["payments"] if it.get("payments") else []
            })


def update_name():
    common_db.city.update_one(
        {"name": "Barisal"}, {"$set": {"name": "Barishal"}})
    common_db.state.update_one(
        {"name": "Barisal"}, {"$set": {"name": "Barishal"}})
    common_db.city.update_one({"name": "Lakshmipur"}, {"$set": {"stateId": 2}})


def get_bd_city_last_index():
    for it in common_db.city.find({"regionId": 1}).sort(
            [("index", -1)]).limit(1):
        return it["index"]


def get_city_last_id():
    for it in common_db.city.find().sort([("id", -1)]).limit(1):
        return it["id"]


def get_bd_area_last_id():
    for it in common_db.area.find().sort([("id", -1)]).limit(1):
        return it["id"]


def get_bd_area_last_index():
    for it in common_db.area.find({"regionId": 1}).sort(
            [("index", -1)]).limit(1):
        return it["index"]


def get_bd_city_map():
    for it in common_db.city.find({"regionId": 1}):
        city_map[it["name"]] = it


def get_bd_division_map():
    for it in common_db.state.find({"regionId": 1}):
        division_map[it["name"]] = it["id"]


def append_bd_city(city_li):
    city_id = get_city_last_id()
    index = get_bd_city_last_index()
    for it in city_li:
        city_di = common_db.city.find_one({"name": it, "regionId": 1})
        if not city_di:
            city_id += 1
            index += 1
            data_city = {
                "index": index, "name": it, "minAppVersion": 11,
                "stateId": division_map[division_city_map[it]],
                "regionId": 1, "id": city_id, "enabled": True,
                "visible": True}
            common_db.city.insert_one(data_city)
            city_map[it] = data_city
        else:
            common_db.city.find_one_and_update(
                {"name": it, "regionId": 1},
                {"$set": {"enabled": True, "visible": True}})


def append_bd_area_and_update_ec_address(address_li):
    area_id = get_bd_area_last_id()
    index = get_bd_area_last_index()
    area_ids = []
    for it in address_li:
        area_e = order_db.eCourierAddress.find_one({"area": it[4]})
        if it[5] in ["New", 1]:
            area_id += 1
            index += 1
            data_area = {
                "regionId": 1, "postage": int(it[3]), "index": index,
                "name": it[2],  "minAppVersion": 11,
                "stateId": division_map[division_city_map[
                    city_area_map[it[2]]]],
                "cityId": city_map[city_area_map[it[2]]]["id"],
                "id": area_id, "supportCod": True,  "enabled": True,
                "visible": True, "ett": 7
            }
            common_db.area.insert_one(data_area)
            a_ids = [area_id]
            if area_e.get("pfAreaId"):
                a_ids = a_ids + area_e.get("pfAreaId")
            order_db.eCourierAddress.find_one_and_update(
                {"area": it[4]}, {"$set": {"pfAreaId": a_ids}})
        else:
            query_di = {"regionId": 1, "name": {"$regex": "^" + it[2] + "$",
                                                "$options": "i"}}
            area_di = common_db.area.find_one(query_di)
            common_db.area.find_one_and_update(
                query_di,
                {"$set": {"enabled": True, "visible": True, "name": it[2]}})
            a_ids = [area_di["id"]]
            if area_e.get("pfAreaId"):
                a_ids = a_ids + area_e.get("pfAreaId")
            order_db.eCourierAddress.find_one_and_update(
                {"area": it[4]}, {"$set": {"pfAreaId": a_ids}})

            area_ids.append(area_di["id"])
    return area_ids


def excel_pf_data(file):
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    excel_list = []
    for row in range(1, nrows):
        row_data = []
        for col in range(ncols):
            cell_value = table.cell(row, col).value
            if type(cell_value) == str:
                cell_value = cell_value.strip()
            row_data.append(cell_value)
        if set(row_data) == {''}:
            continue
        excel_list.append(row_data)
        row_data[2] = row_data[2].capitalize()
        com_address.append(
            (row_data[0], row_data[1], row_data[2], row_data[3], row_data[8],
             row_data[9]))
        division_city_map[row_data[1]] = row_data[0]
        city_area_map[row_data[2]] = row_data[1]
        pf_cities.add(row_data[1])
        if row_data[2] in pf_areas:
            repeat_areas.append((row_data[1], row_data[2]))
        else:
            pf_areas.append(row_data[2])

    return excel_list


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
    member_db = get_db(config, env, "Member")

    addresses = load_cities("./ec_address.json")
    divisions = load_cities("./bd_division_district.json")
    # generate_e_courier_address(addresses, divisions)
    # update_name()
    com_address = []
    division_city_map = {}
    city_area_map = {}
    city_map = {}
    division_map = {}
    pf_cities = set()

    pf_areas = []
    repeat_areas = []
    pf_data = excel_pf_data(file="PerFee_Address_BD-20201028 update.xlsx")
    com_address = sorted(com_address, key=itemgetter(0, 1, 2))
    # get_bd_city_map()
    # get_bd_division_map()
    # append_bd_city(pf_cities)
    # area_ids = append_bd_area_and_update_ec_address(com_address)
    print(repeat_areas)
    print(len(pf_areas))

    print("---------------------------success-------------------------------")

