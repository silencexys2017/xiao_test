#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
from datetime import datetime
from threading import Thread

uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?"\
      "replicaSet=rs0"
# uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.107.255/admin?"\
#       "replicaSet=rs0"

client = pymongo.MongoClient(uri, 27017)

o_db = client.devOrder
# o_db = client.prdOrder


def account_order_add_fields(item, space):
    query = {"accountId": {"$gt": item*space, "$lte": (item+1)*space},
             "status": 4}

    ac_di = {}
    for it in o_db.ShipPackage.distinct("accountId", query):
        ac_di[it] = 0
    for it in o_db.ShipPackage.find(query):
        ac_di[it["accountId"]] += it["amount"]

    for key, value in ac_di.items():
        o_db.AccountOrder.find_one_and_update(
            {"accountId": key}, {"$inc": {"completeAmount": value}})


def update_account_order():
    thread_num = 20
    space = int(320000/thread_num)
    t_obj = []
    for item in range(thread_num):
        t1 = Thread(target=account_order_add_fields, args=(item, space))
        t_obj.append(t1)
        t1.start()
    for t1 in t_obj:
        t1.join()
    print("update_account_order complete")


if __name__ == "__main__":
    update_account_order()

