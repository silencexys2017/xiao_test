# -*- coding:utf-8 -*-
import sys
import os
import logging
import pymongo
import json
import xlsxwriter
from datetime import datetime
from operator import itemgetter, attrgetter

_DEFAULT_LOG_FILE = 'app.log'
FILE_NAME = "mm_pf_address.xlsx"

K_DB_URL = {
    "dev": "mongodb://root:KB5NF1T0aP@mongodb-headless.os:27017/admin?replicaSet=rs0",
	"test": "mongodb://sk2:Qmvz84mtswuMJz8Kk90zBM7UbdW@ebes-db.cluster-cvxmlpsy4xpw.eu-central-1.docdb.amazonaws.com:27017/admin?authSource=admin",
    # "prd": "mongodb://sk2:Gmbz8i63mtswuMKz8Lk92zNM7UxwO5Txz1@ebes-db.cmxtf8qiglae.eu-central-1.docdb.amazonaws.com:27017/admin?replicaSet=rs0&retrywrites=false"
    "prd": "mongodb://pf_prd_dbo:m2w9ZNZP4gUsx9b2hu6L@mongodb-paas-service:27017/?replicaSet=rs0&authSource=admin"
}


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


def get_db(uri, env, database):
    client = pymongo.MongoClient(uri[env])
    db = '%s%s' % (env, database)
    return client[db]


