# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import csv
import xlrd
from operator import itemgetter

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'
params = [{
        "name": "ORDER_COD_ENABLE",
        "value": "1",
        "dataType": "bool",
        "paramModule": "order"
},
{
        "name": "ORDER_MUST_VERIFIED",
        "value": "1",
        "dataType": "bool",
        "paramModule": "order"
},
{
        "name": "ORDER_VAT_SWITCH",
        "value": "0",
        "dataType": "bool",
        "paramModule": "order"
},
{
        "name": "ORDER_TAX_RATE",
        "value": "0.071",
        "dataType": "float",
        "paramModule": "order"
},
{
        "name": "POSTAGE_REMISSION_NOTIFY_ENABLE",
        "value": "1",
        "dataType": "bool",
        "paramModule": "postage_discount"
},
{
        "name": "POSTAGE_ONLINE_REMISSION_LIMIT",
        "value": "1000",
        "dataType": "int",
        "paramModule": "postage_discount"
},
{
        "name": "POSTAGE_ONLINE_DISCOUNT",
        "value": "0",
        "dataType": "int",
        "paramModule": "postage_discount"
},
{
        "name": "POSTAGE_REMISSION_NOTIFY",
        "value": "To provide convenience to online payment orders, order paid online will get free delivery if the order amount is more than 1,000 TK. The preference is not for some products set by sellers or the order cancelled for no reason.",
        "dataType": "str",
        "paramModule": "postage_discount"
},
{
        "name": "POSTAGE_ONLINE_REMISSION_ENABLE",
        "value": "1",
        "dataType": "bool",
        "paramModule": "postage_discount"
},
{
        "name": "POSTAGE_COD_DISCOUNT",
        "value": "0",
        "dataType": "int",
        "paramModule": "postage_discount"
},
{
        "name": "ORDER_ONLINE_GMO_ENABLE",
        "value": "1",
        "dataType": "bool",
        "paramModule": "order"
},
{
        "name": "ORDER_OPERATION_FEE_CN",
        "value": "26",
        "dataType": "int",
        "paramModule": "order_operation_fee"
},
{
        "name": "ORDER_OPERATION_FEE_BD_SELLER_DELIVERY",
        "value": "0",
        "dataType": "int",
        "paramModule": "order_operation_fee"
},
{
        "name": "LIQUIDATION_SETTINGS_DATE",
        "value": "6",
        "dataType": "int",
        "paramModule": "liquidation_settings"
},
{
        "name": "STORE_COMMISSION_RATE_CN",
        "value": "0.1",
        "dataType": "float",
        "paramModule": "store_commission_rate"
},
{
        "name": "PLATFORM_COLLECTED_FREIGHT_CN_STORE",
        "value": "0",
        "dataType": "bool",
        "paramModule": "freight_settlement"
},
{
        "name": "PLATFORM_COLLECTED_FREIGHT_BD_STORE_PLATFORM_DELIVERY",
        "value": "0",
        "dataType": "bool",
        "paramModule": "freight_settlement"
},
{
        "name": "STORE_COMMISSION_RATE_BD",
        "value": "0.1",
        "dataType": "float",
        "paramModule": "store_commission_rate"
},
{
        "name": "MAXIMUM_SINGLE_FEE_GMO",
        "value": "99999999",
        "dataType": "int",
        "paramModule": "pay_gateway_fee_rate"
},
{
        "name": "PAY_GATEWAY_FEE_RATE_GMO",
        "value": "0.02",
        "dataType": "float",
        "paramModule": "pay_gateway_fee_rate"
},
{
        "name": "PAY_GATEWAY_FEE_RATE_COD",
        "value": "0.01",
        "dataType": "float",
        "paramModule": "pay_gateway_fee_rate"
},
{
        "name": "PLATFORM_COLLECTED_FREIGHT_BD_STORE_SELLER_DELIVERY",
        "value": "1",
        "dataType": "bool",
        "paramModule": "freight_settlement"
},
{
        "name": "ORDER_OPERATION_FEE_BD_PLATFORM_DELIVERY",
        "value": "0",
        "dataType": "int",
        "paramModule": "order_operation_fee"
},
{
        "name": "MAXIMUM_SINGLE_FEE_COD",
        "value": "99999999",
        "dataType": "int",
        "paramModule": "pay_gateway_fee_rate"
},
{
        "name": "PRODUCT_LIMIT_COD_AMOUNT",
        "value": "3000",
        "dataType": "int",
        "paramModule": "cod_rule"
},
{
        "name": "BATCH_LIMIT_COD_AMOUNT",
        "value": "6000",
        "dataType": "int",
        "paramModule": "cod_rule"
}]


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


def delete_jpn_address():
    query = {"regionId": 5, "minAppVersion": 30}
    common_db.state.delete_many(query)
    common_db.city.delete_many(query)
    common_db.area.delete_many(query)


