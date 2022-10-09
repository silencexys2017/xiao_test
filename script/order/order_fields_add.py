# coding=utf-8
import pymongo
from datetime import datetime
from threading import Thread

uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.42.250/admin" \
    "?replicaSet=rs0"
# uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.42.250/admin" \
#       "?replicaSet=rs0"
# uri = "localhost"
mongo_client = pymongo.MongoClient(uri)

# order_db = mongo_client["order"]
order_db = mongo_client["devOrder"]
# order_db = mongo_client["prdOrder"]

# 1：SaleOrder 增加 addressId, payMethod, itemCount, payAmount, skuCount
# 2: shipOrder 增加 storeId，payMethod
# 3: shipPackage 增加saleOrderId, storeId, itemCount, payMethod, warehouseId,
#    skuCount
# 先发布后端服务，再更新代码，期间不要动进行后台操作


def remove_error_data():
    print("start remove_error_data()")
    ids = [5238, 5239, 5240, 5241, 5243, 5244]
    order_db.OrderBatch.delete_many({"id": {"$in": ids}})
    order_db.Bill.delete_many({"id": {"$in": ids}})
    order_db.PayBill.delete_many({"billId": {"$in": ids}})
    print("remove_error_data() end")


def update_so_fields():
    print("start update_so_fields()")
    global so_di
    global so_dic
    so_di = {}
    so_dic = {}
    for so in order_db.SaleOrder.find():
        so_di[so["id"]] = {"payAmount": int(so["itemTotal"] + so["postage"] -
        so["discount"] - so["redeem"] - so.get("postageRedeem", 0) +
        so.get("vat", 0) - so.get("postageDiscount", 0) -
        so.get("voucherRedeem", 0)), "skuCount": 0, "itemCount": 0}
        so_dic[so["id"]] = {
        "billId": so["billId"], "batchId": so["batchId"], "warehouseId": so["warehouseId"],
        "storeId": so["storeId"], "discount": so["discount"], "redeem": so["redeem"],
        "coin": so.get("coin", 0), "voucherRedeem": so.get("voucherRedeem", 0),
        "vat": so.get("vat",0), "postage": so["postage"] - so["postageDiscount"] - so["postageRedeem"]}

    batch_addr = {}
    for item in order_db.OrderBatch.find(
        {}, {"id": 1, "addressId": 1, "_id": 0}):
        batch_addr[item["id"]] = item["addressId"]

    bill_pm = {}
    for item in order_db.Bill.find({}, {"id": 1, "paymethod": 1, "_id": 0}):
        bill_pm[item["id"]] = item["paymethod"]

    for item in order_db.SaleOrderDetail.find(
        {}, {"count": 1, "orderId": 1, "_id": 0}):
        so_di[item["orderId"]]["skuCount"] += 1
        so_di[item["orderId"]]["itemCount"] += item["count"]
    so_list = []
    for key, value in so_di.items():
        value["addressId"] = batch_addr[so_dic[key]["batchId"]]
        value["payMethod"] = bill_pm[so_dic[key]["billId"]]
        so_list.append({"soCond": {"id": key}, "soUpdate": {"$set": value}})

    thread_num = 25
    so_total = len(so_list)
    if so_total < 25:
        thread_num = 1
    avg_num = int(so_total/thread_num)
    avg_li = []
    for item in range(1, thread_num + 1):
        if item != thread_num:
            avg_li.append(so_list[avg_num*(item-1): avg_num*item])
        else:
            avg_li.append(so_list[avg_num*(item-1): so_total])

    t_obj = []
    for item in avg_li:
        t1 = Thread(target=add_fields_in_so, args=(item,))
        t_obj.append(t1)
        t1.start()
    for t1 in t_obj:
        t1.join()

    print("update_so_fields() end")


def add_fields_in_so(so_data):
    for item in so_data:
        order_db.SaleOrder.update_one(item["soCond"], item["soUpdate"])


