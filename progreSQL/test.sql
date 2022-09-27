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

CREATE TABLE enum_sales_target (
        id serial NOT NULL,
        subject_name VARCHAR(256),
        target_name VARCHAR(256),
        display_name VARCHAR(256),
        is_selected BOOLEAN DEFAULT FALSE,
        operator_id INTEGER DEFAULT NULL
        );
        
CREATE TABLE enum_sales_dimension (
            id serial NOT NULL,
            subject_name VARCHAR(256),
            dimension_name VARCHAR(256),
            display_name VARCHAR(256),
            is_selected BOOLEAN DEFAULT FALSE,
            operator_id INTEGER DEFAULT NULL
            );
CREATE TABLE dim_region (
    id INTEGER,
    name VARCHAR(128),
    code VARCHAR(28)
    );
CREATE TABLE dim_province (
    id INTEGER,
    name VARCHAR(128),
    region_id INTEGER
    );
CREATE TABLE dim_city (
    id INTEGER,
    name VARCHAR(128),
    province_id INTEGER,
    region_id INTEGER
    );
CREATE TABLE dim_area (
    id INTEGER,
    name VARCHAR(128),
    province_id INTEGER,
    city_id INTEGER,
    region_id INTEGER
    );
INSERT INTO enum_sales_target (
    subject_name, target_name, display_name, is_selected, operator_id) VALUES
    ('sales_top', 'successOrderCount', 'Success Order Count', False, NULL),
    ('sales_normal', 'successOrderCount', 'Success Order Count', False, NULL);

UPDATE enum_sales_target SET display_name = 'SucOrderCNT' WHERE id in (19,20);

UPDATE COMPANY SET ADDRESS = 'Texas', SALARY=20000;

INSERT INTO enum_sales_target (
    subject_name, target_name, display_name, is_selected, operator_id) VALUES
    ('sales_top', 'gmv', 'GMV', True, NULL),
    ('sales_top', 'orderCount', 'Order Count', False, NULL),
    ('sales_top', 'successGmv', 'Success GMV', False, NULL),
    ('sales_top', 'rejectAmount', 'Reject Amount', False, NULL),
    ('sales_top', 'itemTotal', 'Item Total', False, NULL),
    ('sales_top', 'productQty', 'Product QTY', False, NULL),
    ('sales_top', 'postage', 'Postage', False, NULL),
    ('sales_top', 'coinsRedeem', 'Coins Redeem', False, NULL),
    ('sales_top', 'voucherRedeem', 'Voucher Redeem', False, NULL),
    ('sales_top', 'successOrderCount', 'Success Order Count', False, NULL),
    ('sales_normal', 'gmv', 'GMV', True, NULL),
    ('sales_normal', 'orderCount', 'Order Count', True, NULL),
    ('sales_normal', 'successGmv', 'Success GMV', False, NULL),
    ('sales_normal', 'rejectAmount', 'Reject Amount', False, NULL),
    ('sales_normal', 'itemTotal', 'Item Total', False, NULL),
    ('sales_normal', 'productQty', 'Product QTY', False, NULL),
    ('sales_normal', 'postage', 'Postage', False, NULL),
    ('sales_normal', 'coinsRedeem', 'Coins Redeem', False, NULL),
    ('sales_normal', 'successOrderCount', 'Success Order Count', False, NULL),
    ('sales_normal', 'voucherRedeem', 'Voucher Redeem', False, NULL);


INSERT INTO enum_sales_dimension (subject_name, dimension_name, display_name,
  is_selected, depth, structure, select_type, operator_id) VALUES
    ('sales_top', 'dateTime', 'Date Time', False, 5,
    '{{1,"year"},{2,"quarterly"},{3, "month"}, {4, "week"}, {5, "day"}}',
    NULL, NULL),
    ('sales_top', 'category', 'Category', False, 3,
    '{{1,"first level"},{2,"second level"},{3, "third level"}}', NULL, NULL),
    ('sales_top', 'seller', 'Seller', False, 2,
     '{{1,"seller"},{2,"store"}}', NULL, NULL),
    ('sales_top', 'salesRegions', 'Sales Regions', False, 4,
    '{{1,"region"},{2,"state"},{3, "city"}, {4, "area"}}', NULL, NULL),
    ('sales_top', 'store', 'Store', False, 1, '{{1,"store"}}', NULL, NULL),
    ('sales_top', 'listing', 'Listing', True, 2, '{{1,"listing"},{2,"sku"}}',
    NULL, NULL),
    ('sales_top', 'sku', 'SKU', False, 1, '{{1,"sku"}}', NULL, NULL),
    ('sales_normal', 'dateTime', 'Date Time', True, 5,
     '{{1,"year"},{2,"quarterly"},{3, "month"}, {4, "week"}, {5, "day"}}',
    'col', NULL),
    ('sales_normal', 'category', 'Category', True, 3,
    '{{1,"first level"},{2,"second level"},{3, "third level"}}', 'row', NULL),
    ('sales_normal', 'paymentMethod', 'Payment Method', False, 1,
     '{{1,"paymentMethod"}}', NULL, NULL),
    ('sales_normal', 'seller', 'Seller', False, 2,
      '{{1,"seller"},{2,"store"}}', NULL, NULL),
    ('sales_normal', 'deliveryRegion', 'Delivery Region', False, 1,
    '{{1,"deliveryRegion"}}', NULL, NULL),
    ('sales_normal', 'deliveryWarehouse', 'Delivery Warehouse', False, 1,
    '{{1,"deliveryWarehouse"}}', NULL, NULL),
    ('sales_normal', 'salesRegions', 'Sales Regions', False, 4,
    '{{1,"region"},{2,"state"},{3, "city"}, {4, "area"}}', NULL, NULL);


