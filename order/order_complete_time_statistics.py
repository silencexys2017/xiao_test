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


def seconds_to_dhms(seconds):
    def _days(day):
        return "{} days, ".format(day) if day > 1 else "{} day, ".format(day)

    def _hours(hour):
        return "{} hours, ".format(hour) if hour > 1 else "{} hour, ".format(
            hour)

    def _minutes(minute):
        return "{} minutes and ".format(
            minute) if minute > 1 else "{} minute and ".format(minute)

    def _seconds(second):
        return "{} seconds".format(
            second) if second > 1 else "{} second".format(second)
    seconds = int(seconds)
    days = seconds // (3600 * 24)
    hours = (seconds // 3600) % 24
    minutes = (seconds // 60) % 60
    seconds = seconds % 60
    if days > 0:
        return _days(days) + _hours(hours) + _minutes(minutes) + _seconds(
            seconds)
    if hours > 0:
        return _hours(hours) + _minutes(minutes) + _seconds(seconds)
    if minutes > 0:
        return _minutes(minutes) + _seconds(seconds)
    return _seconds(seconds)


def get_avg_order_complete_time(start_time, end_time):
    time_range = {"createdAt": {"$gte": start_time, "$lt": end_time},
                  "status": {"$in": [4, 5, -2]}}
    all_count = order_db.SaleOrder.count_documents(time_range)
    complete_query = {
        "status": {"$in": [5]},
        "createdAt": {"$gte": start_time, "$lt": end_time}}

    complete_count = 0
    complete_time = 0
    complete_normal_count = 0
    complete_normal_time = 0

    for it in order_db.SaleOrder.find(complete_query):
        complete_count += 1
        interval_t = it.get("closedAt") - it.get("createdAt")
        time_interval = interval_t.total_seconds()
        interval_day = interval_t.days
        if interval_day < 60:
            complete_normal_count += 1
            complete_normal_time += time_interval
        complete_time += time_interval
    avg_complete_time = int(complete_time) / complete_count
    print("%s所有订单=%s，完成订单%s，正常完成订单=%s" % (
        start_time.month, all_count, complete_count, complete_normal_count))
    print("%s月完成的订单平均完成时间=%s" % (
        start_time.month, seconds_to_dhms(avg_complete_time)))
    avg_complete_normal_time = int(complete_normal_time) / complete_normal_count
    print("%s月正常完成的订单（完成时间-下单时间<60天）的平均完成时间=%s" % (
        start_time.month, seconds_to_dhms(avg_complete_normal_time)))
    avg_percent = int(complete_normal_count) / all_count
    print("%s月正常完成的订单在所有订单中的占比=%s" % (
        start_time.month, avg_percent))
    print("\n")


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    for it in range(1, 10):
        get_avg_order_complete_time(
            datetime(2021, it, 1), datetime(2021, it+1, 1))

    # export_spg_order(datetime(2020, 1, 1))
