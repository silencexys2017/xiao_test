include "exceptions.thrift"
include "admin_struct.thrift"
// 后台


service AdminService {
    admin_struct.AdminSignIn admin_sign_in(
        1:string user_name, 2:string password, 3:string ip, 
        4:optional i32 local_sub_id, 5:optional bool is_unx_root=false)  // isUnxRoot：是否是国家站总配置后台账号，如果true则无需传国家站ID，即local_sub_id，如果false，则是国家站账号，必须传国家站ID。
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    admin_struct.AdminSignIn get_admin_user_sign_in_info(
        1:i32 user_id)
    throws (1:exceptions.NotFoundException nfe),

    admin_struct.AdminUsers get_admin_users(
        1:optional i16 limit, 2:optional i16 skip, 3:optional set<i32> user_ids,
        4:optional bool is_root, 5:optional set<i32> local_sub_ids),

    admin_struct.AdminUser get_admin_user(
        1:optional i32 user_id,
        2:optional string username) throws (1:exceptions.NotFoundException nfe),

    admin_struct.AdminUser create_admin_user(
        1:string user_name, 2:string password, 
        3:admin_struct.AdminUserState state, 4:i32 region_id, 5:i32 local_sub_id, 
        6:optional string true_name, 7:optional bool is_root=false)
    throws(1:exceptions.InvalidOperationException ioe),

    admin_struct.AdminUser update_admin_user(
        1:i32 user_id, 2:i32 operator_id, 3:optional string password, 
        4:optional string true_name, 5:optional string user_name, 
        6:optional admin_struct.AdminUserState state)
    throws(1:exceptions.InvalidOperationException ioe, 2:exceptions.NotFoundException nfe),

    admin_struct.AdminUserPermissions get_admin_user_permissions(1:i32 user_id) 
    throws (1:exceptions.NotFoundException nfe),

    void update_admin_user_permissions(
        1:i32 user_id, 2:i32 operator_id, 3:optional list<i16> pages_usable, 
        4:optional list<i16> elements_usable)
    throws (1:exceptions.InvalidOperationException ioe, 2:exceptions.NotFoundException nfe),

    admin_struct.AdminSignIn get_admin_user_permission(1:i32 user_id)
    throws (1:exceptions.NotFoundException nfe),

    admin_struct.AdminInterfaceValidation admin_interface_validation(
        1:i32 user_id, 2:optional list<i16> pages_usable, 
        3:optional list<i16> elements_usable)
    throws (1:exceptions.UnauthorizedException ue)

    admin_struct.AdsRunning create_ads_running(
        1: required string fee_spent_date,
        2: required string title,
        3: required admin_struct.AdsChannel channel,
        4: required string channel_remark,
        5: required admin_struct.AdsType ads_type,
        6: required i64 region_id,
        7: required admin_struct.AdsTarget target_product,
        8: required string landing_page,
        9: required double fee,
        10: required string fee_currency,
        11: required double fee_usd,
        12: required string remark,
        13: required string spender,
        14: required i64 creator_id,
    )

    admin_struct.PagingAdsRunning get_ads_running_list(
        1: optional i64 skip
        2: optional i64 limit
        3: optional string title
        4: optional admin_struct.AdsChannel channel
        5: optional admin_struct.AdsType ads_type
        6: optional admin_struct.AdsTarget target_product
        7: optional string fee_spent_date_gte
        8: optional string fee_spent_date_lt
        9: optional i64 fee_usd_gte
        10: optional i64 fee_usd_lt
        11: optional bool is_deleted
        12: optional i64 region_id
    )

    admin_struct.AdsRunning update_ads_running(
        1: required i64 ads_running_id,
        2: optional bool is_deleted,
        3: optional i64 deleter_id
    )
}

