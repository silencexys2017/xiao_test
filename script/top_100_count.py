# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = 'gmv.log'
_DEFAULT_CONFIG_FILE = '../config.json'
FILE_NAME = "Top_100.xlsx"


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


def count_account_success_order():
    """展示用户id,电话，订单数>=10，成功交易订单数，成功交易比(成功/总订单数)"""
    item_di = {}
    for it in order_db.AccountOrder.find({"orderCount": {"$gte": 10}}):
        item_di[it["accountId"]] = {
            "ratio": round(it.get("completeCount", 0) / it["orderCount"], 3),
            "completeCount": it.get("completeCount", 0),
            "totalCount": it["orderCount"], "accountId": it["accountId"]}

    for it in auth_db.contact.find(
            {"accountId": {"$in": list(item_di.keys())}, "type": 1}):
        item_di[it["accountId"]]["phone"] = it["value"]
    items = []
    for it in list(item_di.values()):
        items.append((it, it["ratio"]*1000, it["accountId"]))
    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)

    return res_li


def count_account_success_order_this_year():
    """展示用户id,电话，订单数>=10，成功交易订单数，成功交易比(成功/总订单数)"""
    common_query = {"createdAt": {"$gt": datetime(2020, 1, 1)}}
    account_di = {it: {"orderCount": 0, "completeCount": 0} for it in
                  order_db.SaleOrder.distinct("accountId", common_query)}
    for it in order_db.SaleOrder.find(common_query):
        account_di[it["accountId"]]["orderCount"] += 1
        if it["status"] == 5:
            account_di[it["accountId"]]["completeCount"] += 1
    account_g_di = {}
    for k, v in account_di.items():
        if v["orderCount"] > 5:
            account_g_di[k] = {
                "ratio": round(v["completeCount"] / v["orderCount"], 3),
                "completeCount": v["completeCount"],
                "totalCount": v["orderCount"], "accountId": k}

    for it in auth_db.contact.find(
            {"accountId": {"$in": list(account_g_di.keys())}, "type": 1}):
        account_g_di[it["accountId"]]["phone"] = it["value"]
    items = []
    for it in list(account_g_di.values()):
        items.append((it, it["ratio"]*1000, it["accountId"]))
    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 200]

    return res_li


def count_account_repurchase_rate():
    """展示用户id,电话,复购率(次数，不在同一天下单的就计算一次，同一天下单的只计一次)"""
    account_di = {it: {"accountId": it, "times": 0, "lastTime": 0} for it in
                  order_db.AccountOrder.distinct(
                      "accountId", {"orderCount": {"$gte": 30}})}
    for it in order_db.SaleOrder.find(
            {"accountId": {"$in": list(account_di.keys())}}).sort([(
            "createdAt", -1)]):
        item = account_di[it["accountId"]]
        time_str = it["createdAt"].strftime("%d/%m/%y")
        if item["lastTime"] != time_str:
            item["times"] += 1
            item["lastTime"] = time_str
    for it in auth_db.contact.find(
            {"accountId": {"$in": list(account_di.keys())}, "type": 1}):
        account_di[it["accountId"]]["phone"] = it["value"]

    items = []
    for it in list(account_di.values()):
        items.append((it, it["times"], it["accountId"]))

    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 100]

    return res_li


def count_account_repurchase_rate_this_year():
    """展示用户id,电话,复购率(次数，不在同一天下单的就计算一次，同一天下单的只计一次)"""
    common_query = {"createdAt": {"$gt": datetime(2020, 1, 1)}}
    account_di = {it: {"accountId": it, "times": 0, "lastTime": 0} for it in
                  order_db.SaleOrder.distinct("accountId", common_query)}
    for it in order_db.SaleOrder.find(common_query).sort([("createdAt", -1)]):
        item = account_di[it["accountId"]]
        time_str = it["createdAt"].strftime("%d/%m/%y")
        if item["lastTime"] != time_str:
            item["times"] += 1
            item["lastTime"] = time_str

    for it in auth_db.contact.find(
            {"accountId": {"$in": list(account_di.keys())}, "type": 1}):
        account_di[it["accountId"]]["phone"] = it["value"]

    items = []
    for it in list(account_di.values()):
        items.append((it, it["times"], it["accountId"]))

    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 100]

    return res_li