SELECT t1.month_key,dim_time_month.month_name,dim_region.id,dim_region.name,
t1.payment_type,t1.payment_type,from_region.id,from_region.name,t1.gmv,
t1.order_count,t1.success_gmv,t1.reject_gmv,t1.item_total,t1.product_qty,
t1.postage,t1.coins_redeem,t1.voucher_redeem
FROM dim_time_month,dim_region,dim_region as from_region,
(SELECT dim_time_date.month_key,dim_area.region_id,
fact_sales_daily_detail.payment_type,fact_sales_daily_detail.from_region_id,
sum(fact_sales_daily_detail.order_total) as gmv,
sum(fact_sales_daily_detail.order_count) as order_count,
sum(fact_sales_daily_detail.success_gmv) as success_gmv,
sum(fact_sales_daily_detail.reject_gmv) as reject_gmv,
sum(fact_sales_daily_detail.item_total) as item_total,
sum(fact_sales_daily_detail.product_qty) as product_qty,
sum(fact_sales_daily_detail.postage) as postage,
sum(fact_sales_daily_detail.coins_redeem) as coins_redeem,
sum(fact_sales_daily_detail.voucher_redeem) as voucher_redeem
FROM fact_sales_daily_detail,dim_time_date,dim_area
WHERE fact_sales_daily_detail.sale_region_id=1 AND
fact_sales_daily_detail.date_key >= 20191124 AND
 fact_sales_daily_detail.date_key < 20211124 AND dim_time_date.date_key =
 fact_sales_daily_detail.date_key AND dim_time_date.quarterly_key=20201
 AND fact_sales_daily_detail.sale_area_id = dim_area.id
 GROUP BY dim_time_date.month_key,dim_area.region_id,
 fact_sales_daily_detail.payment_type,fact_sales_daily_detail.from_region_id) AS t1
WHERE t1.month_key = dim_time_month.month_key AND t1.region_id = dim_region.id
AND t1.from_region_id = from_region.id ;


SELECT t1.year_key,dim_time_year.year_name,dim_cat_1.id,dim_cat_1.name,t1.gmv,count(*) as total_number FROM dim_time_year,dim_cat_1,
(SELECT dim_time_date.year_key,dim_cat_3.cat_1_id,
sum(fact_sales_daily_detail.order_total) as gmv
FROM fact_sales_daily_detail,dim_time_date,dim_cat_3 WHERE fact_sales_daily_detail.sale_region_id=1 AND fact_sales_daily_detail.date_key >= 20210630 AND
        fact_sales_daily_detail.date_key < 20210728 AND dim_time_date.date_key =
        fact_sales_daily_detail.date_key AND fact_sales_daily_detail.cat_3_id = dim_cat_3.id
        GROUP BY dim_time_date.year_key,dim_cat_3.cat_1_id) AS t1
        WHERE t1.year_key = dim_time_year.year_key AND t1.cat_1_id = dim_cat_1.id ORDER BY t1.gmv ASC  LIMIT 10  OFFSET 1;

SELECT t1.year_key,dim_time_year.year_name,dim_cat_1.id,dim_cat_1.name,t1.gmv,t1.total_number
FROM dim_time_year,dim_cat_1,
(SELECT dim_time_date.year_key,dim_cat_3.cat_1_id,sum(fact_sales_daily_detail.order_total) as gmv, COUNT(*) OVER () AS total_number
FROM fact_sales_daily_detail,dim_time_date,dim_cat_3
WHERE fact_sales_daily_detail.sale_region_id=1 AND fact_sales_daily_detail.date_key >= 20210630 AND
fact_sales_daily_detail.date_key < 20210728 AND dim_time_date.date_key =
 fact_sales_daily_detail.date_key AND fact_sales_daily_detail.cat_3_id = dim_cat_3.id
 GROUP BY dim_time_date.year_key,dim_cat_3.cat_1_id ORDER BY gmv ASC  LIMIT 2  OFFSET 1) AS t1 WHERE t1.year_key = dim_time_year.year_key AND t1.cat_1_id = dim_cat_1.id;

