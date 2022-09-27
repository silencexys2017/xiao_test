const string MODULE_SHORTCUT = "app_shortcut"
const string MODULE_SHORTCUT_LINK = "app_shortcut_link"
const string MODULE_SHORTCUT_WAP_LINK = "wap_shortcut_link"
const string MODULE_SHORTCUT_CONFIG = "shortcut_config"

const string MSG_APP_KEY_CUSTOMER = "Customer"
const string MSG_APP_KEY_SELLER = "Seller"

# Email验证码类型: 2:验证邮箱、2:注册Email账号
enum VerifyCodeType {
    LOGIN = 1,
    VERIFY = 2,
    REGISTER = 3
}

struct ActionLog {
    1: optional i64 aid,
    2: optional string sid,
    3: optional string userId,
    4: optional string anonSid,
    5: optional i32 regionId,
    6: optional string countryCode,
    7: optional string countryName,
    8: optional string language,
    9: optional i16 isUseWifi,
    10: optional string ip,
    11: optional string recommendId,
    12: optional string recommendInfo,
    13: optional string actionName,
    14: optional string params,
    15: optional i64 createAt
}

struct SessionLog {
    1: optional string sid,
    2: optional i64 createAt,
    3: optional string packageName,
    4: optional i32 appVer,
    5: optional string appVerName,
    6: optional string romVer,
    7: optional string deviceModel,
    8: optional string deviceId,
    9: optional string deviceName,
    10: optional string deviceBrand,
    11: optional string deviceMaker,
    12: optional string sdkVer,
    13: optional string sdkName,
    14: optional string os,
    15: optional string osVer,
    16: optional string osLanguage,
    17: optional i16 platform,
    18: optional string screenHeight,
    19: optional string screenWidth
}

enum UserAddressInteractionMethod {
    COMMON = 1,
    POSTCODE = 2
}

const list<i16> ADDRESS_METHOD = [1, 2]

struct Region {
    1: required i32 id,
    2: required string code,
    3: required string name,
    4: required string intro,
    5: required string flag,
    6: required i32 currencyId,
    7: required string currencySymbol,
    8: required i32 currencyConversion,
    9: required string language,
    10: required string timeZone,
    11: required string callingCode,
    12: required string currency,
    13: required i32 index,
    14: optional UserAddressInteractionMethod addressMethod
}

struct State {
    1: required i32 id,
    2: required i32 regionId,
    3: required string name,
    4: required i32 index,
    5: optional i32 minAppVersion
}

struct City {
    1: required i32 id,
    2: required i32 regionId,
    3: required i32 stateId,
    4: required string name,
    5: required i32 index,
    6: optional i32 minAppVersion
}

struct Area {
    1: required i32 id,
    2: required i32 regionId,
    3: required i32 stateId,
    4: required i32 cityId,
    5: required string name,
    6: required i32 index,
    7: required bool supportCod,
    8: required i32 postage,
    9: optional i32 minAppVersion,
    10: optional i16 ett,
    11: optional string postcode
}

struct SetParameter{
    1: required string name,
    2: required string value,
    3: required string paramModule,
    4: required i32 regionId,
    5: optional i32 index,
    6: optional string description
}

struct Parameter{
    1: required i64 id,
    2: required i32 regionId,
    3: required string name,
    4: required string value,
    5: required string dataType,
    6: required string paramModule,
    7: optional i32 index,
    8: optional string description,
    9: optional string icon
}

struct Special {
    1: required string title,
    2: required list<i64> listingIds,
    3: optional i64 id,
    4: optional string code,
    5: optional string createAt,
    6: optional i64 creatorId,
    7: optional bool isDeleted
    8: optional i32 regionId,
}

struct PagingSpecial{
    1: required i32 total,
    2: required list<Special> data
}

struct Address {
    1: i32 areaId,
    2: string areaName,
    3: i32 cityId,
    4: string cityName,
    5: optional i32 stateId,
    6: optional string stateName,
    7: optional i16 regionId,
    8: optional string regionName,
    9: optional i32 postage
}

struct EnvRegistration {
    1:optional list<i16> registerMethods=[1, 2],
    2:optional i16 defaultMethod=1,
    3:optional bool enableWelcomeMail=false,
    4:optional string mailSender="",
    5:optional string mailSenderPwd="",
    6:optional string mailSenderName="",
    7:optional string mailServerHost="",
    8:optional i16 mailServerPort,
    9:optional bool enableFacebook=true
}

struct EnvStar {
    1:optional bool isWapIntegration=true,
    2:optional bool isAppIntegration=true,
    3:optional string channelName=""
}

struct ViewSwitch {
    1:optional bool enable,
    2:optional i16 index,
    3:optional bool readonly
}


struct EnvHomepage {
    1:optional ViewSwitch tags,
    2:optional ViewSwitch banner,
    3:optional ViewSwitch flashSales,
    4:optional ViewSwitch todaysDeal,
    5:optional ViewSwitch selective,
    6:optional ViewSwitch hotBrand,
    7:optional ViewSwitch newArrival,
    8:optional ViewSwitch youMayLike,
    9:optional ViewSwitch redeem
}

struct PostcodeAddress {
    1: i16 regionId,
    2: i32 stateId,
    3: string stateName,
    4: i32 cityId,
    5: string cityName,
    6: list<Area> areas
}

struct Captcha {
    1:string image_base64,
    2:string sn
}

struct Entrance {
    1: string imageUrl
    2: i32 linkType
    4: string values
}

struct Channel {
    1: string index
    2: string messenger
    3: string cart
    4: string account
    5: string unSelectedIndex
    6: string unSelectedMessenger
    7: string unSelectedCart
    8: string unSelectedAccount
}

struct Skin {
    1: i32 regionId,
    2: string skinName
    3: bool masterSwitch
    4: bool entranceSwitch
    5: Entrance entrance
    6: bool channelSwitch
    7: Channel channel
}