def add_fields_in_package(pg_data):
    for item in pg_data:
        order_db.ShipOrder.update_one(item["shoCond"], item["shoUpdate"])
        order_db.ShipPackage.update_one(item["pgCond"], item["pgUpdate"])
        order_db.ShipOrderDetail.update_many(item["shodCond"], item["shodUpdate"])


def update_sho_and_pg_fields():
    # 143020: {'skuCount': 1, 'payMethod': 2, 'itemCount': 1,
    # 'addressId': 86132, 'payAmount': 0}
    print("start update_sho_and_pg_fields()")
    match_time = {3: "packedAt", 4: "shippedAt", 5: "dispatchedAt",
    6: "deliveredAt", -2: "cancelledAt", -1: "deliveredAt"}
    st_di = {}
    for item in order_db.ShortageOrder.find():
        st_di[item["shipOrderId"]] = {
        "discount": item["discount"], "redeem": item["redeem"],
        "coin": item["coin"], "voucherRedeem": item.get("voucherRedeem", 0),
        "vat": item.get("vat",0)}


    pg_list = []
    for item in order_db.ShipOrder.find():
        so_1 = so_dic[item["saleOrderId"]]
        so_2 = so_di[item["saleOrderId"]]
        mat_time = item.get(match_time.get(item["status"]))
        last_time = mat_time if mat_time else item.get("packedAt")
        if item["subform"] == 0:
            sho_fields = {"discount": so_1["discount"], "coinRedeem": so_1["redeem"],
            "coin": so_1["coin"], "voucherRedeem": so_1["voucherRedeem"], "vat": so_1["vat"]}

        else:
            st_1 = st_di[item["id"]]
            sho_fields = {"discount": so_1["discount"] - st_1["discount"],
            "coinRedeem": so_1["redeem"] - st_1["redeem"],
            "coin": so_1["coin"] - st_1["coin"], "vat": so_1["vat"] - st_1["vat"],
            "voucherRedeem": so_1["voucherRedeem"] - st_1["voucherRedeem"]}

        sho_cond = {"id": item["id"]}
        sho_fields["storeId"] = so_1["storeId"]
        sho_fields["payMethod"] = so_2["payMethod"]
        sho_fields["postage"] = so_1["postage"]

        sho_update = {"$set": sho_fields}
        pg_cond = {"id": item["packageId"]}
        pg_update = {"$set": {"saleOrderId": item["saleOrderId"],
            "payMethod": so_2["payMethod"], "storeId": so_1["storeId"],
            "warehouseId": so_1["warehouseId"],
            "itemCount": item["items"], "skuCount": item["skus"],
            "lastOperatedAt": last_time}}
        shod_cond = {"shipOrderId": item["id"]}
        shod_update = {"$set": {"packageId": item["packageId"]}}
        pg_list.append({"shoCond": sho_cond, "shoUpdate": sho_update,
                        "pgCond": pg_cond, "pgUpdate": pg_update,
                        "shodCond": shod_cond, "shodUpdate": shod_update})

    thread_num = 25
    pg_total = len(pg_list)
    if pg_total < 25:
        thread_num = 1
    avg_num = int(pg_total/thread_num)
    avg_li = []
    for item in range(1, thread_num + 1):
        if item != thread_num:
            avg_li.append(pg_list[avg_num*(item-1): avg_num*item])
        else:
            avg_li.append(pg_list[avg_num*(item-1): pg_total])
    t_obj = []
    for item in avg_li:
        t1 = Thread(target=add_fields_in_package, args=(item,))
        t_obj.append(t1)
        t1.start()
    for t1 in t_obj:
        t1.join()
    print("update_sho_and_pg_fields() end")


if __name__ == "__main__":
    start_time = datetime.utcnow()
    print (start_time)
    remove_error_data()
    update_so_fields()
    update_sho_and_pg_fields()
    print("-----------success---------------")
    print("spend time = %s" % (datetime.utcnow() - start_time))
