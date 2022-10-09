include "exceptions.thrift"
include "unx_struct.thrift"


service UnxService {
    unx_struct.LocalizedSubsidiaries get_localized_subsidiaries(
        1:optional i32 skip, 2:optional i32 limit, 3:optional bool main_switch, 
        4:optional bool sub_switch, 5:optional set<i32> region_ids,
        6:optional set<i32> local_sub_ids),

    unx_struct.LocalizedSubsidiary create_localized_subsidiary(
        1:i32 region_id, 2:string calling_code, 3:string code, 4:string name,
        5:string flag, 6:i32 currency_id, 7:string currency_symbol, 
        8:string currency, 9:string language, 10:string time_zone, 
        11:bool main_switch, 12:string domain, 13:string exchange_rate_ref,
        14:optional bool sub_switch, 15:optional bool allowed_add_store)
    throws(1:exceptions.InvalidOperationException ioe),

    unx_struct.LocalizedSubsidiary get_localized_subsidiary(
        1:optional i32 region_id, 2:optional i32 local_sub_id, 
        3:optional bool main_switch, 4:optional bool sub_switch)
    throws(1:exceptions.InvalidOperationException ioe),

    void update_localized_subsidiary(
        1:i32 local_sub_id, 2:optional bool main_switch, 
        3:optional bool sub_switch, 4:optional string flag,
        5:optional string time_zone, 6:optional bool allowed_add_store,
        7:optional string domain, 8:optional string exchange_rate_ref)
    throws (1:exceptions.InvalidOperationException nfe),
}