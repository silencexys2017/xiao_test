# -*- coding:utf-8 -*-
import json


def store_di_test():
    store_di = {}
    store_ids = [1]
    for item in store_ids:
        store_di[item] = {}
        for it in [1, 3]:
            store_di[item][it] = {}
            for i in range(1, 13):
                store_di[item][it][i] = {
                    "orderCount": 0, "orderAmount": 0, "rejectCount": 0,
                    "rejectAmount": 0}

    print(store_di)
    print(store_di[1][1])
    print(store_di[1][1][1])


def gmo_error_code_json():
    with open("../gmo_error_code.json", 'r', encoding="utf-8") as f:
        code_li = json.loads(f.read())
        new_dict = {}
        for item in code_li:
            new_dict[item["code"]] = {
                "msg1": item["msg1"], "msg2": item["msg2"]}

        print(new_dict)


if __name__ == "__main__":
    gmo_error_code_json()