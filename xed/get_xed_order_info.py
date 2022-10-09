# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter

_DEFAULT_CONFIG_FILE = '../config.json'

REGION_MATCH = {1: "Bangladesh", 3: "Myanmar"}
MONTH = ["January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]
map_pay_method = {
    1: 'Online',
    2: 'COD',
    3: 'Pre'
}
"""
序号，XE订单号，商户订单号，SKU ID，商品数量， 商品的中创建时间，国内快递单号，目的国，
最后更新时间，状态，是否打印面单, 商品的中文名"""

map_state = {
    1: '待收件',
    2: '已收件',
    3: '已提运',
    4: '已发出',
    5: '待接件',
    6: '待派送',
    7: '尾程派送中',
    8: '已交付',
    -1: '已取消',
    -2: '已拒收',
    -3: '拒揽件'
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


def get_logistics_orders():
    for it in dna_order_db.ShipPackage.find({"isUseXED": True, "status": -2}):
        order = bee_logistics_db.LogisticsOrder.find_one(
            {"orderNo": it.get("fullLogisticsCode")})
        if order and order.get("status") in [7]:
            print(it["saleOrderId"], order["orderNo"])


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("xed-order-export.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    bee_logistics_db = get_db(config, env, "BeeLogistics")
    dna_order_db = get_db(config, env, "Order")
    FILE_NAME = "xed-order.xlsx"

    start_time = datetime(2021, 10, 1)
    end_time = datetime(2022, 1, 1)
    get_logistics_orders()



