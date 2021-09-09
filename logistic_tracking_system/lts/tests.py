
# import os
# import shutil
#
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# print("=>", BASE_DIR)
# path1 = r"D:\zhouzhi\gitlit_code\logistic_tracking_system\logistic_tracking_system\lts\123.xlsx"
#
# # BASE_DIR = str(BASE_DIR).replace("\\", '/')
# #
# # BASE_LOG_DIR = os.path.join(BASE_DIR, "static\models\CO2.xlsx")
# # # BASE_LOG_DIR = BASE_LOG_DIR.replace("\\", '/')
# # BASE_LOG_DIR = BASE_LOG_DIR.replace("\\", '/')
# shutil.copy(path1, r"D:\zhouzhi\gitlit_code\logistic_tracking_system\logistic_tracking_system\media")

# import datetime
# def getEveryDay(begin_date,end_date):
#     # 前闭后闭
#     date_list = []
#     begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
#     end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
#     while begin_date <= end_date:
#         date_str = begin_date.strftime("%Y-%m-%d")
#         date_list.append(date_str)
#         begin_date += datetime.timedelta(days=1)
#     return date_list
#
# s  = '2016-01-01 00:00:00'
# d = "2016-01-01 23:59:59"
# a = s[0:10]
# b = d[0:10]
#
# print(getEveryDay(a, b))
# # start_time = "2021-09-02"
# #             # end_time = "2021-09-03"
# # check_statrt_time = start_time[0:10]
# # print(check_statrt_time)

y = (11, 22, 33)
s = len(y)
print(s)





data_list = []

dr_columns = (('id',), ('finished_product_code',), ('Result',), ('time',), ('PRV_low',), ('PRV_low_result',), ('PRV_high',), ('PRV_high_result',), ('Bleeding_result',), ('Detect_switch',), ('station',))

dr_infos = ((191993, 'SPR001300-2A001387-CMSS-A02-090621-0217', 'PASS', '34', '2', 'PASS', '125', 'PASS', 'PASS', '101', '1'),)
for dr in dr_infos:
    dict_data = {}
    for i in range(10):
        print("==>", dr_columns[i][0])
        if dr_columns[i][0] == "time":
            s = dr[i]
            if s:
                s = s.strftime("%Y-%m-%d %H:%M:%S")
            else:
                s = ""
            dict_data["time"] = s
        else:
            print("---->111")
            print("dr_columns[0][i]---->", dr_columns[i][0])
            print("dr[i]--->", dr[i])
            dict_data[dr_columns[i][0]] = dr[i]
            print("-0-0-0>", dict_data)
    data_list.append(dict_data)
print(data_list)











