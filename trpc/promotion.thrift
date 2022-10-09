include "exceptions.thrift"
include "promotion_struct.thrift"

service PromotionService {
    promotion_struct.PagingSessionGen get_session_gens(
        1:optional string start_time,
        2:optional string end_time,
        3:optional i32 skip,
        4:optional i32 limit),

    void build_sessions_by_gen(1:i64 gen_id, 2:i64 region_id),

    promotion_struct.CurrentSessionSku current_session_sku(
        1:i64 region_id,
        2:optional i32 last_index,
        3:optional i32 limit) throws (1:exceptions.NotFoundException nfe),

    list<promotion_struct.Session> get_current_sessions(
        1:i64 region_id,
        2:optional i32 limit),

    promotion_struct.Session get_session(1: i64 session_id)
    throws (1: exceptions.NotFoundException nfe),

    promotion_struct.PagingSession get_sessions(
        1:optional i64 region_id,
        2:optional string start_time,
        3:optional string end_time,
        4:optional i32 skip,
        5:optional i32 limit),

    promotion_struct.ActivityApply add_apply(
        1:i64 session_id,
        2:i64 sku_id,
        3:i32 activity_type,
        4:i64 activity_price,
        5:i32 promise_stock,
        6:promotion_struct.LimitRule limit_rule,
        7:bool is_accept_adjust,
        8:promotion_struct.OperatorType applicant_type,
        9:i64 applicant_id,
        10:promotion_struct.CloneSku clone_sku,
        11:bool no_remission_postage,
        12:bool no_remission_amount,
        13:bool no_voucher) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    list<i64> batch_add_applies(
        1:i64 session_id,
        2:promotion_struct.OperatorType applicant_type,
        3:i64 applicant_id,
        4:i32 activity_type,
        5:bool is_accept_adjust,
        6:promotion_struct.LimitRule limit_rule,
        7:list<promotion_struct.BatchActivityApply> applies,
        8:bool no_remission_postage,
        9:bool no_remission_amount,
        10:bool no_voucher) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    list<promotion_struct.BatchResult> batch_audit_applies(
        1:list<i64> apply_ids,
        2:promotion_struct.OperatorType operator_type,
        3:i64 operator_id),

    list<promotion_struct.BatchResult> batch_reject_applies(
        1:list<i64> apply_ids, 2:promotion_struct.OperatorType operator_type,
        3:i64 operator_id, 4: string reject_reason),

    list<promotion_struct.BatchResult> batch_copy_applies(
        1:list<promotion_struct.BatchUpdateApply> update_applies,
        2:i64 session_id,
        3:promotion_struct.OperatorType applicant_type,
        4:i64 applicant_id),

    promotion_struct.ActivityApply update_apply(
        1:i64 apply_id,
        2:i64 sku_id,
        3:i32 activity_type,
        4:i64 activity_price,
        5:i32 promise_stock,
        6:promotion_struct.LimitRule limit_rule,
        7:bool is_accept_adjust,
        8:promotion_struct.OperatorType applicant_type,
        9:i64 applicant_id,
        10:promotion_struct.CloneSku clone_sku,
        11:bool no_remission_postage,
        12:bool no_remission_amount,
        13:bool no_voucher,
        14:optional i64 session_id) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    promotion_struct.PagingActivityApply get_applies(
        1:optional string apply_start_time,
        2:optional string apply_end_time,
        3:optional string apply_session_start,
        4:optional string apply_session_end,
        5:optional string final_session_start,
        6:optional string final_session_end,
        7:optional i64 sku_id,
        8:optional string sku_title,
        9:optional promotion_struct.OperatorType applicant_type,
        10:optional i64 applicant_id,
        11:optional i32 activity_type,
        12:optional list<i32> status,
        13:optional list<i64> store_ids,
        14:optional i32 skip,
        15:optional i32 limit,
        16:optional i64 listing_id,
        17:optional list<i64> apply_ids,
        18:optional i64 region_id,
        19:optional i64 apply_session_id,
        20:optional i64 final_session_id),

    promotion_struct.ActivityApply get_apply(
        1:i64 apply_id) throws (1:exceptions.NotFoundException nfe),

    promotion_struct.ActivityApply change_apply_status(
        1:i64 apply_id,
        2:i32 status,
        3:optional promotion_struct.OperatorType operator_type,
        4:optional i64 operator_id,
        5:optional i64 new_session_id,
        6:optional string reject_reason) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    promotion_struct.PagingActivitySku get_activity_skus(
        1:optional i64 session_id,
        2:optional i32 status,
        3:optional i32 last_index,
        4:optional list<i64> apply_ids,
        5:optional i32 skip,
        6:optional i32 limit,
        7:optional i64 store_id),

    list<promotion_struct.ActivitySku> aggregate_session_activities(
        1:i64 session_id,
        2:i32 last_index,
        3:i32 limit),

    void update_activity_sku(
        1:i64 activity_id,
        2:optional i32 status,
        3:optional i32 sold
        4:optional i32 index) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    promotion_struct.ActivitySku get_activity_sku(
        1:i64 activity_id) throws (1:exceptions.NotFoundException nfe),

    promotion_struct.GeneralActivity get_valid_general_activity(
        1:promotion_struct.QueryActivity item) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    list<promotion_struct.GeneralActivity> get_valid_general_activities(
        1:list<promotion_struct.QueryActivity> items) throws (
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    list<promotion_struct.ActivitySku> get_activities_by_items(
        1:list<promotion_struct.QueryActivity> items),

    promotion_struct.ActivitySku move_activity_sku(
        1:i64 activity_id,
        2:i64 new_session_id) throws (1:exceptions.NotFoundException nfe),

    promotion_struct.ActivitySku clone_activity_sku(
        1:i64 activity_id,
        2:i64 new_session_id) throws (1:exceptions.NotFoundException nfe),

    void add_reservations(
        1: list<promotion_struct.ActivitySkuStockItem> items) throws(
            1:exceptions.InvalidOperationException ioe),

    void clean_reservations(
        1: list<promotion_struct.ActivitySkuStockItem> items) throws(
            1:exceptions.InvalidOperationException ioe),

    void decrease_reservations_and_stocks(
        1: list<promotion_struct.ActivitySkuStockItem> items) throws(
            1:exceptions.InvalidOperationException ioe),

    void increase_stocks(
        1: list<promotion_struct.ActivitySkuStockItem> items) throws(
            1:exceptions.InvalidOperationException ioe),

    promotion_struct.RelatedActivitySkus related_activity_skus(
        1:i64 region_id,
        2:list<i64> sku_ids,
        3:optional i64 current_sku_id,
        4:optional i32 activity_type,
        5:optional i64 activity_id) throws (1:exceptions.NotFoundException nfe),

    list<promotion_struct.Parameter> get_parameter_list(
        1:i32 region_id, 2:string param_module),

    promotion_struct.Parameter get_parameter(
        1:i32 region_id,
        2:string name) throws (1:exceptions.NotFoundException nfe),

    void set_parameter(1:promotion_struct.SetParameter parameter, 2: i64 region_id),

    void set_parameters(1:list<promotion_struct.SetParameter> parameter),

    # 抽奖相关
    # dnx
    # 获取当前抽奖规则
    promotion_struct.LuckyDrawRules get_lucky_draw_rules(1: i64 region_id)

    # 设置抽奖规则
    promotion_struct.LuckyDrawRules set_lucky_draw_rules(
        1: i32 daily_free_times,
        2: i32 daily_coins_times,
        3: i32 coins_per_time,
        4: bool add_times_from_order,
        5: i64 region_id
    )

    # 创建新的抽奖序列
    promotion_struct.LuckyDrawBatch create_lucky_draw_batch(
        1: string start_at,
        2: string end_at,
        3: i64 region_id,
        4: i64 operator_id,
        5: list<promotion_struct.NewLuckyDrawAward> awards,  
        # 前端传来的5个二三等奖是不区分的, dnx取两个为二等奖, 3个为三等奖再传到thrift
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    # 获取历史抽奖序列
    promotion_struct.PagingLuckyDrawBatch get_history_lucky_draw_batchs(
        1: i64 region_id,
        2:optional i32 limit,
        3:optional i32 skip,
    )

    # 获取抽奖记录(dnx, chromo)
    promotion_struct.PagingLuckyDrawLog get_lucky_draw_logs(
        1:optional i64 region_id,
        2:optional i64 account_id,
        3:optional list<promotion_struct.AwardLevel> award_levels,
        4:optional string start_at,
        5:optional string end_at,
        6:optional i32 limit,
        7:optional i32 skip,
    )

    # chromo
    # 获取最新的抽奖序列(chromo, dnx)
    promotion_struct.LuckyDrawBatch get_latest_lucky_draw_batch(
        1: i64 region_id,
        2: optional bool is_valid,  # chromo传true
    ) throws (
        1:exceptions.NotFoundException nfe
    )

    # 获取可用抽奖抽奖次数
    promotion_struct.LuckyDrawTimes get_lucky_draw_times(
        1: i64 account_id,
        2: i64 region_id,
    )

    # 抽奖
    promotion_struct.LuckyDrawLog play_lucky_draw(
        1: i64 account_id,
        2: i64 region_id,
        3: i64 draw_batch_id,
        4: promotion_struct.DrawChanceType chance_type,
        5: optional bool can_get_special_awrad,
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )

    # 设置抽奖批次概率
    promotion_struct.LuckyDrawProbability set_lucky_draw_probability(
        1: i64 batch_id,
        2: list<i64> probability,
    ) throws (
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException nfe
    )

    # 获取抽奖批次概率
    list<i64> get_lucky_draw_probability_of_region(
        1: i64 region_id,
    ) 

    # 获取抽奖批次概率
    promotion_struct.LuckyDrawProbability get_lucky_draw_probability_of_batch(
        1: i64 batch_id,
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )

    # 更新的LuckyDrawLog的orderId
    void update_lucky_draw_send_content(
        1: i64 lucky_draw_log_id,
        2: string send_ontent,
    )

    # 当订单complete的时候更新账户下的赚取的免费次数
    promotion_struct.LuckyDrawAccount update_lucky_draw_account_earned_times(
        1: i64 account_id,
        2: i64 order_id,
        3: i32 earned_times_inc
    )

    promotion_struct.PagingRedeemSku get_redeem_sku_list(
        1:optional i64 region_id,
        2:optional i64 sku_id,
        3:optional promotion_struct.ActivityStatus status,
        4:optional string create_time_start,
        5:optional string create_time_end,
        6:optional bool is_only_coins,
        7:optional i32 skip,
        8:optional i32 limit),

    promotion_struct.RedeemSku get_redeem_sku(
        1:i64 redeem_id,
        2:optional promotion_struct.ActivityStatus status) throws (
            1:exceptions.NotFoundException nfe),

    promotion_struct.RedeemSku add_redeem_sku(
        1:i32 region_id,
        2:i64 sku_id,
        3:string display_title,
        4:i64 activity_price,
        5:i32 coins,
        6:i32 promise_stock,
        7:promotion_struct.CloneSku clone_sku,
        8:i64 operator_id) throws (1:exceptions.NotFoundException nfe),

    promotion_struct.RedeemSku update_redeem_sku(
        1:i64 redeem_id,
        2:i64 operator_id,
        3:optional string display_title,
        4:optional i64 activity_price,
        5:optional i32 coins,
        6:optional i32 promise_stock,
        7:optional i32 status) throws (1:exceptions.NotFoundException nfe),

    # app端分页today_deals
    promotion_struct.PagingSimpleTodayDealSku get_active_today_deals(
        1:i64 region_id,
        2:i32 skip,
        3:i32 limit
    )

    promotion_struct.SimpleTodayDealSku get_deal_sku(
        1:i64 region_id,
        2:i64 sku_id
    )

    list<promotion_struct.SimpleTodayDealSku> get_deal_skus(
        1:i64 region_id,
        2:list<i64> sku_ids
    )

    # today_deals申请
    list<promotion_struct.todayDealHandleResult> apply_today_deals(
        1:list<promotion_struct.ApplyTodayDealSku> apply_skus
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    # today_deal审核
    void audit_today_deal(
        1:i64 today_deal_id,
        2:bool is_audited
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.PagingTodayDealSku filter_today_deals(
        1:i32 region_id,
        2:i32 skip,
        3:i32 limit,
        4:optional i64 listing_id,
        5:optional i64 sku_id,
        6:optional i32 store_id,
        7:optional promotion_struct.TodatDealApplyStatus status,
        8:optional string apply_time_start,
        9:optional string apply_time_end,
        10:optional string audit_time_start,
        11:optional string audit_time_end,
        12:optional bool is_active,
        13:optional i32 deal_days
    )

    void update_today_deal(
        1:i64 today_deal_id,
        2:optional i64 region_id,
        3:optional i64 sku_id,
        4:optional i64 listing_id,
        5:optional i64 deal_price,
        6:optional i32 deal_days,
        7: optional string sku_title,
        8: optional i64 list_price,
        9: optional i64 sale_price
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    void remove_today_deal(
        1:i64 today_deal_id,
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )
    
    # today_deals下架
    list<promotion_struct.todayDealHandleResult> off_today_deals(
        1:list<i64> today_deal_ids
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.PagingSimpleTodayDealSku get_active_one_day_today_deals(
        1:i64 region_id,
        2:i32 skip,
        3:i32 limit
    )

    list<promotion_struct.todayDealHandleResult> batch_audit_today_deals(
        1:list<i64> today_deal_ids,
        2:bool is_audited
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    list<promotion_struct.SkuSoldRes> judge_flash_skus_is_sold(
        1:i32 region_id, 2: list<i64> sku_ids, 3: i16 days),

    promotion_struct.Promotion apply_promotion (
        1: string title,
        2: promotion_struct.PromotionType type,
        3: promotion_struct.PromotionRule rule,
        4: string start_time,
        5: string end_time,
        6: bool no_store_voucher,
        7: bool no_platform_voucher,
        8: bool no_coins,
        9: list<i32> store_ids,
        10: promotion_struct.Operator apply_account,
        11: i64 region_id,
        12: i32 limit_store_products
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.Promotion get_promotion_by_id (
        1:i64 promotion_id
        2:optional bool is_active
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )

    list<promotion_struct.Promotion> get_promotions_by_ids (
        1:list<i64> promotion_ids
        2:optional bool is_active
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )


    promotion_struct.PagingPromotion filter_promotions (
        1: required i64 skip,
        2: required i64 limit,
        3: required i64 region_id,
        4: list<promotion_struct.PromotionType> type_list,
        5: list<promotion_struct.PromotionStatus> status_list,
        6: string apply_time_start,
        7: string apply_time_end,
        8: string applicants,
        9: string active_time_start,
        10: string active_time_end,
        11: list<promotion_struct.PromoActiveStatus> active_status
        12: i64 store_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.Promotion update_promotion (
        1:i64 promotion_id,
        2:promotion_struct.PromotionStatus status,
        3:promotion_struct.Operator audit_account
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )

    list<promotion_struct.PromotionProductResult> apply_promotion_products (
        1: list<promotion_struct.PromotionProductMsg> apply_products,
        2: i64 promotion_id,
        3: promotion_struct.Operator apply_account,
        4: i64 store_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.PromotionProduct update_promotion_product (
        1: i64 promotion_product_id,
        2: promotion_struct.PromotionProductStatus status,
        3: promotion_struct.Operator audit_account
    ) throws (
        1:exceptions.InvalidOperationException ioe
        2:exceptions.NotFoundException nfe
    )

    promotion_struct.PagingPromotionProduct filter_promotion_products (
        1: i64 skip,
        2: i64 limit,
        3: list<promotion_struct.PromotionProductStatus> status_list,
        4: string apply_time_start,
        5: string apply_time_end,
        6: list<promotion_struct.PromotionType> promotion_type_list,
        7: i64 promotion_id,
        8: i64 listing_id,
        9: string listing_title,
        10: i64 store_id,
        11: i64 region_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.PagingPromotionProduct get_promo_products_by_promotion_id(
        1: i64 promotion_id,
        2: i64 skip,
        3: i64 limit
    )

    list<promotion_struct.Promotion> get_active_promotions_by_listing_id(
        1: i64 listing_id
        2: i64 region_id
    )

    list<promotion_struct.PromotionsOfListing> get_active_promotions_by_listing_ids(
        1: list<i64> listing_ids
        2: i64 region_id
    )

    list<i64> check_listings_in_promotion(
        1: i64 promotion_id,
        2: list<i64> listing_ids
    )

    list<promotion_struct.DefaultPromotionOfCartItem> get_default_promotion_of_cart_items (
        1: list<promotion_struct.PromotionCartItem> cart_items
        2: i64 region_id
        3: optional bool is_satisfied
    )

    promotion_struct.DefaultPromotionOfCartItem get_default_promotion_of_cart_item (
        1: promotion_struct.PromotionCartItem cart_item
        2: i64 region_id
        3: optional bool is_satisfied
    )

    void create_lucky_draw_probability(1: i64 region_id)

    void create_lucky_draw_rules(1: i64 region_id)

    list<promotion_struct.TodayDealSku> get_exists_today_deal_of_store (
        1: i64 store_id,
        2: i64 region_id
    )

    promotion_struct.PagingGroupBuying get_group_buying_list (
        1: required i16 region_id, 2: i64 limit, 3: i64 skip, 
        4: optional promotion_struct.GroupBuyingStatus status, 
        5: optional string apply_time_start, 6: optional string apply_time_end,
        7: optional string start_time_start, 8: optional string start_time_end,
        9: optional i64 store_id, 10: optional list<i64> listing_ids, 11: optional i64 sku_id, 
        12: optional i16 tag_id, 13: optional i16 expire_days, 14: optional bool expire_soon, 
        15: optional bool is_hot, 16: optional list<i64> group_buying_ids,
        17: optional string active_time_start, 18: optional string active_time_end
    ) throws (
        1:exceptions.NotFoundException nfe
    )

    promotion_struct.GroupBuying get_group_buying_by_id (
        1: i64 group_buying_id
    )

    // operator_id，dnx管理后台调用的时候才需要传
    void update_group_buyings(
        1: required set<i64> group_buying_ids,
        2: optional promotion_struct.GroupBuyingState state,
        3: optional bool is_hot, 4: optional i64 operator_id)

    // 返回活动ID，可根据需要修改
    i64 apply_group_buying(
        1: i64 region_id, 2: i64 store_id, 3: i64 category_id, 
        4: i64 listing_id, 5: i64 buyers_goals, 6: i64 completion_period,
        7: list<promotion_struct.GroupBuyingSku> skus, 8: string start_on,
        9: i64 expire_days, 10: bool robot_enabled)

    list<promotion_struct.GroupBuyingApplyResult> apply_group_buyings(
        1: list<promotion_struct.GroupBuyingListing> listings,
        2: i64 buyers_goals,
        3: i64 completion_period,
        4: string start_on,
        5: i64 expire_days,
        6: bool robot_enabled
    )

    void apply_group_buying_again(
        1: i64 group_buying_id
        2: i64 operator_id
    )

    // 获取拼团下的小组
    promotion_struct.PagingGroupBuyingTeam get_group_buying_teams(
        1: optional i64 skip,
        2: optional i64 limit
        3: optional i64 group_buying_id,
        4: optional bool is_available,
    )

    promotion_struct.PagingGroupBuyingTeam get_group_buying_teams_of_user (
        1: optional i64 skip,
        2: optional i64 limit
        3: optional i64 account_id
        4: required i64 region_id
    )

    // 获取拼团小组
    promotion_struct.GroupBuyingTeam get_group_buying_team(
        1: optional i64 group_team_id,
        2: optional string share_code,
        3: optional i64 account_id
        4: optional i64 sale_order_id
    )
    throws (
        1:exceptions.NotFoundException nfe
    )

    promotion_struct.GroupBuyingTeam get_team_by_gruop_team_member_id(
        1: i64 gruop_team_member_id
    )
    throws (
        1:exceptions.NotFoundException nfe
    )

    // 预下单后预创建一个team，做个标记先不展示，付款成功后才展示。
    promotion_struct.GroupBuyingTeam pre_create_group_buying_team(
        1: i64 group_buying_id, 2: i64 leader_account_id,
        3: i64 sale_order_id, 4: i64 sku_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    void update_group_buying_team(
        1: i64 group_buying_team_id,
        2: promotion_struct.GroupBuyingTeamState state
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    promotion_struct.GroupBuyingTeam join_group_buying_team(
        1: i64 group_team_id, 2: i64 account_id,
        3: i64 sale_order_id, 4: i64 sku_id, 5: optional bool is_robot
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    void update_group_buying_team_member(
        1: i64 sale_order_id,
        2: promotion_struct.GroupBuyingTeamMemberState state
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    // Group Buying Tag Management
    promotion_struct.GroupBuyingTag get_group_buying_tag(
        1: i64 tag_id) throws (1: exceptions.NotFoundException nfe),

    list<promotion_struct.GroupBuyingTag> get_group_buying_tags(
        1: i64 region_id),

    promotion_struct.GroupBuyingTag add_group_buying_tag(
        1: i64 region_id,
        2: i64 index,
        3: string name,
        4: list<i64> category_ids,
        5: i64 operator_id) throws (
            1: exceptions.InvalidOperationException ioe),

    promotion_struct.GroupBuyingTag update_group_buying_tag(
        1: i64 tag_id,
        2: i64 index,
        3: string name,
        4: list<i64> category_ids,
        5: i64 operator_id) throws (
            1: exceptions.InvalidOperationException ioe),

    void delete_group_buying_tag(
        1: i64 tag_id) throws (
            1: exceptions.NotFoundException nfe),

    # 拼团订单确认订单时检查团的状态是否完成
    bool check_group_buying_team_state_when_confirm_order (
        1: i64 sale_order_id
    )

    # 团购订单取消之前判断一下是否能够取消
    bool whether_can_cancel_the_group_buying_order(
        1: i64 sale_order_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    # 拼团订单取消订单后更新对应团员的状态
    bool update_group_member_state_after_order_canceled (
        1: i64 sale_order_id 
    )

    # 团购订单支付之前判断一下是否能够支付
    bool whether_can_paid_the_group_buying_order(
        1: i64 sale_order_id
    )

    bool whether_to_create_robot_order_of_team(
        1: i64 group_team_id
    )

    list<promotion_struct.GroupBuyingTeamMember> update_group_team_state_after_team_expired (
        1: i64 group_team_id
    )

    bool whether_can_start_a_team (
        1: i64 group_buying_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    bool whether_can_join_a_team (
        1: i64 group_team_id
        2: i64 account_id
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    promotion_struct.BigDiscountSale get_big_discount_sale_by_id(
        1: required i64 id
    )

    promotion_struct.PagingBigDiscountSale get_big_discount_sales (
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
        4: optional promotion_struct.BigDiscountSaleStatus status
        5: optional string apply_time_start
        6: optional string apply_time_end
        7: optional string apply_account_name
        8: optional string title
        9: optional string code
    )

    promotion_struct.PagingBigDiscountSale get_available_big_discount_sales(
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
    )

    void create_big_discount_sale (
        1: required i64 region_id
        2: required string title
        3: required string code
        4: required string tag
        5: required string tag_image
        6: required string start_at
        7: required string end_at
        8: required promotion_struct.Operator apply_account
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    void update_big_discount_sale_state (
        1: required i64 big_discount_sale_id
        2: required promotion_struct.BigDiscountSaleState state
        3: optional promotion_struct.Operator audit_account,
    )

    promotion_struct.PagingBigDiscountSaleProduct get_big_discount_sale_products (
        1: required i64 region_id
        2: optional i64 skip
        3: optional i64 limit
        4: optional i64 store_id
        5: optional string apply_time_start
        6: optional string apply_time_end
        7: optional string big_discount_sale_title
        8: optional string big_discount_sale_code
        9: optional i64 listing_id
        10: optional string listing_title
    )

    list<promotion_struct.BigDiscountSale> get_active_big_discount_sales(
        1: required i64 region_id
    )

    list<promotion_struct.BigDiscountSaleProductResult> bulk_create_big_discount_sale_products (
        1: required i64 region_id
        2: required i64 big_discount_sale_id
        3: required i64 store_id
        4: required list<promotion_struct.BigDiscountSaleProductApply> applys
    ) throws (
        1: exceptions.InvalidOperationException ioe
    )

    void update_big_discount_sale_product_state (
        1: required i64 big_discount_sale_product_id
        2: required promotion_struct.BigDiscountSaleProductState state
    )

    i64 get_big_discount_sale_product_count_of_store (
        1: required i64 store_id
        2: required i64 big_discount_sale_id
    )

    list<i64> get_listing_ids_of_big_discount_sale(
        1: required i64 big_discount_sale_id
        2: optional i64 store_id
    )

    i64 get_sku_count_of_listing_in_big_discount_sale(
        1: required i64 listing_id
        2: required i64 big_discount_sale_id
    )

    list<promotion_struct.BigDiscountSaleProduct> check_listings_in_active_big_discount_sale(
        1: required i64 region_id
        2: required list<i64> listing_ids
    )

    list<promotion_struct.BigDiscountSaleSku> get_active_big_discount_sale_sku_of_listing(
        1: required i64 region_id
        2: required i64 listing_id
    )

    list<promotion_struct.BigDiscountSaleSku> get_active_big_discount_sale_skus_by_sku_ids(
        1: required i64 region_id
        2: required list<i64> sku_ids
    )

    promotion_struct.PagingTopicPages get_topic_pages(
        1:optional i64 region_id,
        2:optional i16 skip,
        3:optional i16 limit,
        4:optional string title,
        5:optional string create_time_start,
        6:optional string create_time_end,
        7:optional string expire_time_start,
        8:optional string expire_time_end,
        9:optional i64 operator_id,
        10:optional i64 update_operator_id,
        11:optional promotion_struct.TopicPageStatus status),

    promotion_struct.TopicPage add_topic_page(
        1:i64 region_id,
        2:string code,
        3:string title,
        4:string description,
        5:string background_image,
        6:string background_color,
        7:string html_content,
        8:string expire_time,
        9:i64 operator_id) throws (
            1: exceptions.InvalidOperationException ioe),

    promotion_struct.TopicPage update_topic_page(
        1:i64 region_id,
        2:i64 topic_id,
        3:i64 operator_id,
        4:optional string code,
        5:optional string title,
        6:optional string description,
        7:optional string background_image,
        8:optional string background_color,
        9:optional string html_content,
        10:optional string expire_time) throws (
            1: exceptions.InvalidOperationException ioe,
            2: exceptions.NotFoundException nfe),

    promotion_struct.TopicPage get_topic_page(
        1:i64 region_id,
        2:optional i64 topic_id,
        3:optional string code,
        4:optional promotion_struct.TopicPageStatus status) throws (
            1: exceptions.NotFoundException nfe),

    void delete_topic_page(
        1:i64 region_id,
        2:i64 topic_id,
        3:i64 operator_id) throws (
            1: exceptions.NotFoundException nfe),

    void update_luck_draw_probability(
        1:required i64 region_id,
        2:required list<i64> probability
    )   
}