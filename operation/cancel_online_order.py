# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'
ORDER_FILE_NAME = "online_order.xlsx"

order_status_map = {
    1: "UNPAID", 2: "UN CONFIRMED", 3: "UN SHIPPED", 4: "IN TRANSIT",
    5: "ACCEPT", 6: "WAIT", -1: "CANCEL", -2: "REJECT", -3: "PART ACCEPT"}


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


def strf_time_obj(utc_time):
    if utc_time:
        return datetime.strftime(utc_time, '%Y-%m-%dT%H:%M:%S.%fZ')
    return None


def get_online_order():
    order_li = []
    query_1 = {
        "createdAt": {"$gt": datetime(2020, 1, 1)},
        "payMethod": 1,
        "status": -1,
        "paidAt": {"$exists": True}
    }
    query_2 = {
        "createdAt": {"$lte": datetime.utcnow() - timedelta(days=30)},
        "payMethod": 1,
        "paidAt": {"$exists": True},
        "status": {"$in": [2, 3, 4, 6]}
    }

    for it in order_db.SaleOrder.find(query_1):
        if (it["closedAt"] - it["createdAt"]).days >= 30:
            order_li.append(it)

    for it in order_db.SaleOrder.find(query_2):
        order_li.append(it)

    workbook = xlsxwriter.Workbook(ORDER_FILE_NAME)
    worksheet_1 = workbook.add_worksheet("orderList")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "序号", bold)
    worksheet_1.write("B1", "SaleOrder ID", bold)
    worksheet_1.write("C1", "userID", bold)
    worksheet_1.write("D1", "Create Time(UTC)", bold)
    worksheet_1.write("E1", "Cancel Time(UTC)", bold)
    worksheet_1.write("F1", "Order Amount", bold)
    worksheet_1.write("G1", "Pay Amount", bold)
    worksheet_1.write("H1", "Order Status", bold)
    worksheet_1.write("I1", "IsOnline", bold)

    worksheet_1.set_column('A:I', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_column('D:E', 30, other_bold)
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    for item in order_li:
        worksheet_1.write('A%d' % row_1, row_1)
        worksheet_1.write('B%d' % row_1, item["id"])
        worksheet_1.write('C%d' % row_1, item["accountId"])
        worksheet_1.write(
            'D%d' % row_1, strf_time_obj(item["createdAt"]))
        if item["status"] == -1:
            worksheet_1.write(
                'E%d' % row_1, strf_time_obj(item["closedAt"]))
        worksheet_1.write('F%d' % row_1, item["orderAmount"])
        worksheet_1.write('G%d' % row_1, item["payAmount"])
        worksheet_1.write(
            'H%d' % row_1, order_status_map[item["status"]])
        worksheet_1.write('I%d' % row_1, "Y")

        row_1 += 1

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
    get_online_order()

    print("---------------------------success-------------------------------")

