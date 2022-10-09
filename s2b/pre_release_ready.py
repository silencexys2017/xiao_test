# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from decimal import Decimal

_DEFAULT_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
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


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def utc2local(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime(LOCAL_FORMAT)


def update_bill_collection():
    for bill in quark_order_db.Bill.find({}):
        order_count = 0
        sku_count = 0
        item_count = 0
        for so in quark_order_db.SaleOrder.find({"billId": bill["_id"]}):
            order_count += 1
            sku_count += so["skuCount"]
            item_count += so["itemCount"]
        quark_order_db.Bill.update_one(
            {"_id": bill["_id"]}, {"$set": {
                "preAmount": bill["payAmount"],
                "dueAmount": {"defaults": 0.0, "display": 0.0},
                "prepaymentRatio": 1.0,
                "orderCount": order_count,
                "skuCount": sku_count,
                "itemCount": item_count
            }})


def addition(num_1, num_2):
    return {
        "defaults": addition_operation(num_1["defaults"], num_2["defaults"]),
        "display": addition_operation(num_1["display"], num_2["display"])
    }


def addition_operation(number_1, number_2):
    return float(Decimal(str(number_1)) + Decimal(str(number_2)))


def update_order_detail_collection():
    for order in quark_order_db.OrderDetail.find({}):
        quark_order_db.OrderDetail.update_one(
            {"_id": order["_id"]}, {"$set": {
                "payAmount": addition(order["amount"], order["postage"]),
                "preAmount": addition(order["amount"], order["postage"]),
                "dueAmount": {"defaults": 0.0, "display": 0.0},
                "prepaymentRatio": 1.0,
            }})


def update_sale_order_collections():
    for order in quark_order_db.SaleOrder.find({}):
        quark_order_db.SaleOrder.update_one(
            {"_id": order["_id"]}, {"$set": {
                "preAmount": order["payAmount"],
                "dueAmount": {"defaults": 0.0, "display": 0.0}
            }})


def add_prepayment_permission():
    permission_id = -1
    for it in quark_admin_db.Permission.find({}).sort([("_id", -1)]).limit(1):
        permission_id = it["_id"]

    quark_admin_db.Permission.insert_one(
        {
            "_id": permission_id + 1,
            "name": "COD和预付款设置",
            "code": "prepayment",
            "parentId": None,
            "codePath": "prepayment",
            "idPath": str(permission_id),
            "type": 1
        }
    )

    quark_goods_db.Listing.update_many({}, {
        "$set": {
            "prepayment": {
                "state": 1,
                "prepaymentRatio": 1,
                "isSupportMergeCommit": True
            }
        }
    })


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    quark_goods_db = get_db(config, env, "QuarkGoods")
    quark_admin_db = get_db(config, env, "QuarkAdmin")
    quark_order_db = get_db(config, env, "QuarkOrder")
    # FILE_NAME = "xed-order.xlsx"

    add_prepayment_permission()
    update_bill_collection()
    update_order_detail_collection()
    update_sale_order_collections()



