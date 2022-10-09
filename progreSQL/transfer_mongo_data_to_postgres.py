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
from psycopg2.extras import execute_values

_DEFAULT_LOG_FILE = 'pre_progress_sql_data.log'
_DEFAULT_CONFIG_FILE = '../config.json'
pay_method_di = {2: 'cod', 1: 'online', 3: 'pre'}
order_type = {
    1: 'normal', 2: 'flash', 3: 'luckyDraw', 4: 'redeem', 5: 'mixed',
    6: 'groupBuy', 7: 'promotion'}
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
    uri = config['progresql']['uri']
    database = env + "_data_centers"
    try:
        # connection = psycopg2.connect(
        #     user="postgres",
        #     password="31415926",
        #     host="159.138.82.236",
        #     port="5432",
        #     database=database
        # )
        connection = psycopg2.connect(
            uri, dbname=database)
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


def create_tables(cursor):
    payment_type = """
        CREATE TYPE PAYMENT_TYPE AS ENUM ('cod', 'online', 'pre');
        """
    cursor.execute(payment_type)
    order_types = """
        CREATE TYPE ORDER_TYPE AS ENUM (
        'normal', 'flash', 'luckyDraw', 'groupBuy', 'mixed', 'redeem', 
        'promotion');
        """
    # cursor.execute("""DROP TYPE ORDER_TYPE;""")
    cursor.execute(order_types)

    sale_order_status = """
        CREATE TYPE SALE_ORDER_STATUS AS ENUM (
        'pend_pay', 'pend_confirm', 'pend_ship', 'in_transit', 'accept', 'wait',
        'cancel', 'reject');
        """
    # cursor.execute("""DROP TYPE SALE_ORDER_STATUS;""")
    cursor.execute(sale_order_status)

    fact_sales_table = """CREATE TABLE fact_sales (
    batch_id INTEGER NOT NULL,
    bill_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    order_detail_id INTEGER NOT NULL,
    date_key INTEGER,
    cat_3_id INTEGER,
    listing_id BIGINT NOT NULL,
    sku_id BIGINT NOT NULL,
    sale_price MONEY,
    user_id INTEGER,
    seller_id INTEGER,
    store_id INTEGER,
    sale_area_id INTEGER,
    sale_city_id INTEGER,
    sale_region_id INTEGER,
    warehouse_id INTEGER,
    from_region_id INTEGER,
    deal_price MONEY,
    product_qty INTEGER,
    item_total MONEY,
    postage MONEY,
    coins MONEY,
    coins_redeem MONEY,        
    voucher_redeem MONEY,
    item_discount MONEY,
    postage_discount MONEY,
    order_total MONEY,
    need_pay MONEY,
    online_paid MONEY,
    cod_amount MONEY,
    payment_type PAYMENT_TYPE,
    order_time TIMESTAMP, 
    order_type ORDER_TYPE Default 'normal',
    pay_time TIMESTAMP,
    confirm_time TIMESTAMP,
    pay_during INTERVAL, 
    confirm_during INTERVAL                                                                           
    );"""
    # cursor.execute("""DROP TABLE Fact_Sales;""")
    cursor.execute(fact_sales_table)

    fact_sales_daily_detail = """CREATE TABLE fact_sales_daily_detail (
                    date_key INTEGER,
                    order_id INTEGER,
                    order_type ORDER_TYPE Default 'normal',
                    order_detail_id INTEGER,
                    store_id INTEGER,
                    seller_id INTEGER,
                    cat_3_id INTEGER,
                    sale_area_id INTEGER,
                    sale_city_id INTEGER,
                    sale_region_id INTEGER,
                    warehouse_id INTEGER,
                    from_region_id INTEGER,
                    payment_type PAYMENT_TYPE,
                    user_id INTEGER,
                    listing_id BIGINT NOT NULL,
                    sku_id BIGINT NOT NULL,
                    order_total MONEY DEFAULT 0,
                    item_total MONEY DEFAULT 0,
                    postage MONEY DEFAULT 0,
                    success_gmv MONEY DEFAULT 0,
                    coins_redeem MONEY DEFAULT 0,
                    voucher_redeem MONEY DEFAULT 0,
                    success_voucher_redeem MONEY DEFAULT 0,
                    success_coin_redeem MONEY DEFAULT 0,
                    item_discount MONEY DEFAULT 0,
                    success_item_discount MONEY DEFAULT 0,
                    postage_discount MONEY DEFAULT 0,
                    confirm_gmv MONEY DEFAULT 0,
                    reject_gmv MONEY DEFAULT 0,
                    cancel_gmv MONEY DEFAULT 0,
                    online_paid MONEY DEFAULT 0,
                    need_pay MONEY DEFAULT 0,
                    cod_amount MONEY DEFAULT 0,
                    order_count INTEGER DEFAULT 0,
                    create_order_id INTEGER DEFAULT NULL,
                    paid_count INTEGER DEFAULT 0,
                    paid_order_id INTEGER DEFAULT NULL,
                    confirm_count INTEGER DEFAULT 0, 
                    confirm_order_id INTEGER DEFAULT NULL,
                    cancel_count INTEGER DEFAULT 0,
                    cancel_order_id INTEGER DEFAULT NULL,
                    reject_count INTEGER DEFAULT 0,
                    reject_order_id INTEGER DEFAULT NULL,
                    success_count INTEGER DEFAULT 0, 
                    success_order_id INTEGER DEFAULT NULL,
                    product_qty INTEGER DEFAULT 0,
                    success_qty_count INTEGER DEFAULT 0
                    );"""
    # cursor.execute("""DROP TABLE fact_sales_daily_detail;""")
    cursor.execute(fact_sales_daily_detail)

    dim_cat_3 = """CREATE TABLE dim_cat_3 (
    id INTEGER,
    name VARCHAR(256),
    cat_1_id INTEGER,
    cat_2_id INTEGER
    );"""
    # cursor.execute("""DROP TABLE dim_cat_3;""")
    cursor.execute(dim_cat_3)

    dim_cat_2 = """CREATE TABLE dim_cat_2 (
        id INTEGER,
        name VARCHAR(256),
        cat_1_id INTEGER
        );"""
    # cursor.execute("""DROP TABLE dim_cat_3;""")
    cursor.execute(dim_cat_2)

    dim_cat_1 = """CREATE TABLE dim_cat_1 (
        id INTEGER,
        name VARCHAR(256)
        );"""
    # cursor.execute("""DROP TABLE dim_cat_1;""")
    cursor.execute(dim_cat_1)

    dim_area = """CREATE TABLE dim_area (
    id INTEGER,
    name VARCHAR(128),
    province_id INTEGER,
    city_id INTEGER,
    region_id INTEGER
    );"""
    # cursor.execute("""DROP TABLE dim_area;""")
    cursor.execute(dim_area)

    dim_city = """CREATE TABLE dim_city (
    id INTEGER,
    name VARCHAR(128),
    province_id INTEGER,
    region_id INTEGER
    );"""
    # cursor.execute("""DROP TABLE dim_city;""")
    cursor.execute(dim_city)

    dim_province = """CREATE TABLE dim_province (
    id INTEGER,
    name VARCHAR(128),
    region_id INTEGER
    );"""
    # cursor.execute("""DROP TABLE dim_province;""")
    cursor.execute(dim_province)

    dim_region = """CREATE TABLE dim_region (
    id INTEGER,
    name VARCHAR(128),
    code VARCHAR(28)
    );"""
    # cursor.execute("""DROP TABLE dim_region;""")
    cursor.execute(dim_region)

    dim_warehouse = """CREATE TABLE dim_warehouse (
    id INTEGER,
    name VARCHAR(128),
    region_id INTEGER
    );"""
    # cursor.execute("""DROP TABLE dim_warehouse;""")
    cursor.execute(dim_warehouse)

    dw_sale_order = """CREATE TABLE dw_sale_order (
        sale_order_id INTEGER,
        order_type ORDER_TYPE,
        payment_type PAYMENT_TYPE,
        status SALE_ORDER_STATUS,
        order_time TIMESTAMP,
        dw_begin_date TIMESTAMP,
        dw_end_date TIMESTAMP
        );"""
    # TIMESTAMPTZ 带有时区， TIMESTAMP 不带时区
    # cursor.execute("""DROP TABLE dw_sale_order;""")
    cursor.execute(dw_sale_order)

    dim_seller = """CREATE TABLE dim_seller (
            id INTEGER,
            region_id INTEGER,
            name VARCHAR(128),
            phone VARCHAR(28)
            );"""
    # cursor.execute("""DROP TABLE dim_seller;""")
    cursor.execute(dim_seller)

    dim_store = """CREATE TABLE dim_store (
            id INTEGER PRIMARY KEY,
            seller_id INTEGER,
            region_id INTEGER,
            seller_region_id INTEGER,
            name VARCHAR(128)
            );"""
    # cursor.execute("""DROP TABLE dim_store;""")
    cursor.execute(dim_store)

    fact_sales_daily_summary = """CREATE TABLE fact_sales_daily_summary (
                date_key INTEGER,
                store_id INTEGER,
                store_name VARCHAR(128),
                cat_3_id INTEGER,
                cat_3_name VARCHAR(128),
                gmv MONEY,
                success_gmv MONEY,
                reject_amount MONEY,
                cancel_amount MONEY,
                online_paid MONEY,
                cod_amount MONEY,
                confirm_amount MONEY,
                order_count INTEGER,
                confirm_count INTEGER, 
                cancel_count INTEGER,
                reject_count INTEGER,
                success_count INTEGER, 
                product_qty INTEGER
                );"""
    # cursor.execute("""DROP TABLE fact_sales_daily_summary;""")
    cursor.execute(fact_sales_daily_summary)

    fact_sales_monthly_aggr = """CREATE TABLE fact_sales_monthly_aggr (
                    month_key INTEGER,
                    store_id INTEGER,
                    store_name VARCHAR(128),
                    cat_3_id INTEGER,
                    cat_3_name VARCHAR(128),
                    sku_id INTEGER,
                    sku_title VARCHAR(512),
                    listing_id INTEGER,
                    gmv MONEY,
                    success_gmv MONEY,
                    reject_amount MONEY,
                    cancel_amount MONEY,
                    online_paid MONEY,
                    cod_amount MONEY,
                    confirm_amount MONEY,
                    order_count INTEGER,
                    confirm_count INTEGER, 
                    cancel_count INTEGER,
                    reject_count INTEGER,
                    success_count INTEGER, 
                    product_qty INTEGER
                    );"""
    # cursor.execute("""DROP TABLE fact_sales_monthly_aggr;""")
    cursor.execute(fact_sales_monthly_aggr)

    dim_time_date = """CREATE TABLE dim_time_date (
                date_key INTEGER PRIMARY KEY,
                date_value DATE,
                date_name VARCHAR(128),
                week_key INTEGER,
                week_name VARCHAR(128),
                week_value VARCHAR(128),
                month_key INTEGER,
                month_name VARCHAR(128),
                quarterly_key INTEGER,
                quarterly_name VARCHAR(128),
                year_key INTEGER,
                year_name VARCHAR(128)
                );"""
    """
    year_key: 2019,
    year_name: 2019年,
    quarterly_key: 20191,
    quarterly_name: 2019年第一季度,
    month_key: 201901,
    month_name: 2019年1月,
    week_key: 1,
    week_name: 2019年第1周，
    week_value: 星期一，
    date_key： 20190101,
    date_value: "2019-01-01",
    date_name: "2019年1月11日"
    """
    # cursor.execute("""DROP TABLE dim_time_date;""")
    cursor.execute(dim_time_date)

    dim_time_week = """CREATE TABLE dim_time_week (
            week_key INTEGER PRIMARY KEY,
            week_name VARCHAR(128),
            month_key INTEGER,
            month_name VARCHAR(128),
            quarterly_key INTEGER,
            quarterly_name VARCHAR(128),
            year_key INTEGER,
            year_name VARCHAR(128)                                                                        
            );"""
    # cursor.execute("""DROP TABLE dim_time_week;""")
    cursor.execute(dim_time_week)

    dim_time_month = """CREATE TABLE dim_time_month (
            month_key INTEGER PRIMARY KEY,
            month_name VARCHAR(128),
            quarterly_key INTEGER,
            quarterly_name VARCHAR(128),
            year_key INTEGER,
            year_name VARCHAR(128)                                                       
            );"""
    # cursor.execute("""DROP TABLE dim_time_month;""")
    cursor.execute(dim_time_month)

    dim_time_qtr = """CREATE TABLE dim_time_qtr (
        quarterly_key INTEGER PRIMARY KEY,
        quarterly_name VARCHAR(128),
        year_key INTEGER,
        year_name VARCHAR(128)                                                                          
        );"""
    # cursor.execute("""DROP TABLE dim_time_qtr;""")
    cursor.execute(dim_time_qtr)

    dim_time_year = """CREATE TABLE dim_time_year (
        year_key INTEGER PRIMARY KEY,
        year_name VARCHAR(128)                                                               
        );"""
    # cursor.execute("""DROP TABLE dim_time_year;""")
    cursor.execute(dim_time_year)

    actual_user_and_contact = """CREATE TABLE actual_user_and_contact (
        user_id INTEGER PRIMARY KEY,
        nick VARCHAR(256),
        created_time TIMESTAMP,
        region_id INTEGER,
        phone_number VARCHAR(128),
        mailbox VARCHAR(128),
        facebook_account VARCHAR(128)
        );"""
    # cursor.execute("""DROP TABLE actual_user_and_contact;""")
    cursor.execute(actual_user_and_contact)

    enum_sales_target = """CREATE TABLE enum_sales_target (
        id serial NOT NULL,
        subject_name VARCHAR(256),
        target_name VARCHAR(256),
        display_name VARCHAR(256),
        is_selected BOOLEAN DEFAULT FALSE,
        operator_id INTEGER DEFAULT NULL
        );"""

    # cursor.execute("""DROP TABLE enum_sales_target;""")
    cursor.execute(enum_sales_target)

    enum_sales_dimension = """CREATE TABLE enum_sales_dimension (
            id serial NOT NULL,
            subject_name VARCHAR(256),
            dimension_name VARCHAR(256),
            display_name VARCHAR(256),
            is_selected BOOLEAN DEFAULT FALSE,
            depth INTEGER DEFAULT 1,
            structure text[][], 
            select_type VARCHAR(28) DEFAULT NULL,
            operator_id INTEGER DEFAULT NULL
            );"""

    # cursor.execute("""DROP TABLE enum_sales_dimension;""")
    cursor.execute(enum_sales_dimension)


