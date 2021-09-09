from common.db import DB
from common.Page import Page

class product_live:
    def one_product_live(self, product_id, finished_product_code):
        test_tables = []
        data_list = []
        db = DB()
        conn = db.get_connection(product_id)

        if finished_product_code:
            finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            sn_sql = " and SN = " + "'" + finished_product_code + "'"
        else:
            finished_product_code_sql = ""
            sn_sql = ""

        sql = """
               select * from work_station where work_type = '加工'
               """
        drs = db.execute_sql(conn, sql)

        sql_search_test_table = """
        SELECT table_name FROM work_station left join work_transit 
        on work_station.work_code = work_transit.work_code where work_type = "测试"
        """
        dr_search_test_tables = db.execute_sql(conn, sql_search_test_table)
        if dr_search_test_tables:
            for dr_search_test_table in dr_search_test_tables:
                test_tables.append(dr_search_test_table[0])
        else:
            pass
        jiagong_list = []
        if drs:
            for dr in drs:
                jiagong_list.append(dr[1])
            for wor_id in jiagong_list:
                one_station = "product_transit_" + str(wor_id)
                sql_select = """
                select * from {0} where 2 > 1 {1} group by out_time
                """
                sql_select = sql_select.format(one_station, finished_product_code_sql)
                dr_oneworks = db.execute_sql(conn, sql_select)
                if dr_oneworks:
                    for dr_onework in dr_oneworks:
                        dict_one_data = {}
                        dict_one_data["finished_product_code"] = dr_onework[3]
                        dict_one_data["user_code"] = dr_onework[4]
                        dict_one_data["work_code"] = dr_onework[5]
                        dict_one_data["test_result"] = dr_onework[6]
                        if dr_onework[9]:
                            dp = dr_onework[9]
                            dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                            dict_one_data["time"] = dp
                        else:
                            dict_one_data["time"] = ""
                        data_list.append(dict_one_data)
                else:
                    pass

            sql_other_table = """
            SELECT * FROM work_station left join work_transit on work_station.work_code = work_transit.work_code;
            """
            # sql_other_table = sql_other_table.format(sn_sql)
            df_tbales = db.execute_sql(conn, sql_other_table)

            if df_tbales:
                for df_tab in df_tbales:
                    if df_tab[7]:

                        sql_table = """
                        select finished_product_code, Result, time from {0} where 2 > 1 {1}
                        """
                        sql_table = sql_table.format(df_tab[7], finished_product_code_sql)

                        dffs = db.execute_sql(conn, sql_table)
                        if dffs:
                            for df in dffs:
                                da_dict = {}
                                da_dict["finished_product_code"] = df[0]
                                da_dict["test_result"] = df[1]
                                if df[2]:
                                    dp = df[2]
                                    dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                                    da_dict["time"] = dp
                                else:
                                    da_dict["time"] = ""
                                da_dict["work_code"] = df_tab[0]
                                da_dict["user_code"] = ""
                                data_list.append(da_dict)

                        else:
                            pass
            else:
                pass

            sql_modify_data = """
            select * from modify_in_workstation where 2 > 1 {0} 
            """
            sql_modify_data = sql_modify_data.format(finished_product_code_sql)

            modify_datas = db.execute_sql(conn, sql_modify_data)

            if modify_datas:
                for modify_data in modify_datas:
                    modify_dict1 = {}
                    modify_dict2 = {}
                    modify_dict1["finished_product_code"] = modify_data[2]
                    modify_dict1["test_result"] = "入站"
                    dp = modify_data[6]
                    dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                    modify_dict1["time"] = dp
                    modify_dict1["work_code"] = modify_data[3]
                    modify_dict1["user_code"] = modify_data[5]

                    data_list.append(modify_dict1)
                    if modify_data[7]:
                        modify_dict2["finished_product_code"] = modify_data[2]
                        modify_dict2["test_result"] = "入站"
                        modify_dict2["work_code"] = modify_data[3]
                        modify_dict2["user_code"] = modify_data[5]
#                        modify_dict2["process_method"] = modify_data[7]
                        ds = modify_data[8]
                        print("----ds--->", ds)
                        if ds:
                            ds = ds.strftime("%Y-%m-%d %H:%M:%S")
                        else:
                            ds = ""
                        modify_dict2["time"] = ds
                        modify_dict2["test_result"] = "出站"
                        data_list.append(modify_dict2)
            else:
                pass

            sql_pakege_data = """
            SELECT * FROM enter_storage as a left join enter_storage_status as b on a.pack_id = b.pack_id where 2>1 {0}
            """
            sql_pakege_data = sql_pakege_data.format(finished_product_code_sql)

            pakege_datas = db.execute_sql(conn, sql_pakege_data)

            if pakege_datas:
                sql_work_code = """
                            select work_code from work_station where work_type = "包装"
                            """
                dr_work_codes = db.execute_sql(conn, sql_work_code)
                if dr_work_codes[0][0]:
                    bao_work_code = dr_work_codes[0][0]
                else:
                    bao_work_code = ""

                for pakege_data in pakege_datas:
                    pakege_dict = {}
                    pakege_dict["finished_product_code"] = pakege_data[2]
                    pakege_dict["test_result"] = pakege_data[9]
                    dp = pakege_data[8]
                    if dp:
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        dp = ""
                    pakege_dict["time"] = dp
                    pakege_dict["work_code"] = bao_work_code
                    pakege_dict["user_code"] = pakege_data[7]
                    data_list.append(pakege_dict)
            else:
                pass

        db.close_connection(conn)
        # print("--------------->>>>>>>>", data_list)

        return data_list


