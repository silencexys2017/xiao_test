# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from decimal import Decimal

_DEFAULT_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}
"""
enum SaleOrderState{
    PENDING_PAY = 1,
    PENDING_SHIP = 2,
    IN_TRANSIT = 3,
    IN_DELIVERING = 4,
    DELIVERED = 5,
    COMPLETED = 6,
    CANCEL = -1,
    REJECT = -2
}
"""
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


def count_order_state_sku(status, worksheet_name):
    pipeline = [
        {"$match": {"state": {"$in": status}}},
        {"$group": {
            "_id": {"skuId": "$skuId", "listingId": "$listingId"},
            "skuCount": {"$sum": "$itemCount"}}},
        {"$sort": {"skuCount": -1}}
    ]

    pipeline = [
        {"$match": {"state": {"$in": status}}},
        {"$group": {"_id": "$skuId",
                    "skuCount": {"$sum": "$itemCount"},
                    "listingId": {"$first": "$listingId"}
                    }},
        {"$sort": {"skuCount": -1}}
    ]
    result = quark_order_db.OrderDetail.aggregate(pipeline)
    sku_ids = quark_order_db.OrderDetail.distinct(
        "skuId",  {"state": {"$in": status}})
    sku_dict = {it["_id"]: it["title"]["default"] for it in
                quark_goods_db.Sku.find({"_id": {"$in": sku_ids}})}

    worksheet = workbook.add_worksheet(worksheet_name)
    headings = ['skuId', 'listingId', 'title', 'SKU数量']
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:E', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k in result:
        row += 1
        worksheet.write('A%d' % row, k["_id"])
        worksheet.write('B%d' % row, k["listingId"])
        worksheet.write('C%d' % row, sku_dict.get(k["_id"]))
        worksheet.write('D%d' % row, k["skuCount"])


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("release_ready.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    quark_partner_db = get_db(config, env, "QuarkPartner")
    quark_order_db = get_db(config, env, "QuarkOrder")
    quark_goods_db = get_db(config, env, "QuarkGoods")

    FILE_NAME = "order-sku-count.xlsx"
    workbook = xlsxwriter.Workbook(FILE_NAME)
    count_order_state_sku([1], "待支付")
    count_order_state_sku([2, 3, 4, 5], "已预付")
    count_order_state_sku([-1], "已取消")
    count_order_state_sku([-2], "已拒收")
    count_order_state_sku([6], "已完成")
    workbook.close()

    print("----success----")