def insert_user_and_contact_into_base(cursor, start_id, end_id):
    query = {"id": {"$gte": start_id, "$lt": end_id}}
    for item in auth_db.account.find(query).sort([("id", 1)]):
        user = {}
        for it in auth_db.contact.find({"accountId": item["id"]}):
            if it["type"] == 1:
                user["phone"] = it["value"]
            elif it["type"] == 2:
                user["email"] = it["value"]
            elif it["type"] == 3:
                user["facebook"] = it["value"]
        logging.info(
            "insert into actual_user_and_contact user_id=%s" % item["id"])
        cursor.execute(
            sql.SQL(
                "insert into {} values (%s, %s, %s, %s, %s, %s, %s)").format(
                sql.Identifier('actual_user_and_contact')), [
                item["id"], item["nick"], item["timeCreated"], item["region"],
                user.get("phone"), user.get("email"), user.get("facebook"), ])


def is_leap_year(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):
        days_sum = 366
        return days_sum
    else:
        days_sum = 365
        return days_sum


def generate_year_quarterly_month(year, cursor):
    year_name = str(year) + "年"
    cursor.execute(
        sql.SQL("insert into {} values (%s, %s)").format(
            sql.Identifier('dim_time_year')), [year, year_name])
    month = 1
    for it in [1, 2, 3, 4]:
        quarterly_key = int(str(year) + str(it))
        quarterly_name = year_name + "第" + str(it) + "季度"
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s)").format(
                sql.Identifier('dim_time_qtr')), [
                quarterly_key, quarterly_name, year, year_name])
        for i in range(3):
            month_name = year_name + str(month) + "月"
            month_index = str(month) if len(str(month)) == 2 else "0" + str(month)
            month_key = int(str(year) + month_index)
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s)").format(
                    sql.Identifier('dim_time_month')), [
                    month_key, month_name, quarterly_key, quarterly_name,
                    year, year_name])
            month += 1


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


