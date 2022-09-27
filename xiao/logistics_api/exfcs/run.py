import json
import time

import requests
import os

_API_BASE_URL = 'https://member.shop.com.mm'
_API_GET_ADDRESS = '/locationtree/api/getSubAddressList'


def get_address_list(parent_id=None):
    url = '%s%s?countryCode=MM' % (_API_BASE_URL, _API_GET_ADDRESS)
    if parent_id:
        url += "&addressId=%s" % parent_id

    r = requests.get(url)
    print(json.dumps(r.json()))
    payload = r.json()['module']

    result = {}
    for item in payload:
        result[item['id']] = item['name']
    return result

addresses = []

states = get_address_list()
for state_id, state_name in states.items():
    city_li = []
    cities = get_address_list(state_id)

    for city_id, city_name in cities.items():
        towns = get_address_list(city_id)
        time.sleep(2)
        town_li = []
        for town_id, town_name in towns.items():
            town_li.append({"town_id": town_id, "town_name": town_name})
            # print('%s\t%s\t%s' % (state_name, city_name, town_name))
        city_li.append(
            {"city_id": city_id, "city_name": city_name, "towns": town_li})
    addresses.append(
        {"state_id": state_id, "state_name": state_name, "cities": city_li})


print(json.dumps(addresses))

