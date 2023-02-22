# coding: utf-8

import psycopg2
from psycopg2 import Error
import sys
import os
import logging
import pymongo
import json
import arrow
from psycopg2 import sql
from datetime import datetime, timedelta
from threading import Thread

_DEFAULT_LOG_FILE = 'pre_progress_sql_data.log'
_DEFAULT_CONFIG_FILE = '../config.json'
pay_method_di = {2: 'cod', 1: 'online', 3: 'pre'}
order_type = {1: 'normal', 2: 'flash', 3: 'luckyDraw', 5: 'mixed', 4: 'redeem',
              6: 'promotion'}
order_state = {
    1: "pend_pay", 2: "pend_confirm", 3: "pend_ship", 4: "in_transit",
    5: "accept", -1: "cancel", -2: "reject"}


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


def close_connect(connect):
    connect.commit()
    connect.close()


def close_cursor(cursor):
    cursor.close()


def get_one_cursor(connect):
    cursor = connect.cursor()
    return cursor


def connect_post_gre_db(config=None, env=None):
    connection = None
    # uri = config['progresql']['uri']
    database = env + "_data_center"
    try:
        connection = psycopg2.connect(
            user="postgres",
            password="31415926",
            host="159.138.82.236",
            port="5432",
            database=database
        )
        connection.autocommit = True
        """
        查看是否自动提交
        \echo :AUTOCOMMIT 
        关闭自动提交：
         \set AUTOCOMMIT off
         \echo :AUTOCOMMIT 
        """
        # connection = psycopg2.connect(uri)
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)

    return connection


def judge_generate_week(
        cursor, week_key, week_name, month_key, month_name,
        quarterly_key, quarterly_name, year_key, year_name):
    # cursor_select = get_one_cursor(connect_oj)
    cursor.execute(
        "SELECT * from dim_time_week where week_key=%s", (week_key,))
    if not cursor.fetchone():
        # close_cursor(cursor_select)
        cursor.execute(
            sql.SQL("insert into {} values ("
                    "%s, %s, %s, %s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_time_week')), [
                week_key, week_name, month_key, month_name,
                quarterly_key, quarterly_name, year_key, year_name])


def ratio_split_integer(split_num, each_ratio):
    # each_ratio: for example {1: float(1) / 5, 2: float(2) / 5}
    split_list = [int(round(float(item) * split_num)) for item in
                  each_ratio.values()]
    amount = sum(split_list)
    rest_num = abs(split_num - amount)
    index = 0
    number = 0
    if split_num < amount:
        for num in split_list:
            if num == 0:
                index += 1
                continue
            num = num - 1
            split_list[index] = num
            index += 1
            number += 1
            if number == rest_num:
                break
    elif split_num > amount:
        for num in split_list:
            num = num + 1
            split_list[index] = num
            index += 1
            if index == rest_num:
                break
    return dict(zip(each_ratio.keys(), split_list))


def datetime_str_obj(utc_str):
    if type(utc_str) is str:
        return datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return utc_str


def create_dw_sale_order(
        cursor, so, order_tp, payment_type, order_time, end_time, ship_time,
        close_time, confirm_time, pay_time):
    if so["status"] in [-2, 5]:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[so["status"]],
                order_time, close_time, end_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[4],
                order_time, ship_time, close_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[3],
                order_time, confirm_time, ship_time])
        if so["payMethod"] == 1:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, pay_time, confirm_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1],
                order_time, order_time, pay_time or confirm_time])
    elif so["status"] == -1:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[-1],
                order_time, close_time, end_time])
        if ship_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[4],
                    order_time, ship_time, close_time])
        if confirm_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[3],
                    order_time, confirm_time, ship_time or close_time])
        if pay_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, pay_time, confirm_time or close_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1],
                order_time, order_time, pay_time or confirm_time or close_time])

    elif so["status"] == 4:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[4],
                order_time, ship_time, end_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[3],
                order_time, confirm_time, ship_time])
        if pay_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, pay_time, confirm_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1],
                order_time, order_time, pay_time or confirm_time])
    elif so["status"] == 3:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[3],
                order_time, confirm_time, end_time])
        if pay_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, pay_time, confirm_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1],
                order_time, order_time, pay_time or confirm_time])
    elif so["status"] == 2:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[2], order_time,
                pay_time, end_time])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1], order_time,
                order_time, pay_time])
    elif so["status"] == 1:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1], order_time,
                order_time, end_time])


