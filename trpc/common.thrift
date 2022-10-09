include "exceptions.thrift"
include "common_struct.thrift"

struct Banner {
    1: required i32 id,
    2: required i32 regionId,
    3: required i32 index,
    4: required string imageUrl,
    5: required i16 linkType,
    6: required string value,
    7: required i16 status,
    8: optional i32 type
}

struct PopUpAds {
    1: i64 region,
    2: i64 version,
    3: string title,
    4: string imageUrl,
    5: i32 linkType,
    6: string value,
    7: i32 status
}

struct StartUpImage {
    1: i64 region,
    2: i64 version,
    4: string imageUrl,
    5: i32 linkType,
    6: string value
}


service CommonService {
    list<common_struct.Region> getRegions(1:optional i32 app_version),
    common_struct.Region getRegionById(1:i32 regionId) throws (1:exceptions.NotFoundException nfe),
    common_struct.Region get_region(
        1:optional string calling_code) throws(
            1:exceptions.NotFoundException nfe),
    list<common_struct.State> getStates(1:i32 regionId, 2:optional i32 app_version) throws (1:exceptions.NotFoundException nfe),
    common_struct.State getStateById(1:i32 stateId) throws (1:exceptions.NotFoundException nfe),
    list<common_struct.City> getCities(
        1:i32 regionId, 2:i32 stateId, 3:optional i32 app_version) throws (1:exceptions.NotFoundException nfe,
                                               2:exceptions.InvalidOperationException ioe),
    common_struct.City getCityById(1:i32 cityId) throws (1:exceptions.NotFoundException nfe),
    list<common_struct.City> getCitiesByRegionId(1:i32 regionId, 2:optional i32 app_version) throws (1:exceptions.NotFoundException nfe,
                                                           2:exceptions.InvalidOperationException ioe),
    list<common_struct.Area> getAreas(1:i32 regionId, 2:i32 cityId, 3:optional i32 app_version) throws (1:exceptions.NotFoundException nfe,
                                                              2:exceptions.InvalidOperationException ioe),
    common_struct.Area getAreaById(1:i32 areaId) throws (1:exceptions.NotFoundException nfe),
    string send_sms_verify_code(
        1:string app_key,
        2:i32 region_id,
        3:string phone,
        4:i32 validate_type) throws (
            1:exceptions.InvalidOperationException ioe,
            2:exceptions.NotFoundException nfe),
    bool check_sms_verify_code(
        1:string app_key,
        2:i32 region_id,
        3:string phone,
        4:string sn,
        5:string code,
        6:optional bool is_succeed_delete) throws (
            1:exceptions.InvalidOperationException ioe),
    void delete_sms_verify_code(
        1:string app_key,
        2:i32 region_id,
        3:string phone,
        4:string sn) throws (
            1:exceptions.InvalidOperationException ioe),
    bool setTodayDeals(1:i32 regionId, 2:list<i64> listingIds) throws (1:exceptions.NotFoundException nfe),
    list<i64> getTodayDeals(1:i32 regionId),
    bool set_new_arrival(1:i32 region_id, 2:list<i64> listing_ids) throws (
        1:exceptions.NotFoundException nfe),
    list<i64> get_new_arrival(1:i32 region_id),
    bool set_may_like(1:i32 region_id, 2:list<i64> listing_ids) throws (
        1:exceptions.NotFoundException nfe),
    list<i64> get_may_like(1:i32 region_id),
    list<Banner> getBannerList(
        1:i32 regionId
        2:optional i16 status
        3:optional i16 btype
        ),
    Banner getBanner(1:i32 bannerId) throws (1:exceptions.NotFoundException nfe),
    Banner mergeBanner(
        1:i32 index
        2:string imageUrl
        3:i16 linkType
        4:string value
        5:i16 status
        6:i32 regionId
        7:optional i32 bannerId
        8:optional i32 btype
    ) throws (
        1:exceptions.InvalidOperationException ioe
    ),
    Banner changeBannerStatus(1:i32 bannerId, 2:i16 status) throws (1:exceptions.NotFoundException nfe),
    void deleteBanner(1:i32 bannerId),
    string sendSMS(1:i32 regionId, 2:string phone,
                   3:string message) throws (1:exceptions.NotFoundException nfe,
                                             2:exceptions.InvalidOperationException ioe),
    void upsert_session_logs(1:list<common_struct.SessionLog> session_logs),
    void upsert_action_logs(1:list<common_struct.ActionLog> action_logs),
    list<common_struct.Parameter> get_parameter_list(
        1:i32 region_id, 2:optional list<string> param_modules,
        3:optional list<string> values),
    void set_parameters(1:list<common_struct.SetParameter> parameters),

    common_struct.Special get_special(
        1:string special_code,
        2:optional bool is_deleted)throws (1:exceptions.NotFoundException nfe),
    common_struct.PagingSpecial get_specials(
        1:i32 region_id,
        2:optional string start_time,
        3:optional string end_time,
        4:optional bool is_deleted,
        5:optional i32 skip,
        6:optional i32 limit),
    common_struct.Special add_special(
        1:i32 region_id,
        2:string special_code,
        3:string title,
        4:list<i64> listing_ids,
        5:i64 operator_id) throws (1:exceptions.InvalidOperationException ioe),
    void update_special(
        1:i64 special_id,
        2:optional string special_code,
        3:optional string title,
        4:optional list<i64> listing_ids,
        5:optional i64 operator_id,
        6:optional bool is_deleted) throws (1:exceptions.NotFoundException nfe,
                                            2:exceptions.InvalidOperationException ioe),

    PopUpAds updatePopUpAds(
        1: i64 region,
        2: i64 version,
        3: string title,
        4: string imageUrl,
        5: i32 linkType,
        6: string value,
        7: i32 status
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    PopUpAds getFreshPopUpAds(
        1: i64 region
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    StartUpImage getFreshStartUpImage(
        1: i64 region
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    StartUpImage updateStartUpImage(
        1: i64 region,
        2: i64 version,
        4: string imageUrl,
        5: i32 linkType,
        6: string value,
    ) throws (
        1: exceptions.NotFoundException nfe
    ),

    void record_admin_log(
        1: string source
        2: i64 operator_id
        3: string action
        4: string data
    ),

    list<common_struct.Address> get_support_cod_addresses(1: i16 region_id),

    common_struct.EnvRegistration get_env_registration(
        1: i64 region_id) throws (1: exceptions.NotFoundException nfe),

    common_struct.EnvRegistration update_env_registration(
        1:required i64 region_id,
        2:required common_struct.EnvRegistration env_registration) throws (
            1:exceptions.InvalidOperationException ioe),

    common_struct.EnvStar get_env_star(
        1: i64 region_id) throws (1: exceptions.NotFoundException nfe),

    common_struct.EnvStar update_env_star(
        1:required i64 region_id,
        2:required common_struct.EnvStar env_star) throws (
            1:exceptions.InvalidOperationException ioe),

    common_struct.EnvHomepage get_env_homepage(
        1: i64 region_id) throws (1: exceptions.NotFoundException nfe),

    common_struct.EnvHomepage update_env_homepage(
        1:required i64 region_id,
        2:required common_struct.EnvHomepage env_homepage) throws (
            1:exceptions.InvalidOperationException ioe),

    string send_email(
        1:i64 region_id,
        2:string email,
        3:string subject,
        4:string message,
        5:optional string content_type,
        6:optional string language,
        7:optional bool use_blank_page) throws (
            1:exceptions.InvalidOperationException ioe),

    string send_email_verify_code(
        1:string app_key
        2:i64 region_id,
        3:string email,
        4:common_struct.VerifyCodeType verify_type,
        5:string language) throws (
            1:exceptions.InvalidOperationException ioe),

    bool check_email_verify_code(
        1:string app_key,
        2:string email,
        3:common_struct.VerifyCodeType verify_type,
        4:string sn,
        5:string code,
        6:optional bool is_succeed_delete) throws (
            1:exceptions.InvalidOperationException ioe),

    void delete_email_verify_code(
        1:string app_key,
        2:string email,
        3:string sn),

    void send_welcome_email(
        1:i64 region_id,
        2:string email,
        3:string language,
        4:string nick,
        5:string init_pwd) throws (
            1:exceptions.InvalidOperationException ioe),

    void update_user_address_interaction_method(
        1: i16 region_id, 2: common_struct.UserAddressInteractionMethod method)
    throws (1: exceptions.NotFoundException nfe),

    common_struct.PostcodeAddress get_postcode_address(1: i16 region_id, 2: string postcode)
    throws (1: exceptions.InvalidOperationException ioe,
        2: exceptions.NotFoundException nfe),

    common_struct.Captcha get_captcha(),

    bool check_captcha_verify_code(
        1:string sn,
        2:string code,
        3:optional bool is_succeed_delete) throws (
            1:exceptions.InvalidOperationException ioe),

    void delete_captcha(1:string sn, 2:string code),

    void upsert_skin(
        1: i32 region_id,
        2: string skin_name
        3: bool master_switch
        4: bool entrance_switch
        5: common_struct.Entrance entrance
        6: bool channel_switch
        7: common_struct.Channel channel
    ),

    common_struct.Skin get_skin (
        1: required i32 region_id
    )
}