def get_all_day_per_year(year, cursor):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    generate_year_quarterly_month(year, cursor)
    start_date = '%s-1-1' % year
    a = 0
    all_date_list = []
    days_sum = is_leap_year(int(year))
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a)
        year_key = b.year
        year_name = str(year_key) + "年"
        month_key = int(b.format("YYYYMM"))
        month_index = b.month
        month_name = year_name + str(month_index) + "月"
        if month_index in [1, 2, 3]:
            quarterly_key = int(str(year_key) + str(1))
            quarterly_index = 1
        elif month_index in [4, 5, 6]:
            quarterly_key = int(str(year_key) + str(2))
            quarterly_index = 2
        elif month_index in [7, 8, 9]:
            quarterly_key = int(str(year_key) + str(3))
            quarterly_index = 3
        else:
            quarterly_key = int(str(year_key) + str(4))
            quarterly_index = 4
        quarterly_name = year_name + "第" + str(quarterly_index) + "季度"
        week_tuple = b.isocalendar()
        week_id = week_tuple[1]
        week_index = str(week_id) if len(str(week_id)) == 2 else\
            "0" + str(week_id)
        week_key = int(str(week_tuple[0]) + week_index)
        week_name = str(week_tuple[0]) + "第" + str(week_id) + "周"
        week_value = "星期" + str(b.isoweekday())
        if week_tuple[0] == year:
            judge_generate_week(
                cursor, week_key, week_name, month_key, month_name,
                quarterly_key, quarterly_name, year_key, year_name)

        date_index = str(b.day) if len(str(b.day)) == 2 else "0" + str(b.day)
        date_key = int(b.format("YYYYMMDD"))
        date_name = month_name + date_index
        date_value = b.format("YYYY-MM-DD")
        # if week_tuple[0] != year:
        #     week_key = int(str(week_tuple[0]) + week_index)
        #     week_name = str(week_tuple[0]) + "第" + str(week_id) + "周"

        cursor.execute(
            sql.SQL("insert into {} values ("
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_time_date')), [
                date_key, date_value, date_name, week_key, week_name,
                week_value, month_key, month_name, quarterly_key,
                quarterly_name, year_key, year_name])
        #  b.isoweekday() 当前时间是一周的星期几
        #  b.isocalendar()[1] 当前是一年中的第几周
        # b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)

    print(all_date_list)