def insert_order_into_base(cursor, start_id, end_id):
    regions = list(common_db.region.find())
    region_code_dict = {it["code"]: it for it in regions}
    warehouse_dict = {}
    for it in wms_warehouse_db.Warehouse.find():
        it["regionId"] = region_code_dict[it["regionCode"]]["code"]
        warehouse_dict[it["_id"]] = it

    so_query = {"id": {"$gte": start_id, "$lt": end_id}}
    for so in order_db.SaleOrder.find(so_query).sort([("id", 1)]):
        if so.get("isRobot"):
            continue
        user = auth_db.account.find_one({"id": so["accountId"]})
        contact = auth_db.contact.find_one({"accountId": so["accountId"]})
        store = seller_db.Store.find_one({"_id": so["storeId"]})
        address = member_db.address.find_one({"id": so["addressId"]})
        sod_count = order_db.SaleOrderDetail.count_documents(
            {"orderId": so["id"]})
        each_ratio = {it+1: 1/sod_count for it in range(sod_count)}
        postage_di = ratio_split_integer(so["postage"], each_ratio)
        pos_dis_di = ratio_split_integer(
            so.get("postageDiscount", 0), each_ratio)
        if so.get("discount") > 0:
            order_tp = "promotion"
        else:
            order_tp = order_type.get(so["orderType"])
        payment_type = pay_method_di[so["payMethod"]]
        order_time = datetime_str_obj(so["createdAt"])
        end_time = "2099-12-31T00:00:00.000Z"
        ship_time = datetime_str_obj(so.get("shippedAt"))
        close_time = datetime_str_obj(so.get("closedAt"))
        confirm_time = datetime_str_obj(so.get("confirmAt"))
        pay_time = datetime_str_obj(so.get("paidAt"))
        create_dw_sale_order(
            cursor, so, order_tp, payment_type, order_time, end_time, ship_time,
            close_time, confirm_time, pay_time)
        pay_during = None
        if pay_time and so["payMethod"] == 1:
            pay_during = pay_time - order_time
        elif so["payMethod"] == 2:
            pay_during = timedelta(0)
        confirm_during = None
        if confirm_time:
            confirm_during = confirm_time - order_time
        postage_index = 1
        for it in order_db.SaleOrderDetail.find({"orderId": so["id"]}):
            listing = goods_db.SpecOfListing.find_one({"_id": it["listingId"]})
            if not listing:
                logging.error("listingId=%s not found in goods db")
                continue
            order_total = (it["amount"] + postage_di[postage_index] -
                           pos_dis_di[postage_index] - it["discount"])
            need_pay = order_total - it.get("redeem", 0) - it.get(
                "voucherRedeem", 0)
            if pay_method_di[so["payMethod"]] == "online":
                paid = need_pay
            else:
                paid = 0

            logging.info(
                "insert into fact_sales values (%s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                % (so["batchId"], so["billId"], it["orderId"], it["id"],
                    int(so["createdAt"].strftime("%Y%m%d")),
                   listing["categoryId"], it["listingId"], it["skuId"],
                    it["salePrice"], so["accountId"], user["nick"],
                    contact["value"], store["sellerId"], so["storeId"],
                    store["name"], address["areaId"], address["cityId"],
                    so["region"], so["warehouseId"], warehouse_di[so["region"]],
                    it["dealPrice"], it["count"], it["amount"],
                    postage_di[postage_index], it.get("redeem", 0),
                    it.get("voucherRedeem", 0), it.get("discount", 0),
                    pos_dis_di[postage_index], order_total, need_pay, paid,
                    payment_type, order_time, order_tp, pay_time,
                    confirm_time, pay_during, confirm_during))
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s, %s,"
                        " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, "
                        "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                        " %s, %s, %s, %s, %s)").format(
                    sql.Identifier('fact_sales')), [
                    so["batchId"], so["billId"], it["orderId"], it["id"],
                    int(so["createdAt"].strftime("%Y%m%d")),
                    listing["categoryId"], it["listingId"], it["skuId"],
                    it["salePrice"], so["accountId"], user["nick"],
                    contact["value"], store["sellerId"], so["storeId"],
                    store["name"], address["areaId"], address["cityId"],
                    so["region"], so["warehouseId"], warehouse_di[so["region"]],
                    it["dealPrice"], it["count"], it["amount"],
                    postage_di[postage_index], it.get("coin", 0),
                    it.get("redeem", 0), it.get("voucherRedeem", 0),
                    it.get("discount", 0), pos_dis_di[postage_index],
                    order_total, need_pay, paid, payment_type, order_time,
                    order_tp, pay_time, confirm_time, pay_during,
                    confirm_during])
            postage_index += 1


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
    auth_db = get_db(config, env, "Auth")
    admin_db = get_db(config, env, "Admin")
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    member_db = get_db(config, env, "Member")
    wms_warehouse_db = get_db(config, env, "WmsWarehouse")
    connect_oj = connect_post_gre_db(config, env)

    cursor_oj = get_one_cursor(connect_oj)

    start_id = 350000
    end_id = 400000
    insert_order_into_base(cursor_oj, start_id, end_id)
    close_cursor(cursor_oj)
    close_connect(connect_oj)
