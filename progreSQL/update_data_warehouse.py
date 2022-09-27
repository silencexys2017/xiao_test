# -*- coding=utf-8 -*-

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
import thriftpy2
import thrift_connector.connection_pool as connection_pool

_DEFAULT_LOG_FILE = 'update_data_warehouse.log'
_DEFAULT_CONFIG_FILE = '../config.json'
pay_method_di = {2: 'cod', 1: 'online', 3: 'pre'}
order_type = {1: 'normal', 2: 'flash', 3: 'luckyDraw', 5: 'mixed', 4: 'redeem',
              6: 'promotion'}
order_state = {
    1: "pend_pay", 2: "pend_confirm", 3: "pend_ship", 4: "in_transit",
    5: "accept", -1: "cancel", -2: "reject"}
SERVICE_DEF = thriftpy2.load("../trpc/goods.thrift")
CONT_DEF = SERVICE_DEF.constants

pod_ip_map = {"test": "172.16.0.88", "prd": "172.16.0.88"}


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


def datetime_str_obj(utc_str):
    if type(utc_str) is str:
        return datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    return utc_str


def update_warehouse(cursor, warehouse_dict):
    cursor.execute(sql.SQL("DELETE FROM dim_warehouse;"))

    for it in goods_service.get_warehouses():
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s)").format(
                sql.Identifier('dim_warehouse')), [
                it.id, it.name, it.region_id])

    for key, value in warehouse_dict.items():
        cursor.execute("""UPDATE fact_sales SET warehouse_id = %s 
                    WHERE warehouse_id = %s;""", (value, key))
        cursor.execute("""UPDATE fact_sales_daily_detail SET warehouse_id = %s 
                            WHERE warehouse_id = %s;""", (value, key))


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    goods_service = connection_pool.ClientPool(
        SERVICE_DEF.GoodsService,
        pod_ip_map[env],
        8000,
        connection_class=connection_pool.ThriftPyCyClient)

    connect_oj = connect_post_gre_db(config, env)
    cursor_oj = get_one_cursor(connect_oj)

    warehouse_dict = CONT_DEF.WAREHOUSE_ID_MAP[env]
    update_warehouse(cursor_oj, warehouse_dict)

    close_cursor(cursor_oj)
    close_connect(connect_oj)