def insert_datetime_into_base(cursor):
    for it in range(2018, 2031):
        get_all_day_per_year(it, cursor)


def insert_store_into_base(cursor):
    for it in seller_db.Store.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_store')), [
                it["_id"], it["sellerId"], it["regionId"], it["sellerRegionId"],
                it["name"]])
    for it in seller_db.Seller.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s)").format(
                sql.Identifier('dim_seller')), [
                it["_id"], it["regionId"], it["name"], it["phone"]])


def insert_warehouse_and_cat(cursor):
    for it in goods_db.Warehouse.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s)").format(
                sql.Identifier('dim_warehouse')), [
                it["_id"], it["name"], it["regionId"]])

    for it in goods_db.Category.find({"depth": 2}):
        print(it)
        cat = it["path"].split(":")
        cat_1 = int(cat[0])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s)").format(
                sql.Identifier('dim_cat_2')), [
                it["_id"], it["name"], cat_1])

    for it in goods_db.Category.find({"depth": 3}):
        print(it)
        cat = it["path"].split(":")
        cat_1 = int(cat[0])
        cat_2 = int(cat[1])
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s)").format(
                sql.Identifier('dim_cat_3')), [
                it["_id"], it["name"], cat_1, cat_2])

    for it in goods_db.Category.find({"depth": 1}):
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s)").format(
                sql.Identifier('dim_cat_1')), [
                it["_id"], it["name"]])


