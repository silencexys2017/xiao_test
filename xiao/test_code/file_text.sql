select date_key, order_id, order_type, order_detail_id, store_id, seller_id, cat_3_id from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select sale_area_id, sale_city_id, sale_region_id, warehouse_id, from_region_id, payment_type from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select user_id, listing_id, sku_id, order_total, item_total, postage, success_gmv, product_qty from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select coins_redeem, voucher_redeem, success_voucher_redeem, success_coin_redeem, item_discount from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select success_item_discount, postage_discount, confirm_gmv, reject_gmv, cancel_gmv, online_paid, success_qty_count from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select need_pay, cod_amount, order_count, create_order_id, paid_count, paid_order_id, confirm_count from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;
select confirm_order_id, cancel_count, cancel_order_id, reject_count, reject_order_id, success_count, success_order_id from fact_sales_daily_detail where order_id=315017 order by order_detail_id,order_count,paid_count,confirm_count,success_count,reject_count,cancel_count;


select * from dw_sale_order where sale_order_id=315017 order by dw_end_date;


select batch_id, bill_id, order_id, order_detail_id, date_key, cat_3_id, listing_id, sku_id, sale_price, user_id from fact_sales where order_id = 315017 order by order_detail_id;
select seller_id, store_id, sale_area_id, sale_city_id, sale_region_id, warehouse_id, from_region_id, deal_price, product_qty from fact_sales where order_id = 315017 order by order_detail_id;
select item_total, postage, coins, coins_redeem, voucher_redeem, item_discount, postage_discount, order_total, online_paid, need_pay from fact_sales where order_id = 315017 order by order_detail_id;
select cod_amount, payment_type, order_time, order_type, pay_time, confirm_time,  pay_during, confirm_during from fact_sales where order_id = 315017 order by order_detail_id;


SELECT t1.year_key,dim_time_year.year_name,dim_seller.id,dim_seller.name,t1.gmv,t1.total_number FROM dim_time_year,dim_seller,
(SELECT dim_time_date.year_key,fact_sales_daily_detail.seller_id,sum(fact_sales_daily_detail.order_total) as gmv,
COUNT(*) OVER () AS total_number FROM fact_sales_daily_detail,dim_time_date
WHERE fact_sales_daily_detail.sale_region_id=1 AND fact_sales_daily_detail.date_key >= 20210101 AND
        fact_sales_daily_detail.date_key < 20210804 AND dim_time_date.date_key =
        fact_sales_daily_detail.date_key
GROUP BY dim_time_date.year_key,fact_sales_daily_detail.seller_id
ORDER BY gmv DESC  LIMIT 10) AS t1 WHERE t1.year_key = dim_time_year.year_key AND dim_seller.id = t1.seller_id ORDER BY gmv;

SELECT t1.year_key,dim_time_year.year_name,dim_cat_1.id,dim_cat_1.name,t1.gmv,t1.total_number
FROM dim_time_year,dim_cat_1,(SELECT dim_time_date.year_key,dim_cat_3.cat_1_id,sum(fact_sales_daily_detail.order_total) as gmv,
COUNT(*) OVER () AS total_number
FROM fact_sales_daily_detail,dim_time_date,dim_cat_3
WHERE fact_sales_daily_detail.sale_region_id=1 AND fact_sales_daily_detail.date_key >= 20210801 AND
        fact_sales_daily_detail.date_key < 20210805 AND dim_time_date.date_key =
        fact_sales_daily_detail.date_key AND fact_sales_daily_detail.cat_3_id = dim_cat_3.id
GROUP BY dim_time_date.year_key,dim_cat_3.cat_1_id ORDER BY gmv DESC  LIMIT 10) AS t1
WHERE t1.year_key = dim_time_year.year_key AND t1.cat_1_id = dim_cat_1.id  ORDER BY gmv DESC;
