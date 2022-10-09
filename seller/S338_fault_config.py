# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from puanchen import HeraldMQ
from datetime import datetime

_DEFAULT_LOG_FILE = 'S338_app.log'
_DEFAULT_CONFIG_FILE = '../config.json'
PARAM_LI = [
            {
                "name": "FAULT_1_CH_NAME",
                "value": "轻度取消过失",
                "dataType": "str",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },
            {
                "name": "FAULT_1_FL_NAME",
                "value": "Minor negligence",
                "dataType": "str",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },
            {
                "name": "FAULT_1_IS_PUNISHMENT",
                "value": "1",
                "dataType": "bool",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },
            {
                "name": "FAULT_1_CH_PENALTY_AMOUNT",
                "value": "1.5",
                "dataType": "int",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },
            {
                "name": "FAULT_1_LOCAL_PENALTY_AMOUNT",
                "value": "20",
                "dataType": "int",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },
            {
                "name": "FAULT_1_DESCRIPTION",
                "value": "用户订单被系统(客服)确认后，24小时内 店铺取消订单的",
                "dataType": "str",
                "paramModule": "fault_and_punishment",
                "icon": "",
                "description": "Fault 1"
            },

]


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


def load_cities(filename):
    with open(filename, 'r') as f:
        config = json.loads(f.read())

    return config


def get_db(config, env, database):
    uri = config['mongodb']['uri']
    client = pymongo.MongoClient(uri)
    db = '%s%s' % (env, database)
    return client[db]


def add_fault_and_punishment_config():
    param_id = 0
    param_index = 0
    for it in seller_db.FaultAndPunishmentConfig.find({}).sort(
            [("_id", -1)]).limit(1):
        param_id = it["_id"]
        param_index = it["index"]
    param_li = [
        {
            "name": "过失1",
            "chDisplay": "轻度取消过失",
            "flDisplay": "Minor negligence",
            "isPunishment": True,
            "chPenaltyAmount": 1.5,
            "localPenaltyAmount": 20,
            "isCompensatory": True,
            "compensationCouponId": None,
            "currency": "BDT",
            "description": "用户订单被系统(客服)确认后，24小时内 店铺取消订单的",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失2",
            "chDisplay": "取消过失",
            "flDisplay": "Cancel negligence",
            "isPunishment": True,
            "chPenaltyAmount": 2,
            "localPenaltyAmount": 30,
            "isCompensatory": True,
            "compensationCouponId": None,
            "currency": "BDT",
            "description": "在用户订单被系统(客服)确认后，超过24小时但小于72小时取消订单的",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失3",
            "chDisplay": "懈怠订单",
            "flDisplay": "Slack orders",
            "isPunishment": True,
            "chPenaltyAmount": 4,
            "localPenaltyAmount": 50,
            "isCompensatory": False,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "在用户订单被系统(客服)确认后，超过72小时未发货(未操作成已发货状态)又未取消订单的",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失4",
            "chDisplay": "不处理至取消",
            "flDisplay": "Do not process until cancel",
            "isPunishment": True,
            "chPenaltyAmount": 2,
            "localPenaltyAmount": 30,
            "isCompensatory": True,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "在过失3的基础上，超过120小时不处理的，系统自动取消订单",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失5",
            "chDisplay": "取消过失",
            "flDisplay": "Cancel negligence",
            "isPunishment": True,
            "chPenaltyAmount": 2,
            "localPenaltyAmount": 30,
            "isCompensatory": True,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "在过失3的基础上，即在72-120小时内取消的",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失6",
            "chDisplay": "延迟中转",
            "flDisplay": "Delayed transfer",
            "isPunishment": True,
            "chPenaltyAmount": 4,
            "localPenaltyAmount": 0,
            "isCompensatory": False,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "在订单确认后，已发货且未取消的订单，超过5天(从确认后的次日0点起算) "
                           "未到达中转仓的",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失7",
            "chDisplay": "虚假发货",
            "flDisplay": "False shipping",
            "isPunishment": True,
            "chPenaltyAmount": 4,
            "localPenaltyAmount": 0,
            "isCompensatory": True,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "在订单确认后，已发货且未取消的订单，超过10天未到达中转仓的，系统自动取消订单",
            "paramModule": "fault_and_punishment"
        },
        {
            "name": "过失8",
            "chDisplay": "延迟交付",
            "flDisplay": "Delayed delivery",
            "isPunishment": False,
            "chPenaltyAmount": 0,
            "localPenaltyAmount": 0,
            "isCompensatory": True,
            "currency": "BDT",
            "compensationCouponId": None,
            "description": "从订单确认到订单执行交付关闭时，超过承诺日期+1天的",
            "paramModule": "fault_and_punishment"
        },

    ]
    time_now = datetime.utcnow()
    for item in [1, 3, 4, 5]:
        for it in param_li:
            param_id += 1
            param_index += 1
            add_fields = {
                "_id": param_id,
                "regionId": item,
                "index": param_index,
                "lastUpdatedAt": time_now
            }
            if it == 3:
                add_fields["localPenaltyAmount"] = int(1.5 * 217)
            elif it == 4:
                add_fields["localPenaltyAmount"] = int(1.5 * 24)
            elif it == 5:
                add_fields["localPenaltyAmount"] = int(1.5 * 16.61)
            it.update(add_fields)
            seller_db.FaultAndPunishmentConfig.insert_one(it)


