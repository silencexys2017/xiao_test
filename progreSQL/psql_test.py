# coding: utf-8

import psycopg2
import json
from psycopg2 import Error
import time
import datetime


def select_test(cursor):
    sql_test = """
    select dim_cat_2.name as cat2_name, t_1.payment_type as payment, year_key, dim_region.name as from_region,
    dim_area.name as area_name, dim_seller.name as seller_name, dim_warehouse.name as warehouse_name, t_1.gmv, t_1.order_count,
    t_1.item_total, t_1.product_qty, t_1.postage, t_1.coins_redeem,
    t_1.voucher_redeem from (
    select dim_cat_3.cat_2_id, fact_sales_daily_detail.payment_type, dim_time_date.year_key,
    fact_sales_daily_detail.from_region_id, fact_sales_daily_detail.sale_area_id,
    fact_sales_daily_detail.seller_id, fact_sales_daily_detail.warehouse_id,
    sum(fact_sales_daily_detail.order_total)::money::numeric::float8 as gmv,
    count(distinct fact_sales_daily_detail.create_order_id) as order_count,
    sum(fact_sales_daily_detail.item_total) as item_total,
    sum(fact_sales_daily_detail.product_qty) as product_qty,
    sum(fact_sales_daily_detail.postage) as postage,
    sum(fact_sales_daily_detail.coins_redeem) as coins_redeem,
    sum(fact_sales_daily_detail.voucher_redeem) as voucher_redeem
    from dim_time_date, fact_sales_daily_detail, dim_cat_3 where
    dim_time_date.date_key = fact_sales_daily_detail.date_key and
    fact_sales_daily_detail.cat_3_id = dim_cat_3.id and
    dim_cat_3.cat_1_id = 69
    group by dim_time_date.year_key, fact_sales_daily_detail.from_region_id,
    fact_sales_daily_detail.payment_type, fact_sales_daily_detail.sale_area_id,
    fact_sales_daily_detail.seller_id, fact_sales_daily_detail.warehouse_id, dim_cat_3.cat_2_id)
    as t_1, dim_cat_2, dim_area, dim_region, dim_warehouse, dim_seller where
    dim_cat_2.id = t_1.cat_2_id and dim_area.id=t_1.sale_area_id and dim_region.id=t_1.from_region_id
    and dim_warehouse.id = t_1.warehouse_id and dim_seller.id=t_1.seller_id;
    """
    sql_test = """
    SELECT dim_time_date.year_key,sum(fact_sales_daily_detail.order_total) as gmv 
    FROM fact_sales_daily_detail,dim_time_date,dim_cat_3 WHERE 
    fact_sales_daily_detail.sale_region_id=1 AND 
    fact_sales_daily_detail.date_key >= 20200118 AND
    fact_sales_daily_detail.date_key < 20210118 AND dim_time_date.date_key =
    fact_sales_daily_detail.date_key AND 
    fact_sales_daily_detail.cat_3_id = dim_cat_3.id 
    GROUP BY dim_time_date.year_key;"""
    cursor.execute(sql_test)
    for it in cursor.fetchall():
        print(it)
    cursor.execute(
        """SELECT DISTINCT dimension_name
        from enum_sales_dimension where id in %s;""", (tuple([1, 2]), ))
    for it in cursor.fetchall():
        print(it)


def connect_post_gre_db():
    connection = None
    cursor = None
    try:
        # connection = psycopg2.connect(
        #     user="postgres",
        #     password="31415926",
        #     host="159.138.82.236",
        #     port="5432",
        #     database="test_data_centers"
        # )
        connection = psycopg2.connect(
            "postgresql://pf_test_dbo:3f4k4aDgeQJBKmd3z7c8@159.138.82.236:5432/",
            dbname="test_data_centers")

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        cursor.execute("SELECT * from dim_region;")
        # Fetch result
        record = cursor.fetchone()
        for it in record:
            print(it)
        # select_test(cursor)

        print("You are connected to - ", record, "\n")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def q_year_day():
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }

    for x in range(0, 366):
        time_item = {}
        star_time = int(time.mktime(time.strptime(str(datetime.date.today() - datetime.timedelta(days=1)), '%Y-%m-%d')))
        x_star_time = star_time + 86400 * x
        x_star_time_array = time.localtime(x_star_time)

        date_name = time.strftime("%Y%m%d", x_star_time_array)
        the_date = time.strftime("%Y/%m/%d", x_star_time_array)
        year_name = str(time.strftime("%Y", x_star_time_array)) + '年'
        the_year = time.strftime("%Y", x_star_time_array)

        now = datetime.date.fromtimestamp(x_star_time)
        the_quarter = (now.month - 1) // 3 + 1                  #计算季度
        quarter_name = str(now.year) + '年' + str(the_quarter) + '季度'
        quarter_name_short = str(now.year) + 'Q' + str(the_quarter)

        year = time.strftime("%Y", x_star_time_array)
        month = time.strftime("%m", x_star_time_array)
        day = time.strftime("%d", x_star_time_array)

        month_name = str(year) + '年' + str(month) + '月'
        month_name_short = str(year) + 'M' + str(month)

        now_dimte = (datetime.datetime.fromtimestamp(x_star_time)).isocalendar()
        the_week = now_dimte[1]
        week_name = '第' + str(the_week) + '周'
        week_name_short = str(now_dimte[0]) + 'W' + str(now_dimte[1])
        week_day = now_dimte[2]
        week_day_name = week_day_dict.get(week_day)

        time_item['date_name'] = date_name
        time_item['the_date'] = the_date
        time_item['year_name'] = year_name
        time_item['the_year'] = the_year

        time_item['quarter_name'] = quarter_name
        time_item['quarter_name_short'] = quarter_name_short
        time_item['the_quarter'] = the_quarter
        time_item['month_name'] = month_name
        time_item['month_name_short'] = month_name_short
        time_item['the_month'] = month

        time_item['the_week'] = the_week
        time_item['week_name'] = week_name
        time_item['week_name_short'] = week_name_short
        time_item['week_day'] = week_day
        time_item['week_day_name'] = week_day_name
        time_item['the_day'] = day

        print(json.dumps(time_item))


if __name__ == "__main__":
    connect_post_gre_db()
    # q_year_day()
