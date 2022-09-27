# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
import copy
from datetime import datetime

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'
ORDER_FILE_NAME = "coin_related_statistics.xlsx"

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


def get_coins_user_order():
    account_di = {}
    for it in member_db.points_balance.find({"balance": {"$gt": 100}}):
        account_di[it["accountId"]] = {
            "balance": it["balance"], "historyTotal": it["historyTotal"],
            "invitedCoin": 0, "exchangeCoin": 0, "orderCoin": 0,
            "orderCount": 0, "completeCount": 0}
    query = {"accountId": {"$in": list(account_di.keys())}}
    reward_log_query = copy.deepcopy(query)
    reward_log_query["nodeId"] = 5
    for it in member_db.reward_log.find(reward_log_query):
        account_di[it["accountId"]]["invitedCoin"] += it["amount"]

    for it in order_db.AccountOrder.find(query):
        account_di[it["accountId"]]["orderCount"] += it.get("orderCount", 0)
        account_di[it["accountId"]]["completeCount"] += it.get(
            "completeCount", 0)

    order_query = copy.deepcopy(query)
    order_query["status"] = {"$ne": -1}
    order_query["coin"] = {"$gt": 0}
    for it in order_db.SaleOrder.find(order_query):
        if it["orderType"] == 4:
            account_di[it["accountId"]]["exchangeCoin"] += it.get("coin", 0)
        else:
            account_di[it["accountId"]]["orderCoin"] += it.get("coin", 0)

    workbook = xlsxwriter.Workbook(ORDER_FILE_NAME)
    worksheet_1 = workbook.add_worksheet("coinList")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "User Id", bold)
    worksheet_1.write("B1", "Current Coin", bold)
    worksheet_1.write("C1", "History Total Coin", bold)
    worksheet_1.write("D1", "Invited Coin", bold)
    worksheet_1.write("E1", "Exchange Coin", bold)
    worksheet_1.write("F1", "Order Coin", bold)
    worksheet_1.write("G1", "Order Count", bold)
    worksheet_1.write("H1", "Complete Count", bold)
    worksheet_1.set_column('A:H', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    for k, v in account_di.items():
        worksheet_1.write('A%d' % row_1, k)
        worksheet_1.write('B%d' % row_1, v["balance"])
        worksheet_1.write('C%d' % row_1, v["historyTotal"])
        worksheet_1.write('D%d' % row_1, v["invitedCoin"])
        worksheet_1.write('E%d' % row_1, v["exchangeCoin"])
        worksheet_1.write('F%d' % row_1, v["orderCoin"])
        worksheet_1.write('G%d' % row_1, v["orderCount"])
        worksheet_1.write('H%d' % row_1, v["completeCount"])
        row_1 += 1

    workbook.close()


def estimated_document_count_test():
    number = member_db.address.estimated_document_count({})
    print(number)


if __name__ == "__main__":
    # usage = 'python3 Sxx.py prd|dev|test'
    # init_logging(_DEFAULT_LOG_FILE)
    # if len(sys.argv) < 2:
    #     logging.error(usage)
    #     sys.exit(-1)

    env = "test"
    config = load_config(_DEFAULT_CONFIG_FILE, env)

    order_db = get_db(config, env, "Order")
    member_db = get_db(config, env, "Member")
    estimated_document_count_test()
    # get_coins_user_order()

    print("---------------------------success-------------------------------")

