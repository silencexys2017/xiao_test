# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = 'so_and_spg_import.log'
_DEFAULT_CONFIG_FILE = '../config.json'
FILE_NAME = "User_Top_100.xlsx"
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


def get_online_pay_count():
    account = {}
    for it in order_db.SaleOrder.aggregate(
        [{"$match": {"payMethod": 1, "paidAt": {"$exists": True}}},
         {"$group": {"_id": "$accountId", "amount": {"$sum": "$payAmount"}}},
         {"$sort": {"amount": -1}},
         {"$limit": 100}
         ]):
        account[it["_id"]] = it["amount"]

    return account


def export_account_order(account, sheet_name):
    # 客户ID/姓名/地址/电话
    account_ids = list(account.keys())
    account_di = {k: {"nick": None, "phone": None, "city": None,
                      "countOrAmount": v} for k, v in
                  account.items()}
    for it in auth_db.account.find({"id": {"$in": account_ids}}):
        account_di[it["id"]]["nick"] = it.get("nick")
    for it in auth_db.contact.find(
            {"accountId": {"$in": account_ids}, "type": 1}):
        account_di[it["accountId"]]["phone"] = it.get("value")
    for it in member_db.address.find({"accountId": {"$in": account_ids}}):
        account_di[it["accountId"]]["city"] = it.get("city")
    worksheet = workbook.add_worksheet(sheet_name)
    headings = [
        '客户ID', '姓名', '地址', '电话', sheet_name
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:E', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k, v in account_di.items():
        row += 1
        worksheet.write('A%d' % row, k)
        worksheet.write('B%d' % row, v.get("nick"))
        worksheet.write('C%d' % row, v.get("city"))
        worksheet.write('D%d' % row, v.get("phone"))
        worksheet.write('E%d' % row, v.get("countOrAmount"))


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    auth_db = get_db(config, env, "Auth")
    member_db = get_db(config, env, "Member")

    amount_account_di = {
        it.get("accountId"): it.get("completeAmount") for it in
        order_db.AccountOrder.find(
            {}).sort([("completeAmount", -1)]).limit(100)}
    workbook = xlsxwriter.Workbook(FILE_NAME)
    export_account_order(amount_account_di, "completeAmount")
    order_account_ids = {
        it.get("accountId"): it.get("orderCount") for it in
        order_db.AccountOrder.find({}).sort([("orderCount", -1)]).limit(100)}
    export_account_order(order_account_ids, "placeCount")
    complete_account_di = {
        it.get("accountId"): it["completeCount"] for it in
        order_db.AccountOrder.find({}).sort([("completeCount", -1)]).limit(100)}
    export_account_order(complete_account_di, "completeCount")

    export_account_order(get_online_pay_count(), "payAmount")

    workbook.close()