def insert_address_into_base(cursor):
    for it in common_db.region.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s)").format(
                sql.Identifier('dim_region')), [
                it["id"], it["name"], it["code"]])

    for it in common_db.state.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s)").format(
                sql.Identifier('dim_province')), [
                it["id"], it["name"], it["regionId"]])

    for it in common_db.city.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s)").format(
                sql.Identifier('dim_city')), [
                it["id"], it["name"], it["stateId"], it["regionId"]])

    for it in common_db.area.find():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_area')), [
                it["id"], it["name"], it["stateId"], it["cityId"],
                it["regionId"]])


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


def insert_enum_into_base(cursor):
    execute_values(cursor, """INSERT INTO enum_sales_target (
        subject_name, target_name, display_name, is_selected, operator_id
        ) VALUES %s""", [
        ("sales_top", "gmv", "GMV", False, None),
        ("sales_top", "orderCount", "OrderCNT", False, None),
        ("sales_top", "successGmv", "SucGMV", False, None),
        ("sales_top", "rejectAmount", "RejectAmount", False, None),
        ("sales_top", "itemTotal", "ItemTotal", False, None),
        ("sales_top", "productQty", "Qty", False, None),
        ("sales_top", "postage", "Postage", False, None),
        ("sales_top", "coinsRedeem", "CoinsRedeem", False, None),
        ("sales_top", "voucherRedeem", "VoucherRedeem", False, None),
        ("sales_normal", "gmv", "GMV", True, None),
        ("sales_normal", "orderCount", "OrderCNT", True, None),
        ("sales_normal", "successGmv", "SucGMV", False, None),
        ("sales_normal", "rejectAmount", "RejectAmount", False, None),
        ("sales_normal", "itemTotal", "ItemTotal", False, None),
        ("sales_normal", "productQty", "Qty", False, None),
        ("sales_normal", "postage", "Postage", False, None),
        ("sales_normal", "coinsRedeem", "CoinsRedeem", False, None),
        ("sales_normal", "voucherRedeem", "VoucherRedeem", False, None)
    ])

    execute_values(cursor, """INSERT INTO enum_sales_dimension (
        subject_name, dimension_name, display_name, is_selected, depth, 
        structure, select_type, operator_id) VALUES %s""", [
        ("sales_top", "dateTime", "DateTime", False, 5,
         '{{1,"year"},{2,"quarterly"},{3, "month"}, {4, "week"}, {5, "day"}}',
         None, None),
        ("sales_top", "category", "Category", False, 3,
         '{{1,"first level"},{2,"second level"},{3, "third level"}}',
         None, None),
        ("sales_top", "seller", "Seller", False, 2,
         '{{1,"seller"},{2,"store"}}', None, None),
        ("sales_top", "salesRegions", "SalesRegions", False, 4,
         '{{1,"region"},{2,"state"},{3, "city"}, {4, "area"}}', None, None),
        ("sales_top", "store", "Store", False, 1, '{{1,"store"}}', None, None),
        ("sales_top", "listing", "Listing", True, 2,
         '{{1,"listing"},{2,"sku"}}', None, None),
        ("sales_top", "sku", "SKU", False, 1, '{{1,"sku"}}', None, None),
        ("sales_normal", "dateTime", "DateTime", True, 5,
         '{{1,"year"},{2,"quarterly"},{3, "month"}, {4, "week"}, {5, "day"}}',
         "col", None),
        ("sales_normal", "category", "Category", True, 3,
         '{{1,"first level"},{2,"second level"},{3, "third level"}}',
         "row", None),
        ("sales_normal", "paymentMethod", "PaymentMethod", False, 1,
         '{{1,"paymentMethod"}}', None, None),
        ("sales_normal", "seller", "Seller", False, 2,
         '{{1,"seller"},{2,"store"}}', None, None),
        ("sales_normal", "deliveryRegion", "DeliveryRegion", False, 1,
         '{{1,"deliveryRegion"}}', None, None),
        ("sales_normal", "deliveryWarehouse", "DeliveryWarehouse", False, 1,
         '{{1,"deliveryWarehouse"}}', None, None),
        ("sales_normal", "salesRegions", "SalesRegions", False, 4,
         '{{1,"region"},{2,"state"},{3, "city"}, {4, "area"}}', None, None),
    ])


