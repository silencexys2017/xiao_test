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
g_db = client.devGoods
# g_db = client.prdGoods
# o_db = client.prdOrder


def update_package_source_id():
    for item in g_db.Warehouse.find({}, {"regionId": 1}):
        o_db.ShipPackage.update_many(
            {"sourceInventoryId": None, "warehouseId": item["_id"]},
            {"$set": {"sourceInventoryId": item["regionId"]}})
    print ("update update_package_source_id complete!")


def count_account_order(item, space):
    query = {"accountId": {"$gt": item*space, "$lte": (item+1)*space}}
    ac_ids = o_db.AccountOrder.distinct("accountId", query)
    if ac_ids:
        query["accountId"]["$nin"] = ac_ids
    ac_di = {}
    for it in o_db.SaleOrder.distinct("accountId", query):
        ac_di[it] = {
            "accountId": it, "batchCount": set(), "orderCount": 0, "codCount": 0,
            "onlineCount": 0, "codProcessCount": 0, "rejectCount": 0,
            "completeCount": 0, "cancelCount":0}
    for it in o_db.SaleOrder.find(query).sort([("closedAt", -1)]):
        aims = ac_di[it["accountId"]]
        aims["batchCount"].add(it["batchId"])
        aims["orderCount"] += 1
        if it["payMethod"] == 1:
            aims["onlineCount"] += 1
        else:
            aims["codCount"] += 1
            if it["status"] in [1, 2, 3, 4, 6]:
                aims["codProcessCount"] += 1
        if it["status"] == 5:
            if aims["rejectCount"] == 0 and aims["completeCount"] == 0:
                aims["lastCloseOrderState"] = "complete"
            aims["completeCount"] += 1
        elif it["status"] == -2:
            if aims["rejectCount"] == 0 and aims["completeCount"] == 0:
                aims["lastCloseOrderState"] = "reject"
            aims["rejectCount"] += 1

        elif it["status"] == -1:
            aims["cancelCount"] += 1

    for key, value in ac_di.items():
        value["batchCount"] = len(value["batchCount"])
        o_db.AccountOrder.find_one_and_update({"accountId": key}, {"$set": value}, upsert=True)


def create_account_order():
    thread_num = 10
    space = int(250000/thread_num)
    t_obj = []
    for item in range(thread_num):
        t1 = Thread(target=count_account_order, args=(item, space))
        t_obj.append(t1)
        t1.start()
    for t1 in t_obj:
        t1.join()
    print("create_account_order complete")


if __name__ == "__main__":
    update_package_source_id()
    create_account_order()

