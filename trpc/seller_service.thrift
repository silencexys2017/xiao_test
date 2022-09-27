include "exceptions.thrift"
include "seller.thrift"
include "constants.thrift"

service SellerService {
    list<seller.Store> get_stores_by_ids (
    1: list<i64> ids, 2: optional i16 region_id, 3: bool is_base_station)
    throws (1:exceptions.InternalException ie),

    seller.Store get_store_by_id (
    1: i64 store_id, 2: optional i16 region_id, 3: bool is_base_station)
    throws (1:exceptions.InternalException ie,
    2:exceptions.NotFoundException nfe),

    seller.Store get_store(
    1: optional i32 store_id, 2: optional string store_name,
    3: optional i16 region_id, 4: optional bool is_base_station)
    throws(1:exceptions.InvalidOperationException ioe),

    list<i32> get_store_ids_by_condition(1: optional string store_name),

    seller.Store get_one_store_and_stations(1: i64 store_id),

    bool check_seller_account_is_registered (
        1: optional string account,
        2: optional string phone,
        3: optional i16 region_id,
        4: optional string email)throws(
            1:exceptions.InvalidOperationException ioe),

    seller.Seller create_seller (1: string account, 2: string password,
    3: string phone, 4: seller.SellerType type,
    5: seller.Qualification qualification, 6: seller.SimpleSellerAddress location,
    7: optional string landline_number, 8: optional string fax,
    9: optional string mailbox, 10: optional string reference_no)
    throws(1:exceptions.InvalidOperationException ioe),

    seller.StoreApply create_store_apply (
    1: string name, 2: string icon, 3: string grade, 4: i64 seller_id,
    5: i16 station_region_id, 6: optional seller.Qualification qualification,
    7: optional seller.SimpleSellerAddress location, 8: optional double commission_rate,
    9: optional string currency)
    throws(1:exceptions.InvalidOperationException ioe),

    list<seller.ExpandApplyResult> expand_store_region_stations(
        1: i64 store_id, 2: set<i16> region_ids) throws(
        1: exceptions.NotFoundException nfe),

    list<seller.StoreApply> get_seller_apply_stores (
    1: optional string phone, 2: optional i16 region_id, 3: optional i32 seller_id),

    seller.ApplyStoreList get_apply_stores(
    1: i64 start_index, 2: i16 limit, 3: string start_time,
    4: string end_time, 5: list<i16> status, 6: i16 region,
    7: optional seller.ApplyStoreType apply_types,
    8: optional i16 is_china_seller),

    seller.ApplyStoreDetail get_apply_store_detail(1: i64 apply_store_id)
    throws (1:exceptions.NotFoundException nfe),

    seller.Store review_apply_store(1: i64 apply_store_id,
    2: seller.ReviewStoreOperate operate, 3: i32 staff_id,
    4: optional list<string> attached, 5: optional double commission_rate)
    throws (1:exceptions.NotFoundException nfe),

    seller.StoreList get_stores(
    1: i64 start_index, 2: i16 limit, 3: string start_time,
    4: string end_time, 5: list<i16> status, 6: optional string store_name,
    7: optional i64 store_id, 8: optional i64 seller_id,
    9: optional i16 is_china_seller, 10: optional i16 region_id,
    11: optional seller.MarginStatus margin_state, 12: optional bool is_base_station,
    13: optional list<seller.MarginCompare> margin_compares),

    seller.Store set_store_margin (
    1: i32 store_id, 2: seller.MarginStatus operate, 3: i32 amount,
    4: i16 staff_id) throws (1:exceptions.NotFoundException nfe),

    seller.StoreDetail get_store_detail(
    1: optional i64 store_id, 2: optional i64 store_apply_id,
    3: optional i16 region_id)
    throws (1:exceptions.NotFoundException nfe),

    bool check_login_information(1: seller.LoginType login_type,
    2: string info, 3: optional i16 region_id),

    seller.SellerLogin verify_login_account(
        1: seller.LoginType login_type,
        2: string login_ip,
        3: optional i16 region_id,
        4: optional string account,
        5: optional string password,
        6: optional string phone,
        7: optional string email)
    throws(1:exceptions.InvalidOperationException ioe,
    2:exceptions.UnauthorizedException ue, 3:exceptions.NotFoundException nfe),

    list<seller.Store> get_stores_by_login_account(1: i32 login_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.Seller get_seller_detail(
    1: optional i64 seller_id, 2: optional i64 store_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.Store update_store_apply(
    1: i64 store_id, 2: seller.StoreSetType operate, 3: optional string name,
    4: optional string icon, 5: optional seller.SimpleSellerAddress location,
    6: optional i16 region_id, 7: optional string mailbox)
    throws(1:exceptions.InvalidOperationException ioe),

    seller.StoreCategoryList get_store_categories(
    1: i64 store_id, 2: i64 start_index, 3: optional i16 limit)
    throws(1:exceptions.InvalidOperationException ioe),

    seller.StoreCategory add_store_category(
    1: i64 store_id, 2: string category_name)
    throws(1:exceptions.InvalidOperationException ioe,
    2: exceptions.NotFoundException nfe),

    seller.StoreCategory update_store_category(
    1: i64 store_category_id, 2: i64 store_id, 3: optional string category_name,
    4: optional i64 upload_count, 5: optional i32 shelf_count,
    6: optional i16 region_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.StoreCategory delete_store_category(1: i64 store_category_id,
    2: i64 store_id)throws(1: exceptions.NotFoundException nfe),

    list<i32> get_store_ids(
    1: optional i32 seller_id, 2: optional bool is_self_operated)
    throws(1: exceptions.NotFoundException nfe),

    seller.LoginList get_login_accounts(
    1: optional i32 seller_id, 2: optional i32 store_id,
    3: optional i64 start_index, 4: optional i16 limit,
    5: optional seller.LoginStatus state,
    6: optional seller.AccountType account_type),

    list<seller.SellerLogin> get_staff_accounts(1: set<i64> login_ids),

    seller.SellerLogin get_seller_login_info(
        1:i64 login_id) throws(
            1: exceptions.NotFoundException nfe,
            2: exceptions.InvalidOperationException ioe),

    seller.SellerLogin lock_login_account(
        1: i64 login_id, 2: seller.LoginStatus operate, 3: i64 operator_id,
        4: optional i32 seller_id, 5: optional i32 store_id) 
    throws(1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    seller.SellerLogin change_login_password(
        1: i64 login_id, 2: string password, 3: optional i32 seller_id,
        4: optional i32 store_id, 5: optional i64 operator_id)
    throws(1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    void create_store_account(1:string user_name, 2:string password, 
        3:seller.LoginStatus state, 4:i32 region_id, 5: i64 store_id, 
        6:string true_name, 7:i64 operator_id)
    throws(1:exceptions.InvalidOperationException ioe),

    void update_store_account(
        1:i64 user_id, 2: i64 store_id, 3: i64 operator_id,
        4:optional string password, 5:optional seller.LoginStatus state, 
        6:optional string true_name)throws(
            1:exceptions.InvalidOperationException ioe),

    seller.SellerLogin update_seller_login(
        1:i64 login_id,
        2:i64 operator_id,
        3:optional string set_phone,
        4:optional string set_email) throws(
            1:exceptions.InvalidOperationException ioe),

    seller.AccountPermissions get_account_permissions(
        1:i64 user_id, 2:i64 seller_id)
    throws (1:exceptions.NotFoundException nfe),

    void update_account_permissions(
        1:i64 user_id, 2:i64 operator_id, 3: i64 store_id,
        4:optional list<i16> pages_usable, 5:optional list<i16> elements_usable)
    throws (
        1:exceptions.InvalidOperationException ioe, 
        2:exceptions.NotFoundException nfe),

    seller.VerifyPermissions verify_permissions(
        1:i64 user_id, 2:optional list<i16> pages_usable, 
        3:optional list<i16> elements_usable)
    throws (1:exceptions.UnauthorizedException ue)

    seller.StoreCategory get_store_default_category(
    1: i64 store_id, 2: bool is_others, 3: optional i64 store_category_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.CoinAgreement join_coin_redemption_plan(
    1: i32 seller_id, 2: i64 store_id, 3: i16 region_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.CoinAgreementlist get_join_coin_agreement_stores(
    1: i32 region_id, 2: optional i64 start_index, 3: optional i16 limit),

    seller.Store append_store_follows(
    1: i64 store_id, 2: i16 count, 3: i16 region_id)
    throws(1: exceptions.NotFoundException nfe),

    seller.RecommendProduct set_recommend_products(
    1: i32 store_id, 2: i16 region_id, 3: set<i64> listing_ids)throws(
    1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    seller.RecommendProduct pull_recommend_products(
    1: i32 store_id, 2: i16 region_id, 3: set<i64> listing_ids)throws(
    1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    seller.RecommendProduct get_recommend_products(
    1: i32 store_id, 2: i16 region_id),

    seller.ShipperAddress set_shipper_address (
    1: i32 store_id, 2: seller.MultiAddress zh_address,
    3: seller.MultiAddress en_address, 4: i16 region_id) throws(
    1: exceptions.NotFoundException nfe,
    2: exceptions.InvalidOperationException ioe),

    seller.ShipperAddress get_shipper_address (
    1: i32 store_id, 2: optional i16 region_id),

    seller.Store set_store_transfer_warehouse(
    1: i32 store_id, 2: optional i32 com_trans_ware_id,
    3: optional i32 spe_trans_ware_id, 4: optional i16 region_id) throws(
    1: exceptions.NotFoundException nfe),

    seller.SelfDelivery get_self_delivery_apply(
    1: i32 store_id, 2: i16 region_id),

    seller.SelfDelivery apply_self_delivery(
        1: i32 store_id, 2: list<seller.Warehouse> warehouses,
        3: i16 region_id)
    throws(1: exceptions.InvalidOperationException ioe),

    list<seller.SelfDeliveryRelate> get_self_deliveries(
        1: optional seller.DeliveryApplyState status,
        2: optional i64 start_index, 3: optional i16 limit,
        4: optional i16 region_id),

    seller.SelfDelivery review_self_delivery_apply(
        1: i32 self_delivery_id, 2: bool is_pass, 3: string reviewer,
        4: optional string ecourier_account,
        5: optional i32 ecourier_account_id),

    seller.PickupAddress set_pickup_address(
        1: i32 store_id, 2: string contact_person, 3: string mobile,
        4: string division, 5: string district, 6: string thana,
        7: string pick_union, 8: string address, 9: i16 region_id),

    seller.PickupAddress get_pickup_address(1: i32 store_id, 2: i16 region_id),

    seller.PickupAddress update_pickup_address(
        1: i32 store_id, 2: i32 branch_id),

    list<seller.ExpandStoreLog> get_application_store_logs(
        1: i32 store_id, 2: optional i16 region_id),

    list<seller.StoreStation> get_store_stations(
        1: i64 store_id, 2: optional list<seller.StoreStatus> status),

    seller.LoginInfo get_store_login_info(1: i64 store_id)
    throws(1: exceptions.NotFoundException nfe),

    void verify_store_phone(
        1: i16 region_id, 2: string phone, 3: i32 store_id)
    throws(1: exceptions.NotFoundException ioe),

    void close_the_store(
        1: i32 store_id, 2: i16 region_id, 3: string remark, 4: i32 operator_id)
    throws(1: exceptions.NotFoundException ioe),

    seller.Store shut_or_open_the_store(
        1: i32 store_id, 2: i16 region_id, 3: i32 operator_id, 4: seller.StoreStatus state)
    throws(1: exceptions.NotFoundException ioe),

    seller.StoreOperateLog get_store_operate_log(
        1: i32 store_id, 2: seller.StoreOperate operate, 3: optional i16 region_id)

    list<seller.FaultAndPunishmentConfig> get_fault_and_punishment_configs(
        1: i16 region_id, 2: optional string param_module),

    list<seller.FaultAndPunishmentConfig> get_fault_configs(1: list<i32> fault_config_ids),

    seller.FaultAndPunishmentConfig get_one_fault_and_punishment_config(
        1: i16 region_id, 2: optional i32 config_id, 3: optional string config_name),

    list<seller.FaultAndPunishmentConfig> set_fault_and_punishment_configs(
        1: list<seller.FaultAndPunishmentConfig> configs),

    seller.MarginRecord submit_margin_payment(
        1: i32 store_id, 2: string transfer_date, 3: i32 paid_amount,
        4: string platform_receiving_account, 5: string transfer_account,
        6: string transaction_serial_number, 7: string currency),

    seller.MarginRecordList get_margin_records(
        1: optional i32 store_id, 2: optional i64 margin_record_id,
        3: optional seller.MarginRecordStatus status, 4: optional string submit_start_time,
        5: optional string submit_end_time, 6: optional string transfer_start_time,
        7: optional string transfer_end_time, 8: optional i32 start_index,
        9: optional i32 limit, 10: optional i16 region_id),

    seller.MarginRecord get_margin_detail(1: i32 margin_record_id)
    throws(1: exceptions.NotFoundException ioe),

    seller.MarginRecord confirm_store_margin(
        1: i32 margin_record_id, 2: i32 operator_id)
    throws(1: exceptions.NotFoundException ioe),

    list<seller.MonthlyMarginAndDisclaimer> get_margin_disclaimers(
        1: i32 store_id, 2: string start_years, 3: string end_years),

    seller.MonthlyMarginAndDisclaimer get_margin_disclaimer(
        1: i32 store_id, 2: string year_month),

    seller.FaultRecord create_fault_and_punishment_record(
        1: i16 region_id, 2: i32 store_id, 3: string fault_config_name, 4: i64 sale_order_id,
        5: string sale_order_code, 6: double penalty_amount),

    seller.FaultRecordList get_faults(
        1: optional i32 store_id, 2: optional i32 fault_record_id,
        3: optional i32 punishment_id, 4: optional i32 fault_config_id,
        5: optional string start_time, 6: optional string end_time,
        7: optional i32 start_index, 8: optional i32 limit, 9: optional i16 region_id),

    seller.FaultRecord get_punishment_record(
        1: optional i32 fault_record_id, 2: optional i32 punishment_record_id)
    throws(1: exceptions.NotFoundException ioe),

    seller.MarginOperateLogList get_margin_streams(
        1: optional i32 store_id, 2: optional seller.MARGIN_LOG_DIRECTION direction,
        3: optional string change_start_time, 4: optional string change_end_time,
        5: optional i32 start_index, 6: optional i32 limit, 7: optional i16 region_id),

    list<seller.FaultRecord> get_fault_records(
        1: list<i64> so_ids, 2: list<string> fault_config_names),

    void create_monthly_margin_and_disclaimer(1: string year_month),

    set<i32> get_state_store_ids(
        1: i16 region_id, 2: optional set<seller.StoreStatus> status),

    list<seller.Seller> get_time_range_change_sellers(
        1: optional string start_time, 2: optional string end_time,
        3: optional i32 last_seller_id),

    list<seller.Store> get_time_range_change_stores(
        1: optional string start_time, 2: optional string end_time,
        3: optional i32 last_store_id),

    void create_store_message(
        1: string title,
        2: string content,
        3: list<i32> publish_to,
        4: i32 user_id,
        5: i16 region_id
    ),

    seller.StoreMessage get_store_message_detail(
        1: i64 message_id
        2: optional i64 store_id
        ) throws (1:exceptions.NotFoundException nfe),

    seller.StoreMessageList get_store_messages(
        1: optional i16 status, 2: optional i16 region,
        3: optional i32 skip, 4: optional i32 limit,
        5: optional string start_time, 6: optional string end_time,
        7: optional i32 store_id),

    void delete_store_message(
        1: i32 message_id,
    ) throws (1:exceptions.NotFoundException nfe),

    list<i32> get_store_messages_status(
        1: i64 store_id,
        2: optional i64 status
        ),

    void delete_store_message_status(
        1: i32 message_id,
        2: i32 store_id,
    ) throws (1:exceptions.NotFoundException nfe),

}