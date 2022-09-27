from pymongo import MongoClient
import sys
import json
import argparse
from copy import deepcopy

parser = argparse.ArgumentParser(description='Scan MongoDB Collection Structure')
parser.add_argument('host', default='127.0.0.1', help='mongoDB Server host')
parser.add_argument('-p', '--port', default='27017', type=int, help='mongoDB Server host')
parser.add_argument('database', help='mongoDB Database name')
parser.add_argument('collection', help='mongoDB Collection name')
parser.add_argument('-o', '--out_type', default='tree', choices=['tree', 'path'], help='default is value: tree')

ITEM = {
        "ns" : "testBeeCommon.Area",
        "nInvalidDocuments" : 0,
        "nrecords" : 9153,
        "nIndexes" : 1,
        "keysPerIndex" : {
                "_id_" : 9153
        },
        "indexDetails" : {
                "_id_" : {
                        "valid" : True
                }
        },
        "valid" : True,
        "warnings" : [ ],
        "errors" : [ ],
        "extraIndexEntries" : [ ],
        "missingIndexEntries" : [ ],
        "ok" : 1,
        "$clusterTime" : {
                "clusterTime" : (1648879039, 483),
                "signature" : {
                        "hash" : 343,
                        "keyId" : 343434
                }
        },
        "operationTime" : 34324
}

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


def __write_structure_tree(structure, levels):
    for node in sorted(structure.keys()):
        res = '           ' * levels + "|__________ %s : %s\n" % (
            node, ', '.join(sorted(list(structure[node]['type']))))
        f_southx.write(res)
        if len(structure[node]['children']) == 0:
            continue
        __write_structure_tree(structure[node]['children'], levels + 1)


def __print_structure_tree(structure, levels):
    for node in sorted(structure.keys()):
        print('|\t' * levels + '|____', node, ':', ', '.join(
            sorted(list(structure[node]['type']))))
        if len(structure[node]['children']) == 0:
            continue
        __print_structure_tree(structure[node]['children'], levels + 1)


if __name__ == '__main__':
    f_southx = open('southx_data.txt', 'w')
    db_name, colletion_name = "Xiao", "test"
    collection_structure = {}
    __node_structure(ITEM, collection_structure)
    structure_1 = deepcopy(collection_structure)
    __print_structure_tree(structure_1, 0)
    f_southx.write("db.collection(%s.%s)\n" % (db_name, colletion_name))
    f_southx.write("*" * 20 + "structure" + "*" * 20 + "\n")
    __write_structure_tree(collection_structure, 0)
    f_southx.write("\n")
    f_southx.write("*" * 20 + "example" + "*" * 20 + "\n")
    f_southx.write(json.dumps(ITEM, indent=4))
    f_southx.write("\n\n")
    f_southx.close()
    print(collection_structure)

    """
    python MongoStructure.py  10.188.188.22 test Human
    """