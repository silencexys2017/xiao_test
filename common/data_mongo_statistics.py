# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from datetime import datetime

_DEFAULT_LOG_FILE = 'data_mongo_statistics.log'
_DEFAULT_CONFIG_FILE = '../config.json'


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


def get_client(config):
    return pymongo.MongoClient(config['mongodb']['uri'])


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)

    client = pymongo.MongoClient(config['mongodb']['uri'])
    db_list = []
    for name in client.list_database_names():
        if "prd" in name:
            db_list.append(name)
    per_collection_count = 0
    per_field_count = 0
    per_x_w_collection_count = 0
    per_x_w_field_count = 0
    for db_name in db_list:
        if "prdQuark" in db_name:
            continue
        print(db_name)
        db = client[db_name]
        for collection in db.list_collection_names():
            per_x_w_collection_count += 1
            if "Wms" not in db_name and "Bee" not in db_name:
                per_collection_count += 1
            for it in db[collection].find().sort([("_id", -1)]).limit(1):
                per_x_w_field_count += len(it)
                if "Wms" not in db_name and "Bee" not in db_name:
                    per_field_count += len(it)

    print("perfee_table_count=%s, perfee_field_count=%s" % (
        per_collection_count, per_field_count))
    print("other_table_count=%s, other_field_count=%s" % (
        per_x_w_collection_count, per_x_w_field_count))
