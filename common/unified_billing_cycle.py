import sys
import os
import logging
import pymongo
import json
from datetime import datetime, timedelta


K_DB_URL = {
    "dev": "mongodb://root:NX9NfRBkth@mo-mongodb-headless.os.svc/admin?replicaSet=rs0",
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
        if no and no not in ["null", None]:
            b_cycle = common_db.UnifiedBillingCycle.find_one(
                {"businessLicenseNo": no})
            if b_cycle:
                if b_cycle["settlementCycle"] in [3, 4]:
                    update_cycle = 2
                else:
                    update_cycle = b_cycle["settlementCycle"]

                if update_cycle != settlement_cycle:
                    seller_db.Store.update_one(
                        {"_id": store["_id"]},
                        {"$set": {"settlementAccount.settlementCycle":
                                      update_cycle}})
            else:
                common_db.UnifiedBillingCycle.insert_one(
                    {"businessLicenseNo": no,
                     "settlementCycle": settlement_cycle})
        elif store.get("kiliPartnerInfo"):
            seller_db.Store.update_one(
                {"_id": store["_id"]},
                {"$set": {"qualification.idNumber": store.get(
                    "kiliPartnerInfo").get("kiliUserId")}})

    for vendor in quark_vendor_db.Vendor.find():
        if vendor.get("businessLicenseNo"):
            common_db.UnifiedBillingCycle.find_one(
                {"businessLicenseNo": vendor.get("businessLicenseNo")})

    lite_type = bee_auth_db.UserType.find_one(
        {"platformName": "Kilimall Lite"})["_id"]  # PerFee
    supply_type = bee_auth_db.UserType.find_one(
        {"platformName": "Uomnify"})["_id"]
    print(lite_type, supply_type)
    for store in bee_auth_db.Store.find():
        if store.get("userTypeId") == lite_type:
            st = seller_db.Store.find_one(
                {"_id": int(store["platformStoreId"])})
            if st and st.get("qualification"):
                id_num = st["qualification"].get("idNumber")
                if not id_num:
                    id_num = st.get("kiliPartnerInfo", {}).get("kiliUserId")
                bee_auth_db.CustomerInfo.find_one_and_update(
                    {"userId": store["userId"]},
                    {"$set": {
                        "idNum": id_num,
                        "settlementCycle": st.get("settlementAccount", {}).get(
                            "settlementCycle")}}, upsert=True)
        elif store.get("userTypeId") == supply_type:
            vd = quark_vendor_db.Vendor.find_one(
                {"_id": int(store["platformStoreId"])})
            if vd:
                cycle = vd["settlementMethod"]
                if cycle in [3, 4]:
                    cycle = 2
                bee_auth_db.CustomerInfo.find_one_and_update(
                    {"userId": store["userId"]},
                    {"$set": {"settlementCycle": cycle}}, upsert=True)


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
    quark_vendor_db = get_db(K_DB_URL, env, "QuarkVendor")
    bee_auth_db = get_db(K_DB_URL, env, "BeeAuth")

    record_settlement_cycle()