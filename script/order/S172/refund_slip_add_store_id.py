#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
from datetime import datetime
from threading import Thread

uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.107.255/admin?"\
      "replicaSet=rs0"
# uri = "mongodb://pf_test_dbo:3f4k8aDHeQJBKmd3z7c9@10.20.107.255/admin?"\
#       "replicaSet=rs0"
# uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.107.255/admin?"\
#       "replicaSet=rs0"

client = pymongo.MongoClient(uri, 27017)

o_db = client.devOrder
s_db = client.devSeller
a_db = client.devAdmin
# o_db = client.testOrder
# s_db = client.testSeller
# a_db = client.testAdmin
# g_db = client.prdGoods
# s_db = client.prdSeller
# a_db = client.prdAdmin


def add_store_id():
    so_ids = o_db.RefundSlip.distinct("saleOrderId", {})

    store_di = {it: set() for it in s_db.Store.distinct("_id", {})}
    for it in o_db.SaleOrder.find({"id": {"$in": so_ids}}):
        store_di[it["storeId"]].add(it["id"])

    for key, value in store_di.items():
        if value:
            o_db.RefundSlip.update_many(
                {"saleOrderId": {"$in": list(value)}},
                {"$set": {"storeId": key}})


def add_module_in_admin():
    data = {
        "id": 832,
        "rClassId": 8,
        "pagesId": 83,
        "title": "退款单导出"
    }
    a_db.module.insert_one(data)


if __name__ == "__main__":
    add_store_id()
    add_module_in_admin()
