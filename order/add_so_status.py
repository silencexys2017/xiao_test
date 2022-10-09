# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
import openpyxl
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = 'so_and_spg_import.log'
_DEFAULT_CONFIG_FILE = '../config.json'
FILE_NAME = "so.xlsx"
FILE_NAME_G = "spg.xlsx"
REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
MONTH = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}
map_client = {
    1: 'App',
    2: 'iOS',
    3: 'PC',
    4: 'WAP'
}
map_so_state = {
    1: 'Pending Payment',
    2: 'Pending Confirmation',
    3: 'Pending Dispatch',
    4: 'In Transit',
    5: 'All received',
    6: 'Restocking',
    -1: 'Cancel',
    -2: 'Rejected',
    -3: 'Partially Received'
}

rejection_reason = {
    1: "Goods damaged",
    2: "Goods is not same as in APP",
    3: "no reason",
    5: "Rejection beyond delivery time limit"
}

map_so_type = {
    1: 'Normal',
    2: 'Flash',
    3: 'Lucky Draw',
    4: 'Redeem',
    5: 'Mixed',
    6: 'Group Buying'
}

map_delivery_method = {
    1: '平台承运',
    2: '店铺自发货',
    3: "平台送，店铺设运费"
}

map_package_state = {
    1: 'Pending Dispatch',
    2: 'In Transit',
    3: 'In Delivery',
    4: 'Completed',
    5: 'In Delivery',
    -1: 'Rejected',
    -2: 'Cancel'
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


def xl_read_test():
    workbook = openpyxl.load_workbook("./Orders Status checking 0128.xlsx")
    worksheet = workbook[workbook.sheetnames[0]]
    row_1 = 0
    for row in worksheet.rows:
        row_1 += 1
        if row_1 == 1:
            continue
        so_id = row[2].value
        if so_id:
            so_di = order_db.SaleOrder.find_one({"id": so_id})
            if so_di:
                created_time = so_di["createdAt"]
                worksheet["D%s" % row_1] = map_so_state[so_di["status"]]
                worksheet["F%s" % row_1] = so_di["orderAmount"]
                worksheet["G%s" % row_1] = created_time
                last_update_time = so_di["createdAt"]
                if so_di["status"] == 4:
                    last_update_time = so_di["shippedAt"]
                elif so_di["status"] in [5, -1, -2]:
                    last_update_time = so_di["closedAt"]
                worksheet["H%s" % row_1] = last_update_time
                inter_t = last_update_time - created_time
                int_day = inter_t.days
                int_seconds = inter_t.seconds
                int_hour = int_seconds // 3600
                int_minute = (int_seconds % 3600) // 60
                worksheet["I%s" % row_1] = "%s天%s时%s分" % (
                    int_day, int_hour, int_minute)
                if so_di.get("status") == -2:
                    spg = order_db.ShipPackage.find_one({"saleOrderId": so_id})
                    sr = order_db.ShipmentRefusal.find_one(
                        {"packageId": spg["id"]})
                    if sr:
                        worksheet["E%s" % row_1] = rejection_reason[
                            sr.get("reason")]
    workbook.save(filename="./Orders Status checking 0128.xlsx")


def update_app_cube_order():
    bill_ids = order_db.PaySession.distinct("billId", {"platform": "App-Cube"})
    order_db.SaleOrder.update_many(
        {"billId": {"$in": bill_ids}}, {"$set": {"platform": 5}})


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    # goods_db = get_db(config, env, "Goods")
    # seller_db = get_db(config, env, "Seller")
    # member_db = get_db(config, env, "Member")
    # xl_read_test()
    update_app_cube_order()
