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


def update_s2b_address():
    quark_common.State.delete_many({"regionCode": "KE"})
    quark_common.City.delete_many({"regionCode": "KE"})
    quark_common.Area.delete_many({"regionCode": "KE"})
    for it in common_db.Areas.find({"deep": 1, "regionCode": "KE"}).sort(
            [("_id", 1)]):
        quark_common.State.insert_one(
            {
                "_id": it["_id"],
                "regionCode": "KE",
                "index": it["_id"],
                "name": it["name"],
                "minAppVersion": 1,
                "enabled": True,
                "visible": True,
                "postage": 1.05
            }
        )
    for it in common_db.Areas.find({"deep": 2, "regionCode": "KE"}).sort(
            [("_id", 1)]):
        quark_common.City.insert_one(
            {
                "_id": it["_id"],
                "index": it["_id"],
                "name": it["name"],
                "minAppVersion": 1,
                "stateId": it["parentId"],
                "regionCode": "KE",
                "enabled": True,
                "visible": True,
                "postage": 0
            }
        )

    for it in common_db.Areas.find({"deep": 3, "regionCode": "KE"}).sort(
            [("_id", 1)]):
        city = common_db.Areas.find_one({"_id": it["parentId"]})
        quark_common.Area.insert_one(
            {
                "_id": it["_id"],
                "postage": 0,
                "index": it["_id"],
                "name": it["name"],
                "minAppVersion": 1,
                "stateId": city["parentId"],
                "regionCode": "KE",
                "cityId": it["parentId"],
                "supportCod": False,
                "enabled": True,
                "visible": True,
                "ett": 2
            }
        )


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    # config = load_config(_DEFAULT_CONFIG_FILE, env)

    common_db = get_db(K_DB_URL, env, "Common")
    quark_common = get_db(K_DB_URL, env, "QuarkCommon")

    update_s2b_address()
    print("update_pay_transactions success")

