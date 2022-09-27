#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import codecs
# reload(sys)
# sys.setdefaultencoding('utf-8')


def load_gmo_credentials():
    with open('data/gmo.json', 'r') as f:
        result = json.load(f)
        f.close()
    # f = codecs.open('./gmo.json', encoding='UTF-8')
    # result = json.load(f)
    # f.close()
    return result


def setup_gmo_credentials(settings):
    for (k, v) in settings.items():
        key = 'payapi/gmo/%s' % k
        value = str(v.encode("utf-8"))

        print(u'path: %s, value: %s' % (key, value.decode("utf-8")))


def setup_gmo_api():
    credentials = load_gmo_credentials()

    setup_gmo_credentials(credentials['test'])


if __name__ == '__main__':
    setup_gmo_api()