def create_fact_sales_daily_detail(
        cursor, so, sod, create_date_key, cat_3_id, seller_id, area_id, city_id,
        warehouse_region_id, postage, postage_discount, order_total,
        need_pay, online_paid, cod_amount, payment_type, order_type,
        order_time, pay_time, confirm_time, ship_time, close_time):
    cursor.execute(
        """INSERT INTO fact_sales_daily_detail (
        date_key, order_id, order_type, order_detail_id, store_id, seller_id,
        cat_3_id, sale_area_id, sale_city_id, sale_region_id, warehouse_id,
        from_region_id, payment_type, user_id, listing_id, sku_id, order_total,
        item_total, postage, coins_redeem, voucher_redeem, item_discount,
        postage_discount, need_pay, cod_amount, order_count, create_order_id,
        product_qty) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
        (create_date_key, so["id"], order_type, sod["id"], so["storeId"],
         seller_id, cat_3_id, area_id, city_id, so["region"], so["warehouseId"],
         warehouse_region_id, payment_type, so["accountId"], sod["listingId"],
         sod["skuId"], order_total, sod["amount"], postage,
         sod.get("redeem", 0), sod.get("voucherRedeem", 0),
         sod.get("discount", 0), postage_discount, need_pay, cod_amount, 1,
         so["id"], sod["count"]))
    if pay_time:
        pay_date_key = int(pay_time.strftime("%Y%m%d"))
        cursor.execute(
            """INSERT INTO fact_sales_daily_detail (
            date_key, order_id, order_type, order_detail_id, store_id, 
            seller_id, cat_3_id, sale_area_id, sale_city_id, sale_region_id, 
            warehouse_id, from_region_id, payment_type, user_id, listing_id, 
            sku_id, online_paid, paid_count, paid_order_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);""",
            (pay_date_key, so["id"], order_type, sod["id"], so["storeId"],
             seller_id, cat_3_id, area_id, city_id, so["region"],
             so["warehouseId"], warehouse_region_id, payment_type,
             so["accountId"], sod["listingId"], sod["skuId"], online_paid,
             1, so["id"]))
    if confirm_time:
        confirm_date_key = int(confirm_time.strftime("%Y%m%d"))
        cursor.execute(
            """INSERT INTO fact_sales_daily_detail (
            date_key, order_id, order_type, order_detail_id, store_id, 
            seller_id, cat_3_id, sale_area_id, sale_city_id, sale_region_id, 
            warehouse_id, from_region_id, payment_type, user_id, listing_id, 
            sku_id, confirm_gmv, confirm_count, confirm_order_id) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s);""",
            (confirm_date_key, so["id"], order_type, sod["id"], so["storeId"],
             seller_id, cat_3_id, area_id, city_id, so["region"],
             so["warehouseId"], warehouse_region_id, payment_type,
             so["accountId"], sod["listingId"], sod["skuId"], order_total,
             1, so["id"]))
    if close_time:
        close_date_key = int(close_time.strftime("%Y%m%d"))
        if so["status"] == 5:
            cursor.execute(
                """INSERT INTO fact_sales_daily_detail (
                date_key, order_id, order_type, order_detail_id, store_id, 
                seller_id, cat_3_id, sale_area_id, sale_city_id, sale_region_id, 
                warehouse_id, from_region_id, payment_type, user_id, listing_id, 
                sku_id, success_gmv, success_voucher_redeem, 
                success_coin_redeem, success_item_discount, success_count, 
                success_order_id, success_qty_count) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                (close_date_key, so["id"], order_type, sod["id"], so["storeId"],
                 seller_id, cat_3_id, area_id, city_id, so["region"],
                 so["warehouseId"], warehouse_region_id, payment_type,
                 so["accountId"], sod["listingId"], sod["skuId"], order_total,
                 sod.get("voucherRedeem", 0), sod.get("redeem", 0),
                 sod.get("discount", 0), 1, so["id"], sod["count"]))
        elif so["status"] == -1:
            cursor.execute(
                """INSERT INTO fact_sales_daily_detail (
                date_key, order_id, order_type, order_detail_id, store_id, 
                seller_id, cat_3_id, sale_area_id, sale_city_id, sale_region_id, 
                warehouse_id, from_region_id, payment_type, user_id, listing_id, 
                sku_id, cancel_gmv, cancel_count, cancel_order_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s);""",
                (close_date_key, so["id"], order_type, sod["id"], so["storeId"],
                 seller_id, cat_3_id, area_id, city_id, so["region"],
                 so["warehouseId"], warehouse_region_id, payment_type,
                 so["accountId"], sod["listingId"], sod["skuId"], order_total,
                 1, so["id"]))
        elif so["status"] == -2:
            cursor.execute(
                """INSERT INTO fact_sales_daily_detail (
                date_key, order_id, order_type, order_detail_id, store_id, 
                seller_id, cat_3_id, sale_area_id, sale_city_id, sale_region_id, 
                warehouse_id, from_region_id, payment_type, user_id, listing_id, 
                sku_id, reject_gmv, reject_count, reject_order_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s);""",
                (close_date_key, so["id"], order_type, sod["id"], so["storeId"],
                 seller_id, cat_3_id, area_id, city_id, so["region"],
                 so["warehouseId"], warehouse_region_id, payment_type,
                 so["accountId"], sod["listingId"], sod["skuId"], order_total,
                 1, so["id"]))


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
                    order_time, order_time, pay_time])
        else:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, order_time, confirm_time])
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
        if so["payMethod"] == 1:
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
                    order_time, order_time, pay_time or close_time])
        else:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, order_time, confirm_time or close_time])

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
                    order_time, order_time, pay_time])
        else:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, order_time, confirm_time])
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
                    order_time, order_time, pay_time])
        else:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, order_time, confirm_time])
    elif so["status"] == 2:
        if pay_time:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, pay_time, end_time])
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[1],
                    order_time, order_time, pay_time])
        else:
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                        ).format(sql.Identifier('dw_sale_order')), [
                    so["id"], order_tp, payment_type, order_state[2],
                    order_time, order_time, end_time])

    elif so["status"] == 1:
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s, %s)"
                    ).format(sql.Identifier('dw_sale_order')), [
                so["id"], order_tp, payment_type, order_state[1], order_time,
                order_time, end_time])


