# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
from pymongo.collection import ReturnDocument
import json

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'


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


def update_order_by_bill(bill_id):
    bill_di = order_db.Bill.find_one({"id": bill_id})
    if not bill_di:
        return
    pb_di = order_db.PayBill.find_one({"billId": bill_id, "type": 1})

    pbd_id = ids_db.ids.find_one_and_update(
        {'_id': "PayBillDetail"}, {'$inc': {'seq': 1}},
        projection={'seq': True, '_id': False},
        upsert=True,
        return_document=ReturnDocument.AFTER).get("seq")
    order_db.PayBillDetail.insert_one({
        "id": pbd_id,
        "payBillId": pb_di["id"],
        "amount": pb_di["amount"],
        "paidAt": pb_di["paidAt"]
    })

    so_di = dict()
    for item in order_db.SaleOrder.find({"billId": bill_id}):
        so_di[item["id"]] = {
            "id": item["id"], "code": item["code"], "skus": []}
    for item in order_db.SaleOrderDetail.find(
            {"orderId": {"$in": list(so_di.keys())}}):
        so_di[item["orderId"]]["skus"].append(
            {"skuId": item["skuId"], "count": item["count"],
             "warehouseId": item["warehouseId"]})

    rs = order_db.SaleOrder.update_many(
        {"billId": bill_id, "status": 1},
        {"$set": {"paidAt": pb_di["paidAt"], "status": 2}})
    if rs.modified_count > 0:
        query = {"saleOrderId": {"$in": list(so_di.keys())}}
        update = {"$addToSet": {"logs": {
            "operateCode": 2, "operator": 1,
            "operatorId": bill_di["accountId"], "createdAt": pb_di["paidAt"]}}}
        order_db.OrderOperateLog.update_many(query, update)


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    ids_db = get_db(config, env, "Ids")
    auth_db = get_db(config, env, "Auth")

    for it in [239888]:
        update_order_by_bill(it)

    print("---------------------------success-------------------------------")

