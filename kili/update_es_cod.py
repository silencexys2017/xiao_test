# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from openpyxl import load_workbook
from datetime import timedelta, datetime

_DEFAULT_CONFIG_FILE = '../config.json'

X_DB_URL = {
    "dev": "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongodb-paas-service/admin?replicaSet=rs0",
	"test": "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@159.138.90.30:30734/admin",
	"prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@159.138.90.30:30734",
    # "prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@mongodb-paas-service/admin?replicaSet=rs0"
}

K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://root:IdrCgVpHzv@mongo-mongodb-headless.os:27017/admin?replicaSet=rs0&retrywrites=false",
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


def update_es_cod():
    utc_now = datetime.utcnow()
    for it in wms_warehouse_db.WarehouseProductItem.find(
            {"userId": {"$ne": -1}, "partnerId": 5}):
        sku_id = int(it["skuId"])
        sku = goods_db.SpecOfSku.find_one_and_update(
            {"_id": sku_id},
            {"$set": {"paymentMethodsMask": 7, "updatedAt": utc_now}})
        if not sku:
            print("sku not found %s" % sku_id)
            continue
        es_db.Es.update_one(
            {"_id": sku["listingId"]},
            {'$set': {"codSupported": True, "updatedAt": utc_now}})
        print("listing %s success" % sku["listingId"])


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("xed-order-export.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    es_db = get_db(K_DB_URL, env, "Es")
    goods_db = get_db(K_DB_URL, env, "Goods")
    if env == "prd":
        mongodb_setting = dict(
            host='159.138.90.30',
            port=30734,
            username='pf_prd_dbo',
            password='m2w9ZNZP4gUsx9b2hu6L',
            authSource='admin',
        )
        wms_warehouse_db = pymongo.MongoClient(
            **mongodb_setting)[env + "WmsWarehouse"]
        # wms_warehouse_db = get_db(X_DB_URL, env, "WmsWarehouse")
    else:
        wms_warehouse_db = get_db(K_DB_URL, env, "WmsWarehouse")

    update_es_cod()


