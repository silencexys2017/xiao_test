include "exceptions.thrift"
include "constants.thrift"
include "logistics_struct.thrift"


service LogisticsService {

    logistics_struct.ExpressPackage create_express_package(
    1: i32 tran_ware_id, 2: i64 package_id, 3: i16 region_id, 4: i64 address_id,
    5: i64 account_id, 6: optional i64 so_id, 7: optional string so_code,
    8: optional i64 store_id, 9: optional i32 item_count,
    10: optional string so_created_at, 11: optional string confirmed_at)
    throws (1:exceptions.InvalidOperationException ioe),

    logistics_struct.ExpressPackage domestic_transport_package(
    1: i64 package_id, 2: i32 operate_id,
    3: logistics_struct.china_express delivery_id, 4: string delivery_code,
    5: optional string receiving_location) throws (
    1:exceptions.NotFoundException nfe),

    logistics_struct.ExpressPackageList get_express_packages(
    1: optional string delivery_code, 2: optional i64 so_id,
    3: optional logistics_struct.EpStatus status,
    4: optional i32 start_index, 5: optional i16 limit,
    6: optional logistics_struct.EpTimeType time_type,
    7: optional string start_time, 8: optional string end_time,
    9: optional i16 region_id, 10: optional string receive_location,
    11: optional i32 operator_id, 12: optional set<i64> express_package_ids,
    13: optional i64 box_id, 14: optional i64 delivery_batch_id, 
    15: optional logistics_struct.DeliveryBatchState delivery_batch_state,
    16: optional logistics_struct.AllocateState allocate_state),

    logistics_struct.ExpressPackage get_one_express_package(
        1: optional i64 so_id, 2: optional i64 express_package_id, 3: optional i64 package_id),

    void express_package_bind_box(
        1: set<i64> express_package_ids, 2: i64 box_id, 3: i32 operator_id) 
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    logistics_struct.ExpressPackage confirm_express_package(1: i64 express_package_id, 2: i32 operator_id)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),


    logistics_struct.ExpressPackage problem_express_package(
        1: i64 express_package_id, 2: logistics_struct.ProblemType  problem_type,
        3: string remark, 4: i32 operator_id)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    void delete_express_package(1: i64 express_package_id)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    list<logistics_struct.ProblemProduct> confirm_problem_package(
    1: list<logistics_struct.Sku> skus, 2: i64 package_id, 3: i32 operator_id,
    4: string receive_location)throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    logistics_struct.ReceivingRecord confirm_receive_package(
    1: i64 package_id, 2: i32 operator_id, 3: string receive_location) throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    logistics_struct.ExpressPackage print_head_express_order(
    1: i64 package_id, 2: i32 operator_id, 3: optional string receive_location)
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    list<logistics_struct.ReceivingRecord> get_receiving_records(
    1: optional i64 package_id, 2: optional i64 so_id,
    3: optional string so_code) throws (
    1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    list<logistics_struct.ProblemProduct> get_problem_products(
    1: optional i64 record_id, 2: optional i64 package_id)
    throws (1:exceptions.NotFoundException nfe),

    logistics_struct.TransferWarehouse get_one_transfer_warehouse(
    1: optional i16 tran_ware_id),

    list<logistics_struct.TransferWarehouse> get_transfer_warehouses(
    1: optional logistics_struct.EnableSwitch is_enable=0,
    2: optional set<logistics_struct.ProductNature> nature=[],
    3: optional i16 region_id),

    logistics_struct.TransferWarehouse update_transfer_warehouse(
    1: i16 tran_ware_id, 2: optional logistics_struct.EnableSwitch is_enable=0,
    3: optional string contact, 4: optional string phone,
    5: optional string address, 6: optional set<i16> support_channels=[])
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    logistics_struct.HeadTransportChannel get_one_head_transport_channel(
    1: optional i16 head_channel_id),

    list<logistics_struct.HeadTransportChannel> get_head_transport_channels(
    1: optional logistics_struct.EnableSwitch is_enable=0,
    2: optional set<logistics_struct.ProductNature> nature=[],
    3: optional i16 region_id),

    logistics_struct.HeadTransportChannel update_head_transport_channel(
    1: i16 head_channel_id, 2: optional logistics_struct.EnableSwitch is_enable=0,
    3: optional string contact, 4: optional string phone,
    5: optional set<i16> region_ids=[], 6: optional set<i16> support_natures=[])
    throws (1:exceptions.InvalidOperationException ioe,
    2:exceptions.NotFoundException nfe),

    logistics_struct.DeliveryBatchs get_delivery_batchs(
        1: optional i16 region_id, 2: optional i16 transfer_warehouse_id,
        3: optional string start_time, 4: optional string end_time, 
        5: optional i32 skip=0, 6: optional i16 limit, 
        7: optional set<logistics_struct.DeliveryBatchState> states,
        8: optional set<i64> delivery_batch_ids, 9: optional bool is_alive,
        10: optional i64 so_id),

    logistics_struct.DeliveryBatch create_delivery_batch(
        1: i16 transfer_warehouse_id, 2: i16 head_trans_channel_id,
        3: i16 destination_country_id, 4: i16 operator_id,
        5: optional string remark),

    logistics_struct.DeliveryBatch update_delivery_batch(
        1: i64 delivery_batch_id, 2: logistics_struct.DeliveryBatchState state,
        3: i16 operator_id, 4: optional string remark)
    throws (1:exceptions.NotFoundException nfe),

    void delete_delivery_batch(1: i64 delivery_batch_id, 2: i16 operator_id)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    list<logistics_struct.DeliveryBatchLog> get_delivery_batch_logs(1: i64 delivery_batch_id),

    list<logistics_struct.Box> get_boxs(1: optional set<i64> box_ids, 2: optional i64 delivery_batch_id),

    logistics_struct.Box create_box(
        1: string box_name, 2: logistics_struct.BoxType box_type,
        3: i64 delivery_batch_id, 4: i16 operator_id)
        throws (1:exceptions.InvalidOperationException ioe),

    logistics_struct.Box confirm_box(1: i64 box_id, 2: i16 operator_id)
    throws (1:exceptions.NotFoundException nfe),

    void delete_box(1: i64 box_id, 2: i16 operator_id)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    list<logistics_struct.BoxLog> get_box_logs(
        1: optional set<i64> box_ids, 2: optional i64 delivery_batch_id),

    # 是否存在收件单
    bool is_exist_receipt_order(1:i32 region_id, 2:i64 sale_order_id),

    # 构建收件单
    logistics_struct.ReceiptOrder build_receipt_order(
        1:logistics_struct.ReceiptOrder receipt_order) throws (
            1:exceptions.InvalidOperationException ioe),

    # 录入采购订单
    logistics_struct.ReceiptOrderDetail input_purchase_order(
        1:i32 region_id,
        2:i64 sale_order_id,
        3:i64 sku_id,
        4:i32 qty,
        5:string tracking_number,
        6:string sender_contact,
        7:i64 input_operator_id) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    # 根据运单号获取收件详单列表
    logistics_struct.PagingReceiptOrderDetail get_details_by_tracking_number(
        1:i64 region_id,
        2:string tracking_number,
        3:optional logistics_struct.ReceiptDetailStatus status) throws (
            1:exceptions.NotFoundException nfe),

    # 获取收件详单列表
    logistics_struct.PagingReceiptOrderDetail get_receipt_order_details(
        1:optional i64 region_id,
        2:optional logistics_struct.ReceiptDetailStatus status,
        3:optional i64 sale_order_id,
        4:optional i64 sku_id,
        5:optional i64 store_id,
        6:optional string tracking_number,
        7:optional list<i64> account_ids,
        8:optional i64 receipt_order_id,
        9:optional string create_time_start,
        10:optional string create_time_end,
        11:optional i16 skip,
        12:optional i16 limit),

    # 确认收件
    logistics_struct.BatchOperation received_by_tracking_number(
        1:i64 region_id,
        2:string tracking_number,
        3:i64 operator_id) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    # 添加问题单
    logistics_struct.BatchOperation add_problems(
        1:i64 region_id,
        2:string tracking_number,
        3:list<logistics_struct.ProblemDetailCondition> problems,
        4:i64 operator_id) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    # 处理问题单
    logistics_struct.BatchOperation update_problems(
        1:i64 region_id,
        2:list<i64> receipt_order_detail_ids,
        3:logistics_struct.ReceiptDetailStatus set_status,
        4:i64 operator_id) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    # 获取收件单列表
    logistics_struct.PagingReceiptOrder get_receipt_orders(
        1:optional i64 region_id,
        2:optional logistics_struct.ReceiptStatus status,
        3:optional i64 sale_order_id,
        4:optional i64 sku_id,
        5:optional i64 store_id,
        6:optional string tracking_number,
        7:optional i64 account_id,
        8:optional i64 receipt_order_id,
        9:optional string create_time_start,
        10:optional string create_time_end,
        11:optional string order_create_start,
        12:optional string order_create_end,
        13:optional string completed_start,
        14:optional string completed_end,
        15:optional bool is_followup,
        16:optional bool is_printed,
        17:optional bool has_problems,
        18:optional list<i64> receipt_ids,
        19:optional i16 skip,
        20:optional i16 limit),

    # 获取收件单列表
    logistics_struct.ReceiptOrder get_receipt_order(
        1:i64 receipt_order_id) throws (
            1:exceptions.NotFoundException nfe),

    # 批量打印收件单
    logistics_struct.BatchOperation batch_print_receipt_orders(
        1:i64 region_id,
        2:list<i64> receipt_order_ids) throws (
            1:exceptions.NotFoundException nfe),
}