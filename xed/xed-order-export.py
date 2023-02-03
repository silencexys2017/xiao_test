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


def export_logistics_order(start_time, end_time):
    # 客户ID/姓名/地址/电话
    # logistics_li = list(logistics_db.LogisticsOrder.find(
    #     {"userType": 1, "createdAt": {"$gte": start_time, "$lt": end_time}}
    # ).sort([("_id", -1)]))
    logistics_li = [{"xiao": 1}]
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet("orders")
    headings = [
        '序号', 'XE订单号', '商户订单号', 'SKU ID', "商品数量", "商品的中文名",
        "商品的英文名", "创建时间", "国内快递单号", "目的国", "最后更新时间", "状态",
        "是否打印面单", "支付方式", "COD Amount", "Division", "City", "Area"
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:R', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k in logistics_li:
        row += 1
        worksheet.write('A%d' % row, row-1)
        worksheet.write('B%d' % row, k.get("orderNo"))
        worksheet.write('C%d' % row, k.get("saleOrderId"))
        worksheet.write(2, 2, k.get("xiao"))
        continue
        sku_ids = ""
        sku_count = ""
        skus_ch_name = ""
        skus_en_name = ""
        if k.get("goodsName"):
            skus_ch_name = k.get("goodsName").get("goodsChineseName")
            skus_en_name = k.get("goodsName").get("goodsForeignName")
        for item in k.get("supplierList"):
            for it in item.get("skus"):
                sku_ids = sku_ids + it.get("skuId") + "&"
                sku_count = sku_count + str(it.get("count")) + "&"
        worksheet.write('D%d' % row, sku_ids[:-1])
        worksheet.write('E%d' % row, sku_count[:-1])
        worksheet.write('F%d' % row, skus_ch_name)
        worksheet.write('G%d' % row, skus_en_name)
        worksheet.write('H%d' % row, utc2local(k.get("createdAt")))
        worksheet.write('I%d' % row, k.get("domesticNo"))
        worksheet.write('J%d' % row, REGION_MATCH.get(k.get("regionId")))
        worksheet.write('K%d' % row, utc2local(k.get("lastUpdatedAt")))
        worksheet.write('L%d' % row, map_state.get(k.get("status")))
        worksheet.write('M%d' % row, k.get("isPrinted", False))
        worksheet.write('N%d' % row, map_pay_method.get(k.get("paymentMethod")))
        worksheet.write('O%d' % row, k.get("codAmount"))
        recipient = k.get("recipient")
        worksheet.write('P%d' % row, recipient.get("state"))
        worksheet.write('Q%d' % row, recipient.get("city"))
        worksheet.write('R%d' % row, recipient.get("area"))
    workbook.close()


def get_error_logistics_order():
    for it in logistics_db.LogisticsOrder.find(
            {"paymentMethod": 2, "codAmount": 0}):
        print(it["orderNo"])
    pass


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    # init_logging("xed-order-export.log")
    # if len(sys.argv) < 2:
    #     logging.error(usage)
    #     sys.exit(-1)
    #
    # env = sys.argv[1]
    # config = load_config(_DEFAULT_CONFIG_FILE, env)
    # logistics_db = get_db(config, env, "BeeLogistics")
    FILE_NAME = "xed-order.xlsx"

    start_time = datetime(2021, 12, 1)
    end_time = datetime(2022, 2, 20)
    export_logistics_order(start_time, end_time)
    # get_error_logistics_order()


