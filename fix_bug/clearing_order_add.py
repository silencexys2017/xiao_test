# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from puanchen import HeraldMQ
from datetime import datetime

_DEFAULT_LOG_FILE = 'clearing_order_add.log'
_DEFAULT_CONFIG_FILE = '../config.json'

mq_data = {
    "dev": ('rabbitmq', 5672, 'rmq-dev', '7M9Yrym4L9G6cxhNe9Xf', 'perfee-dev'),
    "test": ('rabbitmq', 5672, 'rmq-test', 'ALpW854bZ29HrAzjce8v',
             'perfee-test'),
    "prd": ('rabbitmq', 5672, 'rmq-prd', 'a3zWdf2X7xuEPWg259Xb', 'perfee-prd')}
host = "10.20.25.177"

# DeliveryMethod
PLATFORM_CARRIER = 1  # 平台派送，平台统收
SHOP_SELF_DELIVERY = 2   # 店铺自己派送，⾮平台统收
SHOP_SELF_SET = 3  # 平台派送, 运费自己设置，⾮平台统收
ALL = 0

# VoucherOwner
PLATFORM_VOUCHER = 1
STORE_VOUCHER = 2
# pay method
ONLINE_PAY = 1
COD = 2
# 支付通道
SSL = 1
BKASH = 2
VIRTUAL = -1
KBZ = 3
GMO = 4
# queue name
ORDER_RECEIVE_COMPLETE = "order_receive_complete"
GOODS_ORDER_COMPLETE_NOTICE = "goods_order_complete_notice"
GOODS_DELAY_30_CHECK_REVIEW = "goods_delay_30_check_review"
PHOENIX_COMPLETE_ORDER = "phoenix_complete_order"
ORDER_REJECT_COMPLETE = "order_reject_complete"
PHOENIX_REJECT_ORDER = "phoenix_reject_order"


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


def get_rmq(env):
    data = mq_data.get(env)
    return HeraldMQ(host, data[1], data[4], data[2], data[3])


def set_queue_name(env):
    return ('order-normal-%s' % env, 'goods-normal-%s' % env,
            'goods-delay-30-%s' % env, 'queue-phoenix-%s' % env)