def get_csv_data(path):
    # utf-8-sig
    result = {}
    with open(path, "r+", encoding="Shift_JIS") as f:
        csv_read = csv.reader(f)
        for line in csv_read:
            if not result.get((line[6], line[3])):
                result[(line[6], line[3])] = {(line[7], line[4]): [
                    (line[2], (line[8], line[5]))]}
            else:
                if result[(line[6], line[3])].get((line[7], line[4])):
                    result[(line[6], line[3])][(line[7], line[4])].append(
                        (line[2], (line[8], line[5])))
                else:
                    result[(line[6], line[3])][(line[7], line[4])] = [
                        (line[2], (line[8], line[5]))]

    # with open('jpn_address.json', 'w', encoding="Shift_JIS") as file_obj:
    #     json.dump(result, file_obj)
    # print(file_obj)
    return result


def import_data_to_database(data_di):
    region_id = 5
    state_id = get_state_last_id()
    city_id = get_city_last_id()
    area_id = get_area_last_id()
    state_index = get_state_last_index(region_id)
    city_index = get_city_last_index(region_id)
    area_index = get_area_last_index(region_id)
    for key, val in data_di.items():
        state_id += 1
        state_index += 1
        state_data = {
            "id": state_id,
            "index": state_index,
            "regionId": region_id,
            "name": key[0],
            "minAppVersion": 30,
            "enabled": True,
            "visible": True
        }
        common_db.state.insert_one(state_data)
        for k, v in val.items():
            city_id += 1
            city_index += 1
            city_data = {
                "id": city_id,
                "index": city_index,
                "name": k[0],
                "stateId": state_id,
                "regionId": region_id,
                "minAppVersion": 30,
                "enabled": True,
                "visible": True
            }
            common_db.city.insert_one(city_data)
            for it in v:
                area_index += 1
                area_id += 1
                area_data = {
                    "id": area_id,
                    "index": area_index,
                    "name": it[1][0],
                    "postage": 50,
                    "postcode": it[0],
                    "minAppVersion": 30,
                    "regionId": region_id,
                    "stateId": state_id,
                    "cityId": city_id,
                    "supportCod": True,
                    "enabled": True,
                    "visible": True,
                    "ett": 2
                }
                common_db.area.insert_one(area_data)


def get_region_last_index():
    for it in common_db.region.find().sort([("index", -1)]).limit(1):
        return it["index"]
    return 0


def get_region_last_id():
    for it in common_db.region.find().sort([("id", -1)]).limit(1):
        return it["id"]
    return 0


def get_state_last_index(region_id):
    for it in common_db.state.find({"regionId": region_id}).sort(
            [("index", -1)]).limit(1):
        return it["index"]
    return 0


def get_state_last_id():
    for it in common_db.state.find().sort([("id", -1)]).limit(1):
        return it["id"]
    return 0


def get_city_last_id():
    for it in common_db.city.find().sort([("id", -1)]).limit(1):
        return it["id"]
    return 0


def get_city_last_index(region_id):
    for it in common_db.city.find({"regionId": region_id}).sort(
            [("index", -1)]).limit(1):
        return it["index"]
    return 0


def get_area_last_id():
    for it in common_db.area.find().sort([("id", -1)]).limit(1):
        return it["id"]
    return 0


def get_area_last_index(region_id):
    for it in common_db.area.find({"regionId": region_id}).sort(
            [("index", -1)]).limit(1):
        return it["index"]
    return 0


def add_initial_params():
    order_db.parameter.delete_many({"regionId": 5})
    start_id = 0
    for it in order_db.parameter.find().sort([("id", -1)]).limit(1):
        start_id = it["id"]
    for it in params:
        start_id = start_id + 1
        it["id"] = start_id
        it["regionId"] = 5
        order_db.parameter.insert_one(it)

    common_db.region.insert_one(
        {
            "id": 5,
            "callingCode": "81",
            "code": "JP",
            "name": "Japan",
            "intro": "The most developed nation in Asia",
            "flag": "https://pimg.perfee.com/country-flags/5.png",
            "currencyId": 392,
            "currencySymbol": "円",
            "currencyConversion": 1,
            "language": "ja",
            "timeZone": "Asia/Tokyo",
            "currency": "JPY",
            "index": 1,
            "minAppVersion": 1
        }
    )


def delete_jpn_data():
    for it in order_db.list_collection_names():
        order_db[it].delete_many({})

    common_db.region.delete_many({"id": {"$ne": 2}})
    common_db.state.delete_many({"regionId": {"$ne": 2}})
    common_db.city.delete_many({"regionId": {"$ne": 2}})
    common_db.area.delete_many({"regionId": {"$ne": 2}})

    for it in seller_db.list_collection_names():
        if it in ["Page"]:
            continue
        seller_db[it].delete_many({})

    for it in statistics_db.list_collection_names():
        statistics_db[it].delete_many({})

    for it in logistics_db.list_collection_names():
        logistics_db[it].delete_many({})


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
    seller_db = get_db(config, env, "Seller")
    statistics_db = get_db(config, env, "Statistics")
    logistics_db = get_db(config, env, "Logistics")

    delete_jpn_data()
    add_initial_params()
    delete_jpn_address()
    address_di = get_csv_data(path="KEN_ALL.CSV")
    import_data_to_database(address_di)

    print("---------------------------success-------------------------------")

