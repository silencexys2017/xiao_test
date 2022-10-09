include "exceptions.thrift"
include "auth_struct.thrift"

enum ContactType {
    PHONE = 1,
    EMAIL = 2,
    FB = 3,
    ACCOUNT = 4,
    KBZ = 5
}

struct Account {
    1: required i32 id,
    2: required string nick,
    3: optional bool enabled,
    4: optional bool authenticated,
    5: optional string timeCreated,
    6: optional bool isRobot
}

struct Contact {
    1: required i32 id,
    2: required i32 accountId,
    3: required i16 type, // 1.phone 2.email 3.facebook
    4: required i32 region,
    5: required string value,
    6: required bool verified,
    7: required bool credential,
    8: required string timeCreated,
    9: optional string timeVerified
}

struct Member {
    1: required i32 id,
    2: required i32 accountId,
    3: optional string avatar,
    4: optional string firstname,
    5: optional string lastname,
    6: optional i16 gender,
    7: optional string birthday,
    8: optional i32 growth
}

struct Token {
    1: required string refreshToken,
    2: required i32 refreshTokenTimeout,
    3: required string accessToken,
    4: required i32 accessTokenTimeout,
    5: optional i32 id,
    6: optional string nick,
    7: optional string phone,
    8: optional string timeCreated,
    9: optional string email,
    10: optional i16 contactType,
    11: optional string contactValue,
    12: optional bool isSetPwd
}

// 后台
struct AccountInfo {
    1: required i32 accountId,
    2: required string nick,
    3: required i16 regionId,
    4: required bool verified,
    5: required string timeCreated,
    6: required string phone,
    7: optional string email,
    8: optional string lastActiveTime,
    9: optional bool enabled,
    10: optional bool isRobot
}

struct TotalAccount {
    1: required i32 totalCount,
    2: required list<AccountInfo> accountInfos
}

struct PersonalInfo {
    1: required string nick,
    2: required i16 region,
    3: required string phone,
    4: optional string email,
    5: optional i64 accountId,
    6: optional bool verified,
    7: optional string timeCreated,
    8: optional string lastActiveTime,
    9: optional bool enabled,
    10: optional bool isRobot,
    11: optional string facebookAccount
}

struct FakeName {
    1: required i64 id,
    2: required string name
}

service AuthService {
    Account getAccountByToken(1:string accessToken) throws(1:exceptions.UnauthorizedException ue),
    Token refreshNewToken(1:string refreshToken) throws(1:exceptions.UnauthorizedException ue),
    Token getSession(
        1:string account_name,
        2:optional string password,
        3:optional i64 region_id
    ) throws(
        1:exceptions.InvalidOperationException ioe,
        2:exceptions.UnauthorizedException ue,
        3:exceptions.DatabaseException de
    ),
    Token create_account(
        1:i32 region_id,
        2:ContactType contact_type,
        3:string contact_value,
        4:string nick,
        5:optional bool validated,
        6:optional string password,
        7:optional string platform) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.InternalException ie,
            3:exceptions.DatabaseException de),
    Token generate_account(
        1:i32 region,
        2:string phone,
        3:string email,
        4:string nick,
        5:optional bool validated,
        6:optional string password
    ) throws(
        1:exceptions.InvalidOperationException ioe
    )

    Account init_account(
        1:i64 account_id,
        2:string init_password) throws(
            1:exceptions.NotFoundException nfe,
            2:exceptions.InvalidOperationException ioe),

    Account updateAccount(
        1:i64 accountId,
        2:optional string nick,
        3:optional bool enabled,
        4:optional string password) throws(1:exceptions.NotFoundException nfe),
    Token login_by_facebook(
        1:i32 regionId,
        2:string fbAccessToken,
        3:string fbUserId,
        4:optional string fbUserName,
        5:optional string phone,
        6:optional string platform) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.InternalException ie,
            3:exceptions.UnauthorizedException ue,
            4:exceptions.DatabaseException de),
    Token login_by_kbz(
        1:i32 region_id,
        2:string access_token,
        3:optional string phone,
        4:optional string platform) throws(
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.InternalException ie,
            3:exceptions.UnauthorizedException ue,
            4:exceptions.DatabaseException de),
    bool is_kbz_existed(1:i32 region_id, 2:string access_token),
    list<Contact> getContactList(1:i32 accountId, 2:optional i32 contactType),
    Contact get_account_contact(
        1:i64 account_id,
        2:i16 contact_type) throws(1:exceptions.NotFoundException nfe),
    Contact validateContact(1:i32 contactId, 2:bool verified) throws(1:exceptions.NotFoundException nfe),
    Contact updateContact(1:i32 regionId, 2:i64 accountId, 3:string value,
                          4:bool verified, 5:i16 contactType) throws(1:exceptions.InvalidOperationException ioe),
    bool isExistContact(1:i32 regionId, 2:string value, 3:i16 contactType),
    Contact bindFacebook(1:i32 regionId, 2:i64 accountId, 3:string fbAccessToken, 4:string fbUserId,
                         5:optional string fbUserName) throws(1:exceptions.InvalidOperationException ioe,
                                                              2:exceptions.InternalException ie,
                                                              3:exceptions.DatabaseException de),

    //后台
    TotalAccount getAccountList(
        1: optional i32 accountId, 2: optional string nick,
        3: optional string phone, 4: optional string email,
        5: optional i32 regionId, 6: optional string startTime,
        7: optional string endTime, 8: optional string sortField,
        9: optional i32 orderType, 10: optional i32 startIndex,
        11: optional i32 limit, 12: optional bool isRobot),

    list<i64> get_account_ids(
        1: optional i64 account_id, 2: optional string nick,
        3: optional list<string> phones, 4: optional string start_time,
        5: optional string end_time)throws(
        1:exceptions.NotFoundException nfe),

    PersonalInfo getAccountInfo(1:required i64 accountId) throws(
         1:exceptions.NotFoundException nfe),

    list<PersonalInfo> get_accounts_info(1:required list<i64> account_ids)
    throws(1:exceptions.NotFoundException nfe),

    Contact get_contact(
        1:required i64 region_id,
        2:required i64 account_id,
        3:required ContactType contact_type,
        4: optional bool is_verified,
        5: optional bool is_credential) throws(
            1:exceptions.NotFoundException nfe),

    list<FakeName> get_fake_name(1:required set<i64> member_ids),

    list<PersonalInfo> get_time_range_change_accounts(
        1: optional string start_time, 2: optional string end_time,
        3: optional i32 last_account_id),
}