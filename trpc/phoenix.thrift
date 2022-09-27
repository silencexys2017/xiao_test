include "exceptions.thrift"
include "phoenix_struct.thrift"


service PhoenixService {
    list<phoenix_struct.Region> get_regions(),

    phoenix_struct.Region get_region(1:i32 region_id) throws (
        1:exceptions.NotFoundException nfe),

    string send_sms_verify_code(
        1:i32 region_id,
        2:string phone,
        3:phoenix_struct.VerifyCodeType verify_type,
        ) throws (1:exceptions.InvalidOperationException ioe,
                  2:exceptions.NotFoundException nfe),

//    bool check_sms_verify_code(
//        1:i32 region_id,
//        2:string phone,
//        3:string sn,
//        4:string code,
//        5:phoenix_struct.VerifyCodeType verify_type
//        ) throws (1:exceptions.InvalidOperationException ioe,
//                  2:exceptions.NotFoundException nfe),

    string send_email_verify_code(
        1:string email,
        2:phoenix_struct.VerifyCodeType verify_type,
        ) throws (1:exceptions.InvalidOperationException ioe),

//    bool check_email_verify_code(
//        1:string email,
//        2:string esn,
//        3:string ecode,
//        4:phoenix_struct.VerifyCodeType verify_type
//        ) throws (1:exceptions.InvalidOperationException ioe,
//                  2:exceptions.NotFoundException nfe),

    phoenix_struct.Actor get_actor_by_token(
        1:string access_token
        ) throws(1:exceptions.UnauthorizedException ue,
                 2:exceptions.NotFoundException nfe),

    phoenix_struct.Token refresh_access_token(
        1:string refresh_token
        ) throws(1:exceptions.UnauthorizedException ue),

    phoenix_struct.LoginInfo login_by_phone(
        1:i32 region_id,
        2:string phone,
        3:string sn,
        4:string code
        ) throws (1:exceptions.InvalidOperationException ioe,
                  2:exceptions.NotFoundException nfe)

    phoenix_struct.LoginInfo login_by_email(
        1:i32 region_id,
        2:string email,
        3:string sn,
        4:string code
        ) throws (1:exceptions.InvalidOperationException ioe,
                  2:exceptions.NotFoundException nfe)

    phoenix_struct.LoginInfo get_login_info(
        1:i32 ad_platform_id,
        2:string open_id) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe)

    void set_pay_pin(
        1:i64 actor_id,
        2:phoenix_struct.PinType pin_type,
        3:string pin,
        4:optional string phone,
        5:optional string sn,
        6:optional string code
        7:optional string email,
        8:optional string esn,
        9:optional string ecode
        ) throws (1:exceptions.InvalidOperationException ioe,
                  2:exceptions.NotFoundException nfe),

    phoenix_struct.Balance get_balance(
        1:i64 actor_id) throws (1:exceptions.NotFoundException nfe),

    phoenix_struct.PagingActorDetail filter_actors(
        1:i32 skip,
        2:i32 limit,
        3:optional list<i64> actor_ids,
        4:optional string phone,
        5:optional string email,
        6:optional phoenix_struct.ActorType actor_type,
        7:optional string referral_code,
        8:optional i32 region_id,
        9:optional string create_time_start,
        10:optional string create_time_end),

    phoenix_struct.ActorDetail get_actor_detail(
        1:i64 actor_id
        ) throws (
            1:exceptions.NotFoundException nfe),

    phoenix_struct.PromoteTotal get_promote_total(
        1:i64 actor_id
        ) throws (
            1:exceptions.NotFoundException nfe),

    phoenix_struct.Actor update_actor(
        1:i64 actor_id,
        2:optional phoenix_struct.ActorType actor_type,
        3:optional bool is_enabled,
        4:optional string nick
        ) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe),

    phoenix_struct.PagingBalanceLog filter_balance_logs(
        1:i32 skip,
        2:i32 limit,
        3:i64 actor_id
        ) throws (
            1:exceptions.NotFoundException nfe),

    phoenix_struct.WithdrawApply add_withdraw_apply(
        1:i64 actor_id,
        2:i64 amount,
        3:phoenix_struct.AccountType account_type,
        4:string account_num,
        5:string pin
        ) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe),

    phoenix_struct.WithdrawApply change_withdraw_status(
        1:i64 apply_id,
        2:phoenix_struct.WithdrawApplyStatus status
        3:optional i64 operator_id,
        4:optional i64 query_actor_id
        ) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe),

    phoenix_struct.WithdrawApply get_withdraw_apply(
        1:i64 apply_id,
        2:optional i64 actor_id) throws (
            1:exceptions.NotFoundException nfe),

    phoenix_struct.WithdrawApplyDetail get_withdraw_detail(
        1:i64 apply_id) throws (
            1:exceptions.NotFoundException nfe),

    phoenix_struct.PagingWithdrawApplyDetail filter_withdraws(
        1:i32 skip,
        2:i32 limit,
        3:optional i64 actor_id,
        4:optional string phone,
        5:optional phoenix_struct.WithdrawApplyStatus status,
        6:optional string apply_time_start,
        7:optional string apply_time_end,
        8:optional string audit_time_start,
        9:optional string audit_time_end,
        10:optional string complete_time_start,
        11:optional string complete_time_end,
        12:optional i32 region_id),

    void generate_advertiser(
        1:i64 actor_id,
        2:optional i64 adp_id
        ) throws (
            1:exceptions.InvalidOperationException ioe),

    void create_invited_user(
        1: string invited_open_id
        2: string used_invite_code
        3: i64 region_id
        4: string phone
        5: optional string nick
        6: optional string email
        7: optional string invited_time
        8: optional bool is_verified
        9: optional string verify_time
        10: optional string last_active_time
    )

    void update_invited_user(
        1: string invited_open_id
        2: optional string last_active_time
        3: optional bool is_verified
        4: optional string verify_time
    )

    phoenix_struct.FilterInvitedUserResult filter_invited_user(
        1: i64 limit
        2: i64 skip
        3: optional string invited_open_id
        4: optional string phone
        5: optional string refer_code
        6: optional i64 region_id
        7: optional string create_time_start
        8: optional string create_time_end
        9: optional i64 actor_id
    )

    phoenix_struct.Advertiser get_advertiser(
        1:optional i64 actor_id
        ) throws (
            1:exceptions.NotFoundException nfe),

    i64 create_advertiser(
        1: i64 actor_id
        2: i64 adplatform_id
        3: string invite_code
        4: string login_name
        5:optional string open_id
        6:optional string nick
    ),

    phoenix_struct.InviteOrderList filter_invite_order_converts (
        1: i64 start_index, 2: i32 limit, 3: optional string start_time,
        4: optional string end_time, 5: optional i64 actor_id,
        6: optional string invite_code, 7: optional string actor_phone,
        8: optional string customer_id, 9: optional string customer_phone,
        10: optional phoenix_struct.PayMethod order_type,
        11: optional list<i16> order_states),

    phoenix_struct.ArticleConvertList filter_article_order_converts (
        1: i64 start_index, 2: i32 limit, 3: optional string start_time,
        4: optional string end_time, 5: optional i64 actor_id,
        6: optional string article_title, 7: optional i64 article_id,
        8: optional string product_id, 9: optional string customer_id,
        10: optional string customer_phone,
        11: optional phoenix_struct.PayMethod order_type,
        12: optional list<i16> order_states),

    phoenix_struct.ShareConvertList filter_share_order_converts (
        1: i64 start_index, 2: i32 limit, 3: optional string start_time,
        4: optional string end_time, 5: optional i64 actor_id,
        6: optional string article_id, 7: optional string product_id,
        8: optional string customer_id, 9: optional string customer_phone,
        10: optional phoenix_struct.PayMethod order_type,
        11: optional list<i16> order_states),

    phoenix_struct.OrderCommissionList filter_order_commission(
        1: i64 start_index, 2: i32 limit, 3: optional string start_time,
        4: optional string end_time, 5: optional i64 actor_id,
        6: optional string customer_id,
        7: optional phoenix_struct.PayMethod order_type,
        8: optional list<i16> order_states,
        9: optional phoenix_struct.AfterSaleOption is_after_sale),

    void create_actor_convert_order(
        1: string customer_id, 2: i16 region_id, 3: string phone,
        4: string nick, 5: phoenix_struct.PayMethod pay_method,
        6: list<phoenix_struct.SaleOrderConverts> so_converts,
        7: string created_at) throws (
        1: exceptions.NotFoundException nfe,
        2: exceptions.InvalidOperationException ioe),

    void update_actor_convert_order_state(
        1: string order_id, 2: phoenix_struct.OrderStatus operate,
        3: string update_time, 4: string customer_id),

    list<phoenix_struct.MonthCommission> get_actor_month_commission_reports(
        1: i64 actor_id, 2: string start_time, 3: string end_time),

    list<phoenix_struct.OrderComRelated> get_actor_order_commissions(
        1: i64 actor_id, 2: i32 skip, 3: i32 limit,
        4: optional string start_time, 5: optional string end_time)

    phoenix_struct.AdminSignIn admin_sign_in(
        1: string username, 2: string password, 3: string ip)
    throws (1:exceptions.NotFoundException nfe, 2:exceptions.InvalidOperationException ioe),

    phoenix_struct.AdminSignIn get_admin_user_sign_in_info(1: i32 user_id)
    throws (1:exceptions.NotFoundException nfe),

    phoenix_struct.AdminUsers get_admin_users(
        1: optional i16 limit, 2: optional i16 skip, 3: optional set<i32> user_ids)

    phoenix_struct.AdminUser create_admin_user(
        1: string username, 2: string password, 3: string true_name, 
        4: phoenix_struct.AdminUserState state)
    throws(1:exceptions.InvalidOperationException ioe),

    phoenix_struct.AdminUser update_admin_user(
        1: i32 user_id, 2: string true_name, 
        3: phoenix_struct.AdminUserState state, 4: i32 operator_id,
        5: optional string password)
    throws(1:exceptions.InvalidOperationException ioe, 2:exceptions.NotFoundException nfe),

    phoenix_struct.AdminUserPermissions get_admin_user_permissions(1: i32 user_id) 
    throws (1:exceptions.NotFoundException nfe),

    void update_admin_user_permissions(
        1: i32 user_id, 2: i32 operator_id, 3: optional list<i16> pages_usable, 
        4: optional list<i16> elements_usable) 
    throws (1:exceptions.InvalidOperationException ioe, 2:exceptions.NotFoundException nfe),

    phoenix_struct.AdminSignIn get_admin_user_permission(1: i32 user_id)
    throws (1:exceptions.NotFoundException nfe),

    phoenix_struct.AdminInterfaceValidation admin_interface_validation(
        1: i32 user_id, 2: optional list<i16> pages_usable, 
        3: optional list<i16> elements_usable)
    throws (1:exceptions.UnauthorizedException ue)

    // actor article
    phoenix_struct.Article create_article(
        1: i64 actor_id, # 修改参数
        2: string title,
        3: string cover,
        4: phoenix_struct.ProductType product_type,
        5: i32 product_count,
        6: list<string> product_ids,
        7: list<phoenix_struct.ArticleContent> content_list,
    )

    phoenix_struct.Article update_article(
        1: i64 id,
        2: optional string title,
        3: optional string cover,
        4: optional phoenix_struct.ProductType product_type,
        5: optional i32 product_count,
        6: optional list<string> product_ids,
        7: optional list<phoenix_struct.ArticleContent> content_list,
        8: optional i64 actor_id
    )

    phoenix_struct.Article update_article_status(
        1: i64 id,
        2: phoenix_struct.ArticleStatus status
        3: optional i64 operator_id,
        4: optional i64 actor_id
    )

    phoenix_struct.Article get_article_by_id(
        1: i64 id
    )

    phoenix_struct.PagingArticle filter_articles(
        1: i32 skip,
        2: i32 limit,
        3: optional list<phoenix_struct.ArticleStatus> status,
        4: optional i64 actor_id,
        5: optional string actor_phone,
        6: optional phoenix_struct.ProductType product_type,
        7: optional string product_id, # 修正
        8: optional string posted_time_start, # 命名修改
        9: optional string posted_time_end, # 命名修改
        10: optional phoenix_struct.ArticleType article_type
    )

    void update_article_status_by_adp_article_id(
        1: string adp_article_id,
        2: phoenix_struct.ArticleStatus status
        3: optional phoenix_struct.ArticleSelectiveStatus selective_status
    )

    void create_article_from_perfee_review(
        1: string nvite_code,
        2: string adp_article_id,
        3: string title,
        4: string cover,
        5: list<string> product_ids
    )
}