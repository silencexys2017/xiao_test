#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import logging
import thriftpy2
from weichigong import zconfig
from puanchen import HeraldMQ
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR


LOG_FILE = "/var/lib/dna/logs/timer.log"
CLEARING_DAY = 6
CONFIRM_CLEARING_DAY = 14
ZERO_TIMEZONE = "Etc/GMT+0"
MONTHLY_STORE_MARGIN_AND_DISCLAIMER_DAY = 1
MONTHLY_STORE_INITIALIZE_DAY = 28
FAULT_BEIJING_HOUR = 2
EIGHT_TIMEZONE = "Etc/GMT+8"
TIMEZONE = "Etc/GMT+0"
TIME_STR_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
DEF_CS = {}


class TimingStatistics(object):
    def __init__(self):
        pass

    @staticmethod
    def get_year_month_str():
        time_now = datetime.utcnow().strftime('%Y%m')
        yea = int(time_now[:4])
        mon = int(time_now[-2:])
        if mon - 1 < 1:
            month = 12
            year = yea - 1
        else:
            month = mon - 1
            year = yea
        year_month = str(year) + "0" + str(month) if len(str(month)) < 2 else \
            str(year) + str(month)

        return year_month

    @staticmethod
    def get_this_year_month_str():
        return datetime.utcnow().strftime('%Y%m')

    @staticmethod
    def get_next_year_month_str():
        time_now = datetime.utcnow().strftime('%Y%m')
        yea = int(time_now[:4])
        mon = int(time_now[-2:])
        if mon + 1 > 12:
            month = 1
            year = yea + 1
        else:
            month = mon + 1
            year = yea
        year_month = str(year) + "0" + str(month) if len(str(month)) < 2 else \
            str(year) + str(month)

        return year_month

    @staticmethod
    def get_last_day_interval_str():
        time_now = datetime.utcnow()
        obj_time = time_now - timedelta(days=1)
        start_time = datetime(obj_time.year, obj_time.month, obj_time.day)
        end_time = datetime(time_now.year, time_now.month, time_now.day)
        return (datetime.strftime(start_time, TIME_STR_FORMAT),
                datetime.strftime(end_time, TIME_STR_FORMAT))

    # def initial_clearing_orders(self):
    #     year_month = "202005"
    #     msg = {"action": "initial_clearing_orders",
    #            "data": {"yearMonth": year_month}}
    #     logging.info("msg=%r" % msg)
    #     self._send_message_to_queue(self.queue_statistics, msg)
    #
    # def month_5_clearing_order(self):
    #     year_month = "202005"
    #     msg = {"action": DEF_CS.STATISTICS_ALL_SOTRES_MONTHLY,
    #            "data": {"yearMonth": year_month}}
    #     logging.info("msg=%r" % msg)
    #     self._send_message_to_queue(self.queue_statistics, msg)

    def initialize_store_monthly_info(self):
        print("success")


def my_listener(event):
    if event.exception:
        logging.error("There's something wrong with the task.")
        # 在生产环境中，你可以把出错信息换成发送一封邮件或者发送一个短信
    else:
        logging.info("The task is in progress.")


if __name__ == "__main__":
    timing_statistics = TimingStatistics()

    scheduler = BlockingScheduler()
    #     func=timing_statistics.initial_clearing_orders, args=(), trigger="date",
    #     next_run_time=datetime.utcnow().replace(
    #         tzinfo=timezone.utc)+timedelta(minutes=10), timezone=ZERO_TIMEZONE)
    # scheduler.add_job(
    #     func=timing_statistics.month_5_clearing_order, args=(), trigger="date",
    #     next_run_time=datetime.utcnow().replace(
    #         tzinfo=timezone.utc) + timedelta(minutes=20),
    #     timezone=ZERO_TIMEZONE)
    # scheduler.add_job(
    #     func=timing_statistics.monthly_detect_store_fault, args=(),
    #     trigger='cron', year="*", month="*", day="*", hour=FAULT_BEIJING_HOUR,
    #     timezone=EIGHT_TIMEZONE, id="monthly_detect_store_fault")
    # scheduler.add_job(
    #     func=timing_statistics.initialize_store_monthly_info, args=(),
    #     trigger='cron', year="*", month="*", day=MONTHLY_STORE_INITIALIZE_DAY,
    #     hour=4, timezone=EIGHT_TIMEZONE, id="initialize_store_monthly_info")

    scheduler.add_job(
        func=timing_statistics.initialize_store_monthly_info, args=(),
        trigger='cron', year="*", month="*", day=7, hour=21,  minute=33,
        second="1-59", timezone=EIGHT_TIMEZONE,
        id="initialize_store_monthly_info")

    scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)
    scheduler._logger = logging
    print("start")
    scheduler.start()





