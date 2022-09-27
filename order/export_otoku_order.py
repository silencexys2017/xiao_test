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
_DEFAULT_CONFIG_FILE = '../jp_config.json'
FILE_NAME_G = "otoku_world_order.xlsx"
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


def export_order(date_time):
    status = [2, 3, 4]
    address_ids = set()
    # store_ids = set()
    # bill_ids = set()
    sku_ids = set()
    listing_ids = set()

    so_di = {}
    for it in order_db.SaleOrder.find({"status": {"$in": status}}):
        sod_li = []
        for i in order_db.SaleOrderDetail.find({"orderId": it["id"]}):
            sod_li.append(i)
            sku_ids.add(i["skuId"])
            listing_ids.add(i["listingId"])

        it["sods"] = sod_li
        so_di[it["id"]] = it
        address_ids.add(it["addressId"])
        # store_ids.add(it["storeId"])
        # bill_ids.add(it["billId"])

    spg_di = {}
    for it in order_db.ShipPackage.find(
            {"saleOrderId": {"$in": list(so_di.keys())}}):
        spg_di[it["saleOrderId"]] = it
    # store_di = {it["_id"]: it["name"] for it in seller_db.Store.find(
    #     {"_id": {"$in": list(store_ids)}})}
    # ware_di = {it["_id"]: it["name"] for it in goods_db.Warehouse.find({})}
    sku_di = {it["_id"]: it for it in goods_db.SpecOfSku.find(
        {"_id": {"$in": list(sku_ids)}})}
    listing_di = {
        it["_id"]: it["categoryId"] for it in goods_db.SpecOfListing.find(
            {"_id": {"$in": list(listing_ids)}})}
    cate_di = {
        it["_id"]: it["name"] for it in goods_db.Category.find(
            {"_id": {"$in": list(listing_di.values())}})
    }
    add_di = {it["id"]: it for
              it in member_db.address.find({"id": {"$in": list(address_ids)}})}
    # vc_di = {it["billId"]: it["ownerType"] for it in order_db.VoucherBill.find(
    #     {"billId": {"$in": list(bill_ids)}})}
    workbook = xlsxwriter.Workbook(FILE_NAME_G)
    worksheet = workbook.add_worksheet("Sheet1")
    headings = [
        "お客様管理番号", "お届け予定日", "配達時間帯", "お届け先コード",
        "お届け先電話番号", "郵便番号", "お届け先アパートマンション名1",
        "お届け先アパートマンション名2", "お届け先アパートマンション名3",
        "お届け先会社・部門2", "お届け先名前", "品名１", "商品番号", "商品番号1"]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:N', 20, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for k, v in so_di.items():
        row += 1
        if spg_di.get(k):
            spg = spg_di.get(k)
        else:
            spg = {"code": k}
        worksheet.write('A%d' % row, k)
        worksheet.write('B%d' % row, spg.get("お届け予定日"))
        worksheet.write('C%d' % row, spg.get("配達時間帯"))
        worksheet.write('D%d' % row, spg.get("お届け先コード"))
        addr = add_di.get(v["addressId"])
        phone = addr["phone"] if addr["phone"].startswith("0") else\
            "0" + addr["phone"]
        worksheet.write('E%d' % row, phone)
        worksheet.write('F%d' % row, addr["postcode"])
        address_1 = addr["state"] + addr["city"] + addr["area"] + \
                    addr["address1"]
        worksheet.write('G%d' % row, address_1)
        worksheet.write('H%d' % row, addr.get("address2"))
        worksheet.write('I%d' % row, addr.get("address3"))
        worksheet.write('J%d' % row, addr.get("お届け先会社・部門２"))
        worksheet.write('K%d' % row, addr.get("name"))
        cat = ""
        name = ""
        # spec = ""
        for it in v.get("sods"):
            cat = cat + cate_di[listing_di[it["listingId"]]] + " / "
            name = name + sku_di[it["skuId"]]["idByVendor"] + " × "+str(
                it["count"]) + " / "
            # spec = spec + sku_di[it["skuId"]]["spec"] + " × "+str(
            #     it["count"]) + " / "

        worksheet.write('L%d' % row, cat[:-3])
        worksheet.write('M%d' % row, name[:-3])
        # worksheet.write('N%d' % row, spec[:-3])

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
    goods_db = get_db(config, env, "Goods")
    seller_db = get_db(config, env, "Seller")
    member_db = get_db(config, env, "Member")

    export_order(datetime(2020, 1, 1))