def insert_order_into_base(cursor, start_id, end_id):
    warehouse_di = {it["_id"]: it["regionId"] for it in
                    goods_db.Warehouse.find({})}
    so_query = {"id": {"$gte": start_id, "$lt": end_id}}
    for so in order_db.SaleOrder.find(so_query).sort([("id", 1)]):
        if so.get("isRobot"):
            continue
        store = seller_db.Store.find_one({"_id": so["storeId"]})
        address = member_db.address.find_one({"id": so["addressId"]})
        sod_count = so["skuCount"]
        each_ratio = {it+1: 1/sod_count for it in range(sod_count)}
        postage_di = ratio_split_integer(so["postage"], each_ratio)
        pos_dis_di = ratio_split_integer(
            so.get("postageDiscount", 0), each_ratio)
        if so.get("discount") > 0 and so.get("orderType") == 1:
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
            paid = 0
            if pay_method_di[so["payMethod"]] == "online":
                cod_amount = 0
                if pay_time:
                    paid = need_pay
            else:
                paid = 0
                cod_amount = need_pay
            create_date_key = int(so["createdAt"].strftime("%Y%m%d"))
            warehouse_region_id = warehouse_di[so["warehouseId"]]
            logging.info(
                "insert into fact_sales values (%s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                " %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                % (so["batchId"], so["billId"], it["orderId"], it["id"],
                   create_date_key, listing["categoryId"], it["listingId"],
                   it["skuId"], it["salePrice"], so["accountId"],
                    store["sellerId"], so["storeId"],
                    address["areaId"], address["cityId"],
                    so["region"], so["warehouseId"], warehouse_region_id,
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
                        " %s, %s, %s)").format(
                    sql.Identifier('fact_sales')), [
                    so["batchId"], so["billId"], it["orderId"], it["id"],
                    create_date_key, listing["categoryId"], it["listingId"],
                    it["skuId"], it["salePrice"], so["accountId"],
                    store["sellerId"], so["storeId"], address["areaId"],
                    address["cityId"],
                    so["region"], so["warehouseId"], warehouse_region_id,
                    it["dealPrice"], it["count"], it["amount"],
                    postage_di[postage_index], it.get("coin", 0),
                    it.get("redeem", 0), it.get("voucherRedeem", 0),
                    it.get("discount", 0), pos_dis_di[postage_index],
                    order_total, need_pay, paid, cod_amount, payment_type,
                    order_time, order_tp, pay_time, confirm_time, pay_during,
                    confirm_during])
            create_fact_sales_daily_detail(
                cursor, so, it, create_date_key, listing["categoryId"],
                store["sellerId"], address["areaId"], address["cityId"],
                warehouse_region_id, postage_di[postage_index],
                pos_dis_di[postage_index], order_total, need_pay, paid,
                cod_amount, payment_type, order_tp, order_time, pay_time,
                confirm_time, ship_time, close_time)
            postage_index += 1


