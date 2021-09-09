from common.db import DB
#  在相应的领料表中的领料库存随着加工的减少（加工一个，领料表中的数量减少一个）
class substarct_pick_num:
    def substarct_pick_num(self, product_id, matter_code):
        try:
            db = DB()
            conn = db.get_connection(product_id)
            sql_old_pick_num = """
            select matter_count from pick_matter where matter_code = '{0}'
            """
            sql_old_pick_num = sql_old_pick_num.format(matter_code)
            dr_counts = db.execute_sql(conn, sql_old_pick_num)
            if len(dr_counts) > 0:
                if dr_counts[0][0]:
                    old_count = dr_counts[0][0]
                    if old_count > 0:
                        matter_count = int(old_count) - 1
                        sql_update = """
                        update pick_matter set matter_count = '{0}' where matter_code = '{1}'
                        """
                        sql_update = sql_update.format(matter_count, matter_code)
                        db.execute_sql(conn, sql_update)
                        data = {'code': 0, "message": "加工一个，领料表中的数量减少一个成功"}
                        return data
                    else:
                        data = {'code': 1, "message": "领料库中物料数量小于1，请先领料"}
                        return data

                else:
                    data = {'code': 1, "message": "找不到领料表中领料的数量"}
                    return data
            else:
                # data = "找不到领料表中领料的数量"
                data = {'code': 1, "message": "找不到领料表中领料的数量"}
                return data
        except Exception as e:
            data = {'code' : 1, "message" : "在相应的领料中减少领料库存报错%s"%e}
            return data
