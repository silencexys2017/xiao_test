#!/usr/bin/env python
# -*- coding:utf-8 -*-
import pymongo
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# uri = "mongodb://pf_dev_dbo:Bp2Q5j3Jb2cmQvn8L4kW@10.20.42.250/admin?" \
#      "replicaSet=rs0"
uri = "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@10.20.42.250/admin?" \
      "replicaSet=rs0"
try:
    client = pymongo.MongoClient(uri, 27017)
except pymongo.errors.ServerSelectionTimeoutError as pme:
    print (pme)
o_db = client.prdOrder
g_db = client.prdGoods
s_db = client.prdSeller
# o_db = client.devOrder
# g_db = client.devGoods
# s_db = client.devSeller


# 生成excel文件
def generate_excel(rec_data, sku_data):
    workbook = xlsxwriter.Workbook('./商品销售数据表.xlsx')
    worksheet = workbook.add_worksheet()
    # 设定格式，等号左边格式名称自定义，字典中格式为指定选项
    # bold：加粗，num_format:数字格式
    bold_format = workbook.add_format({'bold': True})
    money_format = workbook.add_format({'num_format': '$#,##0'})
    date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})

    # 将二行二列设置宽度为15(从0开始)
    worksheet.set_column(14, 14, 50)

    # 用符号标记位置，例如：A列1行
    worksheet.write('A1', 'LISTING_ID', bold_format)
    worksheet.write('B1', 'SKU_ID', bold_format)
    worksheet.write('C1', 'SPEC', bold_format)
    worksheet.write('D1', 'INVENTORY', bold_format)
    worksheet.write('E1', 'WAREHOUSE', bold_format)
    worksheet.write('F1', 'SELLER', bold_format)
    worksheet.write('G1', 'SHOP', bold_format)
    worksheet.write('H1', 'ON_SHELF_TIME', bold_format)
    worksheet.write('I1', 'PRICE', bold_format)
    worksheet.write('J1', 'ALL_SOLD_COUNT', bold_format)
    worksheet.write('K1', 'COMPLETE_COUNT', bold_format)
    worksheet.write('L1', 'IN_TRANSIT_COUNT', bold_format)
    worksheet.write('M1', 'CANCELLED_COUNT', bold_format)
    worksheet.write('N1', 'REJECTED_COUNT', bold_format)
    row = 1
    col = 0
    for key, value in rec_data.items():
        # 使用write_string方法，指定数据格式写入数据
        # worksheet.write_string(row, col, key)
        worksheet.write_string(row, col + 1, str(key))
        worksheet.write_string(row, col + 9, str(value["allAmount"]))
        worksheet.write_string(row, col + 10, str(value["comAmount"]))
        worksheet.write_string(row, col + 11, str(value["traAmount"]))
        worksheet.write_string(row, col + 12, str(value["canAmount"]))
        worksheet.write_string(row, col + 13, str(value["reAmount"]))
        row += 1
    row = 1
    col = 0
    for key, value in sku_data.items():
        # 使用write_string方法，指定数据格式写入数据
        worksheet.write_string(row, col, str(value["listingId"]))
        worksheet.write_string(row, col + 2, str(value["spec"]))
        worksheet.write_string(row, col + 3, str(value["inv"]))
        worksheet.write_string(row, col + 4, str(value["wName"]))
        worksheet.write_string(row, col + 5, str(value["sellerName"]))
        worksheet.write_string(row, col + 6, str(value["storeName"]))
        worksheet.write_string(row, col + 7, str(value["creat"]))
        worksheet.write_string(row, col + 8, str(value["price"]))
        row += 1
    workbook.close()


def find_sod_related():
    so_state = dict()
    for item in o_db.SaleOrder.find({}):
        so_state[item["id"]] = item["status"]
    sku_info = dict()
    sku_li = o_db.SaleOrderDetail.distinct("skuId", {})
    for item in sku_li:
        sku_info[item] = {"allAmount": 0, "comAmount": 0, "traAmount": 0,
                          "canAmount": 0, "reAmount": 0}
    for item in o_db.SaleOrderDetail.find({}):
        obj = sku_info[item["skuId"]]
        # amount = item["salePrice"] * item["count"]
        amount = item["count"]
        obj["allAmount"] = obj["allAmount"] + amount
        state = so_state[item["orderId"]]
        if state == 4:
            obj["traAmount"] = obj["traAmount"] + amount
        elif state == 5:
            obj["comAmount"] = obj["comAmount"] + amount
        elif state == -1:
            obj["canAmount"] = obj["canAmount"] + amount
        elif state == -2:
            obj["reAmount"] = obj["reAmount"] + amount

    return sku_info, sku_li


def find_sku_related(skus):
    store_di = dict()
    seller_di = dict()
    for item in s_db.Seller.find({}):
        seller_di[item["_id"]] = item["name"]
    for item in s_db.Store.find({}):
        store_di[item["_id"]] = {
            "name": item["name"], "sName": seller_di[item["sellerId"]]}
    sku_di = dict()
    for item in g_db.SpecOfSku.find({"_id": {"$in": skus}}):
        sku_di[item["_id"]] = {
            "spec": item["spec"], "storeName": store_di[item["storeId"]]["name"],
            "listingId": item["listingId"], "creat": str(item["createdAt"]),
            "sellerName": store_di[item["storeId"]]["sName"]}
    ware_di = dict()
    for item in g_db.Warehouse.find({}):
        ware_di[item["_id"]] = item["name"]
    for item in g_db.SkuInventory.find({"skuId": {"$in": skus}}):
        sku_di[item["skuId"]]["inv"] = item["stock"]
        sku_di[item["skuId"]]["wName"] = ware_di[item["warehouseId"]]
    for item in g_db.SkuPrice.find({"skuId": {"$in": skus}}):
        sku_di[item["skuId"]]["price"] = item["salePrice"]
    return sku_di


if __name__ == '__main__':
    # return None
    sod_di, sku_list = find_sod_related()
    goods_di = find_sku_related(sku_list)
    generate_excel(sod_di, goods_di)
