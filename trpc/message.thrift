include "message_struct.thrift"
include "exceptions.thrift"
include "constants.thrift"

enum OrderOperate {
    so_create = 1,
    confirm = 2,
    shipped = 3,
    dispatched = 4,
    received = 5,
    bill_create = 6,
    so_cancel = -1,
    rejected = -2,
    bill_cancel = -3
}
struct FeedStatus {
    1: required string userOpenId,
    2: required i32 total,
    3: required i32 unreadTotal
}

struct DeliveryInfo {
    1: optional string messageId,
    2: optional string createdAt
}

struct Feed {
	1: required i64 id,
	2: required string sourceType,
	3: required i64 sourceId,
	4: required string title,
	5: required string linkType,
	6: required string linkValue,
	7: required i32 senderId,
	8: required bool hasRead,
	9: required string createdAt,
	10: optional i64 accountId,
	11: optional i16 status,
	12: optional string deliveryMethod,
	13: optional DeliveryInfo deliveryInfo,
	14: optional string deliveredAt,
	15: optional string readAt
}

struct Feeds {
    1: required string userOpenId,
    2: required i32 total,
    3: required list<Feed> feeds
}

struct OrderNotification {
    1: required i64 id,
    2: required string sourceType,
    3: required i64 sourceId,
    4: required i64 accountId,
    5: required bool hasRead,
    6: required i16 status,
    7: required string createdAt,
    8: optional string deliveredAt,
    9: optional string readAt,
    10: optional OrderOperate operate
}


