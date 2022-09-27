# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from puanchen import HeraldMQ
from datetime import datetime

_DEFAULT_LOG_FILE = 'order_param_rate_app.log'
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


def load_cities(filename):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def update_params_order():
    last_id = 100
    for it in order_db.parameter.find().sort([("id", -1)]).limit(1):
        last_id = it["id"]
    last_id += 1
    order_db.parameter.insert_one(
        {
            "id": last_id,
            "regionId": 3,
            "name": "PAY_GATEWAY_FEE_RATE_KBZ",
            "value": "0.015",
            "dataType": "float",
            "paramModule": "pay_gateway_fee_rate"
        }
    )
    last_id += 1
    order_db.parameter.insert_one(
        {
            "id": last_id,
            "regionId": 3,
            "name": "MAXIMUM_SINGLE_FEE_KBZ",
            "value": "99999999",
            "dataType": "int",
            "paramModule": "pay_gateway_fee_rate"
        }
    )


def retain_decimal_places(num, digits=2):
    if "." in str(num):
        num_x, num_y = str(num).split('.')
        num = float(num_x + '.' + num_y[0: digits])

    return num


def fix_statistics_data():
    for it in statistics_db.ClearingOrder.find({"regionId": 3, "payMethod": 1}):
        if not it.get("payFee"):
            pay_fee = retain_decimal_places(it["payAmount"]*0.015)
            statistics_db.ClearingOrder.update_one(
                {"saleOrderId": it["saleOrderId"]},
                {"$set": {"payFee": pay_fee}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    statistics_db = get_db(config, env, "Statistics")

    update_params_order()
    fix_statistics_data()

    print("---------------------------success-------------------------------")