def export_excel():
    address_li = [it for it in order_db.eCourierAddressNew.find().sort(
        [("city", 1), ("area", 1), ("thana", 1), ("postCode", 1)])]
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet_1 = workbook.add_worksheet("address")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "District", bold)
    worksheet_1.write("B1", "Area", bold)
    worksheet_1.write("C1", "Thana", bold)
    worksheet_1.write("D1", "Postcode", bold)
    worksheet_1.set_column('A:D', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for it in address_li:
        worksheet_1.write('A%d' % row_1, it.get("city"))
        worksheet_1.write('B%d' % row_1, it.get("area"))
        worksheet_1.write('C%d' % row_1, it.get("thana"))
        worksheet_1.write('D%d' % row_1, it.get("postCode"))
        row_1 += 1

    workbook.close()


def export_mm_address_excel(workbook):
    divisions = {it["_id"]: it["name"] for it in bee_common_db.State.find(
        {"regionId": 3})}
    districts = {it["_id"]: it["name"] for it in bee_common_db.City.find(
        {"regionId": 3, "stateId": {"$in": list(divisions.keys())}})}
    areas = {it["name"]: {
        "areaId": it["_id"], "cityId": it["cityId"], "stateId": it["stateId"],
        "stateName": divisions[it["stateId"]], "supportCod": it["supportCod"],
        "postage": it["postage"], "enabled": it["enabled"],
        "visible": it["visible"], "cityName": districts[it["cityId"]]} for it
        in bee_common_db.Area.find(
        {"cityId": {"$in": list(districts.keys())}, "regionId": 3}).sort(
        [("stateId", 1), ("cityId", 1), ("_id", 1), ("name", 1)])}

    worksheet_1 = workbook.add_worksheet("mm_address")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet_1.write("A1", "RegionId", bold)
    worksheet_1.write("B1", "Region", bold)
    worksheet_1.write("C1", "DivisionId", bold)
    worksheet_1.write("D1", "Division", bold)
    worksheet_1.write("E1", "CityId", bold)
    worksheet_1.write("F1", "City", bold)
    worksheet_1.write("G1", "AreaId", bold)
    worksheet_1.write("H1", "Area", bold)
    worksheet_1.write("I1", "postage", bold)
    worksheet_1.write("J1", "IsSupportCod", bold)
    worksheet_1.write("K1", "Enabled", bold)
    worksheet_1.write("L1", "Visible", bold)
    worksheet_1.set_column('A:L', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for k, v in areas.items():
        worksheet_1.write('A%d' % row_1, 3)
        worksheet_1.write('B%d' % row_1, "Myanmar")
        worksheet_1.write('C%d' % row_1, v["stateId"])
        worksheet_1.write('D%d' % row_1, v["stateName"])
        worksheet_1.write('E%d' % row_1, v["cityId"])
        worksheet_1.write('F%d' % row_1, v["cityName"])
        worksheet_1.write('G%d' % row_1, v["areaId"])
        worksheet_1.write('H%d' % row_1, k)
        worksheet_1.write('I%d' % row_1, v["postage"])
        worksheet_1.write('J%d' % row_1, v["supportCod"])
        worksheet_1.write('K%d' % row_1, v["enabled"])
        worksheet_1.write('L%d' % row_1, v["visible"])
        row_1 += 1


def export_bd_address_excel(workbook):
    divisions = {it["_id"]: it["name"] for it in bee_common_db.State.find(
        {"regionId": 1})}
    districts = {it["_id"]: it["name"] for it in bee_common_db.City.find(
        {"regionId": 1, "stateId": {"$in": list(divisions.keys())}})}
    areas = {it["name"]: {
        "areaId": it["_id"], "cityId": it["cityId"], "stateId": it["stateId"],
        "stateName": divisions[it["stateId"]], "supportCod": it["supportCod"],
        "postage": it["postage"], "enabled": it["enabled"],
        "visible": it["visible"], "cityName": districts[it["cityId"]]} for it
        in bee_common_db.Area.find(
            {"cityId": {"$in": list(districts.keys())}, "regionId": 1}).sort(
            [("stateId", 1), ("cityId", 1), ("_id", 1), ("name", 1)])}

    worksheet_1 = workbook.add_worksheet("bd_address")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet_1.write("A1", "RegionId", bold)
    worksheet_1.write("B1", "Region", bold)
    worksheet_1.write("C1", "DivisionId", bold)
    worksheet_1.write("D1", "Division", bold)
    worksheet_1.write("E1", "CityId", bold)
    worksheet_1.write("F1", "City", bold)
    worksheet_1.write("G1", "AreaId", bold)
    worksheet_1.write("H1", "Area", bold)
    worksheet_1.write("I1", "postage", bold)
    worksheet_1.write("J1", "IsSupportCod", bold)
    worksheet_1.write("K1", "Enabled", bold)
    worksheet_1.write("L1", "Visible", bold)
    worksheet_1.set_column('A:L', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for k, v in areas.items():
        worksheet_1.write('A%d' % row_1, 1)
        worksheet_1.write('B%d' % row_1, "Bangladesh")
        worksheet_1.write('C%d' % row_1, v["stateId"])
        worksheet_1.write('D%d' % row_1, v["stateName"])
        worksheet_1.write('E%d' % row_1, v["cityId"])
        worksheet_1.write('F%d' % row_1, v["cityName"])
        worksheet_1.write('G%d' % row_1, v["areaId"])
        worksheet_1.write('H%d' % row_1, k)
        worksheet_1.write('I%d' % row_1, v["postage"])
        worksheet_1.write('J%d' % row_1, v["supportCod"])
        worksheet_1.write('K%d' % row_1, v["enabled"])
        worksheet_1.write('L%d' % row_1, v["visible"])
        row_1 += 1


def export_ke_address_excel(workbook, region_code):
    state_dict = {it["_id"]: it["name"] for it in bee_common_db.Areas.find(
        {"regionCode": region_code, "deep": 1})}
    city_dict = {it["_id"]: {"parentId": it["parentId"], "name": it["name"]} for
                 it in bee_common_db.Areas.find(
            {"regionCode": region_code, "deep": 2})}
    ke_county = {it["_id"]: it["name"] for it in
                 bee_common_db.LogisticsAddress.find(
                     {"regionCode": region_code, "deep": 1})}
    ke_towns = {it["_id"]: {
        "name": it["name"], "parentName": ke_county[it["parentId"]]} for
        it in bee_common_db.LogisticsAddress.find(
            {"regionCode": region_code, "deep": 2})}

    areas = {}
    for it in bee_common_db.Areas.find(
            {"regionCode": region_code, "deep": 3}).sort(
            [("parentId", 1), ("name", 1), ("_id", 1)]):
        address = bee_common_db.LogisticsAddress.find_one(
            {"leafAreaIds": it["_id"]})
        other_id = address["_id"]
        areas[it["_id"]] = {
            "name": it["name"], "cityName": city_dict[it["parentId"]]["name"],
            "stateName": state_dict[city_dict[it["parentId"]]["parentId"]],
            "code": it["code"], "isSupportToDoor": it["isSupportToDoor"],
            "areaType": it["areaType"], "supportCod": it["supportCod"],
            "keCounty": ke_towns[other_id]["parentName"],
            "keTown": ke_towns[other_id]["name"]}

    worksheet_1 = workbook.add_worksheet("ke_address")
    bold = workbook.add_format(
        {'bold': True, 'align': 'center', 'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    worksheet_1.write("A1", "AreaId", bold)
    worksheet_1.write("B1", "code", bold)
    worksheet_1.write("C1", "County", bold)
    worksheet_1.write("D1", "SubCounty", bold)
    worksheet_1.write("E1", "Word", bold)
    worksheet_1.write("F1", "SupportToDoor", bold)
    worksheet_1.write("G1", "SupportCod", bold)
    worksheet_1.write("H1", "AreaType", bold)
    worksheet_1.write("J1", "KiliCounty", bold)
    worksheet_1.write("K1", "KiliTown", bold)
    worksheet_1.set_column('A:K', 20, other_bold)
    worksheet_1.set_row(0, 20)
    row_1 = 2
    for k, v in areas.items():
        worksheet_1.write('A%d' % row_1, k)
        worksheet_1.write('B%d' % row_1, v["code"])
        worksheet_1.write('C%d' % row_1, v["stateName"])
        worksheet_1.write('D%d' % row_1, v["cityName"])
        worksheet_1.write('E%d' % row_1, v["name"])
        worksheet_1.write('F%d' % row_1, v["isSupportToDoor"])
        worksheet_1.write('G%d' % row_1, v["supportCod"])
        worksheet_1.write('H%d' % row_1, v["areaType"])
        worksheet_1.write('J%d' % row_1, v["keCounty"])
        worksheet_1.write('K%d' % row_1, v["keTown"])
        row_1 += 1


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]
    bee_common_db = get_db(K_DB_URL, env, "BeeCommon")

    # export_excel()
    workbook = xlsxwriter.Workbook("kenya_address.xlsx")
    # export_mm_address_excel(workbook)
    # export_bd_address_excel(workbook)
    export_ke_address_excel(workbook, "KE")
    workbook.close()