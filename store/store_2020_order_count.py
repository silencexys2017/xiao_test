# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = '2020_app.log'
_DEFAULT_CONFIG_FILE = './config.json'
FILE_NAME = "2020_store_order.xlsx"
REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
MONTH = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]


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


def get_store_order(date_time):
    store_di = {}
    store_ids = order_db.SaleOrder.distinct(
            "storeId", {"createdAt": {"$gt": date_time}})

    for item in store_ids:
        store_di[item] = {}
        for it in [1, 3]:
            if not order_db.SaleOrder.find_one(
                    {"storeId": item, "region": it,
                     "createdAt": {"$gt": date_time}}):
                continue
            store_di[item][it] = {}
            for i in range(1, 13):
                store_di[item][it][i] = {
                    "orderCount": 0, "orderAmount": 0, "rejectCount": 0,
                    "rejectAmount": 0}

    for it in order_db.SaleOrder.find({"createdAt": {"$gt": date_time}}):
        item = store_di[it["storeId"]][it["region"]][it["createdAt"].month]
        item["orderCount"] += 1
        item["orderAmount"] += it["payAmount"]
        if it["status"] == -2:
            item["rejectCount"] += 1
            item["rejectAmount"] += it["payAmount"]

    store_name = {it["_id"]: it["name"] for it in seller_db.Store.find(
        {"_id": {"$in": store_ids}})}
    return store_di, store_name


def export_excel(data, store):
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet_1 = workbook.add_worksheet("2020")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write(0, 0, 'storeName', bold)
    worksheet_1.write(0, 1, 'country', bold)
    worksheet_1.write(0, 2, 'storeId', bold)
    m_col = 2
    f_col = 3
    l_col = 6
    for month in MONTH:
        for it in ["orderCount", "orderAmount", "rejectCount", "rejectAmount"]:
            m_col += 1
            worksheet_1.write(1, m_col, it, bold)
        worksheet_1.merge_range(0, f_col, 0, l_col, month, bold)
        f_col += 4
        l_col += 4

    row = 2
    for key, value in data.items():
        for ke, val in value.items():
            col = 0
            worksheet_1.write(row, col, store.get(key), other_bold)
            col += 1
            worksheet_1.write(row, col, REGION_MATCH[ke], other_bold)
            col += 1
            worksheet_1.write(row, col, key, other_bold)
            col += 1
            for k, v in val.items():
                worksheet_1.write(row, col, v["orderCount"], other_bold)
                col += 1
                worksheet_1.write(row, col, v["orderAmount"], other_bold)
                col += 1
                worksheet_1.write(row, col, v["rejectCount"], other_bold)
                col += 1
                worksheet_1.write(row, col, v["rejectAmount"], other_bold)
                col += 1
            row += 1
    worksheet_1.set_column(0, 2, 15)
    worksheet_1.set_column(3, 52, 12)
    workbook.close()


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    seller_db = get_db(config, env, "Seller")

    data_li, store_li = get_store_order(datetime(2020, 1, 1))

    export_excel(data_li, store_li)