def count_account_success_gmv():
    """展示用户id,电话, orderAmount , successGMV，按successGMV来倒排，取100个"""
    condition = [
        {"$match": {"status": 5, "createdAt": {"$gt": datetime(2020, 1, 1)}}},
        {"$group": {"_id": "$accountId",
                    "orderAmount": {"$sum": "$orderAmount"}}},
        {"$sort": {"orderAmount": -1}},
        {"$limit": 100}
    ]
    item_di = {}
    for it in order_db.SaleOrder.aggregate(condition):
        item_di[it["_id"]] = {
            "accountId": it["_id"], "orderAmount": it["orderAmount"],
            "successGMV": it["orderAmount"]}
    for it in auth_db.contact.find(
            {"accountId": {"$in": list(item_di.keys())}, "type": 1}):
        item_di[it["accountId"]]["phone"] = it["value"]

    return list(item_di.values())


def store_statistics_gmv(store_ids):
    success_gmvs = []
    transit_gmvs = []
    reject_gmvs = []
    for it in store_ids:
        success_gmv = 0
        transit_gmv = 0
        reject_gmv = 0
        for i in order_db.SaleOrder.find(
                {"storeId": it, "status": {"$in": [-2, 4, 5]},
                 "createdAt": {"$gte": datetime(2021, 1, 1)}}):
            if i.get("status") == 5:
                success_gmv += i.get("orderAmount")
            elif i.get("status") in [4]:
                transit_gmv += i.get("orderAmount")
            elif i.get("status") in [-2]:
                reject_gmv += i.get("orderAmount")
        success_gmvs.append(success_gmv)
        transit_gmvs.append(transit_gmv)
        reject_gmvs.append(reject_gmv)
        print("storeId=%s, gmv=%s,%s,%s" % (
            it, success_gmv, transit_gmv, reject_gmv))
    for it in success_gmvs:
        print(it)
    print("---------------")
    for it in transit_gmvs:
        print(it)
    print("---------------")
    for it in reject_gmvs:
        print(it)
    print("---------------")


def export_excel(rates, gmvs, orders):
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet_1 = workbook.add_worksheet("复购率")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "accountId", bold)
    worksheet_1.write("B1", "phone", bold)
    worksheet_1.write("C1", "times", bold)
    worksheet_1.set_column('A:C', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for it in rates:
        item = it[0]
        worksheet_1.write('A%d' % row_1, item["accountId"])
        worksheet_1.write('B%d' % row_1, item["phone"])
        worksheet_1.write('C%d' % row_1, item["times"])
        row_1 += 1

    worksheet_2 = workbook.add_worksheet("订单金额")
    worksheet_2.write("A1", "accountId", bold)
    worksheet_2.write("B1", "phone", bold)
    worksheet_2.write("C1", "orderAmount", bold)
    worksheet_2.write("D1", "successGMV", bold)
    worksheet_2.set_column('A:D', 20, other_bold)
    worksheet_2.set_row(0, 20)
    row_2 = 2
    for it in gmvs:
        worksheet_2.write('A%d' % row_2, it["accountId"])
        worksheet_2.write('B%d' % row_2, it["phone"])
        worksheet_2.write('C%d' % row_2, it["orderAmount"])
        worksheet_2.write('D%d' % row_2, it["successGMV"])
        row_2 += 1

    worksheet_3 = workbook.add_worksheet("成功交付比例")
    worksheet_3.write("A1", "accountId", bold)
    worksheet_3.write("B1", "phone", bold)
    worksheet_3.write("C1", "orderCount", bold)
    worksheet_3.write("D1", "completeCount", bold)
    worksheet_3.write("E1", "rates", bold)
    worksheet_3.set_column('A:E', 20, other_bold)
    worksheet_3.set_row(0, 20)
    row_3 = 2
    for it in orders:
        item = it[0]
        worksheet_3.write('A%d' % row_3, item["accountId"])
        worksheet_3.write('B%d' % row_3, item.get("phone"))
        worksheet_3.write('C%d' % row_3, item.get("totalCount"))
        worksheet_3.write('D%d' % row_3, item["completeCount"])
        worksheet_3.write('E%d' % row_3, item["ratio"])
        row_3 += 1
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
    statistics_db = get_db(config, env, "Statistics")
    auth_db = get_db(config, env, "Auth")

    # rates = count_account_repurchase_rate_this_year()
    # gmvs = count_account_success_gmv()
    # orders = count_account_success_order_this_year()
    store_ids = [1,2,4,6,41,203,209,210,213,315,317,330,331,365,366,376,378,
                 400,462,463,464,465,466,472,491,492,496]

    store_statistics_gmv(store_ids)

    # export_excel(rates, gmvs, orders)