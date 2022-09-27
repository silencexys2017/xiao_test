import arrow
from psycopg2 import sql


def is_leap_year(years):
    '''
    通过判断闰年，获取年份years下一年的总天数
    :param years: 年份，int
    :return:days_sum，一年的总天数
    '''
    assert isinstance(years, int), "请输入整数年，如 2018"

    if ((years % 4 == 0 and years % 100 != 0) or (years % 400 == 0)):
        days_sum = 366
        return days_sum
    else:
        days_sum = 365
        return days_sum


def generate_year_quarterly_month(year, cursor):
    year_name = str(year) + "年"
    cursor.execute(
        sql.SQL("insert into {} values (%s, %s)").format(
            sql.Identifier('dim_time_year')), [year, year_name])

    for it in [1, 2, 3, 4]:
        quarterly_key = int(str(year) + str(it))
        quarterly_name = year_name + "第" + str(it) + "季度"
        cursor.execute(
            sql.SQL("insert into {} values (%s, %s, %s, %s)").format(
                sql.Identifier('dim_time_qtr')), [
                quarterly_key, quarterly_name, year, year_name])
        month = 1
        for i in range(3):
            month_name = year_name + str(month) + "月"
            month_key = int(str(year) + str(month) if
                            len(str(month)) == 2 else "0" + str(month))
            cursor.execute(
                sql.SQL("insert into {} values (%s, %s, %s, %s, %s, %s)").format(
                    sql.Identifier('dim_time_month')), [
                    month_key, month_name, quarterly_key, quarterly_name,
                    year, year_name])
            month += 1


def judge_generate_week(
        cursor, week_key, week_name, week_value, month_key, month_name,
        quarterly_key, quarterly_name, year_key, year_name):
    if not cursor.execute(
        "SELECT * from dim_time_week where week_key=%s", (
                    week_key,)).fetchone():
        cursor.execute(
            sql.SQL("insert into {} values ("
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_time_week')), [
                week_key, week_name, week_value, month_key, month_name,
                quarterly_key, quarterly_name, year_key, year_name])


def get_all_day_per_year(year, cursor):
    '''
    获取一年的所有日期
    :param years:年份
    :return:全部日期列表
    '''
    generate_year_quarterly_month(year, cursor)
    start_date = '%s-1-1' % year
    a = 0
    all_date_list = []
    days_sum = is_leap_year(int(year))
    while a < days_sum:
        b = arrow.get(start_date).shift(days=a)
        year_key = b.year
        year_name = str(year_key) + "年"
        month_key = int(b.format("YYYYMM"))
        month_index = b.month
        month_name = year_name + str(month_index) + "月"
        if month_index in [1, 2, 3]:
            quarterly_key = int(str(year_key) + str(1))
            quarterly_index = 1
        elif month_index in [4, 5, 6]:
            quarterly_key = int(str(year_key) + str(2))
            quarterly_index = 2
        elif month_index in [7, 8, 9]:
            quarterly_key = int(str(year_key) + str(3))
            quarterly_index = 3
        else:
            quarterly_key = int(str(year_key) + str(4))
            quarterly_index = 4
        quarterly_name = year_name + "第" + str(quarterly_index) + "季度"
        week_id = b.isocalendar()[1]
        week_index = str(week_id) if len(str(week_id)) == 2 else\
            "0" + str(week_id)
        week_key = int(str(year_key) + week_index)

        week_name = year_name + "第" + str(week_id) + "周"
        week_value = "星期" + str(b.isoweekday())
        judge_generate_week(cursor, week_key, week_name, week_value, month_key,
                            month_name, quarterly_key, quarterly_name, year_key,
                            year_name)

        date_index = str(b.day) if len(str(b.day)) == 2 else "0" + str(b.day)
        date_key = int(b.format("YYYYMMDD"))
        date_name = month_name + date_index
        date_value = b.format("YYYY-MM-DD")
        cursor.execute(
            sql.SQL("insert into {} values ("
                    "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)").format(
                sql.Identifier('dim_time_year')), [
                date_key, date_value, date_name, week_key, week_name,
                week_value, month_key, month_name, quarterly_key,
                quarterly_name, year_key, year_name])
        #  b.isoweekday() 当前时间是一周的星期几
        #  b.isocalendar()[1] 当前是一年中的第几周
        # b = arrow.get(start_date).shift(days=a).format("YYYY-MM-DD")
        a += 1
        all_date_list.append(b)

    return all_date_list


if __name__ == '__main__':
    # years = "2001"
    # years = int(years)
    # # 通过判断闰年，获取一年的总天数
    # days_sum = isLeapYear(years)
    b = arrow.get("2018-12-30").shift(days=1)
    print(b.isocalendar())
    # print(b.format("YYYYMMDD"))
    # print(b.format("YYYY年MM月DD日W"))
    # print(b.format("aa AA UU W"))

    # 获取一年的所有日期
    # all_date_list = getAllDayPerYear("2020")
    # print(all_date_list)
