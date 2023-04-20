import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta


K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://root:IdrCgVpHzv@mongo-mongodb-headless.os:27017/admin?replicaSet=rs0&retrywrites=false",
    # "prd": "mongodb://lite-prd",
}


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


def get_db(uri, env, database):
    client = pymongo.MongoClient(uri[env])
    db = '%s%s' % (env, database)
    return client[db]


def record_settlement_cycle():
    for store in seller_db.Store.find():
        if not store.get("settlementAccount"):
            settlement_cycle = 2
            seller_db.Store.update_one(
                {"_id": store["_id"]},
                {"$set": {"settlementAccount.settlementCycle": 2}})
        else:
            settlement_cycle = store["settlementAccount"]["settlementCycle"]
        no = store.get("qualification", {}).get("idNumber")
        if no:
            res = common_db.UnifiedBillingCycle.find_one(
                {"businessLicenseNo": no})
            if res and res["settlementCycle"] != settlement_cycle:
                seller_db.Store.update_one(
                    {"_id": store["_id"]},
                    {"$set": {"settlementAccount.settlementCycle":
                                  res["settlementCycle"]}})
            else:
                common_db.UnifiedBillingCycle.insert_one(
                    {"businessLicenseNo": no,
                     "settlementCycle": settlement_cycle})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging("unified_billing_cycle_%d.log" % int(
        datetime.now().timestamp()))
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    bee_common_db = get_db(K_DB_URL, env, "BeeCommon")
    common_db = get_db(K_DB_URL, env, "Common")
    seller_db = get_db(K_DB_URL, env, "Seller")
    quark_common_db = get_db(K_DB_URL, env, "QuarkCommon")

    record_settlement_cycle()