service MessageService {
    OrderNotification change_order_notification(
        1: i64 accountId,
        2: i64 sourceId,
        3: i16 status,
        4: optional string code
    ) throws (
        1:exceptions.InvalidOperationException ioe
    ),

    FeedStatus get_message_feed_status(1: i64 accountId) throws (
        1:exceptions.NotFoundException nfe
    ),

    Feeds get_message_feeds (
        1: i64 accountId,
        2: i64 lastId,
        3: i16 limit
    ) throws (
        1:exceptions.NotFoundException nfe
    ),

    Feed patch_feed_status(
        1: i64 feedId
    ) throws (
        1:exceptions.NotFoundException nfe
    ),


    void patch_feeds_all_read(
        1: i64 acconutId
    )

    message_struct.TalkMsg add_talk_msg(
        1:i64 region_id,
        2:message_struct.TalkType talk_type,
        3:message_struct.MemberType member_type,
        4:i64 member_id,
        5:message_struct.MsgType talk_msg_type,
        6:message_struct.TalkMsgContent content,
        7:optional i64 talk_id,
        8:optional i64 store_id,
        9:optional message_struct.MsgStatus status,
        10:optional message_struct.MemberType to_member_type,
        11:optional i64 to_member_id,
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InvalidOperationException ioe
    ),

    message_struct.Talk get_talk(
        1:optional i64 talk_id,
        2:optional message_struct.TalkType talk_type,
        3:optional i16 member_type,
        4:optional i64 member_id,
        5:optional i64 store_id,
        6:optional i64 region_id
    ) throws (
        1:exceptions.NotFoundException nfe
    ),

    message_struct.Talk get_last_unread_talk(
        1:optional i64 store_id,
        2:optional message_struct.MemberType member_type,
        3:optional string last_query_time
    ) throws (
        1:exceptions.NotFoundException nfe
    ),

    list<message_struct.TalkMsg> get_talk_msgs(
        1:i64 talk_id,
        2:optional i16 talk_type,
        3:optional i16 member_type,
        4:optional i64 member_id,
        5:optional i64 store_id,
        6:optional i16 limit,
        7:optional string max_create_time,
        8:optional i64 max_id,
        9:optional string min_create_time,
        10:optional i64 min_id
    ) throws (
        1:exceptions.NotFoundException nfe
    ),

    void upsert_message(
        1:i64 region_id,
        2:i16 message_type,
        3:i64 source_id,
        4:optional i64 account_id,
        5:optional string avatar,
        6:optional string title,
        7:optional string describe,
        8:optional i16 unread,
        9:optional i16 inc_unread,
        10:optional message_struct.MessageContent content,
        11:optional bool upsert
    ) throws (
        1:exceptions.NotFoundException nfe,
        2:exceptions.InvalidOperationException ioe
    ),

    message_struct.PagingMessages get_messages(
        1:optional i16 skip,
        2:optional i16 limit,
        3:optional i64 region_id,
        4:optional i64 account_id,
        5:optional bool is_excluding_sys_msg,
    ),

    message_struct.PagingTalk get_talks(
        1:optional i16 skip,
        2:optional i16 limit,
        3:optional i64 region_id,
        4:optional list<i64> store_id,
        5:optional i16 member_type,
        6:optional i64 member_id,
        7:optional string min_last_time,
        8:optional string max_last_time,
        9:optional list<i16> talk_types),

    i32 get_messages_unread(
        1:required i64 account_id,
        2:optional i64 region_id),

    message_struct.PagingSysMessage get_sys_messages(
        1:optional i64 region_id,
        2:optional bool is_app_push,
        3:optional bool is_display_on_sku,
        4:optional string create_time_start,
        5:optional string create_time_end,
        6:optional i16 skip,
        7:optional i16 limit),

    message_struct.SysMessage add_sys_message(
        1:i64 region_id,
        2:message_struct.SysMsgType sys_msg_type,
        3:string title,
        4:string content,
        5:bool is_app_push,
        6:bool is_display_on_sku,
        7:optional string display_time_start,
        8:optional string display_time_end
    ) throws (1:exceptions.InternalException ie),

    void delete_sys_message(1:i64 sys_msg_id) throws (
        1:exceptions.NotFoundException ne),

    message_struct.SysMessageWrap get_sku_sys_message(
        1:i64 region_id),

    i32 get_talk_count(
        1: optional i32 store_id, 2: optional i16 talk_type,
        3: optional i16 member_type, 4:optional i64 region_id)

    void bind_device(1:string token, 2:optional i64 account_id,
        3:optional string platform, 4:optional i32 region_id),

    void unbind_device(1:string token),

    void push_account_notify(1:i64 account_id, 2:string title, 3:string body,
        4:message_struct.NotifyData data),

    void bind_composite_device(
        1:i32 region_id, 2:string platform, 3:string token,
        4:message_struct.MemberType member_type,
        5:i64 member_id),

    void unbind_composite_device(1:string token),

    void push_composite_notify(
        1:message_struct.MemberType member_type, 2:i64 member_id,
        3:string title, 4:string body, 5:message_struct.NotifyData data)

    message_struct.PagingMessages get_sys_messages_for_application(
        1:required i16 skip,
        2:required i16 limit,
        3:required i64 region_id
        4:required i64 account_id
    )

    void read_system_message_for_account (
        1:required i64 region_id,
        2:required i64 system_message_id,
        3:required i64 account_id
    )

    void read_all_system_message_for_account(
        1:required i64 region_id,
        2:required i64 account_id
    )
    
    void create_seller_feed(
        1: required i64 region_id,
        2: required i64 store_id,
        3: required message_struct.SellerFeedType type,
        4: required message_struct.SellerFeedLinkType link_type,
        5: required string link_value,
        6: required string title
    )

    message_struct.PagingSellerFeeds get_seller_feeds(
        1: optional i64 region_id,
        2: optional i64 skip,
        3: optional i64 limit,
        4: optional i64 store_id,
        5: optional bool is_cleared
    )

    void read_seller_feed(
        1: required i64 seller_feed_id
    )

    void clear_seller_feeds(
        1: optional i64 region_id,
        2: required i64 store_id
    )

    i64 get_seller_feed_unread_count(
        1: optional i64 region_id
        2: required i64 store_id
    )
}
