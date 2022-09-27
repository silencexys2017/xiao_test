# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime, timedelta
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'sslcommerz_refund/config.json'
FILE_NAME = "Top_Score_1000.xlsx"


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


def get_sku_score_top():
    """sku的评论数>=5的，按评分倒排 (最⾼分在上⾯)。取 top 1000.
       sku#, store#, title, salePrice, listPrice, score, reviewCount"""
    query = {}
    sku_di = {it: {"scores": [], "reviewCount": 0} for it in
              goods_db.sku_review.distinct("skuId", query)}

    for it in goods_db.sku_review.find(query):
        sku_di[it["skuId"]]["scores"].append(it["skuScore"])
        sku_di[it["skuId"]]["reviewCount"] += 1

    items = []
    for k, v in sku_di.items():
        if v["reviewCount"] >= 5:
            av_score = round(sum(v["scores"]) / v["reviewCount"], 4)
            items.append((k, av_score*1000, v["reviewCount"]))

    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 1000]
    sku_ids = [it[0] for it in res_li]

    spec_di = {it["_id"]: {
        "title": it["title"], "storeId": it["storeId"]} for it in
        goods_db.SpecOfSku.find({"_id": {"$in": sku_ids}})}

    for it in goods_db.SkuPrice.find({"skuId": {"$in": sku_ids}}):
        spec_di[it["skuId"]]["salePrice"] = it["salePrice"]
        spec_di[it["skuId"]]["listPrice"] = it["listPrice"]

    return res_li, spec_di


def get_this_year_sku_score_top():
    """sku的评论数>=5的，按评分倒排 (最⾼分在上⾯)。取 top 1000.
           sku#, store#, title, salePrice, listPrice, score, reviewCount"""
    query = {"createAt": {"$gt": datetime(2020, 1, 1)}}
    sku_di = {it: {"scores": [], "reviewCount": 0} for it in
              goods_db.sku_review.distinct("skuId", query)}

    for it in goods_db.sku_review.find(query):
        sku_di[it["skuId"]]["scores"].append(it["skuScore"])
        sku_di[it["skuId"]]["reviewCount"] += 1

    items = []
    for k, v in sku_di.items():
        if v["reviewCount"] >= 5:
            av_score = round(sum(v["scores"]) / v["reviewCount"], 4)
            items.append((k, av_score * 1000, v["reviewCount"]))

    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 1000]
    sku_ids = [it[0] for it in res_li]

    spec_di = {it["_id"]: {
        "title": it["title"], "storeId": it["storeId"]} for it in
        goods_db.SpecOfSku.find({"_id": {"$in": sku_ids}})}

    for it in goods_db.SkuPrice.find({"skuId": {"$in": sku_ids}}):
        spec_di[it["skuId"]]["salePrice"] = it["salePrice"]
        spec_di[it["skuId"]]["listPrice"] = it["listPrice"]

    return res_li, spec_di


def get_listing_score_top():
    """sku的评论数>=5的，按评分倒排 (最⾼分在上⾯)。取 top 1000.
        listing#, score, reviewCount"""
    items = []
    for it in goods_db.listing_review_total.find(
            {"skuService.count": {"$gte": 5}}):
        ite = it["skuService"]
        av_score = round(ite["score"] / ite.get("count", 0), 3) * 1000
        items.append((it["listingId"], av_score, ite.get("count", 0)))

    res_li = sorted(items, key=itemgetter(1, 2), reverse=True)[0: 1000]
    return res_li


def str_utc_obj(it):
    if it:
        it = it + timedelta(hours=8)
        return datetime.strftime(it, '%Y-%m-%dT%H:%M:%S.%fZ')
    return


