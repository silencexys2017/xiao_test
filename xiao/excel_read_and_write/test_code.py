# -*- coding:utf-8 -*-
import requests
import xlrd
from operator import itemgetter


def test_sort():
    items = [("adf", "dfd"), ("fdf", "ierew"), ("dfsd", "edf"), ("fer", "fd")]
    res_li = sorted(items, key=itemgetter(0, 1), reverse=True)[0: 1000]
    print(res_li)


if __name__ == "__main__":
    test_sort()