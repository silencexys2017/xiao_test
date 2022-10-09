# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'
ORDER_FILE_NAME = "invited_order.xlsx"

order_status_map = {
    1: "UNPAID", 2: "UNCONFIRMED", 3: "UNSHIPPED", 4: "INTRANSIT", 5: "ACCEPT",
    6: "WAIT", -1: "CANCEL", -2: "REJECT", -3: "PART_ACCEPT"}


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


def get_invited_user_order():
    account_di = {}
    for it in member_db.invite_log.find(
        {"inviterId": {"$exists": True},
         "timeCreated": {"$gt": datetime(2020, 1, 1)}}):
        account_di[it["accountId"]] = it["inviteCode"]

    order_li = order_db.SaleOrder.find(
        {"accountId": {"$in": list(account_di.keys())}})

    workbook = xlsxwriter.Workbook(ORDER_FILE_NAME)
    worksheet_1 = workbook.add_worksheet("orderList")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "Order Code", bold)
    worksheet_1.write("B1", "User Id", bold)
    worksheet_1.write("C1", "From Referral Code", bold)
    worksheet_1.write("D1", "Order Amount", bold)
    worksheet_1.write("E1", "Order Status", bold)
    worksheet_1.write("F1", "Create Time(UTC)", bold)
    worksheet_1.set_column('A:F', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    iv_count = 0
    iv_amount = 0
    for item in order_li:
        worksheet_1.write('A%d' % row_1, item["code"])
        worksheet_1.write('B%d' % row_1, item["accountId"])
        worksheet_1.write(
            'C%d' % row_1, account_di[item["accountId"]])
        worksheet_1.write('D%d' % row_1, item["orderAmount"])
        worksheet_1.write(
            'E%d' % row_1, order_status_map[item["status"]])
        worksheet_1.write(
            'F%d' % row_1, strf_time_obj(item["createdAt"]))
        row_1 += 1
        iv_count += 1
        iv_amount += item["orderAmount"]

    all_count = 0
    all_amount = 0
    for it in order_db.SaleOrder.aggregate([
        {"$match": {"createdAt": {"$gt": datetime(2020, 1, 1)}}},
        {"$group": {"_id": None, "orderCount": {"$sum": 1},
                    "orderAmount": {"$sum": "$orderAmount"}}}]):
        all_count = it.get("orderCount", 0)
        all_amount = it.get("orderAmount", 0)

    worksheet_2 = workbook.add_worksheet("orderRatio")
    worksheet_2.set_column('A:D', 20, other_bold)
    worksheet_2.set_row(0, 20)
    worksheet_2.write("B1", "Order Invited", bold)
    worksheet_2.write("C1", "All Order", bold)
    worksheet_2.write("D1", "Ratio", bold)
    worksheet_2.write("A2", "Count", bold)
    worksheet_2.write("A3", "Amount", bold)
    worksheet_2.write("B2", iv_count, other_bold)
    worksheet_2.write("B3", iv_amount, other_bold)
    worksheet_2.write("C2", all_count, other_bold)
    worksheet_2.write("C3", all_amount, other_bold)
    worksheet_2.write("D2", iv_count/all_count, other_bold)
    worksheet_2.write("D3", iv_amount/all_amount, other_bold)

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
    member_db = get_db(config, env, "Member")
    get_invited_user_order()

    print("---------------------------success-------------------------------")

