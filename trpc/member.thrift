include "exceptions.thrift"
include "constants.thrift"
include "member_struct.thrift"

struct Address {
	1: required i64 id,
	2: required i64 accountId,
	3: required i32 regionId,
	4: required string name,
	5: required i32 cityId,
	6: required string city,
	7: required i32 areaId,
	8: required string area,
	9: required string address1,
	10: required string address2,
	11: required string phone,
	12: required bool verified,
	13: required bool isDefault,
	14: optional bool deleted,
	15: required i32 stateId,
	16: required string state,
	17: optional bool isDraw,
	18: optional string postcode,
	19: optional bool isSelected
}


struct Profile {
    1: required i64 id,
    2: required i64 accountId,
    3: required i16 gender,
    4: required i16 age,
    5: required string email,
    6: required string avatar,
    7: required string favorite,
    8: required string inviteCode
}

struct Wish {
    1: required i64 id,
    2: required i32 regionId,
    3: required i64 accountId,
    4: required i64 listingId,
    5: optional bool deleted,
    6: optional string timeCreated,
    7: optional string tempUserKey
}

struct History {
    1: required i64 id,
    2: required i32 regionId,
    3: required i64 accountId,
    4: required i64 listingId,
    5: optional bool deleted,
    6: optional string timeCreated
}

struct Balance {
    3: required i64 balance,
    4: required i64 historyTotal,
    5: required i64 locked
}

struct AccountRewardNode {
    1: required i64 index,
    2: required string name,
    3: required i64 amount,
    4: required string code,
    5: required bool earned
}

struct RewardNode {
    1: required i64 id,
    2: required i64 index,
    3: required string name,
    4: required i64 amount,
    5: required string code,
    6: required i32 canRep,
    7: required string repType,
    8: required string optType,
    9: required string updateTime
}

struct BalanceChangeLog {
    1: required i64 id,
    2: required string name,
    3: required i64 amount,
    4: optional string timeCreated
}

struct SetMemberParameter{
    1: required i64 id,
    2: required string value,
}

struct MemberParameter{
    1: required i64 id,
    2: required i32 regionId,
    3: required string name,
    4: required string value,
    5: required string dataType,
    6: required string paramModule
}

struct Redeem{
    1: required bool enable,
    2: required i32 useCoin,
    3: required i32 deductAmount,
    4: required i32 minUseCoin,
    5: required i32 maxUseCoin,
    6: required i32 availableBalance,
}

struct ContributeRefer{
    1: string type
    2: i64 contributorId
    3: string contributorRole
    4: string referCode
    5: i64 accountId
    6: string platform
    7: optional string source
    8: optional i64 sourceId
    9: optional i64 orderId
    10: optional i64 skuId
}

struct ContributeReferAccount{
    1: i64 accountId
    2: string referCode
}

struct InviteConvert{
    1: string inviteCode
    2: string accountId
    3: i64 validAmount
}

struct ArticleConvert{
    1: string authorCode
    2: string accountId
    3: i64 validAmount
    4: string articleId
    5: string skuId
}

struct ShareConvert{
    1: string referCode
    2: string accountId
    3: i64 validAmount
    4: string sourceType
    5: string sourceId
    6: string skuId
}

struct SaleOrderConvert{
     1: string orderId
     2: string orderCode
     3: i64 storeId
     4: string storeName
     5: i64 payAmount
     6: i32 postage
     7: optional list<ShareConvert> shareConverts
     8: optional list<ArticleConvert> articleConverts
     9: optional InviteConvert inviteConvert
}

struct SaleOrderPlatform{
    1: i64 platform,
    2: list<i64> orderIds
}

struct InviterInfo{
    1: i64 inviterId
    2: string inviteCode
}

