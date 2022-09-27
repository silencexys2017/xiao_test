// postage 版本
db.ClearingOrder.updateMany({"isSelfDelivery" : false}, {"$set": {"deliveryMethod": 1}})
db.ClearingOrder.updateMany({"isSelfDelivery" : true}, {"$set": {"deliveryMethod": 2}})