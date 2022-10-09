# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
from copy import deepcopy
import bson
import datetime
import uuid

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


def __list_structure(node: list, structure: dict):
    for item in node:
        if isinstance(item, list):
            array_index_name = '@array-' + str(len(set(filter(lambda x: x.startswith('@array'), structure.keys()))))
            structure[array_index_name] = {
                'type': {'list', },
                'children': {}
            }
            __list_structure(item, structure[array_index_name]['children'])
        elif isinstance(item, dict):
            __node_structure(item, structure)
        else:
            pass


def __node_structure(node: dict, structure: dict):
    for node_name, node_value in node.items():

        node_type = str(type(node_value)).split("'")[-2]

        if node_name not in structure:
            structure[node_name] = {
                'type': {node_type, },
                'children': {}
            }
        else:
            structure[node_name]['type'].add(node_type)

        if isinstance(node_value, list):
            __list_structure(node_value, structure[node_name]['children'])
        elif isinstance(node_value, dict):
            __node_structure(node_value, structure[node_name]['children'])
        else:
            pass


def __print_structure_tree(structure, levels):
    for node in sorted(structure.keys()):
        print('|\t' * levels + '|____', node, ':', ', '.join(
            sorted(list(structure[node]['type']))))
        if len(structure[node]['children']) == 0:
            continue
        __print_structure_tree(structure[node]['children'], levels + 1)


def __print_structure_path(structure, current_path=''):
    for node in sorted(structure.keys()):
        print(current_path + '.' + node) if len(current_path) else print(node)
        if len(structure[node]['children']) == 0:
            continue
        if len(current_path):
            __print_structure_path(structure[node]['children'], current_path + '.' + node)
        else:
            __print_structure_path(structure[node]['children'], node)


def __write_structure_tree(structure, levels):
    for node in sorted(structure.keys()):
        res = '           ' * levels + "|__________ %s : %s\n" % (
            node, ', '.join(sorted(list(structure[node]['type']))))
        f_southx.write(res)
        if len(structure[node]['children']) == 0:
            continue
        __write_structure_tree(structure[node]['children'], levels + 1)


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    f_southx = open('southx_data.txt', 'w')

    client = pymongo.MongoClient(config['mongodb']['uri'])
    db_list = []
    for name in client.list_database_names():
        if "prd" in name:
            db_list.append(name)
    for db_name in db_list:
        db = client[db_name]
        for collection in db.list_collection_names():
            if "system.profile" in collection:
                continue
            for it in db[collection].find().sort([("_id", -1)]).limit(1):
                if collection == "property":
                    it = db[collection].find_one()
                collection_structure, json_it = {}, deepcopy(it)
                __node_structure(it, collection_structure)
                f_southx.write(
                    "db.collection(%s.%s)\n" % (db_name, collection))
                f_southx.write("*" * 20 + "structure" + "*" * 20 + "\n")
                __write_structure_tree(collection_structure, 0)
                f_southx.write("\n")
                f_southx.write("*" * 20 + "example" + "*" * 20 + "\n")
                json_res = {}
                for key, value in json_it.items():
                    if isinstance(value, bson.objectid.ObjectId):
                        json_res[key] = str(value)
                    elif isinstance(value, datetime.datetime):
                        json_res[key] = str(value)
                    elif isinstance(value, uuid.UUID):
                        json_res[key] = str(value)
                    elif isinstance(value, dict):
                        res_dict = {}
                        for k, v in value.items():
                            if isinstance(v, datetime.datetime) or isinstance(
                                    v, uuid.UUID):
                                res_dict[k] = str(v)
                            else:
                                res_dict[k] = v
                        json_res[key] = res_dict
                    elif isinstance(value, list):
                        res_list = []
                        for item in value:
                            if isinstance(item, dict):
                                res_dict = {}
                                for k, v in item.items():
                                    if isinstance(v, datetime.datetime):
                                        res_dict[k] = str(v)
                                    else:
                                        res_dict[k] = v
                                res_list.append(res_dict)
                            else:
                                res_list.append(item)
                        json_res[key] = res_list

                    else:
                        json_res[key] = value
                try:
                    # specail_key = json_res.get(
                    #     "command", {}).get("lsid", {}).get("id", {})
                    # if isinstance(specail_key, uuid.UUID):
                    #     json_res["command"]["lsid"]["id"] = str(specail_key)
                    f_southx.write(json.dumps(json_res, indent=4))
                except Exception as exc:
                    print(json_it)
                    raise Exception(exc)
                f_southx.write("\n")
                f_southx.write("\n")

    f_southx.close()
