# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime

CLEARING_DAY = 6
TIMEZONE = "Etc/GMT+0"

print(datetime.tzinfo)


def aps_test(x):
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), x)


scheduler = BlockingScheduler()
scheduler.add_job(
    func=aps_test, args=('定时任务',), trigger='cron', year="*", month="*",
    day=CLEARING_DAY, hour=0, timezone='Etc/GMT+0', id="test")
scheduler.add_job(
    func=aps_test, args=('定时任务',), trigger='cron', year="*", month="*",
    day=13, hour=8, minute=8, second='*', timezone='Etc/GMT+0', id="test1")


scheduler.start()


