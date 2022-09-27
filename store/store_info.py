# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter

_DEFAULT_LOG_FILE = 'store_info.log'
DEFAULT_CONFIG_FILE = '../config.json'
REGION_MATCH = {
    1: "Bangladesh", 2: "China", 3: "Myanmar", 5: "Japan"}


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


def get_all_store_info():
    store_di = {}
    for it in seller_db.Store.find().sort([("_id", 1)]):
        store_di[it["_id"]] = {
            "sellerId": it["sellerId"], "storeName": it["name"],
            "sellerRegionId": it["sellerRegionId"]}
    seller_di = {it["_id"]: it for it in seller_db.Seller.find()}
    workbook = xlsxwriter.Workbook("store_info.xlsx")
    worksheet = workbook.add_worksheet("Store")
    headings = [
        'Store Id', 'Store Name', 'SellerRegion', 'Company', 'SellerName',
        'Phone'
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format(
        {'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:F', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k, v in store_di.items():
        row += 1
        seller = seller_di[v["sellerId"]]
        worksheet.write('A%d' % row, k)
        worksheet.write('B%d' % row, v["storeName"])
        worksheet.write('C%d' % row, REGION_MATCH[seller["regionId"]])
        worksheet.write('D%d' % row, seller["qualification"]["name"])
        worksheet.write('E%d' % row, seller["name"])
        worksheet.write('F%d' % row, seller["phone"])
    workbook.close()


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    seller_db = get_db(config, env, "Seller")
    store_li = get_all_store_info()
