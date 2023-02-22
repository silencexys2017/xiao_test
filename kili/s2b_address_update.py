# -*- coding:utf-8 -*-

import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta
from pymongo import ReturnDocument


X_DB_URL = {
    "dev": "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@mongodb-paas-service/admin?replicaSet=rs0",
	"test": "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@159.138.90.30:30734/admin",
	"prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@159.138.90.30:30734/admin?authSource=admin"
}

K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://root:IdrCgVpHzv@mongo-mongodb-headless.os:27017/admin?replicaSet=rs0&retrywrites=false",
    "prd": "mongodb://sk2:Gmbz8i63mtswuMKz8Lk92zNM7UxwO5Txz1@ebes-db.cmxtf8qiglae.eu-central-1.docdb.amazonaws.com:27017/admin?replicaSet=rs0&retrywrites=false"
}

S2B_MONGO = {
    "prd": "mongodb://lite-prd"
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


def update_s2b_user_address():
    quark_auth.Address.update_many({}, {"$set": {"status": False}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    # config = load_config(_DEFAULT_CONFIG_FILE, env)
    if env == "prd":
        quark_common = get_db(S2B_MONGO, env, "QuarkCommon")
        quark_auth = get_db(S2B_MONGO, env, "QuarkAuth")
    else:
        quark_common = get_db(K_DB_URL, env, "QuarkCommon")
        quark_auth = get_db(K_DB_URL, env, "QuarkAuth")
    common_db = get_db(K_DB_URL, env, "Common")

    update_s2b_address()
    update_s2b_user_address()
    print("update_s2b_address success")

