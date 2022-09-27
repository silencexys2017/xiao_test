# -*- coding:utf-8 -*-
import sys
import os
import logging
import time

import pymongo
from datetime import datetime
import json
import xlsxwriter

_DEFAULT_CONFIG_FILE = '../config.json'


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


def get_reject_listings(file_name):
    so_ids = order_db.SaleOrder.distinct("id", {"status": -2})
    # "closedAt": {"$gt": datetime(2021, 1, 1)}
    sku_di = {}
    for it in order_db.SaleOrderDetail.find({"orderId": {"$in": so_ids}}).sort(
            [("_id", -1)]):
        if sku_di.get(it["skuId"]):
            sku_di[it["skuId"]]["saleCount"] += it["count"]
        else:
            sku_di[it["skuId"]] = {
                "salePrice": it["salePrice"], "saleCount": it["count"],
                "listingId": it["listingId"]}
    print(sku_di.keys())
    sku_name = {it["_id"]: it["title"] for it in goods_db.SpecOfSku.find(
        {"_id": {"$in": list(sku_di.keys())}})}
    print(sku_name)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet_1 = workbook.add_worksheet("SkuSale")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "skuId", bold)
    worksheet_1.write("B1", "listingId", bold)
    worksheet_1.write("C1", "salePrice", bold)
    worksheet_1.write("D1", "saleCount", bold)
    worksheet_1.write("E1", "title", bold)
    worksheet_1.set_column('A:D', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for k, v in sku_di.items():
        worksheet_1.write('A%d' % row_1, k)
        worksheet_1.write('B%d' % row_1, v["listingId"])
        worksheet_1.write('C%d' % row_1, v["salePrice"])
        worksheet_1.write('D%d' % row_1, v["saleCount"])
        worksheet_1.write('E%d' % row_1, sku_name[k])
        row_1 += 1
    workbook.close()


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    _DEFAULT_LOG_FILE = str(sys.argv[0])
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    get_reject_listings(file_name="%d-reject-skus.xlsx" % int(time.time()))

    print("---------------------------success-------------------------------")

