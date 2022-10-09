# -*- coding:utf-8 -*-
import requests
import xlrd

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'

env = "prd"
API_KEY = "9eSx"
API_SECRET = "4Y1B4"
USER_ID = "F2901"
Content_type = "application/json"
# base_url = "https://staging.ecourier.com.bd/api"
base_url = "https://backoffice.ecourier.com.bd/api"


HEADERS = {
            "API-SECRET": API_SECRET,
            "API-KEY": API_KEY,
            "USER-ID": USER_ID,
            "Content-Type": Content_type
        }


def get_city_list():
    body = {}
    url = base_url + "/city-list"
    result = requests.post(url, json=body, headers=HEADERS, timeout=150).json()
    if type(result) is not list:
        if result.get("errors"):
            print(result["errors"])
    return result
    # return json.dumps(result)


def excel_pf_data(file):
    try:
        # 打开Excel文件读取数据
        data = xlrd.open_workbook(file)
        # 获取第一个工作表
        table = data.sheet_by_index(0)
        # 获取行数
        nrows = table.nrows
        # 获取列数
        ncols = table.ncols
        # 定义excel_list
        excel_list = []
        for row in range(1, nrows):
            row_data = []
            for col in range(ncols):
                # 获取单元格数据
                cell_value = table.cell(row, col).value
                if type(cell_value) == str:
                    cell_value = cell_value.strip()
                row_data.append(cell_value)
            # 把数据追加到excel_list中
            if set(row_data) == {''}:
                continue
            excel_list.append(row_data)
            pf_divisions.add(row_data[0])
            # goal_di = {
            #     "state": row_data[0], "city": row_data[1],
            #     "area": row_data[2], "mapArea": row_data[7]}
            com_address.append(
                (row_data[0], row_data[1], row_data[2], row_data))
            pf_cities.add(row_data[1])
            pf_areas.add(row_data[8])
        return excel_list
    except Exception as e:
        print(str(e))


if __name__ == "__main__":
    com_address = []
    pf_divisions = set()
    pf_cities = set()
    pf_areas = set()
    pf_data = excel_pf_data(file="PerFee_Address_BD-20201028 update.xlsx")
    print(pf_data)
    # print(pf_divisions)
    print("---------------------------success------------------------------")



