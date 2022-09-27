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
_DEFAULT_CONFIG_FILE = '../config.json'
FILE_NAME = "so.xlsx"
FILE_NAME_G = "spg.xlsx"
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


def export_so_order(date_time):
    so_li = [it for it in order_db.SaleOrder.find(
        {"createdAt": {"$gt": date_time}})]
    store_ids = order_db.SaleOrder.distinct("storeId", {})
    store_di = {it["_id"]: it["name"] for it in seller_db.Store.find(
        {"_id": {"$in": store_ids}})}
    ware_di = {it["_id"]: it["name"] for it in goods_db.Warehouse.find({})}
    address_ids = list({it["addressId"] for it in so_li})
    add_di = {it["id"]: {"phone": it.get("phone"), "city": it.get("city")} for
              it in member_db.address.find({"id": {"$in": address_ids}})}

    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet("saleOrders")
    headings = [
        'SO Serial', 'SO#', 'Store', 'Payment', 'Client', 'Type', '配送方式',
        'User ID', 'Contact Phone', 'Order Time', 'Country', 'City',
        'Pay Amount', 'Status'
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:N', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for it in so_li:
        row += 1
        worksheet.write('A%d' % row, it["code"])
        worksheet.write('B%d' % row, it["id"])
        worksheet.write('C%d' % row, '{} && {}'.format(
            store_di[it["storeId"]], ware_di[it["warehouseId"]]))
        worksheet.write('D%d' % row, map_pay_method[it["payMethod"]])
        worksheet.write('E%d' % row, map_client[it["platform"]])
        worksheet.write('F%d' % row, map_so_type[it["orderType"]])
        if it["deliveryMethod"]:
            worksheet.write(
                'G%d' % row, map_delivery_method[it["deliveryMethod"]])
        worksheet.write('H%d' % row, it["accountId"])
        if add_di.get(it["addressId"]):
            worksheet.write('I%d' % row, add_di[it["addressId"]]["phone"])
            worksheet.write('L%d' % row, add_di[it["addressId"]]["city"])

        worksheet.write('J%d' % row, utc2local(it["createdAt"]))
        worksheet.write('K%d' % row, REGION_MATCH[it["region"]])
        worksheet.write('M%d' % row, it["payAmount"])
        worksheet.write('N%d' % row, map_so_state[it["status"]])
    workbook.close()


def export_spg_order(date_time):
    spg_li = []
    so_ids = []
    address_ids = set()
    store_ids = set()
    bill_ids = set()
    for it in order_db.ShipPackage.find({"createdAt": {"$gt": date_time}}):
        spg_li.append(it)
        so_ids.append(it["saleOrderId"])
        address_ids.add(it["addressId"])
        store_ids.add(it["storeId"])

    so_di = {}
    for it in order_db.SaleOrder.find({"id": {"$in": so_ids}}):
        so_di[it["id"]] = {
            "itemTotal": it["itemTotal"], "coinRedeem": it["redeem"],
            "voucher": it.get("voucherRedeem"), "billId": it["billId"],
            "postage": it["postage"] - it["postageDiscount"]}
        bill_ids.add(it["billId"])

    store_di = {it["_id"]: it["name"] for it in seller_db.Store.find(
        {"_id": {"$in": list(store_ids)}})}
    ware_di = {it["_id"]: it["name"] for it in goods_db.Warehouse.find({})}
    add_di = {it["id"]: {"phone": it.get("phone"), "city": it.get("city")} for
              it in member_db.address.find({"id": {"$in": list(address_ids)}})}
    vc_di = {it["billId"]: it["ownerType"] for it in order_db.VoucherBill.find(
        {"billId": {"$in": list(bill_ids)}})}
    workbook = xlsxwriter.Workbook(FILE_NAME_G)
    worksheet = workbook.add_worksheet("shipPackages")
    headings = [
        'Ship Package', 'SHO Contain', 'SO#', 'Store', 'Payment',
        'Early SHO Create', 'User ID', 'Contact Phone', 'Due', 'Online Pay',
        '配送方式', 'Status', 'Print Time', 'Logistics No.', 'Close Time',
        'Actual Sale Price', 'Coin Redeem', 'Platform Voucher Redeem',
        'Store Voucher Redeem', 'Postage'
    ]
    style_headings = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet.set_column('A:T', 15, other_bold)
    worksheet.write_row('A1', headings, style_headings)
    row = 1
    for it in spg_li:
        row += 1
        worksheet.write('A%d' % row, it["code"])
        worksheet.write('B%d' % row, 1)
        worksheet.write('C%d' % row, it["saleOrderId"])
        worksheet.write('D%d' % row, '{} && {}'.format(
            store_di[it["storeId"]], ware_di[it["warehouseId"]]))
        worksheet.write(
            'E%d' % row, map_pay_method[it["payMethod"]])
        worksheet.write('F%d' % row, utc2local(it["createdAt"]))
        worksheet.write('G%d' % row, it["accountId"])
        if add_di.get(it["addressId"]):
            worksheet.write('H%d' % row, add_di[it["addressId"]]["phone"])
        if it["payMethod"] == 1:
            cod_amount = 0
            online_amount = it["amount"]
        else:
            cod_amount = it["amount"]
            online_amount = 0

        worksheet.write('I%d' % row, cod_amount)
        worksheet.write('J%d' % row, online_amount)
        if it["deliveryMethod"]:
            worksheet.write(
                'K%d' % row, map_delivery_method[it["deliveryMethod"]])
        worksheet.write('L%d' % row, map_package_state[it["status"]])
        worksheet.write('M%d' % row, utc2local(it.get("shippedAt")))
        worksheet.write('N%d' % row, it.get("terminalDeliveryCode"))
        worksheet.write('O%d' % row, utc2local(it.get("deliveredAt")))
        so = so_di[it["saleOrderId"]]
        worksheet.write('P%d' % row, so["itemTotal"])
        worksheet.write('Q%d' % row, so["coinRedeem"])

        if vc_di.get(so["billId"]) == 1:
            platform_voucher = so["voucher"]
            store_voucher = 0
        elif vc_di.get(so["billId"]) == 2:
            platform_voucher = 0
            store_voucher = so["voucher"]
        else:
            platform_voucher = 0
            store_voucher = 0
        worksheet.write('R%d' % row, platform_voucher)
        worksheet.write('S%d' % row, store_voucher)
        worksheet.write('T%d' % row, so["postage"])
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

    export_so_order(datetime(2020, 1, 1))

    export_spg_order(datetime(2020, 1, 1))
