#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json


def json_loads_gmo_error():
    with open("gmo_error.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    f.close()
    error_code = {}
    for item in lines:
        it = item.split(" ")
        error_code[it[0]] = {"msg1": it[1], "msg2": it[2].replace('\n', '')}
    print(error_code)
    print(len(error_code.keys()))
    with open("gmo_error.json", "w") as f:
        f.write(json.dumps(error_code))
    f.close()


if __name__ == "__main__":
    json_loads_gmo_error()
    # print("接続方式エラー")