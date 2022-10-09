include "exceptions.thrift"
include "constants.thrift"
include "statistics_struct.thrift"


service StatisticsService {
    void create_order_skus(
        1: list<statistics_struct.OrderSku> order_skus),

    oneway void update_product_statistics(
        1: i64 sku_id, 2: i64 listing_id, 3: i32 store_id,
        4: statistics_struct.ProductUpdateType update_type,
        5: i16 region_id, 6: optional i16 order_count=0,
        7: optional i16 reject_count=0, 8: optional i16 complete_count=0,
        9: optional i16 view_count=0),

    list<statistics_struct.OneListing> get_top_products(
        1: string start_time, 2: string end_time,
        3: statistics_struct.SoldSortType sort_type, 4: i32 store_id,
        5: i16 region_id, 6: optional i16 limit) throws(
        1:exceptions.InvalidOperationException ioe),

    void create_clearing_orders(
        1: i32 store_id, 2: string year_month,
        3: list<statistics_struct.ClearingOrder> clearing_orders), // no use

    void create_clearing_order(1: statistics_struct.ClearingOrder clearing_order),

    void create_monthly_clearing(
        1: i32 store_id, 2: i16 region_id, 3: bool is_self_delivery,
        4: string year_month, 5: optional i64 reward, 6: optional i64 penalty,
        7: optional i64 after_sale_amount, 8: optional i64 logistics_cost),

    void create_monthly_clearing_summary(
        1: i32 store_id, 2: i16 region_id, 3: bool is_self_delivery,
        4: i64 item_total, 5: i64 discount, 6: i64 total_postage,
        7: i64 plat_postage, 8: i64 store_postage, 9: i64 pay_amount,
        10: i64 coin_redeem, 11: i64 settlement_coin_redeem,
        12: i64 plat_voucher, 13: i64 store_voucher, 14: i64 pay_fee,
        15: i64 commission, 16: i64 operate_fee, 17: i64 settlement_amount,
        18: string year_month, 19: optional i64 after_sale_amount,
        20: optional i64 reward, 21: optional i64 penalty,
        22: optional i64 logistics_cost), // no use

    statistics_struct.MonthlyClearingsRes get_monthly_clearings(
        1: statistics_struct.RequestFrom request_from,
        2: optional string start_time, 3: optional string end_time,
        4: optional i32 store_id, 5: optional i16 region_id,
        6: optional i64 skip, 7: optional i32 limit),

    statistics_struct.ClearingOrdersRes get_clearing_orders(
        1: string single_number, 2: optional i64 skip, 3: optional i32 limit),

    statistics_struct.MonthlyClearingSummary get_summary_clearing(
        1: string single_number),

    statistics_struct.MonthlyClearingSummary get_store_monthly_clearing(
        1: i32 store_id, 2: i16 year, 3: i16 month, 4: i16 region_id),

    statistics_struct.MonthlyClearingSummary correct_summary_clearing(
        1: string single_number, 2: i32 correction_amount,
        3: optional string information, 4: optional list<string> annex_names,
        5: optional statistics_struct.Operator operator, 6: optional i32 operator_id)
    throws(1: exceptions.InvalidOperationException ioe),

    list<statistics_struct.ClearingLog> get_clearing_operate_logs(
        1: string single_number),

    statistics_struct.MonthlyClearingSummary confirm_clearing(
        1: string single_number, 2: statistics_struct.ClearingOperateCode operate,
        3: statistics_struct.Operator operator, 4: i32 operator_id)throws(
        1: exceptions.InvalidOperationException ioe),

    void auto_confirm_clearing(1: string year_month),

    i16 get_month_clearing_summary_count(
        1: string compare_time, 2: i32 store_id, 3: optional i16 region_id),



}