def export_excel(score, spec, score_1, spec_1, score_l):
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet_1 = workbook.add_worksheet("SkuScore")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "sku#", bold)
    worksheet_1.write("B1", "store#", bold)
    worksheet_1.write("C1", "title", bold)
    worksheet_1.write("D1", "salePrice", bold)
    worksheet_1.write("E1", "listPrice", bold)
    worksheet_1.write("F1", "score", bold)
    worksheet_1.write("G1", "reviewCount", bold)
    worksheet_1.set_column('A:G', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for it in score:
        sku_id = it[0]
        worksheet_1.write('A%d' % row_1, sku_id)
        worksheet_1.write('B%d' % row_1, spec[sku_id]["storeId"])
        worksheet_1.write('C%d' % row_1, spec[sku_id]["title"])
        worksheet_1.write('D%d' % row_1, spec[sku_id]["salePrice"])
        worksheet_1.write('E%d' % row_1, spec[sku_id]["listPrice"])
        worksheet_1.write('F%d' % row_1, it[1]/1000)
        worksheet_1.write('G%d' % row_1, it[2])
        row_1 += 1

    worksheet_2 = workbook.add_worksheet("SkuScore2020")
    worksheet_2.write("A1", "sku#", bold)
    worksheet_2.write("B1", "store#", bold)
    worksheet_2.write("C1", "title", bold)
    worksheet_2.write("D1", "salePrice", bold)
    worksheet_2.write("E1", "listPrice", bold)
    worksheet_2.write("F1", "score", bold)
    worksheet_2.write("G1", "reviewCount", bold)
    worksheet_2.set_column('A:G', 20, other_bold)
    worksheet_2.set_row(0, 20)
    row_2 = 2
    for it in score_1:
        sku_id = it[0]
        worksheet_2.write('A%d' % row_2, sku_id)
        worksheet_2.write('B%d' % row_2, spec_1[sku_id]["storeId"])
        worksheet_2.write('C%d' % row_2, spec_1[sku_id]["title"])
        worksheet_2.write('D%d' % row_2, spec_1[sku_id]["salePrice"])
        worksheet_2.write('E%d' % row_2, spec_1[sku_id]["listPrice"])
        worksheet_2.write('F%d' % row_2, it[1]/1000)
        worksheet_2.write('G%d' % row_2, it[2])
        row_2 += 1

    worksheet_3 = workbook.add_worksheet("ListingScore")
    worksheet_3.write("A1", "listing#", bold)
    worksheet_3.write("B1", "score", bold)
    worksheet_3.write("C1", "reviewCount", bold)
    worksheet_3.write("D1", "storeId", bold)
    worksheet_3.write("E1", "storeName", bold)
    worksheet_3.write("F1", "PriceMin", bold)
    worksheet_3.write("G1", "PriceMax", bold)
    worksheet_3.write("H1", "maxListPrice", bold)
    worksheet_3.write("I1", "minListPrice", bold)
    worksheet_3.write("J1", "FlashStartTime", bold)
    worksheet_3.write("K1", "TDStartTime", bold)
    worksheet_3.write("L1", "PromotionStartTime", bold)
    worksheet_3.write("M1", "GroupStartTime", bold)
    worksheet_3.set_column('A:M', 20, other_bold)
    worksheet_3.set_row(0, 20)
    row_3 = 2
    listing_ids = [it[0] for it in score_l]
    store_di = {it["_id"]: it["name"] for it in seller_db.Store.find()}
    now_time = datetime.utcnow()
    # flash_ids = promotion_db.activity_sku.distinct(
    #     "cloneSku.listingId", {"sessionStartTime": {"$gt": now_time}})
    flash_di = {it["cloneSku"]["listingId"]: it["sessionStartTime"] for it in
                promotion_db.activity_sku.find(
                    {"status": 1, "sessionStartTime": {"$gt": now_time}})}
    td_di = {it["listingId"]: it["startTime"] for it in
             promotion_db.DealOfToday.find(
                 {"status": 2, "startTime": {"$lte": now_time},
                  "endTime": {"$gte": now_time}, "isDeleted": False})}
    pro_id = {it["_id"]: it["startTime"] for it in promotion_db.Promotion.find(
        {"status": 2, "$or": [
            {"startTime": {"$gt": now_time}},
            {"startTime": {"$lte": now_time}, "endTime": {"$gte": now_time}}]})}
    pro_di = {it["product"]["id"]: pro_id[it["promotionId"]] for it in
              promotion_db.PromotionProduct.find(
                  {"promotionId": {"$in": list(pro_id.keys())}, "status": 2})}
    gb_di = {it["listingId"]: it["startOn"] for it in
             promotion_db.GroupBuying.find(
                 {"status": 2, "$or": [
                     {"startOn": {"$gt": now_time}},
                     {"startOn": {"$lte": now_time},
                      "expiredOn": {"$gte": now_time}}]})}

    lis_di = {}
    for it in goods_db.SpecOfListing.find({"_id": {"$in": listing_ids}}):
        lis_di[it["_id"]] = {
            "PriceMin": it["minPrice"]["1"], "PriceMax": it["maxPrice"]["1"],
            "maxListPrice": it["maxListPrice"]["1"],
            "minListPrice": it["minListPrice"]["1"],
            "storeId": it["storeId"], "storeName": store_di[it["storeId"]]}

    for it in score_l:
        lis = lis_di[it[0]]
        worksheet_3.write('A%d' % row_3, it[0])
        worksheet_3.write('B%d' % row_3, it[1]/1000)
        worksheet_3.write('C%d' % row_3, it[2])
        worksheet_3.write('D%d' % row_3, lis["storeId"])
        worksheet_3.write('E%d' % row_3, lis["storeName"])
        worksheet_3.write('F%d' % row_3, lis["PriceMin"])
        worksheet_3.write('G%d' % row_3, lis["PriceMax"])
        worksheet_3.write('H%d' % row_3, lis["maxListPrice"])
        worksheet_3.write('I%d' % row_3, lis["minListPrice"])
        worksheet_3.write("J%d" % row_3, str_utc_obj(flash_di.get(it[0])))
        worksheet_3.write("K%d" % row_3, str_utc_obj(td_di.get(it[0])))
        worksheet_3.write("L%d" % row_3, str_utc_obj(pro_di.get(it[0])))
        worksheet_3.write("M%d" % row_3, str_utc_obj(gb_di.get(it[0])))
        row_3 += 1
    workbook.close()


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    config = load_config(_DEFAULT_CONFIG_FILE, env)
    order_db = get_db(config, env, "Order")
    goods_db = get_db(config, env, "Goods")
    auth_db = get_db(config, env, "Auth")
    seller_db = get_db(config, env, "Seller")
    promotion_db = get_db(config, env, "Promotion")

    score, spec = get_sku_score_top()
    score_1, spec_1 = get_this_year_sku_score_top()
    print(spec_1)
    score_l = get_listing_score_top()

    export_excel(score, spec, score_1, spec_1, score_l)