def obj_time_to_str(utc_time):
    if utc_time:
        return datetime.strftime(utc_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return None


def retain_decimal_places(num, digits=2):
    if "." in str(num):
        num_x, num_y = str(num).split('.')
        num = float(num_x + '.' + num_y[0: digits])

    return num


def _send_message_to_queue(queue_name, msg, is_delay=False, ttl=0):
    retry_times = 0
    while True:
        try:
            retry_times += 1
            if is_delay:
                rmq_con.send_delay_message(queue_name, json.dumps(msg))
            elif ttl:
                rmq_con.send_ttl_message(
                    queue_name, json.dumps(msg), str(ttl))
            else:
                rmq_con.send_message(queue_name, json.dumps(msg))
            break
        except Exception as exc:
            logging.error('[order] _send_message_to_queue(%s)' % exc)

            raise Exception(exc)


def get_related_data(start_time):
    sp_query = {"status": 4, "deliveredAt": {"$gt": start_time}}
    co_query = {"completedAt": {"$gt": start_time}}
    so_ids_1 = order_db.ShipPackage.distinct("saleOrderId", sp_query)
    so_ids_2 = statistics_db.ClearingOrder.distinct("saleOrderId", co_query)
    so_ids = []
    for it in so_ids_1:
        if it not in so_ids_2:
            so_ids.append(it)
    cod_rate = float(order_db.parameter.find_one(
        {"name": "PAY_GATEWAY_FEE_RATE_COD"})["value"])
    cod_max = float(order_db.parameter.find_one(
        {"name": "MAXIMUM_SINGLE_FEE_COD"})["value"])
    ssl_rate = float(order_db.parameter.find_one(
        {"name": "PAY_GATEWAY_FEE_RATE_SSL"})["value"])
    ssl_max = float(order_db.parameter.find_one(
        {"name": "MAXIMUM_SINGLE_FEE_SSL"})["value"])
    bkash_rate = float(order_db.parameter.find_one(
        {"name": "PAY_GATEWAY_FEE_RATE_BKASH"})["value"])
    bkash_max = float(order_db.parameter.find_one(
        {"name": "MAXIMUM_SINGLE_FEE_BKASH"})["value"])
    kbz_rate = float(order_db.parameter.find_one(
        {"name": "PAY_GATEWAY_FEE_RATE_KBZ"})["value"])
    kbz_max = float(order_db.parameter.find_one(
        {"name": "MAXIMUM_SINGLE_FEE_KBZ"})["value"])

    for item in so_ids:
        so_di = order_db.SaleOrder.find_one({"id": item})
        spg_di = order_db.ShipPackage.find_one({"saleOrderId": item})
        shod_li = []
        for it in order_db.ShipOrderDetail.find({"packageId": spg_di["id"]}):
            shod_li.append(
                {"id": it["id"], "skuId": it["skuId"], "count": it["count"],
                 "listingId": it.get("listingId")})
        data = {
            "accountId": spg_di["accountId"], "regionId": spg_di["region"],
            "packageId": spg_di["id"], "shipOrders": [{
                "saleOrderId": spg_di["saleOrderId"],
                "storeId": spg_di["storeId"], "shipOrderDetails": shod_li}]}

        ac_data = {}
        so_rs = order_db.PromotionPlatformOrder.find_one(
            {"saleOrderId": spg_di["saleOrderId"]})
        if so_rs:
            ac_data = {"orderId": str(spg_di["saleOrderId"]),
                       "accountId": spg_di["accountId"],
                       "time": obj_time_to_str(datetime.utcnow())}

        is_self_delivery = True if so_di.get(
            "deliveryMethod") == SHOP_SELF_DELIVERY else False
        postage = so_di["postage"] - so_di.get("postageRedeem", 0) - \
                  so_di.get("postageDiscount", 0)
        add_data = {
            "packageCode": spg_di["code"], "SHOContain": 1,
            "saleOrderId": so_di["id"], "postage": postage,
            "payMethod": so_di["payMethod"], "orderType": so_di["orderType"],
            "createdAt": obj_time_to_str(so_di["createdAt"]),
            "commissionRate": so_di["commissionRate"],
            "isSelfDelivery": is_self_delivery, "regionId": so_di["region"],
            "warehouseId": so_di["warehouseId"], "status": spg_di["status"],
            "terminalDeliveryCode": spg_di["terminalDeliveryCode"],
            "terminalDeliveryId": spg_di.get("terminalDeliveryId", 1),
            "completedAt": obj_time_to_str(spg_di["deliveredAt"]),
            "storeId": so_di["storeId"], "accountId": so_di["accountId"],
            "deliveryMethod": so_di.get("deliveryMethod"),
            "coinRedeem": so_di["redeem"],
            "discount": so_di["discount"],
            "payAmount": so_di["payAmount"],
            "voucherRedeem": so_di.get("voucherRedeem", 0),
            "itemTotal": so_di["itemTotal"]
        }
        if add_data["voucherRedeem"] > 0:
            vb_di = order_db.VoucherBill.find_one({"billId": so_di["billId"]})
            if vb_di["ownerType"] == PLATFORM_VOUCHER:
                add_data["platVoucher"] = add_data["voucherRedeem"]
            else:
                add_data["storeVoucher"] = add_data["voucherRedeem"]

        if add_data["payMethod"] == ONLINE_PAY:
            pay_di = order_db.PayTransactions.find_one(
                {"billId": so_di["billId"]})
            if pay_di["gatewayId"] == SSL:
                if pay_di.get("responseData"):
                    store_amount = float(pay_di["responseData"]["store_amount"])
                    add_data["payFee"] = retain_decimal_places(
                        float(add_data["payAmount"]) / pay_di["amount"]*(
                                pay_di["amount"]-store_amount))
                else:
                    fee = retain_decimal_places(add_data["payAmount"]*ssl_rate)
                    if fee > ssl_max:
                        fee = ssl_max
                    add_data["payFee"] = fee

            elif pay_di["gatewayId"] == BKASH:
                fee = retain_decimal_places(add_data["payAmount"]*bkash_rate)
                if fee > bkash_max:
                    fee = bkash_max
                add_data["payFee"] = fee

            elif pay_di["gatewayId"] == KBZ:
                fee = retain_decimal_places(add_data["payAmount"]*kbz_rate)
                if fee > kbz_max:
                    fee = kbz_max
                add_data["payFee"] = fee

        elif add_data["payMethod"] == COD:
            fee = retain_decimal_places(add_data["payAmount"]*cod_rate)
            if fee > cod_max:
                fee = cod_max
            add_data["payFee"] = fee
        print("------data-----=%s" % data)
        print("------add_data-----=%s" % add_data)
        print("------ac_data------=%s" % ac_data)
        com_data = data
        com_data["clearData"] = add_data
        msg_1 = {"action": ORDER_RECEIVE_COMPLETE, "data": com_data}
        _send_message_to_queue(QUEUE_ORDER_NORMAL, msg_1)
        msg_2 = {"action": GOODS_ORDER_COMPLETE_NOTICE, "data": data}
        msg_3 = {"action": GOODS_DELAY_30_CHECK_REVIEW, "data": data}
        _send_message_to_queue(QUEUE_GOODS_NORMAL, msg_2)
        _send_message_to_queue(
            QUEUE_GOODS_DELAY_30, msg_3, is_delay=True)
        if so_rs:
            msg_4 = {
                "action": PHOENIX_COMPLETE_ORDER, "data": ac_data}
            _send_message_to_queue(QUEUE_PHOENIX, msg_4)


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
    rmq_con = get_rmq(env)
    QUEUE_ORDER_NORMAL, QUEUE_GOODS_NORMAL, QUEUE_GOODS_DELAY_30,\
    QUEUE_PHOENIX = set_queue_name(env)
    get_related_data(start_time=datetime(2021, 1, 1))

    print("---------------------------success-------------------------------")

