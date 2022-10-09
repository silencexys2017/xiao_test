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


def update_partner_store():
    quark_partner_db.B2CPartnerStore.update_many(
        {}, {"$set": {
            "orderSynchronizationMethod": 2,
            "orderPullRules": 2,
            "orderSynchronizationInterval": 24,
            "lastPullOrderTime": datetime(2021, 12, 1, 1)
        }})


def update_order():
    quark_order_db.SaleOrder.update_many(
        {}, {"$set": {
            "thirdOrder": {},
            "thirdAccount": {},
            "thirdAddress": {}
        }})
    quark_order_db.SaleOrder.update_many(
        {"package": {"$exists": False}}, {"$set": {
            "package": {}
        }})
    quark_order_db.Bill.update_many(
        {}, {"$set": {
            "orderType": 1,
            "thirdPlatformId": None,
            "thirdStoreId": None,
            "thirdOrder": {}
        }})


def update_refund_bill():
    for it in quark_order_db.RefundBill.find({}):
        so = quark_order_db.SaleOrder.find_one(
            {"_id": it["sourceOrder"]["saleOrderIds"][0]})
        quark_order_db.RefundBill.update_one(
            {"_id": it["_id"]},
            {"$set": {"refundAmount": so["preAmount"],
                      "sourceOrder.payAmount": so["preAmount"]}})


def update_logistics_order():
    for it in bee_logistics_db.LogisticsOrder.find().sort([("_id", 1)]):
        supplier_state = 3
        if it.get("status") in [1, -3]:
            supplier_state = 2
        package = it["package"] if it.get("package") else {}
        sku_li = []
        for sku in it.get("skus"):
            sku["supplierSkuId"] = None
            sku["supplierId"] = it.get("storeId")
            sku_li.append(sku)
        supplier_li = [
            {
                "suppliers": [
                    {"id": it.get("storeId"), "name": it.get("storeName")}],
                "sourceStores": [
                    {"id": it.get("storeId"), "name": it.get("storeName")}],
                "supplierType": 1,
                "supplierOrderId": it.get("saleOrderId"),
                "xedUserId": it.get("userId"),
                "state": supplier_state,
                "weight": package.get("weight"),
                "volumeWeight": package.get("volumeWeight"),
                "chargedWeight": package.get("chargedWeight"),
                "charge": package.get("charge"),
                "deliveryLocation": it.get("deliveryLocation"),
                "domesticLogistics": it.get("domesticLogistics"),
                "domesticNo": it.get("domesticNo"),
                "deliveryAddressId": it.get("deliveryAddressId"),
                "skus": sku_li,
                "shippedAt": it.get("soShippedAt"),
                "receivedAt": it.get("receivedAt")
            }

        ]
        paid_amount = 0
        if it["paymentMethod"] == 1:
            paid_amount = it.get("payAmount")

        bee_logistics_db.LogisticsOrder.update_one(
            {"_id": it["_id"]},
            {"$set": {
                "paidAmount": paid_amount,
                "isDropShip": False,
                "sourceUserType": it["userType"],
                "dropUserType": None,
                "numOfPackage": 1,
                "platformStoreId": it["storeId"],
                "supplierList": supplier_li,
            },
                "$unset": {"skus": "", "domesticLogistics": "",
                           "domesticNo": "", "storeId": "", "storeName": "",
                           "deliveryAddressId": ""}}
        )


def update_receiving_record():
    for it in bee_logistics_db.ReceivingRecord.find():
        bee_logistics_db.ReceivingRecord.update_one(
            {"_id": it["_id"]},
            {"$set": {"supplierOrderId": it["saleOrderId"]}}
        )


def add_bee_user_and_store():
    store = bee_auth_db.Store.find_one(
        {"platformStoreId": "-1", "platformStoreName": "Uomnify"})
    user = bee_auth_db.User.find_one({"_id": store["userId"]})
    last_user_id = -2
    for it in bee_auth_db.User.find({}).sort([("_id", -1)]).limit(1):
        last_user_id = it["_id"] + 1

    last_store_id = -2
    for it in bee_auth_db.Store.find({}).sort([("_id", -1)]).limit(1):
        last_store_id = it["_id"] + 1
    utc_now = datetime.utcnow()
    bee_auth_db.User.insert_one(
        {
            "_id": last_user_id,
            "name": "15073155455",
            "avatar": None,
            "phoneRegionId": 2,
            "phone": "15073155455",
            "state": 1,
            "typeIds": [1, 3],
            "email": None,
            "account": "WuShaoChu",
            "secretKey": "rHJef6Sb7aY5uOQ2mFyAs9qiIlWgjCvKN4dc", # xys201801
            "password": "aab704c87529e209758bb9ff37fe76badf16246ba5f36f02d3d1ac60c08003b5",
            "createdTime": utc_now,
            "updatedTime": utc_now,
            "lastLoginTime": utc_now,
            "lastLoginIP": "111.22.249.33",
            "inviteCode": "1PTHAU"
        }
    )

    bee_auth_db.Store.insert_one(
        {
            "_id": last_store_id,
            "userId": last_user_id,
            "userTypeId": store["userTypeId"],
            "platformStoreId": "-2",
            "platformStoreName": "UomnifyDropShipping",
            "createdTime": utc_now,
            "updatedTime": utc_now
        }
    )


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    quark_partner_db = get_db(config, env, "QuarkPartner")
    quark_order_db = get_db(config, env, "QuarkOrder")
    bee_logistics_db = get_db(config, env, "BeeLogistics")
    bee_auth_db = get_db(config, env, "BeeAuth")

    # FILE_NAME = "xed-order.xlsx"

    update_partner_store()
    print("----success---update_partner_store")
    update_order()
    print("----success---update_order")
    update_refund_bill()
    print("----success---update_refund_bill")

    update_logistics_order()
    print("----success---update_logistics_order")
    update_receiving_record()
    print("----success---update_receiving_record")



