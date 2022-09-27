const i16 MEMBER_TYPE_STORE = 1
const i16 MEMBER_TYPE_CUSTOMER = 2
const i16 MEMBER_TYPE_ACCOUNT = 3
const i16 MEMBER_TYPE_SYS_NOTIFY = 4
const i16 MESSAGE_TYPE_STORE_TALK = 1
const i16 MESSAGE_TYPE_ORDER_NOTIFY = 2
const i16 MESSAGE_TYPE_SYS_MSG = 3
const i16 MESSAGE_TYPE_CUSTOMER_TALK = 5
const i16 TALK_TYPE_SOTRE = 1
const i16 TALK_TYPE_CUSTOMER = 2
const string APP_ACTION_TALK = "talking"

# 系统消息类型: 1:纯文本、2:H5链接、3:APP内部界面:
enum SysMsgType {
    TEXT = 1
    H5 = 2
    APP_VIEW = 3
}
# 聊天类型：1: store talk; 2: platform customer service talk
enum TalkType {
    STORE = 1
    PLAT_CUSTOMER_SERVICE = 2
}
# 聊天成员类型：1: store admin id; 2: platform customer service id; 3: account id; 4:system notify
enum MemberType {
    STORE_ADMIN = 1
    PLAT_CUSTOMER_SERVICE = 2
    ACCOUNT_ID = 3
    SYS_NOTIFY = 4
}
# 聊天内容类型：1.text；2.image；3.order info；4.sku info, 5.notify 6.order confirm; 7.order terminal
enum MsgType {
    TEXT = 1
    IMAGE = 2
    ORDER_INFO = 3
    SKU_INFO = 4
    SYS_NOTIFY = 5
    ORDER_CONFIRM = 6
    ORDER_TERMINAL = 7
    AFTER_SALE = 8
}
# 聊天内容状态： -1. deleted；1.unread；2.read；
enum MsgStatus {
    DELETED = -1
    UNREAD = 1
    READ = 2
}
# 推送通知消息Link类型： 2. H5链接跳转；3.纯文本；9.跳转至APP视图；
enum LinkType {
    H5 = 2
    TEXT = 3
    APP_VIEW = 9
}

enum SellerFeedType {
    ORDER = 1
    AFTER_SALE = 2
}

enum SellerFeedLinkType {
    SALE_ORDER = 1
    BILL = 2
    SHIP_PACKAGE = 3
    AFTER_SALE = 4
}

struct Member{
    1: required MemberType memberType,
    2: required i64 memberId,
    3: optional i64 unread,
}

struct MessageContent {
    1: optional i64 talkId,
    2: optional i16 linkType, # 1.text; 2.url；3.android
    3: optional string linkValue,
//    4: optional string imageUrl
//    2: optional i64 storeId,
//    5: optional string image
}


struct TalkMsgContent {
    1: optional string text,
    2: optional string image,
    3: optional i64 saleOrderId,
    4: optional i64 skuId,
    5: optional i64 shipOrderId,
    6: optional string title,
    7: optional string describe,
    8: optional string imageUrl,
    9: optional i64 listingId
    10: optional i64 afterSaleId
    # image
}


struct Message {
    1: required i64 id,
    2: required i64 regionId,
    3: required i16 type,  #1.store talk; 2.order notify; 3.msg; 4.promotion; 5.platform customer service talk
    4: required i64 sourceId, # talk id(type=1);
    5: required i64 accountId,
    6: required string avatarUrl,
    7: required string title,
    8: required string describe,
    9: required i16 unreadCount,
    10: required string lastTime,
    11: required string createAt,
    12: optional MessageContent content,
    13: optional bool hasRead
//    9: optional i64 readTime,
//    6: required i16 status, # -1.deleted; 1.unread; 2.read;
//    10: optional string avatar,
    # accountId
}

struct TalkMsg {
    1: required i64 id,
    2: required i64 talkId,
    3: required TalkType talkType,
    4: required MemberType memberType,
    5: required i64 memberId,
    6: required MsgType msgType, # 1.text；2.image；3.order info；4.sku info; 5.notify; 6.order confirm; 7.order terminal
    7: required MsgStatus status,
    8: required string createAt,
    9: optional TalkMsgContent content,
    11: optional i64 storeId,
    12: optional string readTime,
//    6: optional string avatarUrl,
//    3: optional string nick,
    # avatar
}

struct Talk {
    1: required i64 id,
    2: required i64 regionId,
    3: required i16 talkType, # 1: store talk; 2: platform customer service talk
    4: required list<Member> members,
    5: required string createAt,
    6: optional i64 storeId,
    7: optional string lastTime,
    8: optional i64 lastAccountId,
    9: optional i64 lastStaffId,
    10: optional string lastContent,
    11: optional i16 lastMemberType
}

struct PagingMessages {
    1: required i32 total,
    2: required list<Message> data
}

struct PagingTalk {
    1: required i32 total,
    2: required list<Talk> data
}

struct SysMessage {
    1: required i64 id,
    2: required i64 regionId,
    3: required SysMsgType type,
    4: required string title,
    5: required string content,
    6: required bool isAppPush,
    7: required bool isDisplayOnSku,
    8: required string createTime,
    9: optional string displayTimeStart,
    10: optional string displayTimeEnd
}

struct PagingSysMessage {
    1: required i32 total,
    2: required list<SysMessage> data
}

struct SysMessageWrap {
    1: optional SysMessage obj
}

struct ActionParam{
    1:string name,
    2:string value,
}

struct NotifyAction{
    1: string action_name,
    2: optional list<ActionParam> params
}

struct NotifyData{
    1:LinkType link_type,
    2:optional string link_value="",
    3:optional NotifyAction action
}

struct SellerFeed{
    1:required i64 id
    2:required i64 regionId
    3:required i64 senderId
    4:required i64 storeId
    5:required SellerFeedType type
    6:required SellerFeedLinkType linkType
    7:required string linkValue
    8:required string title
    9:required bool hasRead
    10:required bool isCleared
    11:required string createdAt
}

struct PagingSellerFeeds {
    1: required i64 total,
    2: required list<SellerFeed> sellerFeeds
}
