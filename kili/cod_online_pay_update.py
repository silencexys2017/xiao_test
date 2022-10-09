# -*- coding:utf-8 -*-

import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta
from pymongo import ReturnDocument

_DEFAULT_CONFIG_FILE = '../kili_config.json'
_SOUTHX_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}

X_DB_URL = {
    "dev": "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongodb-paas-service/admin?replicaSet=rs0",
	"test": "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@159.138.90.30:30734/admin",
	"prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@159.138.90.30:30734/admin?authSource=admin"
}

K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://sk2:Qmvz84mtswuMJz8Kk90zBM7UbdW@ebes-db.cluster-cvxmlpsy4xpw.eu-central-1.docdb.amazonaws.com:27017/admin?authSource=admin",
    "prd": "mongodb://sk2:Gmbz8i63mtswuMKz8Lk92zNM7UxwO5Txz1@ebes-db.cmxtf8qiglae.eu-central-1.docdb.amazonaws.com:27017/admin?replicaSet=rs0&retrywrites=false"
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


def get_db(uri, env, database):
    client = pymongo.MongoClient(uri[env], retryWrites=False)
    db = '%s%s' % (env, database)
    return client[db]


def utc2local(utc_datetime):
    if not utc_datetime:
        return utc_datetime
    # utc_dt = datetime.strptime(utcstr, UTC_FORMAT)
    # local: 东6区
    lo_dt = utc_datetime + timedelta(hours=6)
    return lo_dt.strftime(LOCAL_FORMAT)


def update_pay_transactions():
    for it in order_db.PayTransactions.find({}):
        pay_stage, refund_state, refund_amount, so_ids = None, None, None, None
        if it.get("paymentStage") is None:
            pay_stage = 1
        if it.get("refundStatus") is None:
            refund_state = 1
        if it.get("refundAmount") is None:
            refund_amount = 0
        if it.get("saleOrderIds") is None:
            so_ids = order_db.SaleOrder.distinct("id", {"billId": it["billId"]})

        fields, ps_fields = {}, {}
        if isinstance(pay_stage, int):
            fields["paymentStage"] = pay_stage
            ps_fields["paymentStage"] = pay_stage
        if isinstance(refund_state, int):
            fields["refundStatus"] = refund_state
        if isinstance(refund_amount, int):
            fields["refundAmount"] = refund_amount
        if isinstance(so_ids, list):
            fields["saleOrderIds"] = so_ids
            ps_fields["saleOrderIds"] = so_ids
        if fields:
            order_db.PayTransactions.update_one(
                {"_id": it["_id"]}, {"$set": fields})
        if ps_fields:
            order_db.PaySession.update_many(
                {"tranId": it["tranId"]}, {"$set": ps_fields})


def update_bill():
    order_db.Bill.update_many(
        {"receivedAmount": {"$exists": False}},
        {"$set": {"receivedAmount": 0}})
    for it in order_db.PayTransactions.find({"refundAmount": {"$gt": 0}}):
        order_db.Bill.update_one(
            {"id": it["billId"]},
            {"$inc": {"refundedAmount": it["refundAmount"]}})
    order_db.Bill.update_many(
        {"refundedAmount": {"$exists": False}},
        {"$set": {"refundedAmount": 0}})


def update_so():
    for it in order_db.SaleOrder.find({}):
        pay_state = 1
        if it["payMethod"] == 1:
            if it.get("paidAt"):
                pay_state = 3
        if it["payMethod"] == 3:
            if it.get("paidAt"):
                pay_state = 2
        order_db.SaleOrder.update_one(
            {"id": it["id"]}, {"$set": {"paymentState": pay_state}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    # config = load_config(_DEFAULT_CONFIG_FILE, env)

    order_db = get_db(K_DB_URL, env, "Order")
    common_db = get_db(K_DB_URL, env, "Common")
    common_db.Areas.update_one({"deep": 3, "name": "Syokimau/Mlolongo"},
                               {"$set": {"supportCod": True}})

    res = order_db.PayTransactions.find_one({})
    print(res)

    update_pay_transactions()
    print("update_pay_transactions success")
    update_bill()
    print("update_bill success")
    update_so()
    print("update_so success")
