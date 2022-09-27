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
_DEFAULT_CONFIG_FILE = '../config.json'

env = "prd"


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


def shut_down_pf_address(area_id, area_name):
    shut_down_update = {"$set": {"enabled": False, "visible": False}}
    res = common_db.area.update_one(
        {"name": area_name, "regionId": 1, "id": area_id}, shut_down_update)
    print(res.matched_count, res.modified_count)
    if res.modified_count < 1:
        print("-------------error-----------area_id=%d" % area_id)


def update_e_courier_map_address(
        state_id, pf_area_id, city, thana, area, postcode):
    ea_query = {
        "postCode": postcode, "city": city, "thana": thana, "area": area}
    if order_db.eCourierAddress.find_one(ea_query):
        order_db.eCourierAddress.update_one(
            ea_query, {"$push": {"pfAreaId": pf_area_id}})
        return
    res_di = order_db.eCourierAddress.find_one({"city": city})
    if not res_di:
        state_di = common_db.state.find_one({"id": state_id})
        state_name = state_di["name"]
    else:
        state_name = res_di["division"]
    order_db.eCourierAddress.update_one(
        {"pfAreaId": pf_area_id}, {"$pull": {"pfAreaId": pf_area_id}})

    order_db.eCourierAddress.insert_one(
        {
            "division": state_name,
            "city": city,
            "thana": thana,
            "area": area,
            "postCode": postcode,
            "payments": [
                "COD",
                "MPAY",
                "CCRD"
            ],
            "pfAreaId": [
                pf_area_id
            ]
        }
    )


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


def update_the_city_name(b_name, a_name):
    query = {"name": b_name, "regionId": 1}
    update = {"$set": {"name": a_name, "enabled": True, "visible": True}}
    common_db.city.update_one(query, update)


def append_bd_area_and_update_ec_address(
        state_id, city_name, area_name, postage, e_city, e_tha, e_area,
        postcode):
    city_di = common_db.city.find_one({"name": city_name, "regionId": 1})
    if not city_di:
        city_id = get_city_last_id() + 1
        city_index = get_bd_city_last_index() + 1
        c_data = {
            "index": city_index,
            "name": city_name,
            "minAppVersion": 15,
            "stateId": state_id,
            "regionId": 1,
            "id": city_id,
            "enabled": True,
            "visible": True
        }
        common_db.city.insert_one(c_data)
    else:
        city_id = city_di["id"]
    open_update = {"$set": {"enabled": True, "visible": True}}
    area_id = None
    area_1 = common_db.area.find_one({"name": area_name, "regionId": 1})
    area_have = False
    if area_1:
        city_1 = common_db.city.find_one(
            {"id": area_1["cityId"], "name": city_name})
        if city_1:
            common_db.area.update_one({"id": area_1["id"]}, open_update)
            common_db.city.update_one({"id": city_1["id"]}, open_update)
            area_id = area_1["id"]
            area_have = True
    if not area_have:
        area_id = get_bd_area_last_id() + 1
        index = get_bd_area_last_index() + 1
        area_data = {
            "postage": postage,
            "index": index,
            "name": area_name,
            "minAppVersion": 15,
            "stateId": state_id,
            "regionId": 1,
            "cityId": city_id,
            "supportCod": False,
            "id": area_id,
            "enabled": True,
            "visible": True,
            "ett": 2
            }
        common_db.area.insert_one(area_data)

    update_e_courier_map_address(
        state_id, area_id, e_city, e_tha, e_area, postcode)


def excel_pf_data(file):
    data = xlrd.open_workbook(file)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    excel_list = []
    for row in range(1, nrows):
        row_data = []
        for col in range(ncols):
            if table.cell(row, 13).value not in ["修正", "停止支持", "新增"]:
                continue
            cell_value = table.cell(row, col).value
            if type(cell_value) == str:
                cell_value = cell_value.strip()
            row_data.append(cell_value)

        if not row_data or set(row_data) == {''}:
            continue
        excel_list.append(row_data)

    new_areas = set()
    for it in excel_list:
        if it[13] == "新增":
            new_areas.add(it[5])
    print(new_areas)

    return excel_list


def update_the_data(excel_list):
    for it in excel_list:
        if it[13] == "停止支持":
            shut_down_pf_address(int(it[4]), it[5])
        elif it[13] == "修正":
            update_e_courier_map_address(
                int(it[0]), int(it[4]), it[9], it[10], it[11], str(int(it[12])))
        elif it[13] == "新增":
            append_bd_area_and_update_ec_address(
                int(it[0]), it[3], it[5], int(it[6]), it[9], it[10], it[11],
                str(int(it[12])))


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

    update_the_city_name("Rangmati", "Rangamati")
    pf_data = excel_pf_data(file="./PerFee_BD-update0207.xlsx")
    update_the_data(pf_data)

    print("---------------------------success-------------------------------")