service MemberService {
    Address addAddress(1:i64 accountId, 2:i32 regionId, 3:string name, 4:i32 stateId, 5:string stateName,
                       6:i32 cityId, 7:string cityName, 8:i32 areaId, 9:string areaName, 10:string address1,
                       11:string phone, 12:bool verified, 13:bool isDefault, 14:optional string address2,
                       15:optional bool isDraw, 16: optional string postcode
                       ) throws ( 1:exceptions.InternalException ne),

    Address update_address(
        1:i64 account_id, 2:i32 region_id, 3: i64 address_id, 4:string name, 5:i32 state_id,
        6:string state_name, 7:i32 city_id, 8:string city_name, 9:i32 area_id, 10:string area_name,
        11:string address1, 12:string phone, 13:bool verified, 14:bool is_default,
        15:optional string address2, 16:optional bool is_draw, 17: optional string postcode)
        throws (1:exceptions.InternalException ne, 2: exceptions.NotFoundException nfe),

    Profile updateProfile(1: required i64 accountId,  2: optional i16 gender, 3: optional i16 age,
                       4: optional string email, 5: optional string avatar, 6: optional string favorite),
    Profile getProfile(1:i64 accountId),
    list<Profile> getProfileListByIds(1:list<i64> accountIds),
    Address getAddress(
        1:i32 addressId,
        2:optional bool deleted,
        3:optional i64 accountId) throws (1:exceptions.NotFoundException ne),
    void deleteAddress(1:i64 accountId, 2:i32 addressId) throws (1:exceptions.NotFoundException ne),
    list<Address> getAddressList(1:i64 accountId, 2: optional i32 regionId),
    Address getDefaultAddress(1:i64 accountId, 2:i32 regionId) throws (1:exceptions.NotFoundException ne),
    Address get_anyone_address(1:i64 account_id, 2:i32 region_id) throws (1:exceptions.NotFoundException ne),
    bool changeToDefault(1:i64 accountId, 2:i32 regionId, 3:i32 addressId) throws (1:exceptions.NotFoundException ne),
    bool change_to_select(1:i64 account_id, 2:i32 region_id, 3:i32 address_id) throws (1:exceptions.NotFoundException ne),
    void addWishListings(1:i32 regionId, 2:i64 accountId, 3:i64 listingId) throws(1:exceptions.DatabaseException de),
    void deleteWishListings(1:i32 regionId, 2:i64 accountId, 3:i64 listingId) throws(1:exceptions.DatabaseException de),
    Address get_shipping_address(1:i64 account_id, 2:i32 region_id, 3: optional i32 address_id) throws (1:exceptions.NotFoundException ne),

    void add_temp_wish(
        1:i32 region_id,
        2:string temp_user_key,
        3:i64 listing_id),

    void delete_temp_wish(
        1:i32 region_id,
        2:string temp_user_key,
        3:i64 listing_id),

    bool is_exist_temp_wish(
        1:i32 region_id,
        2:string temp_user_key,
        3:i64 listing_id),

    void change_to_formal_wishes(
        1:string temp_user_key,
        2:i64 account_id)

    list<Wish> getWishListings(
        1:i32 regionId,
        2:i64 accountId,
        3:optional i64 lastId,
        4:optional i32 limit,
        5:optional list<i64> listing_ids) throws(
            1:exceptions.DatabaseException de),

    list<Wish> get_temp_wish_list(
        1:i32 region_id,
        2:string temp_user_key,
        3:optional i64 last_id,
        4:optional i32 limit,
        5:optional list<i64> listing_ids),

    bool isExistWish(1:i32 regionId, 2:i64 accountId, 3:i64 listingId) throws(1:exceptions.DatabaseException de),
    void addHistory(1:i32 regionId, 2:i64 accountId, 3:i64 listingId) throws(1:exceptions.DatabaseException de),
    void deleteAllHistory(1:i32 regionId, 2:i64 accountId) throws(1:exceptions.DatabaseException de),
    list<History> getHistory(1:i32 regionId, 2:i64 accountId, 3:i64 lastId, 4:i32 limit) throws(1:exceptions.DatabaseException de),

    i64 add_reward(
        1:i32 region_id,
        2:i64 account_id,
        3:string node_code,
        4:optional string from_source,
        5:optional i64 source_id,
        6:optional i64 origin_amount,
        7:optional i64 locked) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.DatabaseException de),
    void init_invite_log(
        1:i32 region_id,
        2:i64 account_id) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.DatabaseException de),
    void update_invite_log_code(
        1:i32 region_id,
        2:i64 account_id,
        3:string invite_code) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.DatabaseException de),
    void update_invite_log_verified(1:i32 region_id, 2:i64 account_id),
    void update_invite_log_email_verified(1:i32 region_id, 2:i64 account_id),
    list<AccountRewardNode> get_account_reward_nodes(
        1:i32 region_id,
        2:i64 account_id),
    list<RewardNode> get_reward_nodes(1:i32 region_id),
    RewardNode update_reward_node(
        1:i64 node_id,
        2:optional i64 amount,
        3:optional string name,
        4:optional i32 status) throws(
            1:exceptions.InvalidOperationException ioe),
    list<BalanceChangeLog> get_balance_change_log(
        1:i32 region_id,
        2:i64 account_id,
        3:optional i64 last_id,
        4:optional i32 limit),
    Balance get_balance(1:i32 region_id, 2:i64 account_id),
    bool has_earned_reward(
        1:i32 region_id,
        2:i64 account_id,
        3:string node_code),
    i64 add_spend(
        1:i32 region_id,
        2:i64 account_id,
        3:string spend_name,
        4:string spend_code,
        5:string from_source,
        6:i64 source_id,
        7:i64 spend_amount,
        8:optional bool is_opt_lock) throws(
            1:exceptions.InvalidOperationException ioe),
    i64 refund_spend(
        1:i32 region_id,
        2:i64 account_id,
        3:string spend_name,
        4:string spend_code,
        5:string from_source,
        6:i64 source_id,
        7:i64 refund_amount,
        8:optional bool is_opt_lock) throws(
            1:exceptions.InvalidOperationException ioe),
    i64 platform_reward(
        1:i32 region_id,
        2:i64 account_id,
        3:i64 amount,
        4:string name,
        5:optional string code,
        6:optional string from_source,
        7:optional i64 source_id),

    Redeem get_place_order_redeem(
        1:i32 region_id,
        2:i64 account_id,
        3:i32 amount,
        4:optional bool is_redeem_all,
        5:optional i32 limit_coins) throws(
            1:exceptions.InvalidOperationException ioe),
    list<MemberParameter> getParameterList(1:i32 regionId, 2:string paramModule),
    #MemberParameter setParameter(1:i32 regionId, 2:string name, 3:string value, 4:optional string paramModule),
    MemberParameter getParameter(1:i32 regionId, 2:string paramModule, 3:string name),
    void setParameters(1:list<SetMemberParameter> parameters),

    member_struct.PagingVoucherTemplate get_voucher_templates(
        1:i32 region_id, 2:optional bool enable, 3:optional i32 skip,
        4:optional i32 limit, 5:optional list<i64> ids,
        6:optional i32 owner_type),
    member_struct.VoucherTemplate update_voucher_template(
        1:i64 temp_id,
        2:optional bool enable),

    member_struct.PagingVoucherGen get_voucher_gens(
        1:i32 region_id,
        2:optional list<i32> status,
        3:optional string create_start_date,
        4:optional string create_end_date,
        5:optional i32 skip,
        6:optional i32 limit,
        7:optional list<i64> ids,
        8:optional list<i32> gen_types,
        9:optional i32 owner_type,
        10:optional i64 store_id,
        11:optional list<i64> voucher_types),

    member_struct.VoucherGen get_voucher_gen(
        1:i64 gen_id) throws(1:exceptions.NotFoundException ne),

    list<member_struct.VoucherGen> get_valid_voucher_gens(
        1:i32 region_id,
        2:optional i64 account_id,
        3:optional i64 last_id,
        4:optional i32 limit,
        5:optional i32 owner_type,
        6:optional i64 store_id,
        7:optional list<i64> gen_ids),
    member_struct.VoucherGen update_voucher_gen(
        1:i64 gen_id,
        2:optional i64 operator_id,
        3:optional i32 status) throws(1:exceptions.NotFoundException ne),
    member_struct.VoucherGen create_voucher_gen(
        1:i64 template_id,
        2:string name,
        3:i32 limit_bill_amount,
        4:i32 amount,
        5:i32 limit_type,
        6:i32 number,
        7:i32 prebuilt_num,
        8:string start_date,
        9:string end_date,
        10:i32 expired_days,
        11:i64 operator_id,
        12:i64 gen_type,
        13:optional list<i64> limit_ids,
        14:optional list<i64> store_ids) throws(
            1:exceptions.NotFoundException ne,
            2:exceptions.InvalidOperationException ioe),


    list<member_struct.ValidVoucher> get_valid_vouchers(
        1:i32 region_id, 2:i64 account_id, 3:optional i64 last_id,
        4:optional i32 limit, 5:optional list<member_struct.Item> items),
    member_struct.ValidVoucher get_valid_voucher(
        1:i64 account_id,
        2:i64 voucher_id,
        3:optional list<member_struct.Item> items) throws(1:exceptions.InvalidOperationException ioe,
                                                          2:exceptions.NotFoundException ne),
    member_struct.Voucher update_voucher_status(1:i64 voucher_id, 2:i64 operator_id, 3:i32 status),
    void refund_voucher(
        1:i64 voucher_id,
        2:i64 account_id,
        3:optional i64 operator_id) throws(1:exceptions.InvalidOperationException ioe,
                                           2:exceptions.NotFoundException ne),
    member_struct.Voucher receive_voucher(
        1:i64 account_id,
        2:i64 voucher_gen_id) throws(1:exceptions.InvalidOperationException ioe,
                                     2:exceptions.NotFoundException ne),
    member_struct.Voucher use_voucher(
        1:i64 voucher_id,
        2:i64 account_id,
        3:i64 pay_bill_id) throws(1:exceptions.InvalidOperationException ioe,
                                  2:exceptions.NotFoundException ne),

    member_struct.PagingVoucher get_vouchers(
        1:i32 region_id,
        2:optional list<i64> account_ids,
        3:optional list<i64> pay_bill_ids,
        4:optional list<i32> get_type,
        5:optional list<i32> status,
        6:optional string code,
        7:optional string create_start_date,
        8:optional string create_end_date,
        9:optional string get_start_date,
        10:optional string get_end_date,
        11:optional string expired_start_date,
        12:optional string expired_end_date,
        13:optional i32 skip,
        14:optional i32 limit,
        15:optional i32 owner_type,
        16:optional i64 store_id,
        17:optional list<i64> voucher_ids),

    member_struct.ReceivableVouchers get_receivable_vouchers(
        1:i32 region_id,
        2:list<member_struct.Item> items,
        3:optional i64 account_id),

    list<member_struct.ItemMapGens> map_item_gens(
        1:i32 region_id,
        2:list<member_struct.Item> items,
        3:optional i64 not_gen_id,
        4:optional i16 limit),

    oneway void batch_distribute_voucher(
        1:i64 dis_id, 2:list<i64> account_ids)
        throws(1:exceptions.InvalidOperationException ioe,
               2:exceptions.NotFoundException ne),
    oneway void auto_distribute_voucher(
        1:i32 region_id,
        2:i64 account_id,
        3:optional string invite_code)
        throws(1:exceptions.InvalidOperationException ioe,
               2:exceptions.NotFoundException ne),
    member_struct.Voucher single_distribute_voucher(
        1:i64 dis_id,
        2:i64 account_id) throws(1:exceptions.InvalidOperationException ioe,
                                 2:exceptions.NotFoundException ne),
    member_struct.PagingDistribute get_distributes(
        1:i32 region_id,
        2:optional list<i32> status,
        3:optional string create_start_date,
        4:optional string create_end_date,
        5:optional i32 skip,
        6:optional i32 limit,
        7:optional list<i32> types),
    member_struct.Distribute update_distribute(
        1:i64 dis_id,
        2:optional i64 operator_id,
        3:optional i32 status) throws(1:exceptions.NotFoundException ne,
                                      2:exceptions.InvalidOperationException ioe),
    member_struct.Distribute create_distribute(
        1: i64 gen_id,
        2: member_struct.Rule rule,
        3: member_struct.Reason reason,
        4: i32 dis_type,
        5: i64 operator_id) throws(1:exceptions.NotFoundException ne,
                                   2:exceptions.InvalidOperationException ioe),
    list<i64> get_account_ids(1:optional list<string> invite_codes),
    void add_store_follow(
        1:i64 account_id,
        2:i64 store_id) throws(1:exceptions.InvalidOperationException ioe),
    void delete_store_follow(
        1:i64 account_id,
        2:i64 store_id) throws(1:exceptions.InvalidOperationException ioe),
    bool is_followed_store(1:i64 account_id, 2:i64 store_id),
    list<i64> get_followed_store_ids(
        1:i64 account_id,
        2:optional i32 skip,
        3:optional i32 limit),

    list<member_struct.FollowedStore> get_followed_stores(
        1: i32 account_id,
        2:optional i32 skip,
        3:optional i32 limit),

    # 后台
    list<i64> getAddressIdsByPhone(1: string phone),

    list<Address> get_addresses(
        1: list<i64> address_ids, 2:optional bool deleted) throws (
        1:exceptions.NotFoundException ne),

    bool exists_draw_address(
        1: i64 account_id,
        2: i32 region_id
    ),

    Address get_draw_address(
        1: i64 account_id,
        2: i32 region_id
    ) throws (
        1:exceptions.NotFoundException ne
    ),

    void set_draw_address(
        1: i64 address_id,
        2: i64 account_id,
        3: i32 region_id
    ) throws (
        1:exceptions.InternalException ne
    ),

    member_struct.ReferralCode get_referral_code(
        1:string invite_code) throws(1:exceptions.NotFoundException ne),

    list<member_struct.ReferralCode> get_referral_code_list(
        1:list<i64> account_ids),

    list<member_struct.InviteLog> get_invite_log_list(
        1:list<i64> account_ids)

    void record_contribute_refers(
        1: list<ContributeRefer> contribute_refers
    )

    list<ContributeReferAccount> get_account_ids_by_refer_codes(
        1: list<string> refer_codes
    )

    string get_refer_code_by_account_id(
        1: i64 account_id
    )

    string generate_refer_code(
        1: i64 account_id
        2: string source
        3: optional string phone
        4: optional string email
        5: optional i64 external_account_id
        6: optional i64 region_id
    ) throws (
        1:exceptions.InvalidOperationException ioe
    )

    void create_invited_user(
        1: i64 account_id
        2: string used_invite_code
        3: string nick
        4: string phone
        5: string email
        6: i64 region_id
        7: bool is_verified
        8: optional string verify_time
    )

    void update_invited_user_last_active_time(
        1: i64 account_id
    )

    void update_invited_user_verify(
        1: i64 account_id
        2: bool is_verified
        3: optional string verify_time
    )

    bool is_invited_by_actor(
        1: i64 account_id
        2: optional string time_start
        3: optional string time_end
    )

    void create_order_convert(
        1: string account_id
        2: i64 order_type
        3: i64 region_id
        4: string phone
        5: string nick
        6: list<SaleOrderConvert> so_converts
    )

    InviterInfo get_inviter_info(
        1: i64 account_id
    )

    string get_promoter_source(
        1: string refer_code
    )

    bool is_star_promoter(1:i64 account_id)

    member_struct.Voucher receive_compensatory_voucher(
        1:i64 account_id,
        2:i64 voucher_gen_id
    )throws(
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.NotFoundException ne
    )
}