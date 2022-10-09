# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = '../sslcommerz_refund/config.json'


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


def add_dispatch_package_lack():
    pg_ids = logistics_db.ExpressPackage.distinct("packageId", {"status": 1})
    pg_di = {}
    so_ids = []
    query = {"id": {"$in": pg_ids}, "status": {"$nin": [1, -2]}}
    for it in order_db.ShipPackage.find(query):
        pg_di[it["id"]] = it
        so_ids.append(it["saleOrderId"])
    opt_di = {}
    for it in order_db.OrderOperateLog.find({"saleOrderId": {"$in": so_ids}}):
        for ite in it.get("packageLogs")[0].get("logs"):
            if ite.get("operateCode") == 4:
                opt_di[it["saleOrderId"]] = ite["operatorId"]
    print(opt_di)

    for key, value in pg_di.items():
        logistics_db.ExpressPackage.update_one(
            {"packageId": key}, {"$set": {
                "status": 2, "deliveryId": value.get("deliveryId"),
                "deliveryCode": value.get("deliveryCode"),
                "shipOperatorId": opt_di.get(value["saleOrderId"], 0),
                "shippedAt": value.get("shippedAt")}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    logistics_db = get_db(config, env, "Logistics")

    add_dispatch_package_lack()