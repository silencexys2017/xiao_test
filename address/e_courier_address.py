# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import requests
import time
import xlrd

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'

env = "prd"
API_KEY = "9eSx"
API_SECRET = "4Y1B4"
USER_ID = "F2901"
Content_type = "application/json"
# base_url = "https://staging.ecourier.com.bd/api"
base_url = "https://backoffice.ecourier.com.bd/api"


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
    error_info = []
    if result.get("success") not in [True]:
        if url != "https://backoffice.ecourier.com.bd/api/area-list":
            error_info.append((url, params, result.get("errors")))
        else:
            error_info.append(params.get("postcode"))
        result = {"message": error_info}
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
    for it in order_db.eCourierAddress.find({"thana": {"$exists": False}}):
        res = order_db.eCourierAddress.find_one(
            {"city": it["city"], "area": it["area"], "thana": {"$exists": True}})
        if not res:
            ex_areas.append({"city": it["city"], "area": it["area"]})
    print(ex_areas)


def find_multi_map_address():
    area_li = []
    ex_areas = []
    for it in order_db.eCourierAddress.find({"thana": {"$exists": True}}):
        if it.get("area"):
            if it.get("area") in area_li:
                ex_areas.append(it["area"])
            else:
                area_li.append(it.get("area"))
    print(ex_areas)


def get_e_courier_address_by_api():
    error_info = []
    address_set = set()
    cities = {it.get("name") for it in get_city_list()}
    for item in cities:
        thana_set = {it.get("name") for it in get_thana_list(item)["message"]}
        for ite in thana_set:
            code_set = {it.get("name") for it in get_post_code_list(
                item, ite)["message"]}
            for it in code_set:
                areas = {i.get("name") for i in get_area_list_by_post_code(
                    it)["message"]}
                if not areas:
                    data = {"city": item, "thana": ite, "postCode": it}
                    print(data)
                    address_set.add((item, ite, it))
                    # insert_e_courier_address(data)
                else:
                    for i in areas:
                        data = {"city": item, "thana": ite, "postCode": it,
                                "area": i}
                        address_set.add((item, ite, it, i))
                        print(data)
                        # insert_e_courier_address(data)
    for it in address_set:
        if len(it) == 3:
            insert_e_courier_address(
                {"city": it[0], "thana": it[1], "postCode": it[2]})
        elif len(it) == 4:
            insert_e_courier_address(
                {"city": it[0], "thana": it[1], "postCode": it[2],
                 "area": it[3]})

    print(error_info)


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    # find_e_courier_change_address()
    # find_multi_map_address()
    # delete_e_courier_address()

    print("---------------------------success-------------------------------")



