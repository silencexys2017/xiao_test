include "exceptions.thrift"
include "information_center_struct.thrift"

service InformationCenterService {
    void add_actual_users_and_contacts(
        1: list<information_center_struct.ActualUserAndContact> users),

    void add_sellers(1: list<information_center_struct.DimSeller> sellers),

    void add_stores(1: list<information_center_struct.DimStore> stores),

    void add_warehouses(
        1: list<information_center_struct.DimWarehouse> warehouses),

    void add_categories_one(
        1: list<information_center_struct.DimCat1> categories),

    void add_categories_two(
        1: list<information_center_struct.DimCat2> categories),

    void add_categories_three(
        1: list<information_center_struct.DimCat3> categories),

    void create_and_update_daily_orders(
        1: list<information_center_struct.OrderList> order_list,
        2: string start_time, 3: string end_time),

    list<information_center_struct.SalesTarget> get_sales_targets(
        1: optional information_center_struct.ReportType report_type,
        2: optional list<i32> target_ids
    ),

    list<information_center_struct.SalesDimension> get_sales_dimensions(
        1: optional information_center_struct.ReportType report_type,
        2: optional list<i32> dimension_ids
    ),

    information_center_struct.SalesDataList get_sales_data(
        1: string start_time, 2: string end_time, 3: list<i16> target_ids,
        4: list<i16> column_dimension_ids, 5: list<i16> row_dimension_ids,
        6: i16 region_id,
        7: optional information_center_struct.TimeDimensionType time_dimension_type,
        8: optional i64 time_dimension_id,
        9: information_center_struct.CategoryDimensionType category_dimension_type,
        10: optional i64 category_dimension_id,
        11: optional information_center_struct.SalesRegionsDimensionType sales_regions_dimension_type,
        12: optional i64 sales_regions_dimension_id,
        13: optional information_center_struct.SellerDimensionType seller_dimension_type,
        14: optional i64 seller_dimension_id
    ),

    information_center_struct.TopDataList get_sales_tops(
        1: string start_time, 2: string end_time, 3: list<i16> target_ids,
        4: list<i16> dimension_ids, 5: i16 region_id,
        6: optional information_center_struct.TimeDimensionType time_dimension_type,
        7: optional i64 time_dimension_id,
        8: information_center_struct.CategoryDimensionType category_dimension_type,
        9: optional i64 category_dimension_id,
        10: optional information_center_struct.SalesRegionsDimensionType sales_regions_dimension_type,
        11: optional i64 sales_regions_dimension_id,
        12: optional information_center_struct.SellerDimensionType seller_dimension_type,
        13: optional i64 seller_dimension_id,
        14: optional information_center_struct.ListingDimensionType listing_dimension_type,
        15: optional i64 listing_dimension_id,
        16: optional i32 top_item,
        17: optional information_center_struct.OrderWay order_way,
        18: optional i32 off_set,
        19: optional i32 limit,
        20: optional bool is_export
    ),
}
