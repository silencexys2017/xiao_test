
fo = open("all_skus.txt", "r")

sku_ids = []
for line in fo.readlines():                          #依次读取每行
    str_list = line.split(' ')
    sku_ids.append(int(str_list[0]))

print(sku_ids)