def add_pages():
    page_id = 0
    for it in admin_db.Page.find().sort([("_id", -1)]).limit(1):
        page_id = it["_id"]
    page = {
        "_id": page_id+1,
        "sortIndex": 14,
        "name": "Fault Set",
        "url": "/fault-punishment-configs",
        "menuClassId": 5,
        "activated": True
    }
    admin_db.Page.insert_one(page)
    admin_db.Page.insert_one(
        {"_id": page_id + 2, "sortIndex": 8, "name": "Margin Records",
         "url": "/store/margin-records", "menuClassId": 9, "activated": True}
    )
    admin_db.Page.insert_one(
        {"_id": page_id + 3, "sortIndex": 9, "name": "Margin Streams",
         "url": "/store/margin-streams", "menuClassId": 9, "activated": True}
    )
    admin_db.Page.insert_one(
        {"_id": page_id + 4, "sortIndex": 10, "name": "Fault Records",
         "url": "/store/faults", "menuClassId": 9, "activated": True}
    )

    s_page_id = 0
    for it in seller_db.Page.find().sort([("_id", -1)]).limit(1):
        s_page_id = it["_id"]
    seller_db.Page.insert_one(
        {
            "_id": s_page_id+1,
            "sortIndex": 17,
            "name": "Margin Records",
            "menuClassId": 4,
            "activated": True
        }
    )
    seller_db.Page.insert_one(
        {
            "_id": s_page_id+2,
            "sortIndex": 18,
            "name": "Margin Streams",
            "menuClassId": 4,
            "activated": True
        }
    )
    seller_db.Page.insert_one(
        {
            "_id": s_page_id + 3,
            "sortIndex": 19,
            "name": "Fault Punishment",
            "menuClassId": 4,
            "activated": True
        }
    )
    seller_db.Page.insert_one(
        {
            "_id": s_page_id + 4,
            "sortIndex": 20,
            "name": "Margin Disclaimer",
            "menuClassId": 4,
            "activated": True
        }
    )


def store_add_currency_and_initialize_margin():
    currency_di = {it["id"]: it["currency"] for it in common_db.region.find({})}
    now_utc = datetime.utcnow()
    years = datetime(now_utc.year, now_utc.month, 1)
    for it in seller_db.StoreApply.find({}):
        currency = currency_di[it["sellerRegionId"]]
        seller_db.StoreApply.update_one(
            {"_id": it["_id"]}, {"$set": {
                "margin.currency": currency, "margin.amount": 0}})
    for it in seller_db.Store.find({}):
        currency = currency_di[it["sellerRegionId"]]
        store_field = {"margin.currency": currency}
        if it["margin"]["status"] == 1:
            store_field["margin.amount"] = 0
        seller_db.Store.update_one(
            {"_id": it["_id"]}, {"$set": store_field})
        seller_db.MonthlyMarginAndDisclaimer.insert_one(
            {
                "storeId": it["_id"],
                "sellerRegionId": it["sellerRegionId"],
                "currency": currency,
                "years": years,
                "disclaimerCount": 2,
                "disclaimerDeducted": 0,
                "marginDeducted": 0
            }
        )


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    seller_db = get_db(config, env, "Seller")
    common_db = get_db(config, env, "Common")
    admin_db = get_db(config, env, "Admin")
    add_fault_and_punishment_config()
    add_pages()
    store_add_currency_and_initialize_margin()
    pass

    print("---------------------------success-------------------------------")

