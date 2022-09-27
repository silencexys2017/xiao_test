import json
import os
import xlsxwriter

MM_NAME = "mm_address.xlsx"
DA_RAZ_NAME = "da_raz_address.xlsx"
SYL_LA_NAME = "sl_address.xlsx"
NAME = "address.xlsx"


def export_excel_per_fee(data):
    workbook = xlsxwriter.Workbook(DA_RAZ_NAME)
    worksheet_1 = workbook.add_worksheet("PerFeeAddress")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "State", bold)
    worksheet_1.write("B1", "City", bold)
    worksheet_1.write("C1", "Town", bold)
    worksheet_1.set_column('A:B', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_column('C:C', 30, other_bold)
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    a_1 = 2
    s_1 = 2
    for item in data:
        cities = item["cities"]
        city_count = 0
        for it in cities:
            town_count = len(it.get("towns"))
            for i in it.get("towns"):
                worksheet_1.write('C%d' % row_1, i["town_name"])
                row_1 += 1
            if town_count > 1:
                worksheet_1.merge_range(
                    "B%d:B%d" % (a_1, a_1+town_count-1), it["city_name"],
                    other_bold)
            else:
                worksheet_1.write(
                    'B%d' % (a_1+town_count-1), it["city_name"], other_bold)
            a_1 += town_count
            city_count += town_count

        if city_count > 1:
            mer_range = "A%d:A%d" % (s_1, s_1+city_count-1)
            worksheet_1.merge_range(mer_range, item["state_name"], other_bold)
        else:
            worksheet_1.write(
                'A%d' % (s_1+city_count-1), item["state_name"], other_bold)
        s_1 += city_count

    workbook.close()


def export_excel_per_fee_not_merge(data):
    workbook = xlsxwriter.Workbook(MM_NAME)
    worksheet_1 = workbook.add_worksheet("PerFeeAddress")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "State", bold)
    worksheet_1.write("B1", "City", bold)
    worksheet_1.write("C1", "Town", bold)
    worksheet_1.set_column('A:B', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_column('C:C', 30, other_bold)
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    for item in data:
        cities = item["cities"]
        for it in cities:
            for i in it.get("towns"):
                worksheet_1.write('C%d' % row_1, i["town_name"])
                worksheet_1.write('A%d' % row_1, item["state_name"])
                worksheet_1.write('B%d' % row_1, it["city_name"])
                row_1 += 1

    workbook.close()


def export_excel_syl_la(data):
    workbook = xlsxwriter.Workbook(SYL_LA_NAME)
    worksheet_1 = workbook.add_worksheet("sylLaAddress")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "State", bold)
    worksheet_1.write("B1", "City", bold)
    worksheet_1.write("C1", "Town", bold)
    worksheet_1.set_column('A:B', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    a_1 = 2
    for item in data:
        cities = item["cities"]
        city_count = len(cities)
        for it in cities:
            worksheet_1.write('B%d' % row_1, it["city_name"])
            row_1 += 1

        if city_count > 1:
            mer_range = "A%d:A%d" % (a_1, a_1 + city_count - 1)
            worksheet_1.merge_range(mer_range, item["state_name"], other_bold)
        else:
            worksheet_1.write(
                'A%d' % (a_1 + city_count - 1), item["state_name"], other_bold)
        a_1 += city_count

    workbook.close()


def export_excel(data_1, data_2):
    workbook = xlsxwriter.Workbook(NAME)
    worksheet_1 = workbook.add_worksheet("PerFeeAddress")
    bold = workbook.add_format({'bold': True, 'align': 'center',
                                'valign': 'vcenter'})
    other_bold = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

    worksheet_1.write("A1", "State", bold)
    worksheet_1.write("B1", "City", bold)
    worksheet_1.write("C1", "Town", bold)
    worksheet_1.set_column('A:B', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_1.set_column('C:C', 30, other_bold)
    worksheet_1.set_row(0, 20)  # 设置第1行的高度为20
    row_1 = 2
    a_1 = 2
    for item in data_1:
        cities = item["cities"]
        city_count = len(cities)
        for it in cities:
            worksheet_1.write('B%d' % row_1, it["city_name"])
            towns = ""
            for i in it.get("towns"):
                towns = towns + i.get("town_name") + ","
            worksheet_1.write('C%d' % row_1, towns[:-1])
            row_1 += 1

        if city_count > 1:
            mer_range = "A%d:A%d" % (a_1, a_1 + city_count - 1)
            worksheet_1.merge_range(mer_range, item["state_name"], other_bold)
        else:
            worksheet_1.write(
                'A%d' % (a_1 + city_count - 1), item["state_name"], other_bold)
        a_1 += city_count

    worksheet_2 = workbook.add_worksheet("sylLaAddress")
    worksheet_2.write("A1", "State", bold)
    worksheet_2.write("B1", "City", bold)
    worksheet_2.write("C1", "Town", bold)
    worksheet_2.set_column('A:B', 20, other_bold)  # 设置A-B的单元格宽度为20
    worksheet_2.set_row(0, 20)  # 设置第1行的高度为20
    row_2 = 2
    a_2 = 2
    for item in data_2:
        cities = item["cities"]
        city_count = len(cities)
        for it in cities:
            worksheet_2.write('B%d' % row_2, it["city_name"])
            row_2 += 1

        if city_count > 1:
            mer_range = "A%d:A%d" % (a_2, a_2 + city_count - 1)
            worksheet_2.merge_range(mer_range, item["state_name"], other_bold)
        else:
            worksheet_2.write(
                'A%d' % (a_2 + city_count - 1), item["state_name"], other_bold)
        a_2 += city_count

    workbook.close()


if __name__ == "__main__":

    with open('mm_address.json', 'r', encoding='utf8')as fp1:
        json_data = json.load(fp1)
        export_excel_per_fee(json_data)
        fp1.close()
        # os.remove(DA_RAZ_NAME)

    # with open('./shop_mm_address.json', 'r', encoding='utf8')as fp1:
    #     json_data = json.load(fp1)
    #     export_excel_per_fee_not_merge(json_data)
    #     fp1.close()
    #
    # with open('./exfcs.json', 'r', encoding='utf8')as fp2:
    #     json_data = json.load(fp2)
    #     export_excel_syl_la(json_data)
    #     fp2.close()
    #
    # with open('./shop_mm_address.json', 'r', encoding='utf8') as fp1, \
    #         open('./exfcs.json', 'r', encoding='utf8')as fp2:
    #     export_excel(json.load(fp1), json.load(fp2))
    #     fp1.close()
    #     fp2.close()