def insert_data_into_base(cursor):
    insert_datetime_into_base(cursor)
    insert_store_into_base(cursor)
    insert_warehouse_and_cat(cursor)
    insert_address_into_base(cursor)
    insert_enum_into_base(cursor)
    close_cursor(cursor)

    thread_num_1 = 20
    t_obj_1 = []
    # interval_times = 25000
    interval_times_1 = 24000
    for item in range(thread_num_1):
        start_id = interval_times_1 + (item - 1) * interval_times_1
        end_id = interval_times_1 + item * interval_times_1
        cursor = get_one_cursor(connect_oj)
        t1 = Thread(
            target=insert_user_and_contact_into_base,
            args=(cursor, start_id, end_id,))
        t_obj_1.append(t1)
        t1.start()

    for t1 in t_obj_1:
        t1.join()

    thread_num = 20
    t_obj = []
    # interval_times = 25000
    interval_times = 18000
    for item in range(thread_num):
        start_id = interval_times + (item - 1) * interval_times
        end_id = interval_times + item * interval_times
        cursor = get_one_cursor(connect_oj)
        t1 = Thread(
            target=insert_order_into_base, args=(cursor, start_id, end_id,))
        t_obj.append(t1)
        t1.start()

    for t1 in t_obj:
        t1.join()


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
    connect_oj = connect_post_gre_db(config, env)

    cursor_oj = get_one_cursor(connect_oj)

    # query = sql.SQL("select {field} from {table} where {pkey} = %s").format(
    #     field=sql.Identifier('week_key'),
    #     table=sql.Identifier('dim_time_week'),
    #     pkey=sql.Identifier('week_key'))
    # cursor_oj.execute(query, (201801,))

    create_tables(cursor_oj)
    insert_data_into_base(cursor_oj)
    close_cursor(cursor_oj)
    close_connect(connect_oj)
