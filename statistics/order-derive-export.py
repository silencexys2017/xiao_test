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

so_ids = [353676,
353608,
353487,
353435,
353303,
353259,
353188,
353115,
353106,
352968,
352835,
352696,
352682,
352517,
352464,
352410,
352388,
352333,
352289,
352237,
351961,
351835,
351808,
351667,
351663,
351607,
351600,
351552,
351488,
351450,
351368,
351336,
351331,
351256,
351052,
351019,
350926,
350901,
350854,
350848,
350789,
350746,
350740,
350712,
350698,
350661,
350648,
350615,
350602,
350562,
350536,
350433,
350344,
350294,
350265,
350148,
350089,
350018,
350010,
349983,
349872,
349671,
349652,
349644,
349627,
349596,
349572,
349565,
349494,
349452,
349440,
349437,
349432,
349426,
349383,
349342,
349290,
349285,
349280,
349255,
349242,
349039,
349023,
348982,
348938,
348932,
348908,
348821,
348768,
348740,
348712,
348689,
348637,
348630,
348623,
348556,
348451,
348429,
348414,
348394,
348378,
348375,
348362,
348325,
348309,
348304,
348303,
348286,
348257,
348196,
348065,
348041,
348031,
347999,
347965,
347962,
347948,
347799,
347789,
347782,
347777,
347761,
347750,
347694,
347619,
347604,
347574,
347534,
347508,
347475,
359489,
359459,
359401,
359395,
359306,
359188,
359152,
359132,
359028,
358884,
358616,
358604,
358603,
358516,
358513,
358497,
358490,
358394,
358369,
358362,
358252,
358160,
358142,
358050,
357978,
357972,
357903,
357881,
357811,
357673,
357652,
357625,
357537,
357514,
357479,
357476,
357425,
357419,
357393,
357348,
357154,
357105,
357070,
356936,
356906,
356897,
356725,
356717,
356687,
356541,
356486,
356483,
356438,
356428,
356422,
356349,
356339,
356335,
356325,
356261,
356238,
356213,
356198,
356185,
356145,
356129,
356060,
356002,
355951,
355888,
355813,
355781,
355707,
355682,
355637,
355582,
355505,
355455,
355291,
355251,
354966,
354932,
354797,
354726,
354693,
354681,
354505,
354444,
354376,
354335,
354306,
354237,
354067,
354014,
353822,
366942,
366864,
366854,
366693,
366582,
366544,
366507,
366503,
366483,
366427,
366426,
366390,
366348,
366333,
366327,
366314,
366301,
366290,
366085,
365901,
365830,
365759,
365743,
365659,
365457,
365440,
365346,
365317,
365239,
365161,
365076,
364953,
364850,
364797,
364775,
364761,
364755,
364710,
364548,
364483,
364367,
364331,
364300,
364282,
364204,
364183,
364165,
364055,
363782,
363745,
363578,
363565,
363438,
363000,
362931,
362925,
362920,
362906,
362710,
362583,
362555,
362524,
362517,
362506,
362499,
362343,
362341,
362297,
362257,
362209,
362190,
362120,
361926,
361920,
361869,
361831,
361777,
361720,
361646,
361624,
361622,
361520,
361468,
361428,
361181,
361143,
361104,
360990,
360989,
360889,
360865,
360661,
360616,
360597,
360570,
360556,
360553,
360471,
360426,
360332,
360259,
360239,
360226,
360178,
360168,
359955,
359943,
359937]

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
    map_state = {}
    logistics_li = list(logistics_db.LogisticsOrder.find(
        {"userType": 1, "createdAt": {"$gte": start_time, "$lt": end_time}}
    ).sort([("_id", -1)]))
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet("orders")
    headings = [
        '序号', 'XE订单号', '商户订单号', 'SKU ID', "商品数量", "商品的中文名",
        "商品的英文名", "创建时间", "国内快递单号", "目的国", "最后更新时间", "状态",
        "是否打印面单"
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:M', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k in logistics_li:
        row += 1
        worksheet.write('A%d' % row, row-1)
        worksheet.write('B%d' % row, k.get("orderNo"))
        worksheet.write('C%d' % row, k.get("saleOrderId"))
        sku_ids = ""
        sku_count = ""
        skus_ch_name = ""
        skus_en_name = ""
        if k.get("goodsName"):
            skus_ch_name = k.get("goodsName").get("goodsChineseName")
            skus_en_name = k.get("goodsName").get("goodsForeignName")
        for it in k.get("skus"):
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
    workbook.close()


def get_order_derive_skus_info():
    source_sku_ids = set()
    for so_id in so_ids:
        sku_dict = {}
        for sod in order_db.SaleOrderDetail.find({"orderId": so_id}):
            sku_dict[sod.get("skuId")] = sod["count"]
        sku_map = {"count": 0, "deriveSku": 0, "sourceSku": 0, "soId": so_id}
        for sku in goods_db.SpecOfSku.find(
                {"_id": {"$in": list(sku_dict.keys())}}):
            sku_map["count"] = sku_dict[sku["_id"]]
            if sku["type"] == 1:
                sku_map["sourceSku"] = sku["_id"]
                source_sku_ids.add(sku["_id"])
            else:
                sku_map["sourceSku"] = sku["sourceSkuId"]
                source_sku_ids.add(sku["sourceSkuId"])
                sku_map["deriveSku"] = sku["_id"]
            print(sku_map)
            if len(sku_dict) > 1:
                print("----------")
    print(list(source_sku_ids))


def get_error_orders(start_time):
    sale_ids = [str(it) for it in order_db.SaleOrder.distinct(
            "id",
            {"createdAt": {"$gt": start_time}, "status": -1,
             "shippedAt": {"$exists": False}})]
    for order in bee_logistics_db.LogisticsOrder.find(
            {"saleOrderId": {"$in": sale_ids}, "userType": 2}):
        print(order["saleOrderId"])


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'

    init_logging("xed-order-export.log")
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    logistics_db = get_db(config, env, "Order")
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    bee_logistics_db = get_db(config, env, "BeeLogistics")
    FILE_NAME = "xed-order.xlsx"

    get_order_derive_skus_info()
    # get_error_orders(datetime(2021, 6, 17))


