# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from threading import Thread
from datetime import datetime

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


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def set_up_goods_prepayment():
    goods_db.SpecOfListing.update_many(
        {"status.1": {"$exists": True}, "prepayment.1": {"$exists": False}},
        {"$set": {
            "prepayment.1": {
                "state": 1,
                "prepaymentRatio": 1,
                "isSupportMergeCommit": True
            }}
        })
    goods_db.SpecOfListing.update_many(
        {"status.3": {"$exists": True}, "prepayment.1": {"$exists": False}},
        {"$set": {
            "prepayment.3": {
                "state": 1,
                "prepaymentRatio": 1,
                "isSupportMergeCommit": True
            }}
        })


def add_admin_page():
    menu = admin_db.MenuClass.find_one({"name": "Operation"})
    sort_index = 0
    for it in admin_db.Page.find(
            {"menuClassId": menu["_id"]}).sort([("sortIndex", -1)]).limit(1):
        sort_index = it["sortIndex"] + 1
    for it in admin_db.Page.find().sort([("_id", -1)]).limit(1):
        admin_db.Page.insert_one({
            "_id": it["_id"]+1,
            "sortIndex": sort_index,
            "name": "Prepayment Setting",
            "url": "/prepayment-setting",
            "menuClassId": menu["_id"],
            "activated": True
        })


def add_prepayment_setting_parameter():
    param_id = 0
    for it in order_db.parameter.find().sort([("id", -1)]).limit(1):
        param_id = it["id"]
    for region_id in [1, 3]:
        param_id += 1
        order_db.parameter.insert_one(
            {
                "id": param_id,
                "regionId": region_id,
                "name": "PREPAYMENT_SWITCH",
                "value": "1",
                "dataType": "bool",
                "paramModule": "prepayment"
            }
        )
        param_id += 1
        order_db.parameter.insert_one(
            {
                "id": param_id,
                "regionId": region_id,
                "name": "PREPAYMENT_RATIO",
                "value": "0.1",
                "dataType": "float",
                "paramModule": "prepayment"
            }
        )
        param_id += 1
        order_db.parameter.insert_one(
            {
                "id": param_id,
                "regionId": region_id,
                "name": "PREPAYMENT_POSTAGE_TYPE",
                "value": "1",
                "dataType": "int",
                "paramModule": "prepayment"
            }
        )


def update_bill_prepayment(times, start_bill_id, end_bill_id):
    query = {"id": {"$gte": start_bill_id, "$lt": end_bill_id},
             "preAmount": {"$exists": False}}
    for it in order_db.Bill.find(query).sort([("id", 1)]):
        if it["paymethod"] == 1:
            order_db.Bill.update_one(
                {"id": it["id"]}, {"$set": {"prepaymentRatio": 1,
                                            "preAmount": it["payAmount"],
                                            "dueAmount": 0}})
        elif it["paymethod"] == 2:
            order_db.Bill.update_one(
                {"id": it["id"]}, {"$set": {"prepaymentRatio": 1,
                                            "preAmount": 0,
                                            "dueAmount": it["payAmount"]}})
    print("----update-bill-times-%s-success----" % times)


def update_package_prepayment(times, start_id, end_id):
    query = {"id": {"$gte": start_id, "$lt": end_id},
             "preAmount": {"$exists": False}}
    for it in order_db.ShipPackage.find(query).sort([("id", 1)]):
        if it["payMethod"] == 1:
            order_db.ShipPackage.update_one(
                {"id": it["id"]}, {"$set": {"preAmount": it["amount"],
                                            "dueAmount": 0}})
        elif it["payMethod"] == 2:
            order_db.ShipPackage.update_one(
                {"id": it["id"]}, {"$set": {"preAmount": 0,
                                            "dueAmount": it["amount"]}})
        elif it["payMethod"] == 3:
            so = order_db.SaleOrder.find_one({"id": it["saleOrderId"]})
            order_db.ShipPackage.update_one(
                {"id": it["id"]}, {"$set": {"preAmount": so["preAmount"],
                                            "dueAmount": so["dueAmount"]}})

    print("----update-package-times-%s-success----" % times)


def fix_cod_pre():
    query = {"createdAt": {"$gte": datetime(2021, 11, 18)}, "paymethod": 2}
    for it in order_db.Bill.find(query).sort([("id", 1)]):
        order_db.Bill.update_one(
            {"id": it["id"]}, {"$set": {"prepaymentRatio": 0,
                                        "preAmount": 0,
                                        "dueAmount": it["payAmount"]}})
        for so in order_db.SaleOrder.find({"billId": it["id"]}):
            order_db.SaleOrder.update_one(
                {"id": so["id"]}, {"$set": {"preAmount": 0,
                                            "dueAmount": so["payAmount"]}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging('prepayment_release.log')
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    admin_db = get_db(config, env, "Admin")
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")

    package_id = 0

    for it in order_db.ShipPackage.find().sort([("_id", -1)]).limit(1):
        package_id = it["id"] + 300

    thread_num = 10
    pg_interval = int(package_id / 10)

    t_obj = []
    for item in range(thread_num):
        start_id = item * pg_interval
        end_id = start_id + pg_interval
        t1 = Thread(target=update_package_prepayment, args=(
            item, start_id, end_id))
        t_obj.append(t1)
        t1.start()
    for t1 in t_obj:
        t1.join()

    print("---------------------------success-------------------------------")

