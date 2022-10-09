# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json


_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'


Dhaka = ["Gazipur", "Kishoreganj", "Madaripur", "Narayanganj",
         "Narsingdi", "Rajbari", "Savar", "Tangail", "Dhaka-North",
         "Dhaka-South"]

Chattogram = ["Brahmanbaria", "Chandpur", "Chattogram", "Comilla",
              "Cox's Bazar", "Feni", "Lakshmipur", "Noakhali"]
Other = ["Barishal", "Bhola", "Jhalakathi", "Bagerhat", "Chuadanga", "Jessore",
         "Jhenaidah", "Khulna", "Kushtia", "Magura", "Narail", "Satkhira",
         "Jamalpur", "Mymensingh", "Netrokona", "Sherpur", "Bogura",
         "Chapainawabganj", "Rajshahi", "Rangpur", "Sunamganj", "Sylhet",
         "Moulvibazar"]
Barishal = ["Barishal", "Bhola", "Jhalakathi"]

Khulna = ["Bagerhat", "Chuadanga", "Jessore", "Jhenaidah", "Khulna", "Kushtia",
          "Magura", "Narail", "Satkhira"]

Mymensingh = ["Jamalpur", "Mymensingh", "Netrokona", "Sherpur"]

Rajshahi = ["Bogura", "Chapainawabganj", "Rajshahi"]

Rangpur = ["Rangpur"]

Sylhet = ["Sunamganj", "Sylhet", "Moulvibazar"]


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


def update_naraiil():
    kh_state_id = common_db.state.find_one({"name": "Khulna"})["id"]
    na_city = common_db.city.find_one(
        {"name": "Naraiil", "regionId": 1})
    if not na_city:
        return
    na_city_id = na_city["id"]
    common_db.city.update_one(
        {"id": na_city_id},
        {"$set": {"name": "Narail", "stateId": kh_state_id}})
    common_db.area.update_one({"cityId": na_city_id},
                              {"$set": {"stateId": kh_state_id}})


def update_mm_cod_area():
   dk_state_id = common_db.state.find_one({"name": "Dhaka"})["id"]
   city_1 = common_db.city.distinct(
       "id", {"name": {"$nin": Dhaka}, "stateId": dk_state_id})
   res_1 = common_db.area.update_many(
       {"cityId": {"$in": city_1}}, {"$set": {"supportCod": False}})
   print(res_1.matched_count)
   print(res_1.modified_count)

   cha_state_id = common_db.state.find_one({"name": "Chattogram"})["id"]
   city_2 = common_db.city.distinct(
       "id", {"name": {"$nin": Chattogram}, "stateId": cha_state_id})
   res_2 = common_db.area.update_many(
       {"cityId": {"$in": city_2}}, {"$set": {"supportCod": False}})
   print(res_2.matched_count)
   print(res_2.modified_count)

   city_3 = common_db.city.distinct("id", {"name": {"$in": Other}})
   res_3 = common_db.area.update_many(
       {"cityId": {"$in": city_3}}, {"$set": {"supportCod": True}})
   print(res_3.matched_count)
   print(res_3.modified_count)


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
    update_naraiil()
    update_mm_cod_area()