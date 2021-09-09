

def post(self, request):
    try:

        json_data = request.body
        str_data = json.loads(json_data)

        db = DB()
        product_id = request.session.get("session_projectId")
        conn = db.get_connection(product_id)

        sql_matter = """
               SELECT max(order_number) FROM back_matter;
               """
        matter_type = db.execute_sql(conn, sql_matter)
        if matter_type[0][0] == None:
            matter_num = 0
        else:
            matter_num = matter_type[0][0]

        sql = """
              SELECT max(order_number) FROM product_back_matter;
              """
        product_type = db.execute_sql(conn, sql)
        if product_type[0][0] == None:
            id_num = 1
        else:
            id_num = product_type[0][0] + 1

        materials_back_code = str("Im_Product_back_matter_" + str(id_num))
        back_person = str_data.get("back_person")
        product_plan_code = str_data.get("product_plan_code")
        back_time = str_data.get("back_time")
        description = str_data.get("description")
        response_datas = str_data.get("response_datas")
        # back_person = "小小笑"
        # product_plan_code = "Im_ProductPlan_1"
        # back_time = "2021-07-06"
        # description = "无"
        # response_datas = [{"matter_code": "Im_Matter_10", "matter_count": "10"},
        #                   {"matter_code": "Im_Matter_11", "matter_count": "20"}]

        order_number = id_num

        sql_insert = """
                           insert into product_back_matter(materials_back_code, back_person, 
                           product_plan_code,
                           back_time, description, order_number)
                           values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                           """
        sql_insert_format = sql_insert.format(materials_back_code, back_person,
                                              product_plan_code, back_time,
                                              description, order_number)
        drs = db.execute_sql(conn, sql_insert_format)
        for response_data in response_datas:
            # db = DB()
            # conn = db.get_connection("db_common")
            matter_code = response_data.get("matter_code")
            matter_count = response_data.get("matter_count")
            matter_num = matter_num + 1
            deal_back_code = str("Im_Deal_Back_" + str(matter_num))
            sql_response = """
                           insert into back_matter(deal_back_code, materials_back_code,matter_code, matter_count,
                           order_number)
                           values('{0}', '{1}', '{2}', '{3}', '{4}')
                   """
            sql_response_format = sql_response.format(deal_back_code, materials_back_code,
                                                      matter_code, matter_count,
                                                      matter_num)
            matter_drs = db.execute_sql(conn, sql_response_format)

            print("---->>>>", matter_code)

        data = {"code": 0, "message": "创建产品详情表成功"}
        logger.info("创建产品详情表成功")
        data = json.dumps(data)

        return HttpResponse(data)
    except Exception as e:
        print(e)
        data = {"code": 1, "message": "创建产品详情表失败"}
        logger.error("创建产品详情表失败")
        data = json.dumps(data)
        return HttpResponse(data)