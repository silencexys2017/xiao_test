# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from puanchen import HeraldMQ
from datetime import datetime

_DEFAULT_LOG_FILE = 's328_app.log'
_DEFAULT_CONFIG_FILE = '../config.json'

mq_data = {
    "dev": ('rabbitmq', 5672, 'rmq-dev', '7M9Yrym4L9G6cxhNe9Xf', 'perfee-dev'),
    "test": ('rabbitmq', 5672, 'rmq-test', 'ALpW854bZ29HrAzjce8v',
             'perfee-test'),
    "prd": ('rabbitmq', 5672, 'rmq-prd', 'a3zWdf2X7xuEPWg259Xb', 'perfee-prd')}
host = "10.20.25.177"


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


def get_rmq(env):
    data = mq_data.get(env)
    return HeraldMQ(host, data[1], data[4], data[2], data[3])


def get_queue_name(env):
    return "goods-to-es-normal-%s" % env


def update_seller_related(store_id, region_id):
    query = {"storeId": store_id, "regionId": region_id}
    ss_di = seller_db.StoreStation.find_one(query)
    if not ss_di:
        raise Exception("The Store does not exist.")
    seller_id = ss_di["sellerId"]
    if ss_di["isBaseStation"]:
        seller_db.StoreStation.update_many(
            query, {"$set": {"status": 1}, "$unset": {"closedAt": ""}})
        seller_db.StoreOperateLog.delete_one(query)
        seller_db.SellerLogin.update_one(
            {"sellerId": seller_id, "accountType": 1}, {"$set": {"status": 1}})


def update_goods_related(store_id, region_id):
    query = {"status.%s" % region_id: {"$exists": True}, "storeId": store_id}

    update = {
        "$currentDate": {"updatedAt": True},
        "$set": {
            "status.%s" % region_id: 1
        }
    }

    goods_db.SpecOfListing.update_many(query, update)

    query_1 = {
        "status.%s" % region_id: {"$exists": True}, "storeId": store_id
    }

    update_1 = {
        "$currentDate": {"updatedAt": True},
        "$set": {
            "status.%s" % region_id: 1
        }
    }

    goods_db.SpecOfSku.update_many(query_1, update_1)


def send_msg_to_queue(queue_name, store_id, region_id):
    query_2 = {"storeId": store_id,
               "status.%s" % region_id: {"$exists": True}}
    update_data = {
        "status.%s" % region_id: 1}
    message_body = json.dumps(
        {
            'operation': 'bulk_update',
            'data': {"query": query_2, "update_data": update_data}
        }
    )
    rmq_con.send_message(queue_name, message_body)


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    common_db = get_db(config, env, "Common")
    seller_db = get_db(config, env, "Seller")
    goods_db = get_db(config, env, "Goods")
    rmq_con = get_rmq(env)
    queue_name = get_queue_name(env)
    update_seller_related(store_id=395, region_id=1)
    update_goods_related(store_id=395, region_id=1)
    send_msg_to_queue(queue_name, store_id=395, region_id=1)

    print("---------------------------success-------------------------------")

