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
ORDER_FILE_NAME = "price_abnormal_order.xlsx"

order_status_map = {
    1: "UNPAID", 2: "UN CONFIRMED", 3: "UN SHIPPED", 4: "IN TRANSIT",
    5: "ACCEPT", 6: "WAIT", -1: "CANCEL", -2: "REJECT", -3: "PART ACCEPT"}

pay_method_map = {1: "ONLINE", 2: "COD"}

order_type_map = {1: "NORMAL", 2: "FLASH", 3: "PRIZE", 4: "REDEEM", 5: "MIX",
                  6: "GROUP"}


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


def get_price_abnormal_order(sku_ids):
    query_1 = {
        "createdAt": {"$gt": datetime(2020, 8, 20)},
        "skuId": {"$in": sku_ids}
    }
    order_ids = order_db.SaleOrderDetail.distinct("orderId", query_1)
    query_2 = {"id": {"$in": order_ids}}
    order_di = {}
    for it in order_db.SaleOrder.find(query_2):
        order_di[it["id"]] = it

    order_li = order_db.SaleOrderDetail.find(query_1).sort(
        [("skuId", -1), ("createdAt", -1)])

    workbook = xlsxwriter.Workbook(ORDER_FILE_NAME)
    worksheet_1 = workbook.add_worksheet("orderList")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "Sku ID", bold)
    worksheet_1.write("B1", "Price", bold)
    worksheet_1.write("C1", "Count", bold)
    worksheet_1.write("D1", "Sku Amount", bold)
    worksheet_1.write("E1", "Create Time(UTC)", bold)
    worksheet_1.write("F1", "SaleOrder ID", bold)
    worksheet_1.write("G1", "Order Sku Count", bold)
    worksheet_1.write("H1", "Order Amount", bold)
    worksheet_1.write("I1", "Pay Amount", bold)
    worksheet_1.write("J1", "Order Status", bold)
    worksheet_1.write("K1", "PayMethod", bold)
    worksheet_1.write("L1", "Store ID", bold)
    worksheet_1.write("M1", "Order Type", bold)

    worksheet_1.set_column('A:M', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_column('E:E', 30, other_bold)
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    for item in order_li:
        od = order_di[item["orderId"]]
        worksheet_1.write('A%d' % row_1, item["skuId"])
        worksheet_1.write('B%d' % row_1, item["dealPrice"])
        worksheet_1.write('C%d' % row_1, item["count"])
        worksheet_1.write('D%d' % row_1, item["amount"])
        worksheet_1.write(
            'E%d' % row_1, strf_time_obj(item["createdAt"]))

        worksheet_1.write('F%d' % row_1, item["orderId"])
        worksheet_1.write('G%d' % row_1, od["skuCount"])
        worksheet_1.write('H%d' % row_1, od["orderAmount"])
        worksheet_1.write('I%d' % row_1, od["payAmount"])
        worksheet_1.write(
            'J%d' % row_1, order_status_map[od["status"]])
        worksheet_1.write(
            'K%d' % row_1, pay_method_map[od["payMethod"]])
        worksheet_1.write('L%d' % row_1, od["storeId"])
        worksheet_1.write('M%d' % row_1, order_type_map[od["orderType"]])

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
    with open('sku_ids.json', 'r') as f:
        sku_ids = json.load(f).get("skuIds")
        f.close()
    print(len(sku_ids))
    get_price_abnormal_order(sku_ids)

    print("---------------------------success-------------------------------")

