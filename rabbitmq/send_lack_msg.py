# -*- coding:utf-8 -*-
import sys
import os
import logging
import json
from puanchen import HeraldMQ
from datetime import datetime

_DEFAULT_LOG_FILE = 'app.log'
_DEFAULT_CONFIG_FILE = 'config.json'

mq_data = [
    ('rabbitmq', 5672, 'rmq-prd', 'a3zWdf2X7xuEPWg259Xb', 'perfee-prd'),
    ('rabbitmq', 5672, 'rmq-test', 'ALpW854bZ29HrAzjce8v', 'perfee-test'),
    ('rabbitmq', 5672, 'rmq-dev', '7M9Yrym4L9G6cxhNe9Xf', 'perfee-dev')]
# host = "10.20.25.177"
# mq_port = "5672"
# mq_user = "rmq-prd"
# mq_password = "a3zWdf2X7xuEPWg259Xb"
# mq_virtual_host = "perfee-prd"
# rmq_con = HeraldMQ(host, int(mq_port), mq_virtual_host, mq_user, mq_password)

queue_name = "seller-prd"


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


if __name__ == "__main__":
    usage = 'python3 Sxx.py prd|dev|test'
    init_logging(_DEFAULT_LOG_FILE)
    if len(sys.argv) < 2:
        logging.error(usage)
        sys.exit(-1)

    env = sys.argv[1]

    rmq_param = (
        "mq.os.svc", 5672, "/", "default_user_pG5VCrtM-4F1yb3Mrts",
        "dvtp1bwGemzgDBIRKEs_7df_n26QFCcw")

    rmq_con = HeraldMQ(*rmq_param)
    rmq_con.send_message(
        queue_name, json.dumps(
            {"action": "seller_initialize_store_monthly_info",
             "data": {"yearMonth": "202208", "nextYearMonth": "202209"}}))

    print("---------------------------success-------------------------------")

