// add purview for close store S307
promotion
db.parameter.insertMany(
[{
        "id" : 1,
        "regionId" : 1,
        "name" : "ACTIVITY_FLASH_SALE_ENABLE",
        "value" : "1",
        "dataType" : "bool",
        "paramModule" : "activity_flash_sale",
        "index" : 1
},
{
        "id" : NumberLong(9),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_ROBOT_ENABLE",
        "value" : "1",
        "dataType" : "bool",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(5),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_LIMIT_STORE_IDS",
        "value" : "",
        "dataType" : "list-int",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(6),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_VALIDITY_PERIOD",
        "value" : "1,2,3,5,7,30",
        "dataType" : "list-int",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(10),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_TAG_ENABLE",
        "value" : "0",
        "dataType" : "bool",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(7),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_COMPLETION_PERIOD_HOURS",
        "value" : "12,24,48",
        "dataType" : "list-int",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(11),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_TAG_OTHERS_ENABLE",
        "value" : "0",
        "dataType" : "bool",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(4),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_LIMIT_STORE_TYPE",
        "value" : "1",
        "dataType" : "int",
        "paramModule" : "promotion",
        "index" : 0
},
{
        "id" : NumberLong(8),
        "regionId" : NumberLong(1),
        "name" : "GROUP_BUYING_BUYERS_GOALS",
        "value" : "1,2,3,5",
        "dataType" : "list-int",
        "paramModule" : "promotion",
        "index" : 0
}]
)