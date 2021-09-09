import os
import time
# import wmi,json
# import pythoncom

import clr
clr.AddReference("iMDS_AES")

# clr.AddReference("iMDS_AES")
from iMDS_AES import *


from django.shortcuts import render
from django.http import HttpResponse
from django.urls.conf import re_path
from django.views import View
import json
import logging
import datetime
from utils.import_common import test11
from utils.test import opt
# from utils import *


from django.contrib.auth.hashers import make_password, check_password
from common.product_live import product_live
from common.db import DB
from page.Page import Page
from pathlib import Path
logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)

# Create your views here.


class test2(View):

    def get_live_data(self, product_id, finished_product_code):
        func = product_live()
        data_list = func.one_product_live(product_id, finished_product_code)

        return data_list

    def get(self, request):
        try:
            data_add_int = {}
            page = 1
            page_size = 100

            product_id = 'co2'
            finished_product_code = "sun123456781111"

            data_list = self.get_live_data(product_id, finished_product_code)
            data_list.sort(key=lambda x: (x['time']), reverse=False)

            print("===>>", data_list)

            page_result = Page(page, page_size, data_list)
            data = page_result.get_str_json()
            dfs = int(len(data_list))
            sql_num_int = dfs
            if dfs:
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
            result = {"code": 0, "message": "调取成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("生命周期成功:")
            return HttpResponse(result)

        except Exception as e:
            data = {"code": 1, "message": "创建人员失败%s" % e}
            logger.error("生命周期失败%s"%e)
            data = json.dumps(data)
            print(e)
            return HttpResponse(data)


class LogisticLogin(View):
    """
    登录系统，  校验通过就进入系统， 用户侧登录接口
    AEC 自带加密解密
    """
    def get(self, request):
        try:
            aes = AES()
            db = DB()
            conn = db.get_connection_nodb()
            db_list = []
            sql = """
            show databases
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                db_list.append(dr[0])

            auth_user = request.GET.get("user")
            pwd = request.GET.get("password")
            pwd = aes.AESEncrypt(pwd)
            product_id = request.GET.get("product_id")
            work_id = request.GET.get("work_id")
            # work_type = request.GET.get("work_type")
            request.session.set_expiry(0)
            if product_id in db_list:
                conn = db.get_connection(product_id)
                sql = """
                        select * from person where user_name = '{0}' and  user_password = '{1}'
                  """
                sql_main = sql.format(auth_user, pwd)
                drs = db.execute_sql(conn, sql_main)
                if drs:
                    sql_type = """
                            select work_type from work_station where work_id = '{0}'
                            """
                    sql_type = sql_type.format(work_id)
                    drs_type = db.execute_sql(conn, sql_type)
                    if drs_type:
                        work_type = drs_type[0][0]
                    else:
                        work_type = "没有工站类型"

                    sql = """
                           select * from person where user_name = '{0}' and  user_password = '{1}'
                     """
                    sql_main = sql.format(auth_user, pwd)
                    dfs = db.execute_sql(conn, sql_main)

                    if dfs:
                        work_ids = dfs[0][4]
                        work_ids_list = str(work_ids).split(",")
                        if work_id in work_ids_list:
                            current_person_id = drs[0][0]
                            request.session['session_projectId'] = product_id
                            request.session['session_currentId'] = current_person_id
                            request.session['session_workId'] = work_id
                            request.session['session_workType'] = work_type
                            data = {"code": 0, "message": "登录成功"}
                            data = json.dumps(data)
                            logger.info("登录成功")
                            return HttpResponse(data)
                        else:
                            data = {"code": 1, "message": "用户没有进入此工站的权限"}
                            data = json.dumps(data)
                            logging.error("用户没有进入此工站的权限")
                            return HttpResponse(data)
                else:
                    data = {"code": 1, "message": "该用户没有此项目的权限或者用户名密码错误"}
                    data = json.dumps(data)
                    return HttpResponse(data)

            else:
                data = {"code": 1, "message": "无此项目"}
                data = json.dumps(data)
                return HttpResponse(data)

        except Exception as e:

            data = {"code": 1, "message": "登录失败"}
            data = json.dumps(data)
            logger.error("用户登录失败----%s" % e)
            print(e)
            return HttpResponse(data)


class ManageLogisticLogin(View):
    """
    管理端登录接口 AES 自带加密解密
    """
    def get(self, request):
        try:
            aes = AES()
            db = DB()
            auth_user = request.GET.get("user")
            pwd = request.GET.get("password")
            pwd = aes.AESEncrypt(pwd)
            product_id = request.GET.get("product_id")
            request.session.set_expiry(0)
            if product_id:
                request.session.set_expiry(0)
                request.session['session_projectId'] = product_id
                conn = db.get_connection(product_id)
                sql = """
                select * from person where user_name = '{0}' and  user_password = '{1}'
                """
                sql = sql.format(auth_user, pwd)
                drs = db.execute_sql(db.get_connection("db_common"), sql)
                if drs:
                    for dr in drs:
                        current_person_id = dr[0]
                        request.session['session_projectId'] = product_id
                        request.session['session_currentId'] = current_person_id


                        data = {"code": 0, "message": "登录成功"}
                        data = json.dumps(data)
                        logger.info("登录成功")
                        return HttpResponse(data)
                else:
                    data = {"code": 1, "message": "用户名或者密码不正确或者没有管理员的权限"}
                    data = json.dumps(data)
                    logger.error("用户名或者密码不正确或者没有管理员的权限")
                    return HttpResponse(data)
            else:
                db = DB()
                product_id = "db_common"
                conn = db.get_connection("db_common")
                sql = """
                select * from person where user_name = '{0}' and user_password = '{1}'
                """
                sql_main = sql.format(auth_user, pwd)
                drs = db.execute_sql(conn, sql_main)
                request.session.set_expiry(0)
                if drs:
                    for dr in drs:
                        if dr[7] == "超级管理员":
                            current_person_id = dr[0]
                            request.session['session_projectId'] = "db_common"
                            request.session['session_currentId'] = current_person_id

                            data = {"code": 0, "message": "登录成功"}
                            data = json.dumps(data)
                            logger.info("登录成功")
                            return HttpResponse(data)
                        else:
                            data = {"code": 1, "message": "该用户不是超级管理员"}
                            data = json.dumps(data)
                            return HttpResponse(data)
                else:
                    data = {"code": 1, "message": "该用户不是超级管理员"}
                    data = json.dumps(data)
                    logger.error("该用户不是超级管理员")
                    return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("登录时候用户名操作失败%s"% e)

            return HttpResponse(data)


class ModifyPassword(View):
    """
    修改密码接口
    """
    def get(self, request):
        try:
            db = DB()
            product_id= request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            current_person_id = request.session['session_currentId']
            old_password = request.GET.get("old_password")
            new_password = request.GET.get("new_password")
            sql = """
            select user_password from person where user_code = '{0}'
            """
            sql = sql.format(current_person_id)
            drs = db.execute_sql(conn, sql)

            if old_password == drs[0][0]:
                sql_update = """
                     update person set 
                     user_password='{0}'
                     where user_code = '{1}'    
                """
                sql_update = sql_update.format(new_password, current_person_id)
                db.execute_sql(conn, sql_update)
                data = {"code": 0, "message": "操作成功"}
                data = json.dumps(data)
                logger.info("修改密码成功")
                return HttpResponse(data)
            else:
                data = {"code": 1, "message": "输入的旧密码有误"}
                data = json.dumps(data)
                logger.error("输入的旧密码有误")
                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("修改密码操作失败>>>>%s"% e)
            return HttpResponse(data)


class ShowDatabase(View):
    def get(self, request):
        try:
            data_list = []
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
            show tables
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_list.append(dr[0])
            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("查询数据库成功", data)
            return HttpResponse(data)

        except Exception as e:
            data = {"code": 1, "message": "操作失败", "data": ""}
            data = json.dumps(data)
            print(e)
            logger.error("查询数据库失败"%e)
            return HttpResponse(data)


class NewDatabase(View):
    """
    新建数据库表 和新建数据库接口
    """
    def get(self, request):
        try:
            database_list = []
            db_base = "db_common"
            # db_base = request.GET.get("")
            db = DB()
            conn = db.get_connection_mysql()
            sql = """
            show databases
            """
            drs = db.execute_sql(conn, sql)

            for dr in drs:
                database_list.append(dr[0])
            if db_base in database_list:
                data = {"code": 1, "message": "数据库已经存在"}
                logger.info("数据库已经存在")
            else:
                sql = """
                CREATE DATABASE {0} DEFAULT CHARACTER SET utf8
                """
                sql_main = sql.format(db_base)
                drs = db.execute_sql(conn, sql_main)
                data = {"code": 0, "message": "数据库已经建好"}
                logger.info("数据库已经建好")

            # data = {"code": 1, "message": "操作成功"}
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "新建数据库失败"}
            logger.error("新建数据库失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PersonDeal(View):

    def get(self, request):
        """
        登录如果带了项目 查询此项目下的人员
        如果没有带项目 就查询db_common下的人员
        """
        try:
            product_id = request.session.get("session_projectId")
            user_id = request.GET.get("user_id")
            user_name = request.GET.get("user_name")
            status = request.GET.get("status")
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            if user_id:
                user_id_sql = "and user_id = " + "'" + user_id + "'"
            else:
                user_id_sql = ""
            if user_name:
                user_name_sql = "and user_name = " + "'" + user_name + "'"
            else:
                user_name_sql = ""
            if status:
                status_sql = "and status = " + "'" + status + "'"
            else:
                status_sql = ""

            data_add_int = {}
            data = []
            data_list = []
            db = DB()
            conn = db.get_connection(product_id)
            sql = """
            select * from person where user_name != 'admin' {0} {1} {2}
            """
            sql = sql.format(user_id_sql, user_name_sql, status_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["user_code"] = dr[0]
                    dict_data["user_id"] = dr[1]
                    dict_data["user_name"] = dr[2]
                    dict_data["user_password"] = dr[3]
                    dict_data["user_authority"] = dr[4]
                    dict_data["status"] = dr[5]
                    dict_data["user_product_id"] = dr[6]
                    dict_data["user_role"] = dr[7]
                    data_list.append(dict_data)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                dfs = int(len(data_list))
                sql_num_int = dfs
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("调取人员详情成功:")
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                logger.info("调取人员详情成功但是没有数据:")
                return HttpResponse(result)
        except Exception as e:
            logger.error("调取person数据库有错误 %s" % e)
            result = {"code": 1, "message": "调取失败"}
            result = json.dumps(result)
            return HttpResponse(result)

    def post(self, request):
        """
        新增人员接口
        :param request:
        :return:
        """

        try:
            aes = AES()
            product_id = request.session.get("session_projectId")
            json_data = request.body
            str_data = json.loads(json_data)
            user_id = str_data.get("user_id")
            user_name = str_data.get("user_name")
            user_password = str_data.get("user_password")
            user_password = aes.AESEncrypt(user_password)
            user_authority = str_data.get("user_authority")
            status = str_data.get("status")
            user_product_id = str_data.get("user_product_id")
            user_role = str_data.get("user_role")

            if product_id == "db_common":
                # product_id = user_product_id
                db = DB()
                conn = db.get_connection(product_id)
            else:
                # product_id = request.session.get("session_projectId")
                db = DB()
                conn = db.get_connection(product_id)

            sql_check = """
            select * from person where user_name = '{0}' and user_id = '{1}'
            """
            sql_check = sql_check.format(user_name, user_id)
            dffs = db.execute_sql(conn, sql_check)
            if dffs:
                data = {"code": 1, "message": "人员已经存在"}
                logger.error("创建人员失败， 人员已经存在")
                data = json.dumps(data)
                return HttpResponse(data)

            else:
                sql = """
                     select max(order_number) from person
                    """
                id_num = db.execute_sql(conn, sql)

                if id_num[0][0] == None:
                    id_num = 1
                else:
                    id_num = id_num[0][0] + 1
                user_code = str("Im_User_" + str(id_num))

                sql_insert = """
                    insert into person(user_code, user_id, user_name, user_password, user_authority, 
                    status, user_product_id, user_role, order_number)
                    values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')
                    """

                sql_insert_format = sql_insert.format(user_code, user_id, user_name,
                                                      user_password, user_authority, status, user_product_id,
                                                      user_role, id_num)

                drs = db.execute_sql(conn, sql_insert_format)
                data = {"code": 0, "message": "创建人员成功"}
                data = json.dumps(data)
                logger.info("创建人员成功")
                return HttpResponse(data)

        except Exception as e:
            data = {"code": 1, "message": "创建人员失败%s" % e}
            logger.error("创建人员失败%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class PutPerson(View):
    """
    修改人员接口
    """

    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)

            user_code = request.GET.get("user_code")
            user_id = request.GET.get("user_id")
            user_name = request.GET.get("user_name")
            user_password = request.GET.get("user_password")
            user_authority = request.GET.get("user_authority")
            status = request.GET.get("status")
            user_product_id = request.GET.get("user_product_id")
            user_role = request.GET.get("user_role")
            sql = """
                      update person set user_id='{0}',
                      user_name='{1}',user_password='{2}',user_authority='{3}',status='{4}'
                      ,user_product_id = '{5}', user_role = '{6}' where user_code = '{7}'
                      """
            sql_format = sql.format(user_id, user_name, user_password, user_authority,
                                    status, user_product_id, user_role, user_code)
            db.execute_sql(conn, sql_format)

            data = {"code": 0, "message": "修改人员成功"}
            data = json.dumps(data)
            logger.info("修改人员成功")
            return HttpResponse(data)

        except Exception as e:
            data = {"code": 1, "message": "修改人员失败,---%s" % e}
            data = json.dumps(data)
            logger.error("修改人员失败"%e)
            return HttpResponse(data)


class DeletePerson(View):
    """
    删除人员接口
    """

    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)
            user_code = request.GET.get("user_code")
            sql = """
            delete FROM person where user_code = '{0}'       
            """
            sql_format = sql.format(user_code)
            db.execute_sql(conn, sql_format)
            data = {"code": 0, "message": "删除成功"}
            data = json.dumps(data)
            logger.info("删除人员成功")
            return HttpResponse(data)
        except Exception as e:
            data = {"code":1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除人员失败%s"% e)
            return HttpResponse(data)


class PersonTable(View):
    """
    新增个人详情表  在公共库里面加一张表格 加人员
    """
    def get(self, request):
        try:
            table_list = []
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
            create table person(user_code varchar(64) primary key not null,
            user_id varchar(64), user_name varchar(32),
            user_password varchar(64), user_authority varchar(255), status varchar(10), user_product_id varchar(255),
            user_role varchar(255), order_number int);
            """
            dr = db.execute_sql(conn, sql)
            sql_main = """
            show tables
            """
            drs = db.execute_sql(conn, sql_main)
            for pe in drs:
                table_list.append(pe[0])
            if "person" in table_list:
                data = {"code": 0, "message": "操作成功"}
            else:
                data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)


class CreatePersonMatter(View):

    def get(self, request):
        try:
            table_list = []
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
            create table Person_Matter(matter_code varchar(64) primary key not null,
            matter_id varchar(64),
            matter_name varchar(64), matter_category varchar(64), rule varchar(64),
            matter_count int, product_time datetime, status varchar(128), order_number int);
            """
            dr = db.execute_sql(conn, sql)
            sql_main = """
            show tables
            """
            drs = db.execute_sql(conn, sql_main)
            for pe in drs:
                table_list.append(pe[0])
            if "person" in table_list:
                data = {"code": 0, "message": "操作成功"}
                logger.info("创建物料详情结构表成功！")
            else:
                data = {"code": 1, "message": "操作失败"}
                logger.info("创建物料详情结构表失败！")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            data = {"code": 0, "message": "操作失败"}
            data = json.dumps(data)
            print(e)
            logger.error("----创建物料详情结构表失败%s"% e)
            return HttpResponse(data)


class PersonMatter(View):
    """
    物料查询接口
    """

    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")
            data_list = []
            data_add_int = {}
            matter_id = request.GET.get("matter_id")
            matter_name = request.GET.get("matter_name")
            matter_category = request.GET.get("matter_category")
            operate_user = request.GET.get("operate_user")

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            db = DB()
            conn = db.get_connection(product_id)

            if matter_id:
                matter_id_sql = " and matter_id =" + "'" + matter_id + "'"
            else:
                matter_id_sql = ""
            if matter_name:
                matter_name_sql = " and matter_name = " + "'" + matter_name + "'"
            else:
                matter_name_sql = ""
            if matter_category:
                matter_category_sql = " and matter_category = " + "'" + matter_category+"'"
            else:
                matter_category_sql = ""
            if operate_user:
                operate_user_sql = " and operate_user = " + "'" + operate_user+"'"
            else:
                operate_user_sql = ""

            sql = """
             select pm.matter_code, ml.matter_name, ml.rule, ml.matter_category, pm.matter_count,
              pm.product_time, pm.operate_user,ml.code_length from person_matter as pm left join matter_list as ml on pm.matter_code = ml.bom_matter_code
              where 2 > 1 {0} {1} {2} {3}
            """

            sql_main = sql.format(matter_id_sql, matter_name_sql, matter_category_sql, operate_user_sql)
            drs = db.execute_sql(conn, sql_main)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["matter_code"] = dr[0]
                    dict_data["matter_name"] = dr[1]
                    dict_data["rule"] = dr[2]
                    dict_data["matter_category"] = dr[3]
                    dict_data["matter_count"] = dr[4]
                    s = dr[5]
                    if s:
                        s1 = s.strftime("%Y-%m-%d %H:%M:%S ")
                    else:
                        s1 = ""
                    dict_data["product_time"] = s1
                    dict_data["operate_user"] = dr[6]
                    dict_data["code_length"] = dr[7]
                    data_list.append(dict_data)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num_int = int(len(data_list))
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("查询物料成功")
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                logger.info("查询物料成功查询没有数据")
                return HttpResponse(result)
        except Exception as e:
            logger.error("调取personmatter数据库有错误%s"% e)
            result = {"code": 1, "message": "调取失败", "data": ""}
            result = json.dumps(result)
            print(e)
            return HttpResponse(result)

    def post(self, request):
        """
        物料清单表
        :param request:
        :return:
        """

        try:
            db = DB()

            product_id = request.session.get("session_projectId")
            operate_user_code = request.session['session_currentId']
            conn = db.get_connection(product_id)
            conn_common = db.get_connection("db_common")

            sql_person = """
            select user_name from person where user_code = '{0}'
            """
            sql_person = sql_person.format(operate_user_code)
            dr_persons = db.execute_sql(conn_common, sql_person)
            if dr_persons:
                operate_user = dr_persons[0][0]
            else:
                operate_user = operate_user_code
            sql = """
             SELECT max(order_number) FROM person_matter;
            """
            matter_type = db.execute_sql(conn, sql)
            if matter_type[0][0] == None:
                id_num = 1
            else:
                id_num = matter_type[0][0] + 1
            json_data = request.body
            str_data = json.loads(json_data)

            matter_code = str_data.get("matter_code")

            matter_count = str_data.get("matter_count")
            product_time = str_data.get("product_time")

            order_number = id_num

            sql_insert = """
                       insert into Person_Matter(matter_code, matter_count, product_time, operate_user, order_number)
                       values('{0}', '{1}', '{2}', '{3}', '{4}')
                       """
            sql_insert_format = sql_insert.format(matter_code, matter_count, product_time, operate_user, order_number)
            drs = db.execute_sql(conn, sql_insert_format)

            data = {"code": 0, "message": "创建物料详情表成功"}
            logger.info("创建物料详情表成功")

            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:

            data = {"code": 1, "message": "创建物料详情表失败%s" % e}
            logger.error("创建物料详情表失败%s"% e)
            data = json.dumps(data)
            print(e)

            return HttpResponse(data)


class PutPersonMatter(View):
    """
    修改物料接口
    """
    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")

            db = DB()
            conn = db.get_connection(product_id)
            matter_code = request.GET.get("matter_code")
            matter_count = request.GET.get("matter_count")
            product_time = request.GET.get("product_time")
            operate_user = request.GET.get("operate_user")

            sql = """
             update person_matter set 
             matter_count ='{0}', product_time='{1}', operate_user = '{2}'
             where matter_code = '{3}'          
            """
            sql_main = sql.format(matter_count, product_time, operate_user, matter_code)
            drs = db.execute_sql(conn, sql_main)
            db.close_connection(conn)

            data = {"code": 0, "message": "修改成功"}
            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message":"修改失败"}
            logger.error("修改失败---->%s",e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeletePersonMatter(View):
    """
    删除物料接口

    """

    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)
            matter_code = request.GET.get("matter_code")
            sql = """
            delete from person_matter where matter_code = '{0}'
            """
            sql_main = sql.format(matter_code)
            des = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "删除成功"}

            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message":"删除失败"}
            data = json.dumps(data)
            return HttpResponse(data)


class CreateBOMProductList(View):
    """
    创建产品列表结构表
    """

    def get(self, request):
        try:
            table_list = []
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
            create table ProductList(prodect_code varchar(255) primary key not null,
            product_name varchar(255), product_id varchar(255), rule varchar(255),
            product_status varchar(255), description varchar(255), order_number int);          
            """
            dr = db.execute_sql(conn, sql)
            sql_main = """
                        show tables                 
                      """
            drs = db.execute_sql(conn, sql_main)
            for pe in drs:
                table_list.append(pe[0])

            if "productlist" in table_list:
                data = {"code": 0, "message": "操作成功"}
                logger.info("创建产品列表结构表成功")
            else:
                data = {"code": 1, "message": "操作失败"}
                logger.info("创建的表格已经存在")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": "操作失败-%s"%e}
            data = json.dumps(data)
            logger.error("创建表格失败！！%s"% e)

            return HttpResponse(data)


class CreateBOMMatterList(View):
    """
    创建物料结构表
    """
    def get(self, request):
        try:
            table_list = []
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                       create table matter_list(bom_matter_code varchar(64) primary key not null,
                    prodect_code varchar(64) not null,
                       matter_name varchar(64), rule varchar(64),matter_category varchar(64),
                       matter_usage int, order_number int)         
                       """
            dr = db.execute_sql(conn, sql)
            sql_main = """
                        show tables                 
                        """
            drs = db.execute_sql(conn, sql_main)
            for pe in drs:
                table_list.append(pe[0])

            if "matter_list" in table_list:
                data = {"code": 0, "message": "操作成功"}
                logger.info("创建产品物料列表结构表成功")
            else:
                data = {"code": 1, "message": "操作失败"}
                logger.info("创建产品物料已经存在")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": "操作失败-%s" % e}
            data = json.dumps(data)
            logger.error("创建产品物料列表结构表失败！！%s"% e)

            return HttpResponse(data)


class BOMProductList(View):
    """
    GET  查询产品列表
    post  插入产品名称 状态 型号等  新增产品列表
    产品信息插入db_common的数据库中 物料是进入相应的项目下加入相应的项目下的matter_list中
    create 多个表格
    """

    def get(self, request):
        try:
            data_list = []
            matter_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            product_name = request.GET.get("product_name")
            rule = request.GET.get("rule")
            product_status = request.GET.get("product_status")

            if product_id == "db_common":

                if product_id == "db_common":
                    s = ""
                else:
                    s = "and product_id =" + "'" + product_id + "'"

                if product_name:
                    product_name_sql = "and product_name = " + "'" + product_name + "'"
                else:
                    product_name_sql = ""
                if rule:
                    rule_sql = "and rule = " + "'" + rule + "'"
                else:
                    rule_sql = ""
                if product_status:
                    product_status_sql = "and product_status = " + "'" + product_status + "'"
                else:
                    product_status_sql = ""
                sql = """
                 select * from productlist where 2 > 1 {0} {1} {2} {3}
                """
                sql_main = sql.format(s, product_name_sql, rule_sql, product_status_sql)
                drs = db.execute_sql(db.get_connection("db_common"), sql_main)

                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["prodect_code"] = dr[0]
                        dict_data["product_name"] = dr[1]
                        dict_data["product_id"] = dr[2]
                        dict_data["rule"] = dr[3]
                        dict_data["product_status"] = dr[4]
                        dict_data["description"] = dr[5]
                        data_list.append(dict_data)
                    page_result = Page(page, page_size, data_list)
                    data = page_result.get_str_json()
                    sql_num_int = int(len(data_list))

                    data_add_int["data"] = data
                    data_add_int["total"] = sql_num_int

                    result = {"code": 0, "message": "操作成功", "data": data_add_int}
                    result = json.dumps(result)

                    return HttpResponse(result)

                else:
                    data_add_int["data"] = []
                    data_add_int["total"] = 0
                    result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                    result = json.dumps(result)
                    return HttpResponse(result)

            if product_id != "db_common":
                if product_name:
                    product_name_sql = "and product_name = " + "'" + product_name + "'"
                else:
                    product_name_sql = ""
                if rule:
                    rule_sql = "and rule = " + "'" + rule + "'"
                else:
                    rule_sql = ""
                if product_status:
                    product_status_sql = "and product_status = " + "'" + product_status + "'"
                else:
                    product_status_sql = ""
                sql = """
                 select * from productlist where product_id = '{0}' {1} {2} {3} 
                """
                sql_main = sql.format(product_id, product_name_sql, rule_sql, product_status_sql)
                drs = db.execute_sql(db.get_connection("db_common"), sql_main)
                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["prodect_code"] = dr[0]
                        dict_data["product_name"] = dr[1]
                        dict_data["product_id"] = dr[2]
                        dict_data["rule"] = dr[3]
                        dict_data["product_status"] = dr[4]
                        dict_data["description"] = dr[5]
                        sql_matter = """
                        select * from matter_list where prodect_code = '{0}'
                        """
                        sql_matter_format = sql_matter.format(dr[0])
                        matter_dfs = db.execute_sql(conn, sql_matter_format)
                        if matter_dfs:
                            respose_list = []
                            for matter_df in matter_dfs:
                                response_data = {}
                                response_data["bom_matter_code"] = matter_df[0]
                                response_data["prodect_code"] = matter_df[1]
                                response_data["matter_name"] = matter_df[2]
                                response_data["rule"] = matter_df[3]
                                response_data["matter_category"] = matter_df[4]
                                response_data["matter_usage"] = matter_df[5]
                                response_data["code_length"] = matter_df[6]
                                respose_list.append(response_data)
                            dict_data["response_datas"] = respose_list
                            data_list.append(dict_data)
                        else:
                            dict_data["response_datas"] = []
                            data_list.append(dict_data)
                            # data_list.append(response_data)

                    page_result = Page(page, page_size, data_list)
                    data = page_result.get_str_json()
                    if data_list:
                        sql_num_int = int(len(data_list))
                    else:
                        sql_num_int = 0

                    data_add_int["data"] = data
                    data_add_int["total"] = sql_num_int

                    result = {"code": 0, "message": "操作成功", "data": data_add_int}
                    result = json.dumps(result)

                    return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)

                return HttpResponse(result)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "调取BOM产品列表失败"}
            data = json.dumps(data)
            logger.error("查询产品列表失败%s"% e)

            return HttpResponse(data)

    def post(self, request):
        """
        新增产品  （在新增产品的同时会创建很多表格 例如人员、物料、工站、工序等）
        新增的产品内容会插入到db_common数据库的product_list表中,
        在项目（一个产品）的管理端增加产品的物料内容会进入到项目下的matter_list中

        :param request:
        :return:
        """

        try:
            product_id = request.session.get("session_projectId")

            print("===>, ", product_id)
            json_data = request.body
            str_data = json.loads(json_data)
            product_db = str_data.get("product_id")
            db = DB()
            db.create_database(product_db)
            conn = db.get_connection(product_db)
            sql_person = """
                        CREATE TABLE IF NOT EXISTS person(user_code varchar(64) primary key not null,
                        user_id varchar(64), user_name varchar(32),
                        user_password varchar(64), user_authority varchar(255), status varchar(10), 
                        user_product_id varchar(255),
                        user_role varchar(255),order_number int);
                        """
            dr = db.execute_sql(conn, sql_person)

            sql_matter = """           
                       CREATE TABLE IF NOT EXISTS Matter_List(bom_matter_code varchar(64) primary key not null,
                       prodect_code varchar(64) not null,
                       matter_name varchar(64), rule varchar(64),matter_category varchar(64),
                       matter_usage int, code_length int, order_number int)                                    
                     """
            dr = db.execute_sql(conn, sql_matter)

            sql_work = """
                            CREATE TABLE IF NOT EXISTS Work_Station(work_code varchar(255) primary key not null,
                            work_id varchar(255) not null,leader_work_id varchar(255),
                            work_name varchar(255), work_type varchar(255), order_number int)         
                            """
            dr = db.execute_sql(conn, sql_work)

            sql_process = """
                                          CREATE TABLE IF NOT EXISTS Process_Deal(production_code varchar(128) primary key not null,
                                          production_id varchar(128) not null,
                                          production_name varchar(128), work_id varchar(128),
                                          description varchar(128), order_number int)         
                                          """
            dr = db.execute_sql(conn, sql_process)

            sql_check = """
                            CREATE TABLE IF NOT EXISTS Check_ProductDeal(check_code varchar(128) primary key not null,
                            prodect_code varchar(128),
                            work_code varchar(128) not null,
                            production_code varchar(128), check_method varchar(128), order_number int)         
                            """
            dr = db.execute_sql(conn, sql_check)

            sql_product_plan = """
                            CREATE TABLE IF NOT EXISTS Product_PlanDeal(
                            product_plan_code varchar(128) primary key not null,
                            plan_name varchar(128), plan_count int, plan_start_day datetime, plan_end_day datetime, 
                            description varchar(128), plan_status varchar(255), order_number int)         
                            """
            dr = db.execute_sql(conn, sql_product_plan)

            sql_pick_matter = """
                                   CREATE TABLE IF NOT EXISTS Product_PickMatter(
                                   materials_production_code varchar(128) primary key not null,
                                   materials_person varchar(128) not null,
                                   product_plan_code varchar(128), material_time datetime, description varchar(128),
                                    order_number int)         
                                   """
            dr = db.execute_sql(conn, sql_pick_matter)

            sql_transit = """
                            CREATE TABLE IF NOT EXISTS ProductTransitInfo(product_transit_code varchar(128) primary key not null,
                                                 matter_code varchar(128), user_code varchar(128),
                                                 work_code varchar(128),
                                                 test_result varchar(128), 
                                                 description varchar(255), 
                                                 enter_time datetime,
                                                 out_time datetime,
                                                 product_plan_code varchar(128),
                                                 end_product_code varchar(128),
                                                 product_code varchar(128),                                     
                                                 order_number int)         
                                                 """
            dr = db.execute_sql(conn, sql_transit)

            sql_martial = """
                       CREATE TABLE IF NOT EXISTS Person_Matter(matter_code varchar(128) primary key not null,
                       matter_count int, product_time datetime, operate_user varchar(255), order_number int);
                       """
            dr = db.execute_sql(conn, sql_martial)

            sql_product_parameter = """
                                                 CREATE TABLE IF NOT EXISTS Product_Parameter(test_code varchar(128) primary key not null,
                                                 check_code varchar(128), test_parameter varchar(128),
                                                 test_parameter_count varchar(128),
                                                 test_status varchar(128), order_number int)         
                                                 """
            dr = db.execute_sql(conn, sql_product_parameter)

            sql_matters = """
                        CREATE TABLE IF NOT EXISTS Pick_Matter(materials_code varchar(128) primary key not null, 
                        materials_production_code varchar(128) not null,
                        matter_code varchar(128), matter_count int, order_number int)
                        """
            df = db.execute_sql(conn, sql_matters)

            sql_pick = """
                        CREATE TABLE IF NOT EXISTS Pick_box(pick_code varchar(255) primary key not null,
                        work_id varchar(255), 
                        pick_number int,
                        description varchar(255), order_number int)
                        """
            df = db.execute_sql(conn, sql_pick)

            sql_back = """
                        CREATE TABLE IF NOT EXISTS product_back_matter(materials_back_code varchar(255) primary key not null,
                        back_person varchar(255), 
                        product_plan_code varchar(255),
                        back_time datetime,
                        description varchar(255), order_number int)
                      """
            df = db.execute_sql(conn, sql_back)

            sql_deal_back = """
                        CREATE TABLE IF NOT EXISTS back_matter(deal_back_code varchar(255) primary key not null,
                        materials_back_code varchar(255), 
                        matter_code varchar(255),
                        matter_count int,
                        order_number int)
                      """
            df = db.execute_sql(conn, sql_deal_back)

            sql_enter_status = """           
            CREATE TABLE IF NOT EXISTS enter_storage_status(pack_id varchar(255) primary key not null,
                              product_id varchar(255),product_name varchar(255),
                              enter_user varchar(255), enter_time datetime, 
                              status varchar(255),product_plan_code varchar(255), order_number int)
            """
            db.execute_sql(conn, sql_enter_status)

            sql_enter = """
            CREATE TABLE IF NOT EXISTS enter_storage(enter_storage_code varchar(255) primary key not null, 
                              pack_id varchar(255),
                              finished_product_code varchar(255),
                              order_number int)
            """
            db.execute_sql(conn, sql_enter)

            sql_operate = """
            CREATE TABLE IF NOT EXISTS operate(ID int primary key not null, 
                     Package_Qty int,
                     Rv varchar(255),
                     Itemcode_C_Shipping varchar(255),
                     Supplier varchar(255),
                     No_Ship int,
                     CS_type varchar(255),
                     Shipping_SN_length int,
                     Product_length int,
                     order_number int);
            """
            db.execute_sql(conn, sql_operate)

            sql_function = """
                        CREATE TABLE IF NOT EXISTS function_list(function_list_code int AUTO_INCREMENT primary key not null, 
                                 function_name varchar(255));
                        """
            db.execute_sql(conn, sql_function)

            sql_work_tran = """
                        CREATE TABLE IF NOT EXISTS work_transit(table_code varchar(255) primary key not null,
                                              table_name varchar(255), work_code varchar(255),  
                                              description varchar(255),
                                              create_time datetime,
                                              order_number int)
            """
            db.execute_sql(conn, sql_work_tran)

            sql_file_list = """           
               CREATE TABLE IF NOT EXISTS field_list(field_code varchar(255) primary key not null, 
                                              table_name varchar(255),
                                              field_name varchar(255),  
                                              field_type varchar(255),
                                              field_PK varchar(255),
                                              field_NN varchar(255),
                                              field_AI varchar(255),order_number int)
            """
            db.execute_sql(conn, sql_file_list)

            sql_ = """
            CREATE TABLE IF NOT EXISTS process_matter_deal(process_matter_deal_code varchar(255) primary key not null,
                              work_id varchar(255) not null,
                              matter_code varchar(255),
                               install_number int, order_number int)
            """
            db.execute_sql(conn, sql_)

            sql_Work_Unqualified_Result = """
            CREATE TABLE IF NOT EXISTS Work_Unqualified_Result(unqualified_result_code varchar(255) primary key not null,
                        work_id varchar(255), unqualified_result_name varchar(255),
                        content varchar(64), process_mode varchar(255), operate_user varchar(255), 
                        time DATETIME DEFAULT CURRENT_TIMESTAMP not null,order_number int);
            """
            db.execute_sql(conn, sql_Work_Unqualified_Result)

            sql_modify_station = """
            CREATE TABLE IF NOT EXISTS Modify_In_WorkStation(modify_in_workstation_code varchar(255) primary key not null,
                        product_name varchar(255), finished_product_code varchar(255), work_id varchar(255), 
                        product_plan_code varchar(255),
                        operate_user varchar(255), 
                        enter_time DATETIME DEFAULT CURRENT_TIMESTAMP not null,process_method varchar(255),
                        out_time datetime, 
                        status varchar(255),
                        order_number int);           
            """

            db.execute_sql(conn, sql_modify_station)


            sql_matter = """
            SELECT max(order_number) FROM matter_list;
            """
            matter_type = db.execute_sql(conn, sql_matter)
            if matter_type[0][0] == None:
                matter_num = 0
            else:
                matter_num = matter_type[0][0]

            conn_product = db.get_connection("db_common")

            sql_common = """
                        SELECT max(order_number) FROM matter_list;
                        """
            common_matter = db.execute_sql(conn_product, sql_common)
            if common_matter[0][0] == None:
                common_num = 0
            else:
                common_num = common_matter[0][0]

            sql = """
                         SELECT max(order_number) FROM productlist;
                """
            product_type = db.execute_sql(conn_product, sql)
            if product_type[0][0] == None:
                id_num = 1
            else:
                id_num = product_type[0][0] + 1
            prodect_code = str("Im_Product_" + str(id_num))
            product_name = str_data.get("product_name")
            rule = str_data.get("rule")
            product_status = str_data.get("product_status")
            description = str_data.get("description")
            response_datas = str_data.get("response_datas")

            order_number = id_num
            print("=-=->>>>>>",order_number)
            sql_insert = """
                        insert into productlist(prodect_code, product_name, product_id, rule,
                        product_status, description, order_number)
                        values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')
                        """
            sql_insert_format = sql_insert.format(prodect_code, product_name, product_db, rule, product_status,
                                                  description, order_number)
            print("=>", sql_insert_format)


            drs = db.execute_sql(conn_product, sql_insert_format)

            if product_id == "db_common":
                data = {"code": 0, "message": "创建产品详情表成功"}
                logger.info("创建产品详情表成功")

                data = json.dumps(data)

                return HttpResponse(data)
            else:
                print("=-=-=->09999")
                for response_data in response_datas:
                    # db = DB()
                    # conn = db.get_connection("db_common")
                    matter_name = response_data.get("matter_name")
                    rule = response_data.get("rule")
                    matter_category = response_data.get("matter_category")
                    matter_usage = response_data.get("matter_usage")
                    code_length = response_data.get("code_length")
                    matter_num = matter_num+1
                    common_num = common_num +1
                    bom_matter_code = str("Im_BOM_Matter_" + str(matter_num))
                    bom_matter_code2 = str("Im_BOM_Matter_" + str(common_num))
                    sql_response = """
                            insert into matter_list(bom_matter_code,prodect_code, matter_name, rule,
                            matter_category, matter_usage, code_length, order_number)
                            values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')
                    """
                    sql_response_format = sql_response.format(bom_matter_code, prodect_code, matter_name,
                                                              rule, matter_category, matter_usage,
                                                              code_length, matter_num)

                    sql_common_format = sql_response.format(bom_matter_code2, prodect_code, matter_name,
                                                              rule, matter_category, matter_usage, code_length,
                                                            common_num)
                    matter_drs = db.execute_sql(conn, sql_response_format)
                    matter_dfs = db.execute_sql(conn_product, sql_common_format)

                data = {"code": 0, "message": "创建产品详情表成功"}
                logger.info("创建产品详情表成功")

                data = json.dumps(data)

                return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建产品详情表失败"}
            logger.error("创建产品详情表失败%s" %e)
            data = json.dumps(data)
            return HttpResponse(data)


class PutBOMProductList(View):

    """
    修改产品列表

    """
    def get(self, request):
        try:

            db = DB()
            conn = db.get_connection("db_common")

            prodect_code = request.GET.get("prodect_code")
            product_name = request.GET.get("product_name")
            rule = request.GET.get("rule")
            product_status = request.GET.get("product_status")
            description = request.GET.get("description")
            response_datas = request.GET.get("response_datas")
            product_id = request.session['session_projectId']

            conn_project = db.get_connection(product_id)
            if response_datas:
                response_datas = eval(response_datas)
            else:
                response_datas = response_datas
            sql = """
                update productlist set 
                   product_name='{0}',rule='{1}',product_status='{2}', description ='{3}'
                   where prodect_code = '{4}'
                   """
            sql_main = sql.format(product_name, rule, product_status, description, prodect_code)
            drs = db.execute_sql(conn, sql_main)

            if product_id != "db_common":
                for response_data in response_datas:
                    bom_matter_code = response_data.get("bom_matter_code")
                    if bom_matter_code:
                        sql_delete = """
                         delete FROM matter_list where bom_matter_code = '{0}'
                        """
                        sql_delete_format = sql_delete.format(bom_matter_code)
                        db.execute_sql(conn_project, sql_delete_format)

                sql_after = """
                            SELECT max(order_number) FROM matter_list
                            """
                num = db.execute_sql(conn_project, sql_after)
                if num[0][0]:
                    sql_num = num[0][0]
                else:
                    sql_num = 0

                for response_data in response_datas:
                    # db = DB()
                    # conn = db.get_connection("db_common")
                    matter_name = response_data.get("matter_name")
                    rule = response_data.get("rule")
                    matter_category = response_data.get("matter_category")
                    matter_usage = response_data.get("matter_usage")
                    code_length = response_data.get("code_length")
                    sql_num = sql_num + 1
                    bom_matter_code = str("Im_BOM_Matter_" + str(sql_num))
                    sql_response = """
                                        insert into matter_list(bom_matter_code,prodect_code, matter_name, rule,
                                        matter_category, matter_usage, code_length, order_number)
                                        values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')
                                """
                    sql_response_format = sql_response.format(bom_matter_code, prodect_code, matter_name,
                                                              rule, matter_category, matter_usage, code_length, sql_num)
                    matter_drs = db.execute_sql(conn_project, sql_response_format)
                data = {"code": 0, "message": "修改成功"}

                data = json.dumps(data)

                db.close_connection(conn)

                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}
            logger.error("修改失败---->%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeleteBOMProductList(View):
    """
    删除产品列表的一行
    """
    def get(self, request):
        try:
            db = DB()
            db_base = request.GET.get("product_id")
            product_id = request.session['session_projectId']
            conn = db.get_connection("db_common")
            conn_project = db.get_connection(product_id)
            prodect_code = request.GET.get("prodect_code")

            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)

            if response_datas:
                for response_data in response_datas:
                    bom_matter_code = dict(response_data).get("bom_matter_code")
                    sql = """
                    delete from matter_list where bom_matter_code = '{0}'
                    """
                    sql_format = sql.format(bom_matter_code)
                    db.execute_sql(conn_project, sql_format)
            else:
                sql_database = """
                select product_id from productlist where prodect_code = '{0}'
                """
                sql_database = sql_database.format(prodect_code)
                drs_ids = db.execute_sql(conn, sql_database)
                drs_id = drs_ids[0][0]
                con_db = db.get_connection_nodb()
                sql_drop_db = """
                drop database {0}
                """
                sql_drop_db = sql_drop_db.format(drs_id)
                db.execute_sql(con_db, sql_drop_db)
                sql = """
                    delete from productlist where prodect_code = '{0}'
                    """
                sql_main = sql.format(prodect_code)
                des = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "删除成功"}
            logger.info("修改产品列表或者物料表成功")

            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("修改产品列表失败,%s"% e)
            return HttpResponse(data)


class BOMMatterList(View):

    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            conn = db.get_connection("db_common")
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            matter_name = request.Get.get("matter_name")
            rule = request.Get.get("rule")
            if len(rule) == 0 and len(matter_name) == 0:
                sql = """
                    select * from matter_list
                    """
                drs = db.execute_sql(conn, sql)
                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["prodect_code"] = dr[0]
                        dict_data["matter_name"] = dr[1]
                        dict_data["rule"] = dr[2]
                        dict_data["matter_usage"] = dr[3]
                        dict_data["code_length"] = dr[4]
                        dict_data["order_number"] = dr[5]
                        data_list.append(dict_data)

                    page_result = Page(page, page_size, data_list)
                    data = page_result.get_str_json()
                    sql_num = """
                                    select count(*) from matter_list
                                    """
                    dfs = db.execute_sql(conn, sql_num)
                    sql_num_int = dfs[0][0]

                    data_add_int["data"] = data
                    data_add_int["total"] = sql_num_int

            else:
                sql = """
                select * from matter_list where matter_name = '{0}' and rule = '{1}'               
                """
                sql_main = sql.format(matter_name, rule)
                drs = db.execute_sql(conn, sql_main)
                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["prodect_code"] = dr[0]
                        dict_data["matter_name"] = dr[1]
                        dict_data["rule"] = dr[2]
                        dict_data["matter_usage"] = dr[3]
                        dict_data["code_length"] = dr[4]
                        dict_data["order_number"] = dr[5]
                        data_list.append(dict_data)

                    page_result = Page(page, page_size, data_list)
                    data = page_result.get_str_json()
                    sql_num = """
                        select count(*) from matter_list 
                        where matter_name = '{0}' and rule = '{1}'
                          """
                    sql_format = sql_num.format(matter_name, rule)
                    dfs = db.execute_sql(conn, sql_format)
                    sql_num_int = dfs[0][0]

                    data_add_int["data"] = data
                    data_add_int["total"] = sql_num_int

            data = {"code": 0, "message": "操作成功", "data": data_add_int}
            data = json.dumps(data)
            logger.info("调取BOM产品列表失败")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "调取BOM产品列表失败"}
            data = json.dumps(data)
            logger.error("调取BOM产品列表失败")

            return HttpResponse(data)

    def post(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")

            sql = """
                         SELECT max(order_number) FROM matter_list;
                        """
            matter_type = db.execute_sql(conn, sql)
            if matter_type[0][0] == None:
                id_num = 1
            else:
                id_num = matter_type[0][0] + 1

            prodect_code = request.POST.get("prodect_code")
            matter_name = request.POST.get("matter_name")
            rule = request.POST.get("rule")
            matter_usage = request.POST.get("matter_usage")
            code_length = request.POST.get("code_length")
            order_number = id_num

            # prodect_code = "Im_Product_3"
            # matter_name = "键格"
            # rule = "发光"
            # matter_usage = 26
            # order_number = id_num

            # product_name = "键盘"
            # rule = "10,23,22"
            # product_status = "正常"
            # description = "办公用品"
            # order_number = id_num
            sql_insert = """
                        insert into matter_list(prodect_code, matter_name, rule,
                        matter_usage, code_length, order_number)
                        values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                        """
            sql_insert_format = sql_insert.format(prodect_code, matter_name, rule, matter_usage, code_length,
                                                  order_number)

            drs = db.execute_sql(conn, sql_insert_format)
            sql_after = """
                        SELECT max(order_number) FROM matter_list
                        """
            num = db.execute_sql(conn, sql_after)
            if num[0][0] == order_number:
                data = {"code": 0, "message": "创建物料详情表成功"}
                logger.info("创建物料详情表成功")
            else:
                data = {"code": 1, "message": "创建物料详情表失败"}
                logger.error("创建物料详情表失败")
            data = json.dumps(data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建物料详情表失败"}
            logger.error("创建物料详情表失败")
            data = json.dumps(data)


class CreateWorkStation(View):
    def get(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                create table Work_Station(work_code varchar(64) primary key not null,
                work_id varchar(64) not null,
                work_name varchar(64), work_type varchar(128), leader_work_id varchar(255),order_number int)         
                """
            dr = db.execute_sql(conn, sql)

            data = {"code": 0, "message": "操作成功"}
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}

        data = json.dumps(data)

        return HttpResponse(data)


class WorkStation(View):
    """
    查询工作站的信息--- 根据工站编号和工站名称
    """

    def get(self, request):
        try:
            data_list = []
            matter_list = []
            data_add_int = {}
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            work_id = request.GET.get("work_id")
            work_name = request.GET.get("work_name")

            if work_id:
                work_id_sql = " and work_id =" + "'" + work_id + "'"
            else:
                work_id_sql = ""
            if work_name:
                work_name_sql = " and work_name =" + "'" + work_name + "'"
            else:
                work_name_sql = ""

            sql = """
                select * from  work_station where 2>1 {0} {1}
                """
            sql_main = sql.format(work_id_sql, work_name_sql)
            drs = db.execute_sql(conn, sql_main)

            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["work_code"] = dr[0]
                    dict_data["work_id"] = dr[1]
                    dict_data["work_name"] = dr[3]
                    dict_data["work_type"] = dr[4]
                    dict_data["leader_work_id"] = dr[2]
                    data_list.append(dict_data)
                data_list.sort(key=lambda x: (x['work_id']), reverse=False)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num = """
                          select count(*) from work_station
                           """
                dfs = db.execute_sql(conn, sql_num)
                sql_num_int = dfs[0][0]

                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "调取成功", "data": data_add_int}
            result = json.dumps(result)
            return HttpResponse(result)
        except Exception as e:
            print(e)
            result = {"code": 0, "message": "调取失败", "data": e}
            result = json.dumps(result)
            logger.error("调取工站信息失败%s"% e)
            return HttpResponse(result)

    def post(self, request):
        """
        新增项目下的工站接口

        如果是新增加工工站 会创建加工工站过站信息表和不合格品表

        :param request:
        :return:
        """
        try:
            respose_data_json = request.body
            respose_data_dict = json.loads(respose_data_json)
            work_id_str = respose_data_dict.get("work_id")

            work_id = str("product_transit_") + str(work_id_str)
            work_name = respose_data_dict.get("work_name")
            work_type = respose_data_dict.get("work_type")
            leader_work_id = respose_data_dict.get("leader_work_id")

            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            sql = """
             SELECT max(order_number) FROM work_station;
            """
            works = db.execute_sql(conn, sql)
            if works[0][0] == None:
                id_num = 1
            else:
                id_num = works[0][0] + 1
            work_code = str("Im_WorkStation_" + str(id_num))

            sql_insert = """
                               insert into work_station(work_code, work_id, work_name,
                               work_type, leader_work_id, order_number)
                               values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')   
                        """
            sql_insert_format = sql_insert.format(work_code, work_id_str, work_name, work_type, leader_work_id, id_num)
            drs = db.execute_sql(conn, sql_insert_format)

            if work_type == "加工":
                # work_id = "check_" + str(work_id_str)
                # select_table = "product_transit_" +
                sql_create_table = """
                    CREATE TABLE IF NOT EXISTS {0}(product_transit_code varchar(128) primary key not null,
                                         matter_code varchar(128),
                                         matter_id varchar(128),
                                         finished_product_code varchar(128),
                                         user_code varchar(128),
                                         work_code varchar(128),
                                         test_result varchar(128),
                                         description varchar(255),
                                         enter_time datetime,
                                         out_time datetime,
                                         product_plan_code varchar(128),
                                         end_product_code varchar(128),
                                         product_code varchar(128),
                                         order_number int) 
                                     """
                sql_create_table_main = sql_create_table.format(work_id)
                dr = db.execute_sql(conn, sql_create_table_main)

                sql_un_table = str("unqualified_product_") + str(work_id_str)
                sql_create_un_table = """
                CREATE TABLE IF NOT EXISTS {0}(unqualified_product_code varchar(255) primary key not null,
                                                          product_plan_code varchar(255),
                                                          finished_product_code varchar(255),
                                                          matter_code varchar(255),
                                                          matter_id varchar(255),
                                                          description varchar(255),
                                                          leader_work_id varchar(255),
                                                          later_work_id varchar(255),
                                                          solve_method varchar(255),
                                                          solve_result varchar(255),
                                                          order_number int)
                """
                sql_create_un_table = sql_create_un_table.format(sql_un_table)
                db.execute_sql(conn, sql_create_un_table)
                data = {"code": 0, "message": "创建工站信息表和产品过站表成功"}

                data = json.dumps(data)
                logger.info("创建加工工站信息表和产品过站表成功%s")
                return HttpResponse(data)
            else:
                data = {"code": 0, "message": "创建工站信息表成功"}

                data = json.dumps(data)
                logger.info("创建工站信息表和产品过站表成功%s")

                return HttpResponse(data)

        except Exception as e:
            print(e)

            data = {"code":1, "message":"创建工站信息表失败"}
            data = json.dumps(data)
            logger.error("新增工站信息失败%s" % e)

            return HttpResponse(data)


class PutWorkStation(View):
    """
    修改工站信息
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            work_code = request.GET.get("work_code")
            work_id = request.GET.get("work_id")
            work_name = request.GET.get("work_name")
            work_type = request.GET.get("work_type")
            leader_work_id = request.GET.get("leader_work_id")

            sql = """
                    update work_station set 
                    work_id='{0}',work_name='{1}', work_type ='{2}', leader_work_id = '{3}'
                    where work_code = '{4}'
                    """
            sql_main = sql.format(work_id, work_name, work_type, leader_work_id, work_code)
            drs = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "修改成功", "data": ""}
            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("修改工站信息失败%s" % e)

            return HttpResponse(data)


class DeleteWorkStation(View):
    """
    删除工站信息
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            work_code = request.GET.get("work_code")
            sql = """
            delete FROM work_station where work_code = "{0}"           
            """
            sql_num = sql.format(work_code)
            drs = db.execute_sql(conn, sql_num)
            data = {"code": 0, "message": "删除成功"}
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败", "data": e}
            data = json.dumps(data)
            logger.error("删除工站信息失败%s" % e)

            return HttpResponse(data)


class CreateProductPlanDeal(View):

    def get(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                create table Product_PlanDeal(prodect_code varchar(128) not null,
                product_plan_code varchar(128) primary key not null,
                plan_name varchar(128), plan_count int, plan_start_day datetime, plan_end_day datetime, 
                description varchar(128), order_number int)         
                """
            dr = db.execute_sql(conn, sql)

            data = {"code": 0, "message":"操作成功"}
            # data = json.dumps(data)
        except Exception as e:
            print(e)
            data = {"code":1, "message":"操作失败"}

        data = json.dumps(data)

        return HttpResponse(data)


class ProductPlanDeal(View):
    """
    查询生产计划详情表接口   前端传入计划名称或者计划状态
    """

    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))
            product_plan_code = request.GET.get("product_plan_code")
            plan_name = request.GET.get("plan_name")
            plan_status = request.GET.get("plan_status")

            if plan_name:
                plan_name_sql = " and plan_name =" + "'" + plan_name + "'"
            else:
                plan_name_sql = ""
            if plan_status:
                plan_status_sql = " and plan_status =" + "'" + plan_status + "'"
            else:
                plan_status_sql = ""

            sql = """
                select * from product_plandeal where 2 >1 {0} {1}
                """
            sql = sql.format(plan_name_sql, plan_status_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["product_plan_code"] = dr[0]
                    dict_data["plan_name"] = dr[1]
                    dict_data["plan_count"] = dr[2]
                    s = dr[3]
                    s1 = s.strftime("%Y-%m-%d %H:%M:%S ")
                    dict_data["plan_start_day"] = s1
                    d = dr[4]
                    s2 = d.strftime("%Y-%m-%d %H:%M:%S ")
                    dict_data["plan_end_day"] = s2
                    dict_data["description"] = dr[5]
                    dict_data["plan_status"] = dr[6]
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()

                if data_list:

                    sql_num_int = int(len(data_list))
                else:
                    sql_num_int = 0

                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                result = {"code": 0, "message": "操作成功", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "查询失败"}
            data = json.dumps(data)
            logger.error("查询生产计划表信息失败%s" % e)
            return HttpResponse(data)

    def post(self, request):
        """
        新增生产计划---  进行中的计划只能新增一个  其他状态的计划可以有多个

        :param request:
        :return:
        """
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            sql = """
             SELECT max(order_number) FROM product_plandeal;
            """
            works = db.execute_sql(conn, sql)
            if works[0][0] == None:
                id_num = 1
            else:
                id_num = works[0][0] + 1

            order_number = id_num

            response_data_json = request.body
            response_data = json.loads(response_data_json)
            product_plan_code = str("Im_ProductPlan_" + str(id_num))

            plan_name = response_data.get("plan_name")
            plan_count = response_data.get("plan_count")
            plan_start_day = response_data.get("plan_start_day")
            plan_end_day = response_data.get("plan_end_day")
            description = response_data.get("description")
            plan_status = response_data.get("plan_status")
            sql_status = """
            select * from product_plandeal where plan_status = '进行中'
            """
            # sql_status = sql_status.format(plan_status)
            df_status = db.execute_sql(conn, sql_status)
            if df_status:
                if plan_status == "进行中":
                    result = {"code": 1, "message": "进行中的生产计划只能有一个，已经存在"}

                    result = json.dumps(result)

                    return HttpResponse(result)
                else:
                    sql_insert = """
                                                   insert into product_plandeal(product_plan_code,
                                                   plan_name, plan_count, plan_start_day, plan_end_day, description, plan_status, order_number)
                                                   values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')   
                                            """
                    sql_insert_format = sql_insert.format(product_plan_code, plan_name, plan_count,
                                                          plan_start_day, plan_end_day, description, plan_status,
                                                          order_number)
                    drs = db.execute_sql(conn, sql_insert_format)

                    data = {"code": 0, "message": "创建生产计划成功"}

                    data = json.dumps(data)
                    logger.info("创建生产计划成功")
                    return HttpResponse(data)
            else:
                sql_insert = """
                                               insert into product_plandeal(product_plan_code,
                                               plan_name, plan_count, plan_start_day, plan_end_day, description, plan_status, order_number)
                                               values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')   
                                        """
                sql_insert_format = sql_insert.format(product_plan_code, plan_name, plan_count,
                                                      plan_start_day, plan_end_day, description, plan_status,
                                                      order_number)
                drs = db.execute_sql(conn, sql_insert_format)

                data = {"code": 0, "message": "创建生产计划成功"}

                data = json.dumps(data)

                return HttpResponse(data)

        except Exception as e:
            print(e)

            data = {"code": 1, "message": "创建生产计划失败"}
            data = json.dumps(data)
            logger.error("新增生产计划表信息失败%s" % e)

            return HttpResponse(data)


class PutProductPlanDeal(View):
    """
    修改生产计划
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            product_plan_code = request.GET.get("product_plan_code")
            plan_name = request.GET.get("plan_name")
            plan_count = request.GET.get("plan_count")
            plan_start_day = request.GET.get("plan_start_day")
            plan_end_day = request.GET.get("plan_end_day")
            description = request.GET.get("description")
            plan_status = request.GET.get("plan_status")

            sql_status = """
                        select * from product_plandeal where plan_status = '进行中'
                        """
            df_status = db.execute_sql(conn, sql_status)
            if df_status:
                if df_status[0][0] == product_plan_code:
                    sql = """
                        update product_plandeal set plan_name='{0}', plan_count ='{1}', 
                        plan_start_day='{2}',plan_end_day = '{3}', description = '{4}', 
                        plan_status = '{5}' where product_plan_code = '{6}'
                        """
                    sql_main = sql.format(plan_name, plan_count,
                                          plan_start_day, plan_end_day, description, plan_status, product_plan_code)
                    drs = db.execute_sql(conn, sql_main)
                    data = {"code": 0, "message": "修改成功", "data": ""}
                    data = json.dumps(data)
                    logger.info("修改生产计划成功")

                    return HttpResponse(data)
                else:
                    result = {"code": 1, "message": "进行中的生产计划只能有一个,已经存在,不能修改为进行中"}
                    result = json.dumps(result)
                    logger.error("进行中的生产计划只能有一个,已经存在,不能修改为进行中")

                    return HttpResponse(result)

            else:
                sql = """
                            update product_plandeal set plan_name='{0}', plan_count ='{1}', 
                            plan_start_day='{2}',plan_end_day = '{3}', description = '{4}', 
                            plan_status = '{5}' where product_plan_code = '{6}'
                      """

                sql_main = sql.format(plan_name, plan_count,
                                      plan_start_day, plan_end_day, description, plan_status, product_plan_code)
                drs = db.execute_sql(conn, sql_main)

                data = {"code": 0, "message": "修改成功", "data": ""}
                data = json.dumps(data)

                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("修改生产计划表信息失败%s" % e)

            return HttpResponse(data)


class DeleteProductPlanDeal(View):
    """
    删除生产计划
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            product_plan_code = request.GET.get("product_plan_code")
            sql = """
            delete FROM product_plandeal where product_plan_code = "{0}"           
            """
            sql_num = sql.format(product_plan_code)
            drs = db.execute_sql(conn, sql_num)

            data = {"code":0, "message": "删除成功", "data":""}

            data = json.dumps(data)
            logger.info("删除生产计划成功")
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code":1, "message": "删除失败", "data":e}
            data = json.dumps(data)
            logger.error("删除生产计划表信息失败%s" % e)

            return HttpResponse(data)


class ProductCodeName(View):
    """
    返回产品的内码和产品名称
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            # product_id = request.session.get("session_projectId")
            # conn = db.get_connection(product_id)
            product_id = "db_common"
            conn = db.get_connection(product_id)
            sql = """
            select prodect_code,product_name from productlist
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["product_code"] = dr[0]
                data_dict["product_name"] = dr[1]
                data_list.append(data_dict)
            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回产品的内码和产品名称%s" % e)
            return HttpResponse(data)


class CreateProductPickMatter(View):
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
                       create table Product_PickMatter(materials_production_code varchar(128) primary key not null,
                       materials_person varchar(128) not null,
                       product_plan_code varchar(128), material_time datetime, description varchar(128), order_number int)         
                       """
            dr = db.execute_sql(conn, sql)

            sql_matter = """
            create table Pick_Matter(materials_code varchar(128) primary key not null, 
            materials_production_code varchar(128) not null,
            matter_code varchar(128), matter_count int, order_number int)
            """
            df = db.execute_sql(conn, sql_matter)

            data = {"code": 0, "message": "操作成功"}
            # data = json.dumps(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}

        data = json.dumps(data)

        return HttpResponse(data)


class ProductPickMatter(View):
    """
    查询生产领料
    """

    def get(self, request):
        try:
            data_list = []
            matter_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            materials_person = request.GET.get("materials_person")
            product_plan_code = request.GET.get("product_plan_code")

            if materials_person:
                materials_person_sql = "and materials_person = " + "'" + materials_person + "'"
            else:
                materials_person_sql = ""
            if product_plan_code:
                product_plan_code_sql = "and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""

            sql = """
            select * from product_pickmatter where 2 > 1 {0} {1} 
            """
            sql = sql.format(materials_person_sql, product_plan_code_sql)
            drs = db.execute_sql(conn, sql)

            for dr in drs:
                dict_data = {}
                dict_data["materials_production_code"] = dr[0]
                dict_data["materials_person"] = dr[1]
                dict_data["product_plan_code"] = dr[2]
                s = dr[3]
                s1 = s.strftime("%Y-%m-%d %H:%M:%S ")
                dict_data["material_time"] = s1

                dict_data["description"] = dr[4]
                sql_matter = """
                select * from pick_matter where materials_production_code = '{0}'
                """
                sql_matter_format = sql_matter.format(dr[0])
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                if matter_dfs:
                    respose_list = []
                    for matter_df in matter_dfs:
                        response_data = {}
                        response_data["materials_code"] = matter_df[0]
                        response_data["materials_production_code"] = matter_df[1]
                        response_data["matter_code"] = matter_df[2]
                        response_data["matter_count"] = matter_df[3]
                        respose_list.append(response_data)
                    dict_data["response_datas"] = respose_list
                    data_list.append(dict_data)

            page_result = Page(page, page_size, data_list)
            data = page_result.get_str_json()

            sql_num_int = int(len(data_list))
            data_add_int["data"] = data
            data_add_int["total"] = sql_num_int
            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("查询生产领料成功")
            return HttpResponse(result)

        except Exception as e:

            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("查询生产领料失败%s" % e)
            return HttpResponse(result)

    def post(self, request):
        try:

            json_data = request.body
            str_data = json.loads(json_data)

            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            sql_matter = """
                   SELECT max(order_number) FROM pick_matter;
                   """
            matter_type = db.execute_sql(conn, sql_matter)
            if matter_type[0][0] == None:
                matter_num = 0
            else:
                matter_num = matter_type[0][0]

            sql = """
                  SELECT max(order_number) FROM product_pickmatter;
                  """
            product_type = db.execute_sql(conn, sql)
            if product_type[0][0] == None:
                id_num = 1
            else:
                id_num = product_type[0][0] + 1

            materials_production_code = str("Im_Product_Pick_Matter_" + str(id_num))
            materials_person = str_data.get("materials_person")
            product_plan_code = str_data.get("product_plan_code")
            material_time = str_data.get("material_time")
            description = str_data.get("description")
            response_datas = str_data.get("response_datas")

            order_number = id_num

            sql_insert = """
                               insert into product_pickmatter(materials_production_code, materials_person, 
                               product_plan_code,
                               material_time, description, order_number)
                               values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                               """
            sql_insert_format = sql_insert.format(materials_production_code, materials_person,
                                                  product_plan_code, material_time,
                                                  description, order_number)
            drs = db.execute_sql(conn, sql_insert_format)
            for response_data in response_datas:
                # db = DB()
                # conn = db.get_connection("db_common")
                matter_code = response_data.get("matter_code")
                matter_count = response_data.get("matter_count")
                matter_num = matter_num + 1
                materials_code = str("Im_Materials_Pick_" + str(matter_num))
                sql_response = """
                               insert into pick_matter(materials_code, materials_production_code,matter_code, matter_count,
                               order_number)
                               values('{0}', '{1}', '{2}', '{3}', '{4}')
                       """
                sql_response_format = sql_response.format(materials_code, materials_production_code,
                                                          matter_code, matter_count,
                                                          matter_num)
                matter_drs = db.execute_sql(conn, sql_response_format)
            data = {"code": 0, "message": "创建领料表成功"}
            logger.info("创建领料表成功")
            data = json.dumps(data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建领料表失败"}
            logger.error("创建领料表失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PutProductPickMatter(View):
    """
    修改产品物料领料表
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            materials_production_code = request.GET.get("materials_production_code")
            materials_person = request.GET.get("materials_person")
            product_plan_code = request.GET.get("product_plan_code")
            material_time = request.GET.get("material_time")
            description = request.GET.get("description")

            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            else:
                response_datas = response_datas

            sql = """
                      update product_pickmatter set 
                      materials_person='{0}',product_plan_code='{1}', material_time ='{2}',
                      description= '{3}' where materials_production_code = '{4}'
                      """
            sql_main = sql.format(materials_person, product_plan_code, material_time, description,
                                  materials_production_code)
            drs = db.execute_sql(conn, sql_main)

            sql_matter_num = """
             SELECT max(order_number) FROM pick_matter
            """
            dras = db.execute_sql(conn, sql_matter_num)

            if dras[0][0] != None:
                sql_num = dras[0][0]
            else:
                sql_num = 0

            for response_data in response_datas:
                # materials_production_code = response_data.get("materials_production_code")
                materials_code = response_data.get("materials_code")
                # materials_production_code = response_data.get("materials_production_code")
                matter_code = response_data.get("matter_code")
                matter_count = response_data.get("matter_count")
                if materials_code:
                    sql = """
                       update pick_matter set materials_production_code = '{0}', 
                       matter_code = '{1}', matter_count ='{2}' where materials_code = '{3}'
                    """
                    sql = sql.format(materials_production_code, matter_code, matter_count, materials_code)
                    db.execute_sql(conn, sql)
                else:
                    sql_num = sql_num + 1

                    materials_code = str("Im_Materials_Pick_" + str(sql_num))

                    sql_response = """
                                          insert into pick_matter(materials_code,materials_production_code, 
                                          matter_code, matter_count, order_number) values('{0}',
                                           '{1}', '{2}', '{3}', '{4}')
                                  """
                    sql_response_format = sql_response.format(materials_code, materials_production_code,
                                                              matter_code, matter_count, sql_num)
                    db.execute_sql(conn, sql_response_format)

            data = {"code": 0, "message": "修改成功"}

            data = json.dumps(data)
            logger.info("修改物料领料表成功")
            db.close_connection(conn)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}
            logger.error("修改物料领料表失败---->%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeleteProductPickMatter(View):
    """
    删除产品物料领料表中的数据

    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            materials_production_code = request.GET.get("materials_production_code")
            response_datas = request.GET.get("response_datas")
            response_datas = eval(response_datas)
            if response_datas:
                for response_data in response_datas:
                    materials_code = dict(response_data).get("materials_code")
                    sql = """
                       delete from pick_matter where materials_code = '{0}'
                       """
                    sql_format = sql.format(materials_code)
                    db.execute_sql(conn, sql_format)
            else:
                sql_matter = """
                                  SELECT * FROM product_pickmatter where materials_production_code = '{0}'
                                  """
                sql_matter_format = sql_matter.format(materials_production_code)
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                for matter_df in matter_dfs:
                    materials_code = matter_df[0]
                    sql_delete = """
                       delete FROM pick_matter where materials_code = '{0}'
                       """
                    sql_delete_format = sql_delete.format(materials_code)
                    db.execute_sql(conn, sql_delete_format)
                sql = """
                       delete from product_pickmatter where materials_production_code = '{0}'
                       """
                sql_main = sql.format(materials_production_code)
                des = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "删除成功"}
            logger.info("删除生产物料领料表数据成功")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除生产物料领料表数据失败,%s" % e)
            return HttpResponse(data)


class NoPagePersonMatter(View):
    """
    不分页的物料查询,返回物料的code name 类别 数量
    """

    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            # conn = db.get_connection("db_common")
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
            select pm.matter_code, ml.matter_name, ml.rule, ml.matter_category, 
            pm.matter_count,pm.product_time,ml.code_length from person_matter as pm
            left join matter_list as ml on pm.matter_code = ml.bom_matter_code
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                dict_data = {}
                dict_data["matter_code"] = dr[0]
                dict_data["matter_name"] = dr[1]
                dict_data["rule"] = dr[2]
                dict_data["matter_category"] = dr[3]
                dict_data["matter_count"] = dr[4]
                s = dr[5]
                if s:
                    s1 = s.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    s1 = ""
                dict_data["product_time"] = s1
                dict_data["code_length"] = dr[6]
                data_list.append(dict_data)
            if data_list:
                sql_num_int = int(len(data_list))
            else:
                sql_num_int = 0

            data_add_int["data"] = data_list
            data_add_int["total"] = sql_num_int
            result = {"code": 0, "message": "调取成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("不分页的物料详情返回成功")
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("不分页的物料查询返回失败")
            return HttpResponse(result)


class CreateProcessDeal(View):
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
                              create table Process_Deal(production_code varchar(128) primary key not null,
                              production_id varchar(128) not null,
                              production_name varchar(128), prodect_code varchar(128), work_id varchar(128),
                               description varchar(128), order_number int)         
                              """
            dr = db.execute_sql(conn, sql)
            data = {"code": 0, "message": "操作成功"}
            # data = json.dumps(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
        data = json.dumps(data)

        return HttpResponse(data)


class ProcessDeal(View):
    """
    工序查询接口
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            current_person_id = request.session['session_currentId']
            conn = db.get_connection(product_id)
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))
            production_name = request.GET.get("production_name")
            work_id = request.GET.get("work_id")
            if production_name:
                production_name_sql = "and production_name =" + "'"+ production_name+"'"
            else:
                production_name_sql = ""

            if work_id:
                work_id_sql = "and work_id = " + "'" + work_id + "'"
            else:
                work_id_sql = ""

            sql = """
                       select * from  process_deal where 2>1 {0} {1}
                       """

            sql_main = sql.format(production_name_sql, work_id_sql)

            drs = db.execute_sql(conn, sql_main)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["production_code"] = dr[0]
                    dict_data["production_id"] = dr[1]
                    dict_data["production_name"] = dr[2]
                    dict_data["work_id"] = dr[3]
                    # dict_data["leader_work_id"] = dr[4]
                    dict_data["description"] = dr[4]
                    sql_matter = """
                            select * from process_matter_deal where work_id = '{0}'
                             """
                    sql_matter_format = sql_matter.format(dr[3])
                    matter_dfs = db.execute_sql(conn, sql_matter_format)
                    if matter_dfs:
                        respose_list = []
                        for matter_df in matter_dfs:
                            response_data = {}
                            response_data["process_matter_deal_code"] = matter_df[0]
                            response_data["work_id"] = matter_df[1]
                            response_data["matter_code"] = matter_df[2]
                            response_data["install_number"] = matter_df[3]
                            response_data["production_code"] = dr[0]
                            respose_list.append(response_data)
                        dict_data["response_datas"] = respose_list
                        data_list.append(dict_data)
                    else:
                        dict_data["response_datas"] = []
                        data_list.append(dict_data)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num_int = int(len(data_list))
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                data = {"code": 0, "message": "操作成功", "data": data_add_int}
                data = json.dumps(data)
                logger.info("工序查询成功%s" % data)
                return HttpResponse(data)

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                data = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                data = json.dumps(data)
                logger.info("工序查询成功,但是没有数据返回")

                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("工序查询失败%s"% e)
            return HttpResponse(data)

    def post(self, request):
        """
        新增工序---->  也就是在工站当中填加物料

        :param request:
        :return:
        """
        try:
            table_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            current_person_id = request.session['session_currentId']
            conn = db.get_connection(product_id)
            sql = """
                    SELECT max(order_number) FROM process_deal;
                   """
            works = db.execute_sql(conn, sql)
            if works[0][0] == None:
                id_num = 1
            else:
                id_num = works[0][0] + 1

            production_code = str("Im_Process_" + str(id_num))
            respose_data_json = request.body
            respose_data_dict = json.loads(respose_data_json)

            production_id = respose_data_dict.get("production_id")
            production_name = respose_data_dict.get("production_name")
            work_id = respose_data_dict.get("work_id")
            description = respose_data_dict.get("description")
            response_datas = respose_data_dict.get("response_datas")

            sql_check = """
            select * from process_deal where work_id = '{0}'
            """
            sql_check = sql_check.format(work_id)
            df_checks = db.execute_sql(conn, sql_check)
            if df_checks:
                data = {"code": 1, "message": "工站工序已经创建，请在相应工站里面修改，无需创建"}
                data = json.dumps(data)
                logger.error("工站工序已经创建，请在相应工站里面修改，无需创建")
                return HttpResponse(data)
            else:
                sql_insert = """          
                             insert into process_deal(production_code, production_id, production_name,
                              work_id, description, order_number)
                              values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')   
                            """
                sql_insert_format = sql_insert.format(production_code, production_id, production_name,
                                                      work_id, description, id_num)
                drs = db.execute_sql(conn, sql_insert_format)
                if response_datas:
                    for response_data in response_datas:
                        process_matter_deal_code = response_data.get("process_matter_deal_code")
                        matter_code = response_data.get("matter_code")
                        install_number = response_data.get("install_number")
                        if process_matter_deal_code:
                            sql_update = """
                            update process_matter_deal set matter_code = '{0}', 
                            install_number = '{1}',
                            work_id = '{2}',
                            where process_matter_deal_code = '{3}'
                            """
                            sql_update = sql_update.format(matter_code, install_number, work_id,
                                                           process_matter_deal_code)
                            drs = db.execute_sql(conn, sql_update)
                        else:

                            sql_matter_num = """
                                            SELECT max(order_number) FROM process_matter_deal
                                           """
                            dras = db.execute_sql(conn, sql_matter_num)
                            if dras[0][0] == None:
                                id_num = 1
                            else:
                                id_num = dras[0][0] + 1
                            process_matter_deal_code = str("Im_process_matter_deal_" + str(id_num))
                            sql_insert = """
                            insert into process_matter_deal(process_matter_deal_code, work_id, matter_code,
                                              install_number, order_number)
                                              values('{0}', '{1}', '{2}', '{3}', '{4}')   
                            """
                            sql_insert = sql_insert.format(process_matter_deal_code, work_id,
                                                           matter_code, install_number, id_num)
                            drs = db.execute_sql(conn, sql_insert)
                else:
                    pass

                data = {"code": 0, "message": "新增工序信息表成功"}

                data = json.dumps(data)
                logger.info("新增工序信息表成功%s" % data)

                return HttpResponse(data)
        except Exception as e:
            print(e)

            data = {"code": 1, "message": "新增工序信息表失败"}
            data = json.dumps(data)
            logger.error("新增工序信息表失败%s" % e)

            return HttpResponse(data)


class PutProcessDeal(View):
    """
    修改工序信息接口
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            production_code = request.GET.get("production_code")
            production_id = request.GET.get("production_id")
            production_name = request.GET.get("production_name")
            prodect_code = request.GET.get("prodect_code")
            work_id = request.GET.get("work_id")
            description = request.GET.get("description")
            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            for response_data in response_datas:
                # response_data = dict(response_data)
                process_matter_deal_code = response_data.get("process_matter_deal_code")
                install_number = response_data.get("install_number")
                if process_matter_deal_code:
                    sql = """
                    update process_matter_deal set install_number = '{0}' where process_matter_deal_code = '{1}'
                    """
                    sql = sql.format(install_number, process_matter_deal_code)
                    db.execute_sql(conn, sql)
                else:
                    matter_code = response_data.get("matter_code")
                    sql_matter_num = """
                                        SELECT max(order_number) FROM process_matter_deal
                                       """
                    dras = db.execute_sql(conn, sql_matter_num)
                    if dras[0][0] == None:
                        id_num = 1
                    else:
                        id_num = dras[0][0] + 1
                    process_matter_deal_code = str("Im_process_matter_deal_" + str(id_num))
                    sql_insert = """
                                            insert into process_matter_deal(process_matter_deal_code, work_id, matter_code,
                                                              install_number, order_number)
                                                              values('{0}', '{1}', '{2}', '{3}', '{4}')   
                                            """
                    sql_insert = sql_insert.format(process_matter_deal_code, work_id,
                                                   matter_code, install_number, id_num)
                    drs = db.execute_sql(conn, sql_insert)
            sql = """
                            update process_deal set 
                            production_id='{0}', production_name ='{1}',
                            work_id = '{2}', description = '{3}' 
                            where production_code = '{4}'
                            """
            sql_main = sql.format(production_id, production_name, work_id,
                            description, production_code)
            drs = db.execute_sql(conn, sql_main)
            data = {"code": 0, "message": "操作成功", "data": ""}
            data = json.dumps(data)
            logger.info("修改工序信息成功%s"% data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": "操作失败", "data":e}
            data = json.dumps(data)
            logger.error("修改工序信息失败%s"% e)
            return HttpResponse(data)


class DeleteProcessDeal(View):
    """
    删除工序信息数据----> 也就是删除工站下的领料数据
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            conn = db.get_connection(product_id)

            production_code = request.GET.get("production_code")

            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            if response_datas:
                for response_data in response_datas:
                    process_matter_deal_code = dict(response_data).get("process_matter_deal_code")
                    sql = """
                       delete from process_matter_deal where process_matter_deal_code = '{0}'
                       """
                    sql_format = sql.format(process_matter_deal_code)
                    db.execute_sql(conn, sql_format)

            else:
                process_list = []
                sql_matter = """
                              SELECT work_id FROM process_deal where production_code = '{0}'
                              """
                sql_matter_format = sql_matter.format(production_code)
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                if matter_dfs:
                    matter_df = matter_dfs[0][0]
                else:
                    matter_df = ""

                sql_delete = """
                                SELECT process_matter_deal_code FROM process_matter_deal where work_id = '{0}'
                               """
                sql_matter_format = sql_delete.format(matter_df)
                dfs = db.execute_sql(conn, sql_matter_format)
                for df in dfs:
                    sql_de = """
                                   delete from process_matter_deal where process_matter_deal_code = '{0}'
                                   """
                    sql_de = sql_de.format(df[0])
                    db.execute_sql(conn, sql_de)

                sql = """
                       delete from process_deal where production_code = '{0}'
                       """
                sql_format = sql.format(production_code)
                db.execute_sql(conn, sql_format)

            data = {"code": 0, "message": "操作成功", "data": ""}
            data = json.dumps(data)
            logger.info("删除工序中下的工站下添加的物料成功%s" % data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message":"操作失败", "data": e}
            data = json.dumps(data)
            logger.error("删除工序中下的工站下添加的物料失败%s"% e)
            return HttpResponse(data)


class ProductPlanCodeName(View):
    """
    返回生产计划内码和生产名称
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
            SELECT product_plan_code, plan_name FROM product_plandeal
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["product_plan_code"] = dr[0]
                data_dict["product_plan_name"] = dr[1]
                data_list.append(data_dict)
            data = {"code":0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回生产计划内码和生产名称成功%s" % data)
            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回生产计划内码和生产名称失败%s" % e)
            return HttpResponse(data)


class PersonCodeName(View):
    """
    返回人员的code和name（不分页）
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
                       SELECT user_code, user_name FROM person
                       """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["user_code"] = dr[0]
                data_dict["user_name"] = dr[1]
                data_list.append(data_dict)
            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回人员的内码和名字成功%s" % data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code":1, "message":"操作失败", "data":e}
            data = json.dumps(data)
            logger.error("返回人员的内码和名字失败%s" % e)

            return HttpResponse(data)


class WorkCodeName(View):
    """
    返回工站的内码和名称
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            # project_id = request.GET.get("project_id")
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            # conn = db.get_connection(project_id)
            sql = """
                       SELECT work_code, work_id, work_name FROM work_station
                       """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["work_code"] = dr[0]
                data_dict["work_id"] = dr[1]
                data_dict["work_name"] = dr[2]
                # data_dict["leader_work_id"] = dr[3]
                # data_dict["work_type"] = dr[4]
                data_list.append(data_dict)
            data_list.sort(key=lambda x: (x['work_id']), reverse=False)
            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回工站的内码和名称成功%s"% data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data":e}
            data = json.dumps(data)
            logger.error("返回工站的内码和名称失败%s"% e)

            return HttpResponse(data)


class CreateCheckProductDeal(View):
    def get(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                                     create table Check_ProductDeal(check_code varchar(128) primary key not null,
                                     prodect_code varchar(128),
                                     work_code varchar(128) not null,
                                     production_code varchar(128), check_method varchar(128), order_number int)         
                                     """
            dr = db.execute_sql(conn, sql)
            data = {"code": 0, "message": "操作成功"}

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
        data = json.dumps(data)

        return HttpResponse(data)


class CreateProductParameter(View):
    def get(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                                     create table Product_Parameter(test_code varchar(128) primary key not null,
                                     check_code varchar(128), test_parameter varchar(128),
                                     test_parameter_count varchar(128),
                                     test_status varchar(128), order_number int)         
                                     """
            dr = db.execute_sql(conn, sql)
            data = {"code": 0, "message": "操作成功"}

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
        data = json.dumps(data)

        return HttpResponse(data)


class CheckProductDeal(View):

    """
    c查询产品的检验的一些参数  ----》 现在好像是弃用了

    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            prodect_code = request.GET.get("prodect_code")
            work_code = request.GET.get("work_code")
            production_code = request.GET.get("production_code")
            check_method = request.GET.get("check_method")

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            if prodect_code:
                prodect_code_sql = " and prodect_code =" + "'" + prodect_code + "'"
            else:
                prodect_code_sql = ""
            if work_code:
                work_code_sql = " and work_code = " + "'" + work_code + "'"
            else:
                work_code_sql = ""
            if production_code:
                production_code_sql = " and production_code = " + "'" + production_code+"'"
            else:
                production_code_sql = ""
            if check_method:
                check_method_sql = " and check_method = " + "'"+check_method+"'"
            else:
                check_method_sql = ""

            sql = """
             select * from check_productdeal where 2 > 1 {0} {1} {2} {3}
            """
            sql_main = sql.format(prodect_code_sql, work_code_sql, production_code, check_method_sql)

            # sql_main = sql.format(matter_id_sql, matter_name_sql, matter_category_sql, status_sql)
            # print(sql_main)
            drs = db.execute_sql(conn, sql_main)
            for dr in drs:
                dict_data = {}
                dict_data["check_code"] = dr[0]
                dict_data["prodect_code"] = dr[1]
                dict_data["work_code"] = dr[2]
                dict_data["production_code"] = dr[3]
                dict_data["check_method"] = dr[4]
                # data_list.append(dict_data)

                sql_matter = """
                            select * from product_parameter where check_code = '{0}'
                            """
                sql_matter_format = sql_matter.format(dr[0])
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                if matter_dfs:
                    respose_list = []
                    for matter_df in matter_dfs:
                        response_data = {}
                        response_data["test_code"] = matter_df[0]
                        response_data["check_code"] = matter_df[1]
                        response_data["test_parameter"] = matter_df[2]
                        response_data["test_parameter_count"] = matter_df[3]
                        response_data["test_status"] = matter_df[4]
                        respose_list.append(response_data)
                    dict_data["response_datas"] = respose_list
                    data_list.append(dict_data)
                else:
                    dict_data["response_datas"] = []
                    data_list.append(dict_data)

            page_result = Page(page, page_size, data_list)
            data = page_result.get_str_json()

            sql_num = """
                                        select count(*) from check_productdeal 
                                        where 2 > 1 {0} {1} {2} {3}
                                          """
            sql_format = sql_num.format(prodect_code_sql, work_code_sql, production_code, check_method_sql)
            dfs = db.execute_sql(conn, sql_format)
            sql_num_int = dfs[0][0]

            data_add_int["data"] = data
            data_add_int["total"] = sql_num_int

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("c查询产品的检验的一些参数成功%s"% data)

            return HttpResponse(result)

        except Exception as e:
            logger.error("调取check_productdeal数据库有错误%s"% e)
            result = {"code": 1, "message": "调取失败", "data": ""}
            result = json.dumps(result)
            print(e)
            return HttpResponse(result)

    def post(self, request):

        """
        添加产品检查的一些参数   现在也弃用
        :param request:
        :return:
        """

        db = DB()
        product_id = request.session.get("session_projectId")
        conn = db.get_connection(product_id)

        try:
            json_data = request.body
            str_data = json.loads(json_data)
            sql_matter = """
                          SELECT max(order_number) FROM check_productdeal;
                          """
            checkproduct = db.execute_sql(conn, sql_matter)
            if checkproduct[0][0] == None:
                matter_num = 1
            else:
                matter_num = checkproduct[0][0] + 1
            sql = """
                 SELECT max(order_number) FROM product_parameter;
                 """
            product_parameter = db.execute_sql(conn, sql)
            if product_parameter[0][0] == None:
                id_num = 0
            else:
                id_num = product_parameter[0][0]

            check_code = str("Im_Check_Product_" + str(matter_num))
            prodect_code = str_data.get("prodect_code")
            work_code = str_data.get("work_code")
            production_code = str_data.get("production_code")
            check_method = str_data.get("check_method")
            response_datas = str_data.get("response_datas")

            sql_insert = """
                                      insert into check_productdeal(check_code, prodect_code, 
                                      work_code,
                                      production_code, check_method, order_number)
                                      values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                                      """
            sql_insert_format = sql_insert.format(check_code, prodect_code,
                                                  work_code, production_code,
                                                  check_method, matter_num)
            drs = db.execute_sql(conn, sql_insert_format)
            for response_data in response_datas:
                # db = DB()
                # conn = db.get_connection("db_common")
                test_parameter = response_data.get("test_parameter")
                test_parameter_count = response_data.get("test_parameter_count")
                test_status = response_data.get("test_status")
                id_num = id_num + 1
                test_code = str("Im_Test_" + str(id_num))
                sql_response = """
                                      insert into product_parameter(test_code, check_code, 
                                      test_parameter,test_parameter_count, test_status,
                                      order_number)
                                      values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                              """
                sql_response_format = sql_response.format(test_code, check_code, test_parameter,
                                                          test_parameter_count, test_status,
                                                          id_num)
                matter_drs = db.execute_sql(conn, sql_response_format)

            data = {"code": 0, "message": "创建检验详情表成功"}
            logger.info("创建检验详情表成功")
            data = json.dumps(data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建检验详情表失败"}
            logger.error("创建检验详情表失败%s" %e)
            data = json.dumps(data)
            return HttpResponse(data)


class PutCheckProductDeal(View):
    def get(self, request):
        """
        修改产品检查的一些参数， 现在弃用了
        :param request:
        :return:
        """
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            check_code = request.GET.get("check_code")
            prodect_code = request.GET.get("prodect_code")
            work_code = request.GET.get("work_code")
            production_code = request.GET.get("production_code")
            check_method = request.GET.get("check_method")

            response_datas = request.GET.get("response_datas")

            if response_datas:
                response_datas = eval(response_datas)
            else:
                response_datas = response_datas

            sql = """
                   update check_productdeal set 
                   prodect_code='{0}',work_code='{1}', production_code ='{2}'
                   ,check_method = '{3}' where check_code = '{4}'
                   """
            sql_main = sql.format(prodect_code, work_code, production_code, check_method, check_code)
            drs = db.execute_sql(conn, sql_main)

            for response_data in response_datas:
                test_code = response_data.get("test_code")
                if test_code:
                    sql_delete = """
                     delete FROM product_parameter where test_code = '{0}'
                    """
                    sql_delete_format = sql_delete.format(test_code)
                    db.execute_sql(conn, sql_delete_format)

            sql_after = """
                        SELECT max(order_number) FROM product_parameter
                        """
            num = db.execute_sql(conn, sql_after)
            if num[0][0]:
                sql_num = num[0][0]
            else:
                sql_num = 0

            for response_data in response_datas:
                # db = DB()
                # conn = db.get_connection("db_common")
                # check_code = response_data.get("check_code")
                test_parameter = response_data.get("test_parameter")
                test_parameter_count = response_data.get("test_parameter_count")
                test_status = response_data.get("test_status")
                sql_num = sql_num + 1
                test_code = str("Im_Test_" + str(sql_num))
                sql_response = """
                                    insert into product_parameter(test_code,check_code, test_parameter, test_parameter_count,
                                    test_status,order_number)
                                    values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                            """
                sql_response_format = sql_response.format(test_code, check_code, test_parameter, test_parameter_count,
                                                          test_status, sql_num)
                matter_drs = db.execute_sql(conn, sql_response_format)
            data = {"code": 0, "message": "修改成功"}

            data = json.dumps(data)

            db.close_connection(conn)
            logger.info("修改产品检查的一些参数成功%s")

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}
            logger.error("修改失败---->%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeleteCheckProductDeal(View):
    """
    删除检查的一些参数
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            check_code = request.GET.get("check_code")
            response_datas = request.GET.get("response_datas")
            response_datas = eval(response_datas)
            # materials_production_code = "Im_Product_Pick_Matter_1"
            # response_datas = [{"materials_code": "Im_Materials_Pick_1"}]
            if response_datas:
                for response_data in response_datas:
                    test_code = dict(response_data).get("test_code")
                    sql = """
                              delete from product_parameter where test_code = '{0}'
                              """
                    sql_format = sql.format(test_code)
                    db.execute_sql(conn, sql_format)
            else:
                sql_matter = """
                                         SELECT * FROM check_productdeal where check_code = '{0}'
                                         """
                sql_matter_format = sql_matter.format(check_code)
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                for matter_df in matter_dfs:
                    test_code = matter_df[0]
                    sql_delete = """
                              delete FROM product_parameter where test_code = '{0}'
                              """
                    sql_delete_format = sql_delete.format(test_code)
                    db.execute_sql(conn, sql_delete_format)
                sql = """
                              delete from check_productdeal where check_code = '{0}'
                              """
                sql_main = sql.format(check_code)
                des = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "删除成功"}
            logger.info("删除产品检查的参数成功")

            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除产品检查的参数失败,%s" % e)
            return HttpResponse(data)


class CreateProductTransitInfo(View):

    def get(self, request):
        try:
            db = DB()
            conn = db.get_connection("db_common")
            sql = """
                                     create table ProductTransitInfo(product_transit_code varchar(128) primary key not null,
                                     matter_code varchar(128), user_code varchar(128),
                                     work_code varchar(128),
                                     test_result varchar(128), 
                                     enter_time datetime,
                                     out_time datetime,
                                     product_plan_code varchar(128),
                                     end_product_code varchar(128),
                                     product_code varchar(128),                                     
                                     order_number int)         
                                     """
            dr = db.execute_sql(conn, sql)
            data = {"code": 0, "message": "操作成功"}

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
        data = json.dumps(data)

        return HttpResponse(data)


class ProductTransitInfo(View):
    """
    产品过站信息查询

    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            conn = db.get_connection(product_id)
            sql_work_code = """
                       SELECT work_code FROM work_station where work_id = '{0}'
                       """
            sql_work_code_main = sql_work_code.format(session_work_id)
            drss = db.execute_sql(conn, sql_work_code_main)
            work_code = drss[0][0]

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            matter_code = request.GET.get("matter_code")
            finished_product_code = request.GET.get("finished_product_code")
            matter_id = request.GET.get("matter_id")
            user_code = request.GET.get("user_code")
            description = request.GET.get("description")
            # work_code = request.GET.get("work_code")
            test_result = request.GET.get("test_result")
            enter_time = request.GET.get("enter_time")
            out_time = request.GET.get("out_time")
            product_plan_code = request.GET.get("product_plan_code")
            product_code = request.GET.get("product_code")


            if matter_code:
                matter_code_sql = " and matter_code =" + "'" + matter_code + "'"
            else:
                matter_code_sql = ""
            if user_code:
                user_code_sql = " and user_code = " + "'" + user_code + "'"
            else:
                user_code_sql = ""
            if work_code:
                work_code_sql = " and work_code = " + "'" + work_code+"'"
            else:
                work_code_sql = ""
            if test_result:
                test_result_sql = " and test_result = " + "'"+test_result+"'"
            else:
                test_result_sql = ""
            # if enter_time:
            #     enter_time_sql = " and enter_time = " + "'"+enter_time+"'"
            # else:
            #     enter_time_sql = ""
            if out_time:
                out_time_sql = " and out_time = " + "'"+out_time+"'"
            else:
                out_time_sql = ""
            if product_plan_code:
                product_plan_code_sql = " and product_plan_code = " + "'"+product_plan_code+"'"
            else:
                product_plan_code_sql = ""
            if product_code:
                product_code_sql = " and product_code = " + "'" + product_code + "'"
            else:
                product_code_sql = ""

            if finished_product_code:
                finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            select_table = str("product_transit_") + str(session_work_id)

            sql = """
             select * from {0} where 2 > 1 {1} {2} {3} {4} {5} {6} {7} {8} 
            """

            sql_main = sql.format(select_table, matter_code_sql, finished_product_code_sql, user_code_sql,
                                  work_code_sql, test_result_sql,
                                  out_time_sql,
                                  product_plan_code_sql, product_code_sql)
            drs = db.execute_sql(conn, sql_main)

            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["product_transit_code"] = dr[0]
                    dict_data["matter_code"] = dr[1]
                    dict_data["matter_id"] = dr[2]
                    dict_data["finished_product_code"] = dr[3]
                    dict_data["user_code"] = dr[4]
                    dict_data["work_code"] = dr[5]
                    dict_data["test_result"] = dr[6]
                    dict_data["description"] = dr[7]
                    if dr[8]:
                        dp = dr[8]
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["enter_time"] = dp
                    else:
                        dict_data["enter_time"] = ""
                    ds = dr[9]
                    sq = ds.strftime("%Y-%m-%d %H:%M:%S ")
                    dict_data["out_time"] = sq
                    dict_data["product_plan_code"] = dr[10]
                    dict_data["end_product_code"] = dr[11]
                    dict_data["product_code"] = dr[12]
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num = """
                           select count(*) from {0} where 2 > 1 {1} {2} {3} {4} {5} {6} {7} 
                           """
                sql_num_format = sql_num.format(select_table, matter_code_sql, user_code_sql, work_code_sql,
                                                test_result_sql,
                                                 out_time_sql, product_plan_code_sql,
                                                product_code_sql)
                dfs = db.execute_sql(conn, sql_num_format)

                sql_num_int = dfs[0][0]

                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("产品过站信息查询成功%s"% result)
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "无数据", "data": data_add_int}
                result = json.dumps(result)
                logger.info("产品过站信息查询成功但是没有数据%s" % result)
                return HttpResponse(result)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("产品过站信息查询失败%s"% e)

            return HttpResponse(data)

    def post(self, request):
        """
        加工产品过站信息新增   加工站的产品信息（包括物料信息）会进入product_transit_(work_id) 的表格里面,  不合格品也会进入到
        unqualified_product_（work_id）里面
        :param request:
        :return:
        """

        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_type = request.session.get('session_workType')

            str_data = request.body
            json_data = json.loads(str_data)
            session_work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            conn = db.get_connection(product_id)
            response_datas = json_data.get("response_datas")
            matter_code_list = []
            matter_id_list = []
            for response_data in response_datas:
                matter_code_list.append(dict(response_data).get("matter_code"))
                matter_id_list.append(dict(response_data).get("matter_id"))
            matter_code = matter_code_list
            matter_id = matter_id_list
            finished_product_code = json_data.get("finished_product_code")
            test_result = json_data.get("test_result")
            description = json_data.get("description")

            out_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            product_plan_code = json_data.get("product_plan_code")
            product_code = json_data.get("product_code")

            if test_result == "FAIL":
                tables_list = []

                un_pro_table = str("unqualified_product_") + str(session_work_id)

                sql_unqualified_product = """
                                         SELECT max(order_number) FROM {0};
                                         """
                sql_unqualified_product = sql_unqualified_product.format(un_pro_table)
                unqualified_product_nums = db.execute_sql(conn, sql_unqualified_product)
                if unqualified_product_nums[0][0]:
                    matter_num = unqualified_product_nums[0][0]
                else:
                    matter_num = 0

                s = 0

                for matter_code_one in matter_code:
                    matter_num = matter_num + 1
                    matter_id_one = matter_id_list[s]
                    unqualified_product_code = str("Im_Unqualified_Product_" + str(matter_num))
                    sql_insert = """
                        insert into {0}(unqualified_product_code, product_plan_code, matter_code, matter_id, 
                        finished_product_code,
                        description, order_number)
                                        values('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')
                    """
                    sql_insert_main = sql_insert.format(un_pro_table, unqualified_product_code,
                                                        product_plan_code, matter_code_one, matter_id_one,
                                                        finished_product_code, description, matter_num)
                    db.execute_sql(conn, sql_insert_main)
                    s += 1
            sql_work_code = """
            SELECT work_code FROM work_station where work_id = '{0}'
            """
            sql_work_code_main = sql_work_code.format(session_work_id)
            drss = db.execute_sql(conn, sql_work_code_main)
            work_code = drss[0][0]

            select_table = str("product_transit_") + str(session_work_id)

            dater = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sql_producttransit = """
                                      SELECT max(order_number) FROM {0};
                                      """
            sql_producttransit_main = sql_producttransit.format(select_table)
            producttransit = db.execute_sql(conn, sql_producttransit_main)
            if producttransit[0][0] == None:
                matter_num = 0
            else:
                matter_num = producttransit[0][0]
            # end_product_code = product_id + "_" + dater + "_" + str(matter_num + 1)
            s = 0
            reponse_data_list = []
            for matter_code_one in matter_code:
                dict_data = {}

                matter_num = matter_num + 1
                matter_id_one = matter_id_list[s]
                product_transit_code = str("Im_Product_Transit_" + str(matter_num))
                print("===>", product_transit_code)

                sql_insert = """
                                            insert into {0}(product_transit_code, matter_code, matter_id,
                                             finished_product_code, user_code,
                                              work_code, test_result, description, out_time, product_plan_code, 
                                              end_product_code, product_code,
                                              order_number)
                                              values('{1}', '{2}', '{3}', '{4}', '{5}', '{6}','{7}', 
                                              '{8}', '{9}', '{10}', '{11}', '{12}','{13}')
                                            """
                sql_insert_main = sql_insert.format(select_table, product_transit_code, matter_code_one, matter_id_one,
                                                    finished_product_code, user_code, work_code,
                                                    test_result, description, out_time,
                                                    product_plan_code, matter_id_one, product_code, matter_num)
                drs = db.execute_sql(conn, sql_insert_main)
                s +=1

            data = {"code": 0, "message": "操作成功", "data": reponse_data_list}
            data = json.dumps(data)
            logger.info("加工过站信息新增成功%s" % data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("加工信息新增失败%s"% e)
            return HttpResponse(data)


class MatterNameCode(View):
    """
    返回物料的名称和物料的内码
    """
    def get(self, request):
        try:
            data_list = []

            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
             SELECT pm.matter_code, ml.matter_name FROM person_matter as pm left join matter_list as ml
              on pm.matter_code = ml.bom_matter_code
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["matter_code"] = dr[0]
                data_dict["matter_name"] = dr[1]
                data_list.append(data_dict)

            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回物料的名称和物料的内码成功%s"% data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回物料的名称和物料的内码失败%s" % e)

            return HttpResponse(data)


class ProcessNameCode(View):
    """
    返回工序的名称和内码

    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            sql = """
             SELECT production_code, production_name FROM process_deal
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["production_code"] = dr[0]
                data_dict["production_name"] = dr[1]
                data_list.append(data_dict)

            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回工序的名称和内码成功%s" % data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回工序的名称和内码失败%s" % e)

            return HttpResponse(data)


class CurrentUserInfo(View):
    """
    当前登录的信息（包括带入的work_id, 角色, 类型）
    """
    def get(self, request):
        try:
            dict_data = {}
            product_id = request.session.get("session_projectId")

            work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            work_type = request.session.get("session_workType")
            db = DB()

            if product_id:
                conn_num = db.get_connection(product_id)
                sql_num = """
                 SELECT pick_number FROM pick_box where work_id = '{0}'
                """
                sql_num = sql_num.format(work_id)
                drs = db.execute_sql(conn_num, sql_num)

                if drs:
                    pick_number = drs[0][0]
                else:
                    pick_number = 0
                sql = """
                       select * from person where user_code = '{0}'
                       """
                sql_main = sql.format(user_code)
                drs = db.execute_sql(conn_num, sql_main)


                if drs:
                    for dr in drs:
                        dict_data["user_code"] = dr[0]
                        dict_data["user_id"] = dr[1]
                        dict_data["user_name"] = dr[2]
                        dict_data["user_password"] = dr[3]
                        dict_data["user_authority"] = dr[4]
                        dict_data["status"] = dr[5]
                        dict_data["user_product_id"] = dr[6]
                        dict_data["user_role"] = dr[7]
                        dict_data["product_id"] = product_id
                        dict_data["work_type"] = work_type
                        dict_data["pick_number"] = pick_number
                        dict_data["work_id"] = work_id
                    data = {"code": 0, "message": "操作成功", "data": dict_data}
                    data = json.dumps(data)
                    logger.info("当前登录人的信息返回成功%s"% data)
                    return HttpResponse(data)
                else:

                    conn_conm = db.get_connection("db_common")
                    sql = """
                    select * from person where user_code = '{0}'
                    """
                    sql = sql.format(user_code)
                    drs = db.execute_sql(conn_conm, sql)
                    for dr in drs:
                        dict_data["user_code"] = dr[0]
                        dict_data["user_id"] = dr[1]
                        dict_data["user_name"] = dr[2]
                        dict_data["user_password"] = dr[3]
                        dict_data["user_authority"] = dr[4]
                        dict_data["status"] = dr[5]
                        dict_data["user_product_id"] = dr[6]
                        dict_data["user_role"] = dr[7]
                        dict_data["product_id"] = product_id
                        dict_data["work_type"] = ""
                        dict_data["pick_number"] = pick_number
                        dict_data["work_id"] = ""
                    data = {"code": 0, "message": "操作成功", "data": dict_data}
                    data = json.dumps(data)
                    logger.info("当前登录人的信息返回成功%s"% data)
                    return HttpResponse(data)

            else:
                product_id = "db_common"
                conn_num = db.get_connection(product_id)
                sql_num = """
                        SELECT pick_number FROM pick_box where work_id = '{0}'
                       """
                sql_num = sql_num.format(work_id)
                drs = db.execute_sql(conn_num, sql_num)

                if drs:
                    pick_number = drs[0][0]
                else:
                    pick_number = 0
                sql = """
                      select * from person where user_code = '{0}'
                      """
                sql_main = sql.format(user_code)
                drs = db.execute_sql(conn_num, sql_main)
                print("------>>>", drs)
                for dr in drs:
                    dict_data["user_code"] = dr[0]
                    dict_data["user_id"] = dr[1]
                    dict_data["user_name"] = dr[2]
                    dict_data["user_password"] = dr[3]
                    dict_data["user_authority"] = dr[4]
                    dict_data["status"] = dr[5]
                    dict_data["user_product_id"] = dr[6]
                    dict_data["user_role"] = dr[7]
                    dict_data["product_id"] = product_id
                    dict_data["work_type"] = ""
                    dict_data["pick_number"] = pick_number
                    dict_data["work_id"] = ""
                data = {"code": 0, "message": "操作成功", "data": dict_data}
                data = json.dumps(data)
                logger.info("当前登录人的信息返回成功%s"% data)
                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data":e}
            data = json.dumps(data)
            logger.info("当前登录人的信息返回失败%s" % e)

            return HttpResponse(data)


class ProjectSearchWorkcode(View):
    """
    返回工站的编码和工站的名称
    """
    def get(self, request):
        try:
            data_list = []
            product_id = request.GET.get("product_id")
            db = DB()
            conn = db.get_connection(product_id)
            sql = """
            select work_id, work_name from work_station
            """
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                data_dict = {}
                data_dict["work_id"] = dr[0]
                data_dict["work_name"] = dr[1]
                data_list.append(data_dict)
            data_list.sort(key=lambda x: (x['work_id']), reverse=False)
            data = {"code": 0, "message": "操作成功", "data": data_list}
            data = json.dumps(data)
            logger.info("返回工站的编码和工站的名称成功%s"% data)

            return HttpResponse(data)

        except Exception as e:
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回工站的编码和工站的名称失败%s" % e)
            return HttpResponse(data)


class GetProductId(View):
    """
    返回产品的编号和名称
    """

    def get(self, request):
        try:
            product_id_list = []

            db = DB()
            conn = db.get_connection("db_common")
            sql_product = """
                       select product_id, product_name from productlist
                       """
            dfs = db.execute_sql(conn, sql_product)
            for df in dfs:
                product_id_dict = {}
                product_id_dict["product_id"] = df[0]
                product_id_dict["product_name"] = df[1]
                product_id_list.append(product_id_dict)

            data = {"code": 0, "message": "操作成功", "data": product_id_list}
            data = json.dumps(data)
            logger.info("返回产品的编号和名称成功%s"% data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("返回产品的编号和名称失败%s" % e)

            return HttpResponse(data)


class UnqualifiedProduct(View):
    """
    不合格产品查询
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            conn = db.get_connection(product_id)
            product_plan_code = request.GET.get("product_plan_code")
            matter_code = request.GET.get("matter_code")
            solve_method = request.GET.get("solve_method")
            matter_id = request.GET.get("matter_id")
            finished_product_code = request.GET.get("finished_product_code")

            un_pro_table = str("unqualified_product_") + str(session_work_id)

            if finished_product_code:
                finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if product_plan_code:
                product_plan_code_sql = " and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""
            if matter_code:
                matter_code_sql = " and matter_code = " + "'" + matter_code + "'"
            else:
                matter_code_sql = ""
            if solve_method:
                solve_method_sql = " and solve_method = " + "'" + solve_method + "'"
            else:
                solve_method_sql = ""
            sql = """
                select * from {0} where 2 > 1 {1} {2} {3} {4} group by finished_product_code
               """
            sql_main = sql.format(un_pro_table, product_plan_code_sql, matter_code_sql,
                                  solve_method_sql, finished_product_code_sql)
            drs = db.execute_sql(conn, sql_main)

            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["unqualified_product_code"] = dr[0]
                    dict_data["product_plan_code"] = dr[1]
                    dict_data["finished_product_code"] = dr[2]
                    dict_data["matter_code"] = []
                    dict_data["matter_id"] = []
                    dict_data["description"] = dr[5]
                    dict_data["leader_work_id"] = dr[6]
                    dict_data["later_work_id"] = dr[7]
                    dict_data["solve_method"] = dr[8]
                    dict_data["solve_result"] = dr[9]
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num = """
                        select count(*) from {0} where 2 > 1 {1} {2} {3} {4} group by finished_product_code
                        """
                sql_num_format = sql_num.format(un_pro_table, product_plan_code_sql, matter_code_sql,
                                                solve_method_sql, finished_product_code_sql)
                dfs = db.execute_sql(conn, sql_num_format)
                sql_num_int = dfs[0][0]

                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("不合格产品查询成功%s"% data)

                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "无数据", "data": data_add_int}
                result = json.dumps(result)
                logger.error("不合格产品查询成功，但是没有数据%s" % result)
                return HttpResponse(result)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "查询错误", "data": e}
            data = json.dumps(data)
            logger.error("不合格产品查询失败，%s" % e)
            return HttpResponse(data)


class PutUnqualifiedProduct(View):
    """
    修改不合格产品
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            conn = db.get_connection(product_id)
            unqualified_product_code = request.GET.get("unqualified_product_code")
            product_plan_code = request.GET.get("product_plan_code")
            matter_code = request.GET.get("matter_code")
            solve_method = request.GET.get("solve_method")
            leader_work_id = request.GET.get("leader_work_id")
            later_work_id = request.GET.get("later_work_id")
            solve_result = request.GET.get("solve_result")
            matter_id = request.GET.get("matter_id")
            description = request.GET.get("description")
            un_pro_table = str("unqualified_product_") + str(session_work_id)
            sql_update_unqualified = """
            update {0} set product_plan_code = '{1}',
                       matter_code='{2}',matter_id= '{3}',description='{4}',solve_method='{5}', leader_work_id ='{6}'
                       ,later_work_id = '{7}', solve_result = '{8}' where unqualified_product_code = '{9}'
            """
            sql_update_unqualified_main = sql_update_unqualified.format(un_pro_table, product_plan_code, matter_code,
                                                                        matter_id, description, solve_method,
                                                                        leader_work_id, later_work_id,
                                                                        solve_result, unqualified_product_code)
            drs = db.execute_sql(conn, sql_update_unqualified_main)
            data = {"code": 0, "message": "修改成功", "data": []}
            data = json.dumps(data)
            logger.info("不合格产品修改成功，%s" % data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改错误", "data": e}
            data = json.dumps(data)
            logger.error("不合格产品修改失败%s"% e)

            return HttpResponse(data)


class DeleteUnqualifiedProduct(View):
    """
    删除不合格产品
    """
    def get(self, request):

        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            conn = db.get_connection(product_id)
            un_pro_table = str("unqualified_product_") + str(session_work_id)
            unqualified_product_code = request.GET.get("unqualified_product_code")

            sql = """
                      delete from {0} where unqualified_product_code = '{1}'
                      """
            sql_main = sql.format(un_pro_table, unqualified_product_code)
            des = db.execute_sql(conn, sql_main)

            data = {"code": 0, "message": "操作成功", "data": ""}
            data = json.dumps(data)
            logger.info("删除不合格产品成功%s"% data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("删除不合格产品失败%s"% e)

            return HttpResponse(data)


class QualifiedMatterCode(View):
    #
    #     过站的时候 检验过站的产品编码在上一站是否合格  如果不合格不让进入
    #     检验是否在数据库中 如果在数据库中  提醒扫描下一个
    #
    #     加工过站的时候相当于检验当时产品的接口
    #
    #

    def get_live_data(self, product_id, finished_product_code):
        func = product_live()
        data_list = func.one_product_live(product_id, finished_product_code)

        return data_list


    def get(self, request):
        try:
            db = DB()
            table_list = []
            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            user_code = request.session.get("session_currentId")
            finished_product_code = request.GET.get("finished_product_code")

            conn = db.get_connection(product_id)

            table_se = "product_transit_" + str(session_work_id)
            sql_check = """
                        select * from {0} where finished_product_code = '{1}'
                        """
            sql_check = sql_check.format(table_se, finished_product_code)
            drs_checks = db.execute_sql(conn, sql_check)
            if drs_checks:
                data = {"code": 1, "message": "产品编码已经在数据库中,请扫下一个"}
                data = json.dumps(data)
                logger.error("产品编码已经在数据库中,请扫下一个")
                return HttpResponse(data)
            else:
                da_list = self.get_live_data(product_id, finished_product_code)
                da_list.sort(key=lambda x: (x['time']), reverse=False)
                if da_list:
                    enter_work_code = da_list[-1]["work_code"]
                    test_result = da_list[-1]["test_result"]

                    print("=-=-=---=->", enter_work_code, test_result)

                    if test_result == "FAIL":
                        data = {"code": 1, "message": "产品的生命周期最后一站的状态是不合格,请进维修站或者其他"}
                        data = json.dumps(data)
                        logger.info("产品的生命周期最后一站的状态是不合格")
                        return HttpResponse(data)

                    else:

                        sql_work_id = """               
                        select work_id, leader_work_id from work_station where work_code = '{0}'
                        """
                        sql_work_id = sql_work_id.format(enter_work_code)
                        des = db.execute_sql(conn, sql_work_id)
                        print("==><><>", des)
                        if des:
                            current_id = des[0][0]
                            cureent_leader_id = des[0][1]
                            print("---->", current_id, cureent_leader_id)

                            if cureent_leader_id:
                                select_table = "product_transit_" + str(cureent_leader_id)
                                sql_check = """
                                            SELECT * FROM {0} where finished_product_code = '{1}'
                                            """
                                sql_check = sql_check.format(select_table, finished_product_code)
                                dfs = db.execute_sql(conn, sql_check)
                                if dfs:
                                    if session_work_id == current_id or session_work_id == cureent_leader_id:
                                        if test_result == "PASS":
                                            data = {"code": 0, "message": "操作成功", "data": test_result}
                                            data = json.dumps(data)
                                            logger.info("产品合格,可以进入下一步")
                                            return HttpResponse(data)
                                        else:
                                            data = {"code": 1, "message": "产品的生命周期最后一站检查结果是不合格的不能进入工站"}
                                            data = json.dumps(data)
                                            logger.info("产品的生命周期最后一站检查结果是不合格的不能进入工站")
                                            return HttpResponse(data)
                                    else:
                                        data = {"code": 1, "message": "产品的生命周期最后一站不是它本身或者是前一站"}
                                        data = json.dumps(data)
                                        logger.info("产品的生命周期最后一站不是它本身或者是前一站")
                                        return HttpResponse(data)

                            else:
                                data = {"code": 0, "message": "此产品经过的是第一工站"}
                                data = json.dumps(data)
                                logger.info("此产品经过的是第一工站")
                                return HttpResponse(data)

                        else:
                            pass

                else:
                    data = {"code": 0, "message": "此产品是经过没有经过任何工站"}
                    data = json.dumps(data)
                    logger.info("此产品码工站是第一工站")
                    return HttpResponse(data)


                # sql_search_leader_id = """
                # select leader_work_id from work_station where work_id = '{0}'
                # """
                # sql_search_leader_id = sql_search_leader_id.format(session_work_id)
                # dr_works = db.execute_sql(conn, sql_search_leader_id)
                # if dr_works:
                #     le_work_id = dr_works[0][0]


        except Exception as e:
            print(e)
            data = {"code": 0, "message": "查到前一工站里面的物料报错", "data": e}
            data = json.dumps(data)
            logger.error("查找前一工站里面的物料报错%s"% e)
            return HttpResponse(data)


    #
    # def get(self, request):
    #     try:
    #         db = DB()
    #         table_list = []
    #         product_id = request.session.get("session_projectId")
    #         session_work_id = request.session.get("session_workId")
    #         user_code = request.session.get("session_currentId")
    #         finished_product_code = request.GET.get("finished_product_code")
    #
    #         conn = db.get_connection(product_id)
    #
    #
    #
    #
    #         table_se = "product_transit_" + str(session_work_id)
    #         sql_check = """
    #                     select * from {0} where finished_product_code = '{1}'
    #                     """
    #         sql_check = sql_check.format(table_se, finished_product_code)
    #         drs_checks = db.execute_sql(conn, sql_check)
    #         if drs_checks:
    #             data = {"code": 1, "message": "产品编码已经在数据库中,请扫下一个"}
    #             data = json.dumps(data)
    #             logger.error("产品编码已经在数据库中,请扫下一个")
    #             return HttpResponse(data)
    #         else:
    #             sql_table = "unqualified_product_" + str(session_work_id)
    #
    #             sql = """
    #             show tables
    #             """
    #             drs = db.execute_sql(conn, sql)
    #             for dr in drs:
    #                 table_list.append(dr[0])
    #             if sql_table in table_list:
    #                 sql_check = """
    #                 SELECT * FROM {0} where finished_product_code = '{1}' and leader_work_id = '{2}'
    #                 """
    #                 sql_check = sql_check.format(sql_table, finished_product_code, session_work_id)
    #                 dfs = db.execute_sql(conn, sql_check)
    #                 if dfs:
    #                     test_result = "合格"
    #                     data = {"code": 0, "message": "操作成功", "data": test_result}
    #
    #                     data = json.dumps(data)
    #                     logger.info("产品合格,可以进入下一步")
    #                     return HttpResponse(data)
    #                 else:
    #                     sql_work_id = """
    #                     SELECT leader_work_id FROM work_station where work_id = "{0}";
    #                     """
    #                     sql_work_id = sql_work_id.format(session_work_id)
    #                     drs = db.execute_sql(conn, sql_work_id)
    #                     if drs[0][0]:
    #                         leader_work_id = drs[0][0]
    #                         select_work_table = str("product_transit_") + str(leader_work_id)
    #                         sql_table = """
    #                           SELECT test_result FROM {0} where finished_product_code = '{1}' group by finished_product_code
    #                         """
    #                         sql_table = sql_table.format(select_work_table, finished_product_code)
    #                         dfs = db.execute_sql(conn, sql_table)
    #                         if dfs:
    #                             test_result = dfs[0][0]
    #                             if test_result == "合格":
    #                                 data = {"code": 0, "message": "成功", "data": test_result}
    #                             else:
    #                                 data = {"code": 1, "message": "该产品上一工站不合格", "data": test_result}
    #                         else:
    #                             test_result = "找不到此成品码"
    #                             data = {"code": 1, "message": "找不到此成品码", "data": test_result}
    #
    #                         data = json.dumps(data)
    #                         return HttpResponse(data)
    #                     else:
    #                         data = {"code": 0, "message": "此工站是第一工站", "data": ""}
    #                         data = json.dumps(data)
    #                         logger.info("此工站是第一工站")
    #                         return HttpResponse(data)
    #             else:
    #                 sql_work_id = """
    #                                    SELECT leader_work_id FROM work_station where work_id = "{0}";
    #                                    """
    #                 sql_work_id = sql_work_id.format(session_work_id)
    #                 drs = db.execute_sql(conn, sql_work_id)
    #                 if drs[0][0]:
    #                     leader_work_id = drs[0][0]
    #                     select_work_table = str("product_transit_") + str(leader_work_id)
    #                     sql_table = """
    #                              SELECT test_result FROM {0} where finished_product_code = '{1}'
    #                              group by finished_product_code
    #                            """
    #                     sql_table = sql_table.format(select_work_table, finished_product_code)
    #                     dfs = db.execute_sql(conn, sql_table)
    #                     if dfs:
    #                         test_result = dfs[0][0]
    #                         # data = {"code": 0, "message": "成功", "data": test_result}
    #                         if test_result == "合格":
    #                             print("===>", "kkkkss")
    #                             data = {"code": 0, "message": "成功", "data": test_result}
    #                         else:
    #                             print("===>", "oooooss")
    #                             data = {"code": 1, "message": "该产品上一工站不合格", "data": test_result}
    #                     else:
    #                         test_result = "找不到此成品码"
    #                         data = {"code": 1, "message": "找不到此成品码", "data": test_result}
    #
    #                     data = json.dumps(data)
    #
    #                     return HttpResponse(data)
    #                 else:
    #                     data = {"code": 0, "message": "此工站是第一站,前面没有工站, 找不到数据", "data": ""}
    #                     data = json.dumps(data)
    #
    #                     return HttpResponse(data)
    #
    #     except Exception as e:
    #         print(e)
    #         data = {"code": 0, "message": "查到前一工站里面的物料报错", "data": e}
    #         data = json.dumps(data)
    #         logger.error("查找前一工站里面的物料报错%s"% e)
    #         return HttpResponse(data)
    #

class BomMatterCodeName(View):
    """
    返回物料的内码 名称 规格 长度
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            session_work_id = request.session.get("session_workId")
            conn = db.get_connection(product_id)

            sql = """
                SELECT bom_matter_code, matter_name, rule, code_length FROM matter_list;
                """
            sql = sql.format(session_work_id)
            drs = db.execute_sql(conn, sql)
            if drs:
                for df in drs:
                    matter_code_dict = {}
                    matter_code_dict["matter_code"] = df[0]
                    matter_code_dict["matter_name"] = df[1]
                    matter_code_dict["rule"] = df[2]
                    matter_code_dict["code_length"] = df[3]
                    data_list.append(matter_code_dict)

                data = {"code": 0, "message": "操作成功", "data": data_list}
                data = json.dumps(data)
                logger.info("返回物料的内码 名称 规格 长度成功%s"% data)
            else:
                data = {"code": 0, "message": "没有找到数据", "data": []}
                data = json.dumps(data)
                logger.info("返回物料的内码 名称 规格 长度成功 但是没有找到数据%s"% data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "调取matter_list数据库失败", "data": e}
            data = json.dumps(data)
            logger.error("返回物料的内码 名称 规格 长度失败%s" % data)
            return HttpResponse(data)


class WorkStationGetData(View):
    """
    工站的物料领料信息 安装数量
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            dict_data = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            current_person_id = request.session['session_currentId']
            # work_id = request.session['session_workId']
            conn = db.get_connection(product_id)
            # page = int(request.GET.get("page"))
            # page_size = int(request.GET.get("page_size"))
            sql_matter = """
                        select * from process_matter_deal where work_id = '{0}'
                         """
            sql_matter_format = sql_matter.format(work_id)
            matter_dfs = db.execute_sql(conn, sql_matter_format)
            if matter_dfs:
                respose_list = []
                for matter_df in matter_dfs:
                    response_data = {}
                    response_data["process_matter_deal_code"] = matter_df[0]
                    response_data["work_id"] = matter_df[1]
                    response_data["matter_code"] = matter_df[2]
                    response_data["install_number"] = matter_df[3]
                    respose_list.append(response_data)
                dict_data["response_datas"] = respose_list
                data_list.append(dict_data)

            else:
                dict_data["response_datas"] = []
                data_list.append(dict_data)

            data = {"code": 0, "message": "操作成功", "data": data_list}

            data = json.dumps(data)
            logger.info("工站的物料领料信息 安装数量成功%s"% data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("工站的物料领料信息 安装数量失败%s"% e)
            return HttpResponse(data)


class FinishedCodeGetMatterCodeID(View):
    """
    前端传入成品码 根据成品码得到陈成品码下面的物料等信息(产品维修工站的接口)

    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")

            finished_product_code = request.GET.get("finished_product_code")
            conn = db.get_connection(product_id)

            if finished_product_code:
                finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
                current_person_id = request.session['session_currentId']
                sql_tabale = """
                            show tables like "product_transit_%" 
                            """
                table_list = db.execute_sql(conn, sql_tabale)

                respose_list = []
                for table_type in table_list:
                    table_one = table_type[0]

                    sql_matter = """
                                           select finished_product_code, matter_code, matter_id, 
                                           product_transit_code from {0} where 2 > 1 {1}
                                            """
                    sql_matter_format = sql_matter.format(table_one, finished_product_code_sql)
                    matter_dfs = db.execute_sql(conn, sql_matter_format)
                    if matter_dfs:
                        for matter_df in matter_dfs:
                            response_data = {}
                            response_data["finished_product_code"] = matter_df[0]
                            response_data["matter_code"] = matter_df[1]
                            response_data["matter_id"] = matter_df[2]
                            response_data["work_id"] = table_one[16:]
                            response_data["product_transit_code"] = matter_df[3]
                            respose_list.append(response_data)
                    else:
                        pass
            else:
                respose_list = []
            data = {"code": 0, "message": "操作成功", "data": respose_list}
            data = json.dumps(data)
            logger.info("成品码得到成品码下面的物料等信息成功%s"% data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败", "data": e}
            data = json.dumps(data)
            logger.error("成品码得到成品码下面的物料等信息失败%s"% e)

            return HttpResponse(data)


class PutFinishedCodeGetMatterCodeID(View):
    """
    修改过站信息
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            response_datas = request.GET.get("response_datas")

            print("---<>", response_datas)

            if response_datas:
                response_datas = eval(response_datas)
            finished_product_code = request.GET.get("finished_product_code")
            return_work_id = request.GET.get("return_work_id")
            conn = db.get_connection(product_id)
            sql_tabale = """
                      show tables like "product_transit_%" 
                      """
            table_list = db.execute_sql(conn, sql_tabale)

            print("====>", finished_product_code)
            print("====---->", return_work_id)
            for table_type in table_list:
                for response_data in response_datas:

                    product_transit_code = response_data.get("product_transit_code")
                    matter_id = response_data.get("matter_id")
                    table_one = table_type[0]
                    sql_matter = """
                                      update {0} set matter_id = '{1}' 
                                      where product_transit_code = '{2}'
                                       """
                    sql_matter_format = sql_matter.format(table_one, matter_id, product_transit_code)
                    matter_dfs = db.execute_sql(conn, sql_matter_format)

            sql_select_table = "unqualified_product_" + str(return_work_id)
            sql_is_create_table = """
               CREATE TABLE IF NOT EXISTS {0}(unqualified_product_code varchar(255) primary key not null,
                              product_plan_code varchar(255), finished_product_code varchar(255), 
                              matter_code varchar(255), matter_id varchar(255),description varchar(255),
                              leader_work_id varchar(255), later_work_id varchar(255), solve_method varchar(255),
                              solve_result varchar(255), order_number int) 
            """
            sql_is_create_table = sql_is_create_table.format(sql_select_table)
            drs = db.execute_sql(conn, sql_is_create_table)

            sql_unqualified_product = """
                                     SELECT max(order_number) FROM {0};
                                     """
            sql_unqualified_product = sql_unqualified_product.format(sql_select_table)
            unqualified_product_nums = db.execute_sql(conn, sql_unqualified_product)
            if unqualified_product_nums[0][0]:
                matter_num = unqualified_product_nums[0][0] + 1
            else:
                matter_num = 1

            unqualified_product_code = "Im_Unqualified_Product_" + str(matter_num)

            sql_disqualification = """
            insert into {0}(unqualified_product_code, finished_product_code, leader_work_id, order_number)
                                              values('{1}', '{2}', '{3}','{4}')
            """
            sql_disqualification = sql_disqualification.format(sql_select_table, unqualified_product_code,
                                                               finished_product_code, return_work_id, matter_num)
            db.execute_sql(conn, sql_disqualification)

            print("-----------------------")

            modify_in_workstation_code = request.GET.get("modify_in_workstation_code")

            if modify_in_workstation_code:
                sql_modify_station = """
                select * from modify_in_workstation where modify_in_workstation_code = '{0}'            
                """
                sql_modify_station = sql_modify_station.format(modify_in_workstation_code)
                drs_modifys = db.execute_sql(conn, sql_modify_station)
                out_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                process_method = request.GET.get("process_method")
                status = request.GET.get("status")
                enter_work_code = request.GET.get("enter_work_code")

                print("---=--->", modify_in_workstation_code, process_method, status, enter_work_code)
                if drs_modifys:
                    sql_update_modify_sta_table = """
                                   update modify_in_workstation set out_time = '{0}', process_method = '{1}', status = '{2}'
                                                     where modify_in_workstation_code = '{3}'                   
                                   """
                    sql_update_modify_sta_table = sql_update_modify_sta_table.format(out_time, process_method,
                                                                                     status, modify_in_workstation_code)
                    db.execute_sql(conn, sql_update_modify_sta_table)
                else:
                    pass
                time.sleep(1)

                if process_method != "产品维修":
                    sql_a = """
                    select work_id from work_station where work_code = '{0}'
                    """
                    sql = sql_a.format(enter_work_code)

                    print("==>>>>",sql)
                    enters_ids = db.execute_sql(conn, sql)
                    if enters_ids:
                        select_table_str = enters_ids[0][0]
                        select_table = "product_transit_" + str(select_table_str)
                        print("===->", select_table)

                        sql_in = """
                                         select max(order_number) from {0}
                                        """
                        sql_in =sql_in.format(select_table)
                        id_num = db.execute_sql(conn, sql_in)
                        if id_num[0][0] == None:
                            id_num = 0
                        else:
                            id_num = id_num[0][0]
                        sql_one = """
                        select * from {0} where finished_product_code = '{1}'
                        """
                        sql_one = sql_one.format(select_table, finished_product_code)
                        drfs = db.execute_sql(conn, sql_one)

                        print("--------->", drfs)
                        if drfs:
                            in_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            for drf in drfs:
                                id_num += 1
                                product_transit_code = "Im_Product_Transit_" + str(id_num)
                                # dr_dict = {}
                                print(drf[1])
                                print(drf[2])
                                print(drf[3])
                                print(drf[4])
                                print(drf[5])
                                # dr_dict["matter_id"] =drf[2]
                                # dr_dict["finished_product_code"] =drf[3]
                                # dr_dict["user_code"] =drf[4]
                                # dr_dict["work_code"] =drf[5]
                                # dr_dict["test_result"] = "合格"
                                # dr_dict["description"] = drf[7]
                                # dr_dict["out_time"] = drf[9]
                                # dr_dict["product_plan_code"] = drf[10]
                                # dr_dict["end_product_code"] = drf[11]
                                # dr_dict["product_code"] = drf[12]

                                sql_insert = """
                                insert into {0}(product_transit_code, matter_code, matter_id, finished_product_code,user_code,
                                work_code,test_result, description, out_time, product_plan_code, end_product_code,product_code,
                                order_number)
                                values('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', 
                                '{8}', '{9}', '{10}', '{11}', '{12}', '{13}')                            
                                """
                                sql_insert = sql_insert.format(select_table, product_transit_code,
                                                               drf[1],drf[2], drf[3], drf[4], drf[5], "PASS",
                                                               drf[7], in_time, drf[10], drf[11], drf[12], id_num)
                                db.execute_sql(conn, sql_insert)

                        else:
                            pass

                    else:
                        data = {"code": 1, "message": "传入的来源工站内码找不到工站，请检查"}
                        data = json.dumps(data)
                        logger.info("传入的来源工站内码找不到工站，请检查")
                        return HttpResponse(data)


            data = {"code": 0, "message": "修改成功"}
            data = json.dumps(data)
            logger.info("修改过站信息成功")
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": e }

            data = json.dumps(data)
            logger.error("修改过站信息失败")
            return HttpResponse(data)


class DeleteFinishedCodeGetMatterCodeID(View):
    """
    解绑成品的物料内码
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            finished_product_code = request.GET.get("finished_product_code")
            return_work_id = request.GET.get("work_id")
            conn = db.get_connection(product_id)
            finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
            sql_tabale = """
                       show tables like "product_transit_%" 
                       """
            table_list = db.execute_sql(conn, sql_tabale)
            for table_type in table_list:
                table_one = table_type[0]
                sql_matter = """
                           delete from {0} where 2 > 1 {1}
                            """
                sql_matter_format = sql_matter.format(table_one, finished_product_code_sql)
                matter_dfs = db.execute_sql(conn, sql_matter_format)

            data = {"code": 0, "message": "重置成功"}

            data = json.dumps(data)
            logger.info("解绑或者重置成品的物料内码成功%s"% data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 0, "message": e}

            data = json.dumps(data)
            logger.error("解绑或者重置成品的物料内码失败%s"% e)
            return HttpResponse(data)


class Pick(View):
    """
    产品包装箱的查询

    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            work_id = request.GET.get("work_id")

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            if work_id:
                work_id_sql = "and work_id = " + "'" + work_id + "'"
            else:
                work_id_sql = ""

            sql = """
                        select * from pick_box where 2 > 1 {0}
                       """
            sql_main = sql.format(work_id_sql)

            drs = db.execute_sql(conn, sql_main)

            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["pick_code"] = dr[0]
                    dict_data["work_id"] = dr[1]
                    dict_data["pick_number"] = dr[2]
                    dict_data["description"] = dr[3]
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()

                sql_num = """
                            select count(*) from pick_box where 2 > 1 {0}
                            """
                sql_num_main = sql_num.format(work_id_sql)

                dfs = db.execute_sql(conn, sql_num_main)
                if dfs:
                    sql_num_int = dfs[0][0]
                else:
                    sql_num_int = 0
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("产品包装查询成功%s"% result)
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("产品包装查询失败%s"% e)
            return HttpResponse(result)

    def post(self, request):
        """
        产品包装箱
        :param request:
        :return:
        """
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            json_data = request.body
            str_data = json.loads(json_data)
            work_id = str_data.get("work_id")
            pick_number = str_data.get("pick_number")
            description = str_data.get("description")

            sql = """
                 select max(order_number) from pick_box
                """
            id_num = db.execute_sql(conn, sql)
            if id_num[0][0] == None:
                id_num = 1
            else:
                id_num = id_num[0][0] + 1

            pick_code = str(product_id) + "pickbox" + str(id_num)

            sql_insert = """
                        insert into pick_box(pick_code, work_id, pick_number, description,order_number)
                        values('{0}', '{1}', '{2}', '{3}', '{4}')
                        """

            sql_insert_format = sql_insert.format(pick_code, work_id, pick_number,
                                                  description, id_num)

            drs = db.execute_sql(conn, sql_insert_format)
            data = {"code": 0, "message": "创建包装箱成功"}

            data = json.dumps(data)
            logger.info("产品包装成功%s")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建包装箱失败"}

            data = json.dumps(data)
            logger.error("产品包装失败")

            return HttpResponse(data)


class PutPick(View):
    """
    修改产品的包装

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            pick_code = request.GET.get("pick_code")
            work_id = request.GET.get("work_id")
            pick_number = request.GET.get("pick_number")
            description = request.GET.get("description")

            sql_update = """
                       update pick_box set work_id='{0}',
                        pick_number='{1}',description='{2}' where pick_code = '{3}'
                       """

            sql_insert_format = sql_update.format(work_id, pick_number, description,
                                                  pick_code)

            drs = db.execute_sql(conn, sql_insert_format)
            data = {"code": 0, "message": "修改成功"}

            data = json.dumps(data)
            logger.info("修改产品的包装成功")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}

            data = json.dumps(data)
            logger.error("修改产品的包装失败")

            return HttpResponse(data)


class DeletePick(View):
    """
    删除包装

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            pick_code = request.GET.get("pick_code")
            sql_delete = """
                       delete from pick_box where pick_code = '{0}'
                       """
            sql_insert_format = sql_delete.format(pick_code)

            drs = db.execute_sql(conn, sql_insert_format)
            data = {"code": 0, "message": "删除成功"}

            data = json.dumps(data)
            logger.info("删除包装成功")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}

            data = json.dumps(data)
            logger.error("删除包装失败")
            return HttpResponse(data)


class FinishedProductStorage(View):
    """
    查询包装箱里面有哪些产品（产品编码）
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            enter_time = request.GET.get("enter_time")
            enter_user = request.GET.get("enter_user")
            product_plan_code = request.GET.get("product_plan_code")

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            conn = db.get_connection(product_id)

            if enter_time:
                enter_time_sql = "and enter_time = " + "'" + enter_time + "'"
            else:
                enter_time_sql = ""
            if enter_user:
                enter_user_sql = "and enter_user = " + "'" + enter_user + "'"
            else:
                enter_user_sql = ""

            if product_plan_code:
                product_plan_code_sql = " and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""
            sql = """
                    select * from enter_storage_status where 2 > 1 {0} {1} {2}
                   """
            sql = sql.format(enter_time_sql, enter_user_sql, product_plan_code_sql)

            drs = db.execute_sql(conn, sql)

            if drs:

                for dr in drs:
                    dict_data = {}
                    pick_id = dr[0]
                    print(pick_id)
                    dict_data["pack_id"] = dr[0]
                    dict_data["product_id"] = dr[1]
                    dict_data["product_name"] = dr[2]
                    dict_data["enter_user"] = dr[3]
                    s = dr[4]
                    s = s.strftime("%Y-%m-%d %H:%M:%S ")
                    dict_data["enter_time"] = s
                    dict_data["status"] = dr[5]
                    dict_data["product_plan_code"] = dr[6]

                    sql_status = """
                    select * from enter_storage where pack_id = '{0}'
                    """
                    sql_status = sql_status.format(pick_id)
                    dfs = db.execute_sql(conn, sql_status)

                    response_datas = []

                    for df in dfs:
                        datas_dict = {}
                        datas_dict["enter_storage_code"] = df[0]
                        datas_dict["pack_id"] = df[1]
                        datas_dict["finished_product_code"] = df[2]
                        response_datas.append(datas_dict)
                        dict_data["response_datas"] = response_datas
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()

                dfs = int(len(data_list))
                if dfs:
                    sql_num_int = dfs
                else:
                    sql_num_int = 0
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "操作成功", "data": data_add_int}

                result = json.dumps(result)
                logger.info("查询包装箱里面有哪些产品成功%s"% result)
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}

                result = json.dumps(result)
                return HttpResponse(result)
        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("查询包装箱里面有哪些产品失败%s"% e)
            return HttpResponse(result)

    def post(self, request):
        """
        产品入包装箱接口
        :param request:
        :return:
        """
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            enter_user = request.session.get("session_currentId")
            json_data = request.body
            str_data = json.loads(json_data)
            pack_id = str_data.get("pack_id")
            product_plan_code = str_data.get("product_plan_code")
            # product_name = str_data.get("product_name")
            status = "已包装"
            response_datas = str_data.get("response_datas")
            conn_product_name = db.get_connection("db_common")
            sql_product_name = """
            SELECT product_name FROM productlist where product_id = '{0}'
            """
            sql_product_name = sql_product_name.format(product_id)
            drs = db.execute_sql(conn_product_name, sql_product_name)
            if drs:
                product_name = drs[0][0]
            else:
                product_name = ""

            conn = db.get_connection(product_id)
            sql1 = """
            CREATE TABLE IF NOT EXISTS enter_storage(enter_storage_code varchar(255) primary key not null, 
                              pack_id varchar(255),
                              finished_product_code varchar(255),
                              order_number int) 
            """
            sql2 = """
            CREATE TABLE IF NOT EXISTS enter_storage_status(pack_id varchar(255) primary key not null,
                              product_id varchar(255),product_name varchar(255),
                              enter_user varchar(255), enter_time datetime, 
                              status varchar(255),product_plan_code varchar(255), order_number int)           
            """
            drs = db.execute_sql(conn, sql1)
            dfs = db.execute_sql(conn, sql2)

            sql_num1 = """
                             select max(order_number) from enter_storage
                            """
            id_num = db.execute_sql(conn, sql_num1)
            if id_num[0][0] == None:
                id_num = 0
            else:
                id_num = id_num[0][0]

            sql_num2 = """
                         select max(order_number) from enter_storage_status
                        """
            id_num2 = db.execute_sql(conn, sql_num2)
            if id_num2[0][0] == None:
                id_num2 = 1
            else:
                id_num2 = id_num2[0][0] + 1
            for response_data in response_datas:
                id_num += 1
                enter_storage_code = str("Im_enter_storage_") + str(id_num)
                pack_id = response_data.get("pack_id")
                finished_product_code = response_data.get("finished_product_code")
                # product_name = response_data.get("product_name")
                # enter_user = response_data.get("enter_user")

                sql_insert = """
                insert into enter_storage(enter_storage_code, pack_id, finished_product_code, order_number)
                values('{0}', '{1}','{2}','{3}')
                """
                sql_insert = sql_insert.format(enter_storage_code, pack_id, finished_product_code,
                                               id_num)

                drs = db.execute_sql(conn, sql_insert)
            enter_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            insert_sql = """
            insert into enter_storage_status(pack_id, product_id, 
            product_name, enter_user, enter_time, status, product_plan_code, order_number) 
            values('{0}', '{1}','{2}', '{3}', '{4}', '{5}', '{6}', '{7}')
            """
            insert_sql = insert_sql.format(pack_id, product_id, product_name, enter_user,
                                           enter_time, status, product_plan_code, id_num2)
            dfs = db.execute_sql(conn, insert_sql)

            data = {"code": 0, "message": "装包成功"}

            data = json.dumps(data)
            logger.info("产品装包i成功")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "装包失败"}

            data = json.dumps(data)
            logger.error("产品装包失败")

            return HttpResponse(data)


class PutFinishedProductStorage(View):
    """
    修改装包产品
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            enter_user = request.session.get("session_currentId")

            pack_id = request.GET.get("pack_id")
            # product_id = request.GET.get("product_id")
            product_name = request.GET.get("product_name")
            enter_user = request.GET.get("enter_user")
            enter_time = request.GET.get("enter_time")
            status = request.GET.get("status")
            product_plan_code = request.GET.get("product_plan_code")
            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)

            conn = db.get_connection(product_id)
            for response_data in response_datas:
                enter_storage_code = response_data.get("enter_storage_code")
                pack_id = response_data.get("pack_id")
                finished_product_code = response_data.get("finished_product_code")
                sql_update = """
                 update enter_storage set pack_id='{0}',
                        finished_product_code='{1}' where enter_storage_code = '{2}' 
                """
                sql_update = sql_update.format(pack_id, finished_product_code, enter_storage_code)
                db.execute_sql(conn, sql_update)
            sql_update_status = """
            update enter_storage_status set 
                        product_id='{0}', product_name = '{1}', enter_user = '{2}',enter_time = '{3}',
                        status = '{4}' , product_plan_code = '{5}' 
                        where pack_id = '{6}' 
            """
            sql_update_status = sql_update_status.format(product_id, product_name,
                                                         enter_user, enter_time, status, product_plan_code, pack_id)
            db.execute_sql(conn, sql_update_status)

            data = {"code": 0, "message": "修改成功"}

            data = json.dumps(data)
            logger.info("修改装包产品成功")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}

            data = json.dumps(data)
            logger.error("包装产品修改失败")
            return HttpResponse(data)


class DeleteFinishedProductStorage(View):
    """
    删除包装箱和包装箱里面的产品

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            enter_user = request.session.get("session_currentId")
            pack_id = request.GET.get("pack_id")
            # response_datas = request.GET.get("response_datas")
            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            else:
                response_datas = response_datas
            # product_id = "pen"
            # pack_id = "pen_20210803_1"
            # response_datas = []
            conn = db.get_connection(product_id)
            if response_datas:
                for response_data in response_datas:
                    storage_id = response_data.get("enter_storage_code")
                    sql_delete = """
                    delete FROM enter_storage where enter_storage_code = "{0}"
                    """
                    sql_delete = sql_delete.format(storage_id)
                    db.execute_sql(conn, sql_delete)
            else:
                sql_delete_status = """
                delete FROM enter_storage_status where pack_id = "{0}"
                """
                sql_delete_status = sql_delete_status.format(pack_id)
                db.execute_sql(conn, sql_delete_status)
                sql_storage = """
                SELECT enter_storage_code FROM enter_storage where pack_id = "{0}";
                """
                sql_storage = sql_storage.format(pack_id)
                drs = db.execute_sql(conn, sql_storage)
                for dr in drs:
                    # enter_list.append(dr[0])
                    enter_id = dr[0]
                    sql_delete = """
                    delete FROM enter_storage where enter_storage_code = "{0}"
                    """
                    sql_delete = sql_delete.format(enter_id)
                    db.execute_sql(conn, sql_delete)

            data = {"code": 0, "message": "删除成功"}

            data = json.dumps(data)
            logger.info("删除包装箱和包装箱里面的产品成功%s")

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}

            data = json.dumps(data)
            logger.error("删除包装箱和包装箱里面的产品失败%s"% e)

            return HttpResponse(data)


class stockInStockOut(View):

    """
    出入库接口(主要是修改包装箱的状态 有出有入有包装)

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            enter_user = request.session.get("session_currentId")
            enter_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")

            # product_id = "pen"
            # status = "入库"
            # response_datas = [{"pack_id":"pen_20210803_5"}, {"pack_id":"pen_20210803_6"}]
            conn = db.get_connection(product_id)
            status = request.GET.get("status")
            response_datas = request.GET.get("response_datas")

            if response_datas:
                response_datas = eval(response_datas)
                for response_data in response_datas:
                    pack_id = response_data.get("pack_id")
                    sql_update = """
                    update enter_storage_status set 
                        status ='{0}', enter_time = '{1}' 
                        where pack_id = '{2}' 
                    """
                    sql_update = sql_update.format(status, enter_time, pack_id)
                    db.execute_sql(conn, sql_update)
                    data = {"code": 0, "message": "操作成功"}
                    data = json.dumps(data)
                    logger.info("出入库操作成功")
                    return HttpResponse(data)
            else:
                data = {"code": 1, "message": "response_datas里面没有数据"}
                data = json.dumps(data)
                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}

            data = json.dumps(data)
            logger.error("出入库失败")

            return HttpResponse(data)


class BackMatter(View):
    """
    物料退料查询
    """
    def get(self, request):
        try:
            data_list = []
            matter_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            back_person = request.GET.get("back_person")
            product_plan_code = request.GET.get("product_plan_code")

            if back_person:
                back_person_sql = "and back_person = " + "'" + back_person + "'"
            else:
                back_person_sql = ""
            if product_plan_code:
                product_plan_code_sql = "and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""

            sql = """
            select * from product_back_matter where 2 > 1 {0} {1} 
            """
            sql = sql.format(back_person_sql, product_plan_code_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["materials_back_code"] = dr[0]
                    dict_data["back_person"] = dr[1]
                    dict_data["product_plan_code"] = dr[2]
                    s = dr[3]
                    if s:
                        s = s.strftime("%Y-%m-%d %H:%M:%S ")
                    else:
                        s = ""
                    dict_data["back_time"] = s
                    dict_data["description"] = dr[4]
                    sql_back = """
                    select * from back_matter where materials_back_code = '{0}'
                    """
                    sql_back = sql_back.format(dr[0])
                    back_dfs = db.execute_sql(conn, sql_back)
                    if back_dfs:
                        respose_list = []
                        for matter_df in back_dfs:
                            response_data = {}
                            response_data["deal_back_code"] = matter_df[0]
                            response_data["materials_back_code"] = matter_df[1]
                            response_data["matter_code"] = matter_df[2]
                            response_data["matter_count"] = matter_df[3]
                            respose_list.append(response_data)
                        dict_data["response_datas"] = respose_list
                        data_list.append(dict_data)
                    else:
                        dict_data["response_datas"] = []
                        data_list.append(dict_data)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()

                sql_num_int = int(len(data_list))

                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                result = {"code": 0, "message":"操作成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("物料退料查询成功%s"% result)
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "操作成功", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)

        except Exception as e:

            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("物料退料查询失败%s"% e)

            return HttpResponse(result)

    def post(self, request):
        """
        物料退料新增
        :param request:
        :return:
        """
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

            materials_back_code = str("Im_Back_Matter_" + str(id_num))
            back_person = str_data.get("back_person")
            product_plan_code = str_data.get("product_plan_code")
            back_time = str_data.get("back_time")
            description = str_data.get("description")
            response_datas = str_data.get("response_datas")

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

            data = {"code": 0, "message": "操作成功"}
            logger.info("BackMatter新增操作成功")
            data = json.dumps(data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            logger.error("BackMatter新增操作失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PutBackMatter(View):
    """
    修改物料退料

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            materials_back_code = request.GET.get("materials_back_code")
            back_person = request.GET.get("back_person")
            product_plan_code = request.GET.get("product_plan_code")
            back_time = request.GET.get("back_time")
            description = request.GET.get("description")

            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            else:
                response_datas = response_datas

            sql = """
                      update product_back_matter set 
                      back_person='{0}',product_plan_code='{1}', back_time ='{2}',
                      description= '{3}' where materials_back_code = '{4}'
                      """
            sql_main = sql.format(back_person, product_plan_code, back_time, description,
                                  materials_back_code)
            drs = db.execute_sql(conn, sql_main)

            sql_matter_num = """
             SELECT max(order_number) FROM back_matter
            """
            dras = db.execute_sql(conn, sql_matter_num)

            if dras:
                sql_num = dras[0][0]
            else:
                sql_num = 0

            for response_data in response_datas:
                # materials_production_code = response_data.get("materials_production_code")
                deal_back_code = response_data.get("deal_back_code")
                # materials_production_code = response_data.get("materials_production_code")
                matter_code = response_data.get("matter_code")
                matter_count = response_data.get("matter_count")
                if deal_back_code:
                    sql = """
                       update back_matter set materials_back_code = '{0}', 
                       matter_code = '{1}', matter_count ='{2}' where deal_back_code = '{3}'
                    """
                    sql = sql.format(materials_back_code, matter_code, matter_count, deal_back_code)
                    db.execute_sql(conn, sql)
                else:
                    sql_num = sql_num + 1

                    deal_back_code = str("Im_Deal_Back_" + str(sql_num))

                    sql_response = """
                                      insert into back_matter(deal_back_code,materials_back_code, 
                                      matter_code, matter_count, order_number) values('{0}',
                                       '{1}', '{2}', '{3}', '{4}')
                                  """
                    sql_response_format = sql_response.format(deal_back_code, materials_back_code,
                                                              matter_code, matter_count, sql_num)
                    db.execute_sql(conn, sql_response_format)

            data = {"code": 0, "message": "修改成功"}

            data = json.dumps(data)
            logger.info("修改物料退料成功%s")

            db.close_connection(conn)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}
            logger.error("修改物料退料失败---->%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeleteBackMatter(View):
    """
    删除物料退料

    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            materials_back_code = request.GET.get("materials_back_code")

            response_datas = request.GET.get("response_datas")
            response_datas = eval(response_datas)
            # materials_production_code = "Im_Product_Pick_Matter_1"
            # response_datas = [{"materials_code": "Im_Materials_Pick_1"}]
            if len(response_datas) != 0:

                for response_data in response_datas:
                    deal_back_code = dict(response_data).get("deal_back_code")
                    sql = """
                       delete from back_matter where deal_back_code = '{0}'
                       """
                    sql_format = sql.format(deal_back_code)
                    db.execute_sql(conn, sql_format)
            else:
                sql_matter = """
                              SELECT * FROM back_matter where materials_back_code = '{0}'
                              """
                sql_matter_format = sql_matter.format(materials_back_code)
                matter_dfs = db.execute_sql(conn, sql_matter_format)
                for matter_df in matter_dfs:
                    deal_back_code = matter_df[0]
                    sql_delete = """
                       delete FROM back_matter where deal_back_code = '{0}'
                       """
                    sql_delete_format = sql_delete.format(deal_back_code)
                    db.execute_sql(conn, sql_delete_format)
                sql = """
                       delete from product_back_matter where materials_back_code = '{0}'
                       """
                sql_main = sql.format(materials_back_code)
                des = db.execute_sql(conn, sql_main)
            data = {"code": 0, "message": "删除成功"}
            logger.info("删除物料退料表成功")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除物料退料表失败,%s" % e)
            return HttpResponse(data)


class ModifyFinishProductStatus(View):
    """

    修改成功品码的状态（PASS/FAIL）
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            work_type = request.session.get("session_workType")
            work_id = request.session.get("session_workId")

            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            print("==>", product_id, work_type, response_datas)
            for response_data in response_datas:
                finished_product_code = response_data.get("finished_product_code")
                status = response_data.get("status")
                conn = db.get_connection(product_id)
                table_select = "check_" + str(work_id)
                print(table_select)
                sql_transit = """
                             SELECT max(order_number) FROM {0};
                             """
                sql_transit = sql_transit.format(table_select)
                unqualified_product_nums = db.execute_sql(conn, sql_transit)
                if unqualified_product_nums[0][0]:
                    matter_num = unqualified_product_nums[0][0] + 1
                else:
                    matter_num = 1

                product_transit_code = "Im_Product_Transit_" + str(matter_num)

                sql_insert = """
                            insert into {0}(product_transit_code, finished_product_code, test_result, order_number)
                            values('{1}', '{2}', '{3}', '{4}')
                            """
                sql_insert = sql_insert.format(table_select, product_transit_code,
                                               finished_product_code, status, matter_num)
                db.execute_sql(conn, sql_insert)

            conn = db.get_connection(product_id)
            sql_tabale = """
                        show tables like "product_transit_%" 
                        """
            table_list = db.execute_sql(conn, sql_tabale)
            for table_type in table_list:
                table_one = table_type[0]

                for response_data in response_datas:
                    finished_product_code = response_data.get("finished_product_code")
                    status = response_data.get("status")
                    finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"

                    sql_matter = """
                                  select product_transit_code, finished_product_code, test_result from {0} where 2 > 1 {1}
                                   """
                    sql_matter_format = sql_matter.format(table_one, finished_product_code_sql)
                    matter_dfs = db.execute_sql(conn, sql_matter_format)
                    if matter_dfs:
                        transit_list = []
                        for matter_df in matter_dfs:
                            sql_update = """
                                       update {0} set test_result='{1}' where product_transit_code = '{2}'
                                       """
                            sql_update = sql_update.format(table_one, status, matter_df[0])
                            db.execute_sql(conn, sql_update)
                        if status == "FAIL":
                            sql_un_table = str("unqualified_product_") + str(table_one[16:])
                            sql = """
                            CREATE TABLE IF NOT EXISTS {0}(unqualified_product_code varchar(255) primary key not null, 
                                          product_plan_code varchar(255),
                                          finished_product_code varchar(255),
                                          matter_code varchar(255),
                                          matter_id varchar(255),
                                          description varchar(255),
                                          leader_work_id varchar(255),
                                          later_work_id varchar(255),
                                          solve_method varchar(255),
                                          solve_result varchar(255),                             
                                          order_number int) 
                            """
                            sql = sql.format(sql_un_table)
                            db.execute_sql(conn, sql)

                            sql_unqualified_product = """
                                                     SELECT max(order_number) FROM {0};
                                                     """
                            sql_unqualified_product = sql_unqualified_product.format(sql_un_table)
                            unqualified_product_nums = db.execute_sql(conn, sql_unqualified_product)
                            if unqualified_product_nums[0][0]:
                                matter_num = unqualified_product_nums[0][0] + 1
                            else:
                                matter_num = 1

                            unqualified_product_code = "Im_Unqualified_Product_" + str(matter_num)

                            sql_insert = """
                            insert into {0}(unqualified_product_code, finished_product_code, description, order_number)
                            values('{1}', '{2}', '{3}', '{4}')
                            """

                            sql_insert = sql_insert.format(sql_un_table,
                                                           unqualified_product_code,
                                                           finished_product_code, "状态改变", matter_num)
                            db.execute_sql(conn, sql_insert)
                        else:
                            sql_un_status = "unqualified_product_" + str(table_one[16:])
                            sql_code = """
                            SELECT unqualified_product_code FROM {0} where finished_product_code = '{1}'
                            """
                            sql_code = sql_code.format(sql_un_status, finished_product_code)
                            drs = db.execute_sql(conn, sql_code)
                            if drs:
                                for dr in drs:
                                    sql_delete = """
                                    delete from {0} where unqualified_product_code='{1}'
                                    """
                                    sql_delete = sql_delete.format(sql_un_status, dr[0])
                                    db.execute_sql(conn, sql_delete)
                            else:
                                pass
                    else:
                        pass

            data = {"code": 0, "message": "操作成功"}

            data = json.dumps(data)
            logger.info("修改产品的状态/合格、不合格 成功")
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("修改成品状态失败,%s" % e)
            return HttpResponse(data)


class MatterSearch(View):
    """

    物料查询
    """
    def get(self, request):
        try:
            data_add_int = {}
            db = DB()


            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            finished_product_code = request.GET.get("finished_product_code")
            matter_id = request.GET.get("matter_id")
            work_id = request.GET.get("work_id")
            user_code = request.GET.get("user_code")
            out_start_time = request.GET.get("out_start_time")
            out_end_time = request.GET.get("out_end_time")


            sql_table = """
                        show tables like "product_transit_%" 
                        """
            table_list = db.execute_sql(conn, sql_table)
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            if finished_product_code:
                finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if matter_id:
                matter_id_sql = "and matter_id = " + "'" + matter_id + "'"
            else:
                matter_id_sql = ""
            if work_id:
                work_id_sql = "and work_id = " + "'" + work_id + "'"
            else:
                work_id_sql = ""
            if user_code:
                user_code_sql = "and user_code = " + "'" + user_code + "'"
            else:
                user_code_sql = ""
            if out_start_time:
                out_start_time_sql = "and out_time >= " + "'" + out_start_time + "'"
            else:
                out_start_time_sql = ""
            if out_end_time:
                out_end_time_sql = "and out_time <=" + "'" + out_end_time + "'"
            else:
                out_end_time_sql = ""
            data_list = []
            for table_type in table_list:
                table_one = table_type[0]

                sql = """
                SELECT b.matter_name,a.matter_id,b.rule,
                b.matter_category,c.product_time,
                d.work_name,a.user_code,a.out_time,
                a.finished_product_code FROM {0} as a left join 
                matter_list as b on a.matter_code = b.bom_matter_code 
                left join person_matter as c on c.matter_code = a.matter_code 
                left join work_station as d on d.work_code = a.work_code where 2 > 1 {1} {2} {3} {4} {5} {6}
                order by a.out_time desc;
                """
                sql = sql.format(table_one, finished_product_code_sql, matter_id_sql,
                                 work_id_sql, user_code_sql, out_start_time_sql, out_end_time_sql)
                drs = db.execute_sql(conn, sql)
                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["matter_name"] = dr[0]
                        dict_data["matter_id"] = dr[1]
                        dict_data["rule"] = dr[2]
                        dict_data["matter_category"] = dr[3]
                        s2 = dr[4]
                        if s2:
                            s2 = s2.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["product_time"] = s2
                        dict_data["work_name"] = dr[5]
                        dict_data["user_code"] = dr[6]
                        s = dr[7]
                        if s:
                            s = s.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["out_time"] = s
                        dict_data["finished_product_code"] = dr[8]
                        data_list.append(dict_data)
                    data_list.sort(key=lambda x: (x['out_time']), reverse=True)
                    page_result = Page(page, page_size, data_list)
                    data = page_result.get_str_json()

                    sql_num = int(len(data_list))
                    data_add_int["data"] = data
                    data_add_int["total"] = sql_num

                else:
                    data_add_int["data"] = []
                    data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("物料查询成功%s"% result)

            return HttpResponse(result)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("查询物料信息失败,%s" % e)
            return HttpResponse(data)


class ProductInfoSearch(View):
    """
    产品的查询

    """
    def get(self, request):
        try:
            data_add_int = {}
            db = DB()
            data_list = []
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))
            product_id = request.session.get("session_projectId")
            finished_product_code = request.GET.get("finished_product_code")
            matter_id = request.GET.get("matter_id")

            conn = db.get_connection(product_id)
            if finished_product_code:
                finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if matter_id:
                matter_get_product_code = ""
                sql_table = """
                            show tables like "product_transit_%" 
                            """
                table_list = db.execute_sql(conn, sql_table)
                for table_type in table_list:
                    table_one = table_type[0]
                    sql = """
                    select finished_product_code from {0} where matter_id = '{1}'
                    """
                    sql = sql.format(table_one, matter_id)
                    finisheds = db.execute_sql(conn, sql)
                    if finisheds:
                        matter_get_product_code = finisheds[0][0]
                    else:
                        pass
                matter_id_sql = "and finished_product_code = " + "'" + matter_get_product_code + "'"

            else:
                matter_id_sql = ""

            conn_db = db.get_connection("db_common")

            sql_table1 = """
            select rule from productlist where product_id = '{0}'
            """
            sql_table1 = sql_table1.format(product_id)
            drs = db.execute_sql(conn_db, sql_table1)
            rule = drs[0][0]
            sql_enter_storage = """
            SELECT a.product_name, b.finished_product_code,a.status,a.pack_id,a.enter_time
            FROM enter_storage_status as a left join enter_storage as b on a.pack_id = b.pack_id
            where 2>1 {0} {1} order by a.enter_time desc;
            """
            sql_enter_storage = sql_enter_storage.format(finished_product_code_sql, matter_id_sql)
            dfs = db.execute_sql(conn, sql_enter_storage)
            if dfs:
                for df in dfs:
                    data_dict = {}
                    data_dict["product_name"] = df[0]
                    data_dict["finished_product_code"] = df[1]
                    data_dict["rule"] = rule
                    data_dict["status"] = df[2]
                    data_dict["pack_id"] = df[3]
                    s = df[4]
                    if s:
                        s = s.strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        s = ""
                    data_dict["enter_time"] = s
                    sql_table = """
                                show tables like "product_transit_%" 
                                """
                    table_list = db.execute_sql(conn, sql_table)

                    finish_matter_list = []
                    for table_type in table_list:
                        table_one = table_type[0]
                        sql = """
                        select matter_id from {0} where finished_product_code = '{1}'
                        """
                        sql = sql.format(table_one, df[1])
                        matters = db.execute_sql(conn, sql)
                        if matters:
                            for matter in matters:
                                finish_matter_list.append(matter[0])
                        else:
                            pass
                    data_dict["response_datas"] = finish_matter_list

                    data_list.append(data_dict)
                data_list.sort(key=lambda x: (x['enter_time']), reverse=True)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num = int(len(data_list))
                data_add_int["data"] = data
                data_add_int["total"] = sql_num
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("产品查询成功%s"% result)
            return HttpResponse(result)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("查询物产品信息失败,%s" % e)
            return HttpResponse(data)


class NoPageMatterSearch(View):
    """
    不i分页的物料查询

    """
    def get(self, request):
        try:
            data_add_int = {}
            db = DB()

            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            finished_product_code = request.GET.get("finished_product_code")
            matter_id = request.GET.get("matter_id")

            sql_table = """
                        show tables like "product_transit_%" 
                        """
            table_list = db.execute_sql(conn, sql_table)

            if finished_product_code:
                finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if matter_id:
                matter_id_sql = "and matter_id = " + "'" + matter_id + "'"
            else:
                matter_id_sql = ""

            data_list = []
            for table_type in table_list:
                table_one = table_type[0]
                sql = """
                SELECT b.matter_name,a.matter_id,b.rule,
                b.matter_category,c.product_time,
                d.work_name,a.user_code,a.out_time,
                a.finished_product_code FROM {0} as a left join 
                matter_list as b on a.matter_code = b.bom_matter_code 
                left join person_matter as c on c.matter_code = a.matter_code 
                left join work_station as d on d.work_code = a.work_code where 2 > 1 {1} {2}
                """
                sql = sql.format(table_one, finished_product_code_sql, matter_id_sql)
                drs = db.execute_sql(conn, sql)
                if drs:
                    for dr in drs:
                        dict_data = {}
                        dict_data["matter_name"] = dr[0]
                        dict_data["matter_id"] = dr[1]
                        dict_data["rule"] = dr[2]
                        dict_data["matter_category"] = dr[3]
                        s2 = dr[4]
                        if s2:
                            s2 = s2.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["product_time"] = s2
                        dict_data["work_name"] = dr[5]
                        dict_data["user_code"] = dr[6]
                        s = dr[7]
                        if s:
                            s = s.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["out_time"] = s
                        dict_data["finished_product_code"] = dr[8]
                        data_list.append(dict_data)
                data = data_list
                sql_num = int(len(data_list))
                data_add_int["data"] = data
                data_add_int["total"] = sql_num

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("不分页的物料查询成功")
            return HttpResponse(result)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("不分页的查询物料信息失败,%s" % e)
            return HttpResponse(data)


class NoPageProductInfoSearch(View):
    """
    不分页的产品查询
    """
    def get(self, request):
        try:
            data_add_int = {}
            db = DB()
            data_list = []
            product_id = request.session.get("session_projectId")
            finished_product_code = request.GET.get("finished_product_code")
            matter_id = request.GET.get("matter_id")

            conn = db.get_connection(product_id)
            if finished_product_code:
                finished_product_code_sql = "and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if matter_id:
                matter_get_product_code = ""
                sql_table = """
                            show tables like "product_transit_%" 
                            """
                table_list = db.execute_sql(conn, sql_table)
                for table_type in table_list:
                    table_one = table_type[0]
                    sql = """
                    select finished_product_code from {0} where matter_id = '{1}'
                    """
                    sql = sql.format(table_one, matter_id)
                    finisheds = db.execute_sql(conn, sql)
                    if finisheds:
                        matter_get_product_code = finisheds[0][0]
                    else:
                        pass
                matter_id_sql = "and finished_product_code = " + "'" + matter_get_product_code + "'"

            else:
                matter_id_sql = ""

            conn_db = db.get_connection("db_common")

            sql_table1 = """
            select rule from productlist where product_id = '{0}'
            """
            sql_table1 = sql_table1.format(product_id)
            drs = db.execute_sql(conn_db, sql_table1)
            rule = drs[0][0]
            sql_enter_storage = """
            SELECT a.product_name, b.finished_product_code,a.status,a.pack_id,a.enter_time
            FROM enter_storage_status as a left join enter_storage as b on a.pack_id = b.pack_id
            where 2>1 {0} {1} order by a.enter_time desc;
            """
            sql_enter_storage = sql_enter_storage.format(finished_product_code_sql, matter_id_sql)
            dfs = db.execute_sql(conn, sql_enter_storage)
            if dfs:
                for df in dfs:
                    data_dict = {}
                    data_dict["product_name"] = df[0]
                    data_dict["finished_product_code"] = df[1]
                    data_dict["rule"] = rule
                    data_dict["status"] = df[2]
                    data_dict["pack_id"] = df[3]
                    s = df[4]
                    if s:
                        s = s.strftime("%Y-%m-%d %H:%M:%S ")
                    else:
                        s = ""
                    data_dict["enter_time"] = s
                    sql_table = """
                                show tables like "product_transit_%" 
                                """
                    table_list = db.execute_sql(conn, sql_table)

                    finish_matter_list = []
                    for table_type in table_list:
                        table_one = table_type[0]
                        sql = """
                        select matter_id from {0} where finished_product_code = '{1}'
                        """
                        sql = sql.format(table_one, df[1])
                        matters = db.execute_sql(conn, sql)
                        if matters:
                            for matter in matters:
                                finish_matter_list.append(matter[0])
                        else:
                            pass
                    data_dict["response_datas"] = finish_matter_list

                    data_list.append(data_dict)
                data_list.sort(key=lambda x: (x['enter_time']), reverse=True)

                sql_num = int(len(data_list))
                data_add_int["data"] = data_list
                data_add_int["total"] = sql_num

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("不分页的产品查询成功")
            return HttpResponse(result)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("查询物产品信息失败,%s" % e)
            return HttpResponse(data)


class OperationSystem(View):
    """
    打印参数的一张表
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            sql = """
                    select * from operate where 2 > 1
                   """

            drs = db.execute_sql(conn, sql)

            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["ID"] = dr[0]
                    dict_data["Package_Qty"] = dr[1]
                    dict_data["Rv"] = dr[2]
                    dict_data["Itemcode_C_Shipping"] = dr[3]
                    dict_data["Supplier"] = dr[4]
                    dict_data["No_Ship"] = dr[5]
                    dict_data["CS_type"] = dr[6]
                    dict_data["Shipping_SN_length"] = dr[7]
                    dict_data["Product_length"] = dr[8]
                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                sql_num = """
                            select count(*) from operate where 2 > 1
                            """

                dfs = db.execute_sql(conn, sql_num)
                if dfs:
                    sql_num_int = dfs[0][0]
                else:
                    sql_num_int = 0
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("OperationSystem>>>>操作成功%s"% result)
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("OperationSyste操作失败%s"% e)
            return HttpResponse(result)

    def post(self, request):
        """

        新增打印的一些参数
        :param request:
        :return:
        """
        try:
            json_data = request.body
            str_data = json.loads(json_data)

            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            sql_matter = """
                   SELECT max(order_number) FROM operate;
                   """
            matter_type = db.execute_sql(conn, sql_matter)
            if matter_type[0][0] == None:
                matter_num = 1
            else:
                matter_num = matter_type[0][0] + 1
            # id = str_data.get("ID")
            Package_Qty = str_data.get("Package_Qty")
            Rv = str_data.get("Rv")
            Itemcode_C_Shipping = str_data.get("Itemcode_C_Shipping")
            Supplier = str_data.get("Supplier")
            No_Ship = str_data.get("No_Ship")
            CS_type = str_data.get("CS_type")
            Shipping_SN_length = str_data.get("Shipping_SN_length")
            Product_length = str_data.get("Product_length")

            sql_insert = """
                               insert into operate(ID, Package_Qty,
                               Rv,
                               Itemcode_C_Shipping, Supplier, No_Ship, CS_type, Shipping_SN_length, Product_length, order_number)
                               values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}')
                               """
            sql_insert_format = sql_insert.format(matter_num, Package_Qty,
                                                  Rv, Itemcode_C_Shipping,
                                                  Supplier, No_Ship, CS_type, Shipping_SN_length,
                                                  Product_length, matter_num)
            drs = db.execute_sql(conn, sql_insert_format)

            data = {"code": 0, "message": "操作成功"}
            logger.info("OperationSystem接口新增操作成功")
            data = json.dumps(data)

            return HttpResponse(data)
        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            logger.error("OperationSystem接口新增操作失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PutOperationSystem(View):
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            ID = request.GET.get("ID")
            Package_Qty = request.GET.get("Package_Qty")
            Rv = request.GET.get("Rv")
            Itemcode_C_Shipping = request.GET.get("Itemcode_C_Shipping")
            Supplier = request.GET.get("Supplier")
            No_Ship = request.GET.get("No_Ship")
            CS_type = request.GET.get("CS_type")
            Shipping_SN_length = request.GET.get("Shipping_SN_length")
            Product_length = request.GET.get("Product_length")
            sql = """
                   update operate set
                  Package_Qty='{0}',Rv='{1}',Itemcode_C_Shipping='{2}',Supplier='{3}',
                  No_Ship='{4}',CS_type='{5}', Shipping_SN_length='{6}', Product_length='{7}' where ID = '{8}'
                   """
            sql = sql.format(Package_Qty, Rv, Itemcode_C_Shipping, Supplier, No_Ship,
                             CS_type, Shipping_SN_length, Product_length, ID)
            drs = db.execute_sql(conn, sql)
            result = {"code": 0, "message": "操作成功"}
            result = json.dumps(result)
            logger.info("OperationSystem>>>>修改操作成功%s")
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("修改OperationSystem 失败%s"% e)
            return HttpResponse(result)


class DeleteOperationSystem(View):
    """
    删除打印参数
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            ID = request.GET.get("ID")
            sql = """
                   delete from operate where ID = '{0}'
                   """
            sql = sql.format(ID)
            drs = db.execute_sql(conn, sql)
            result = {"code": 0, "message": "操作成功"}
            result = json.dumps(result)
            logger.info("删除DeleteOperationSystem是成功")
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("删除DeleteOperationSystem是失败%s"% e)
            return HttpResponse(result)


class AddModel(View):
    def post(self, request):
        """
        新增模板的接口

        :param request:
        :return:
        """
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            type_name = request.POST.get("fileType")
            f = request.FILES.get("file")  # 接收前端的文件
            BASE_DIR = Path(__file__).resolve().parent.parent
            path_workstation = os.path.join(BASE_DIR, "media")
            excit_psth = os.path.join(path_workstation, product_id)
            if product_id:
                if "txt" in str(f).split("."):
                    sql_create = """
                    CREATE TABLE IF NOT EXISTS project_model(id int AUTO_INCREMENT primary key not null, 
                                              product_id varchar(255),
                                              model_name varchar(255),
                                              type_name varchar(255))
                    """
                    db.execute_sql(conn, sql_create)

                    sql_check = """
                    select * from project_model where product_id = "{0}" and type_name = "{1}"
                    """
                    sql_check = sql_check.format(product_id, type_name)
                    drs = db.execute_sql(conn, sql_check)

                    if drs:
                        result = {"code": 1, "message": "上传的txt文件已经存在，请先删除再添加"}
                        result = json.dumps(result)

                    else:
                        sql_insert = """
                        insert into project_model(product_id, model_name,
                                       type_name)
                                       values('{0}', '{1}', '{2}')
                        """

                        sql_insert = sql_insert.format(product_id, f.name, type_name)

                        db.execute_sql(conn, sql_insert)
                        if os.path.exists(excit_psth):  # 如果存在文件夹的话就将文件放入文件夹下
                            with open(os.path.join(excit_psth, f.name), "wb+") as k:
                                for chunk in f.chunks():
                                    k.write(chunk)
                        else:
                            os.makedirs(excit_psth)   # 如果不存在文件夹的话就创建文件夹再将文件放到下面

                            with open(os.path.join(excit_psth, f.name), "wb+") as k:
                                for chunk in f.chunks():
                                    k.write(chunk)

                        result = {"code": 0, "message": "操作成功"}
                        result = json.dumps(result)
                        logger.info("新增模板接口i成功%s"% result)

                else:
                    if os.path.exists(excit_psth):  # 如果存在文件夹的话就将文件放入文件夹下
                        with open(os.path.join(excit_psth, f.name), "wb+") as k:
                            for chunk in f.chunks():
                                k.write(chunk)
                    else:
                        os.makedirs(excit_psth)  # 如果不存在文件夹的话就创建文件夹再将文件放到下面

                        with open(os.path.join(excit_psth, f.name), "wb+") as k:
                            for chunk in f.chunks():
                                k.write(chunk)
                        print(excit_psth, "已经创建,已经成功加入")
                    result = {"code": 0, "message": "操作成功"}
                    result = json.dumps(result)
                    logger.info("chengggong")


            else:
                result = {"code": 1, "message": "session过期，没有项目，请重新登录"}
                result = json.dumps(result)

            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("系统失败")
            return HttpResponse(result)


class test(View):
    def get(self, request):
        try:
            BASE_DIR = Path(__file__).resolve().parent.parent
            path_file = os.path.join(BASE_DIR, r"utils\import_common.py")

            result = {"code": 0, "message": "操作成功"}
            result = json.dumps(result)
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            return HttpResponse(result)


class PrintApai(View):
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")

            conn = db.get_connection(product_id)
            type_name = request.GET.get("fileType")

            work_id = request.session.get('session_workId')
            BASE_DIR = Path(__file__).resolve().parent.parent
            path_workstation = os.path.join(BASE_DIR, "media")
            store_work = str(product_id) + "_" + str(work_id)
            print_path = os.path.join(path_workstation, store_work)

            if os.path.exists(print_path):
                pass
            else:
                os.makedirs(print_path)

            if type_name == "box_code":
                stem1 = request.GET.get("stem1")
                sql = """
                            select model_name from project_model where product_id = "{0}" and type_name = "{1}"        
                            """
                sql = sql.format(product_id, type_name)

                drs = db.execute_sql(conn, sql)
                if drs[0][0]:
                    model_name = drs[0][0]
                    file_path1 = os.path.join(path_workstation, product_id)
                    file_path = os.path.join(file_path1, model_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        str1 = f.read()
                        str2 = str1.replace("{0}", stem1)
                    print_file_path = os.path.join(print_path, model_name)
                    with open(print_file_path, "w+", encoding="utf-8") as k:
                        k.write(str2)
                    data = "print_file_path"
                    result = {"code": 0, "message": "操作成功", "data": data}
                    result = json.dumps(result)
                    return HttpResponse(result)
                else:
                    result = {"code": 1, "message": "请先上传txt模板文件"}
                    result = json.dumps(result)
                    return HttpResponse(result)

            elif type_name == "matter_code":
                stem1 = request.GET.get("stem1")
                stem2 = request.GET.get("stem2")
                stem3 = request.GET.get("stem3")
                stem4 = request.GET.get("stem4")
                stem5 = request.GET.get("stem5")
                stem6 = request.GET.get("stem6")
                sql = """
                    select model_name from project_model where product_id = "{0}" and type_name = "{1}"        
                    """
                sql = sql.format(product_id, type_name)

                drs = db.execute_sql(conn, sql)
                if drs[0][0]:
                    model_name = drs[0][0]
                    file_path1 = os.path.join(path_workstation, product_id)
                    file_path = os.path.join(file_path1, model_name)
                    with open(file_path, "r", encoding="utf-8") as f:
                        str1 = f.read()
                        str2 = str1.replace("{0}", stem1)
                        str2 = str2.replace("{1}", stem2)
                        str2 = str2.replace("{2}", stem3)
                        str2 = str2.replace("{3}", stem4)
                        str2 = str2.replace("{4}", stem5)
                        str2 = str2.replace("{5}", stem6)
                    print_file_path = os.path.join(print_path, model_name)
                    with open(print_file_path, "w+", encoding="utf-8") as k:
                        k.write(str2)
                    data = "print_file_path"

                    result = {"code": 0, "message": "操作成功", "data": data}
                    result = json.dumps(result)
                    return HttpResponse(result)
                else:
                    result = {"code": 1, "message": "请先上传txt模板文件"}
                    result = json.dumps(result)
                    return HttpResponse(result)

            elif type_name == "deliver_goods_code":
                stem1 = request.GET.get("stem1")
                stem2 = request.GET.get("stem2")
                stem3 = request.GET.get("stem3")
                stem4 = request.GET.get("stem4")
                stem5 = request.GET.get("stem5")
                stem6 = request.GET.get("stem6")
                sql = """
                    select model_name from project_model where product_id = "{0}" and type_name = "{1}"        
                    """
                sql = sql.format(product_id, type_name)
                drs = db.execute_sql(conn, sql)

                if drs[0][0]:

                    model_name = drs[0][0]
                    file_path1 = os.path.join(path_workstation, product_id)
                    file_path = os.path.join(file_path1, model_name)

                    with open(file_path, "r", encoding="utf-8") as f:
                        str1 = f.read()
                        str2 = str1.replace("{0}", stem1)
                        str2 = str2.replace("{1}", stem2)
                        str2 = str2.replace("{2}", stem3)
                        str2 = str2.replace("{3}", stem4)
                        str2 = str2.replace("{4}", stem5)
                        str2 = str2.replace("{5}", stem6)
                    print_file_path = os.path.join(print_path, model_name)
                    with open(print_file_path, "w+", encoding="utf-8") as k:
                        k.write(str2)
                    data = "print_file_path"
                    result = {"code": 0, "message": "操作成功", "data": data}
                    result = json.dumps(result)
                    return HttpResponse(result)
                else:
                    result = {"code": 1, "message": "请先上传txt模板文件"}
                    result = json.dumps(result)
                    return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败"}
            result = json.dumps(result)
            return HttpResponse(result)


class WorkManage(View):
    """
    测试 检验 包装等工站查询建了哪些数据库（表格）

    """
    def get(self, request):
        try:
            data_list = []
            matter_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            # conn = db.get_connection("db_common")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            table_name = request.GET.get("table_name")
            work_code = request.GET.get("work_code")

            if table_name:
                table_name_sql = "and table_name = " + "'" + table_name + "'"
            else:
                table_name_sql = ""
            if work_code:
                work_code_sql = "and work_code = " + "'" + work_code + "'"
            else:
                work_code_sql = ""

            sql = """
             select * from work_transit where 2 > 1 {0} {1}
            """

            sql_main = sql.format(table_name_sql, work_code_sql)
            print("->", sql_main)

            drs = db.execute_sql(conn, sql_main)

            print("=-=->", drs)
            if drs:

                for dr in drs:
                    dict_data = {}
                    dict_data["table_code"] = dr[0]
                    dict_data["table_name"] = dr[1]
                    dict_data["work_code"] = dr[2]
                    dict_data["description"] = dr[3]

                    s = dr[4]
                    if s:
                        s = s.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["create_time"] = s
                    else:
                        dict_data["create_time"] = ""

                    sql_matter = """
                    select * from field_list where table_name = '{0}' order by order_number asc;
                    """
                    sql_matter_format = sql_matter.format(dr[1])
                    matter_dfs = db.execute_sql(conn, sql_matter_format)
                    if matter_dfs:
                        respose_list = []
                        for matter_df in matter_dfs:
                            response_data = {}
                            response_data["field_code"] = matter_df[0]
                            response_data["table_name"] = matter_df[1]
                            response_data["field_name"] = matter_df[2]
                            response_data["field_type"] = matter_df[3]
                            response_data["field_PK"] = matter_df[4]
                            response_data["field_NN"] = matter_df[5]
                            response_data["field_AI"] = matter_df[6]
                            # response_data["order_number"] = matter_df[7]
                            respose_list.append(response_data)
                        dict_data["response_datas"] = respose_list
                        data_list.append(dict_data)
                    else:
                        dict_data["response_datas"] = []
                        data_list.append(dict_data)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()

                sql_num_int = int(len(data_list))
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

            result = {"code": 0, "message": "操作成功", "data": data_add_int}
            result = json.dumps(result)

            return HttpResponse(result)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "调取BOM产品列表失败"}
            data = json.dumps(data)
            logger.error("查询产品列表失败")

            return HttpResponse(data)

    def post(self, request):
        """

        创建项目下自定义的表格（检验、包装等）
        :param request:
        :return:
        """
        try:
            product_id = request.session.get("session_projectId")
            json_data = request.body
            str_data = json.loads(json_data)
            product_db = str_data.get("product_id")

            work_code = str_data.get("work_code")
            # table_code = str_data.get("table_code")
            table_name = str_data.get("table_name")
            description = str_data.get("description")
            response_datas = str_data.get("response_datas")
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")

            db = DB()

            conn = db.get_connection(product_id)

            sql_transit = """
            SELECT max(order_number) FROM work_transit;
            """
            matter_type = db.execute_sql(conn, sql_transit)
            if matter_type[0][0] == None:
                transit_num = 1
            else:
                transit_num = matter_type[0][0] + 1

            sql_filed = """
                        SELECT max(order_number) FROM field_list;
                        """
            matter_type = db.execute_sql(conn, sql_filed)
            if matter_type[0][0] == None:
                field_num = 0
            else:
                field_num = matter_type[0][0]

            table_code = str("Im_Work_Tran" + str(transit_num))

            sql_check = """
            select * from work_transit where table_name = '{0}' and work_code = '{1}'
            """
            sql_check = sql_check.format(table_name, work_code)
            drs_checks = db.execute_sql(conn, sql_check)
            if drs_checks:
                data = {"code": 1, "message": "项目下的数据库已经存在此表格，请核对"}
                logger.error("项目下的数据库已经存在此表格")
                data = json.dumps(data)
                return HttpResponse(data)
            else:
                sql_insert = """
                            insert into work_transit(table_code, table_name, work_code,
                            description,
                            create_time, order_number)
                            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                            """
                sql_insert_format = sql_insert.format(table_code, table_name, work_code,
                                                      description, now_time, transit_num)

                drs = db.execute_sql(conn, sql_insert_format)

                for response_data in response_datas:
                    # field_code = response_data.get("field_code")
                    field_name = response_data.get("field_name")
                    field_type = response_data.get("field_type")
                    field_PK = response_data.get("field_PK")
                    field_NN = response_data.get("field_NN")
                    field_AI = response_data.get("field_AI")
                    field_num = field_num + 1
                    field_code = str("Im_Field_" + str(field_num))
                    sql_response = """
                            insert into field_list(field_code,table_name, field_name,
                            field_type, field_PK, field_NN, field_AI, order_number)
                            values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')
                    """
                    sql_response_format = sql_response.format(field_code, table_name, field_name,
                                                              field_type, field_PK, field_NN, field_AI, field_num)
                    matter_drs = db.execute_sql(conn, sql_response_format)

                sql_create = """
                CREATE TABLE IF NOT EXISTS {0}({1});
                """
                location_1 = ""
                location_2 = ""
                for response_data in response_datas:

                    field_name = response_data.get("field_name")
                    field_type = response_data.get("field_type")
                    field_PK = response_data.get("field_PK")
                    field_NN = response_data.get("field_NN")
                    field_AI = response_data.get("field_AI")

                    if field_AI:
                        field_AI = " AUTO_INCREMENT "
                    else:
                        field_AI = ""

                    if field_PK:
                        field_PK = " primary key "
                    else:
                        field_PK = ""
                    if field_NN:
                        field_NN = " not null "
                    else:
                        field_NN = ""
                    if field_type == "VARCHAR":
                        field_type = "varchar(255)"

                    if field_type == "DATETIME":
                        field_type = " DATETIME DEFAULT CURRENT_TIMESTAMP "
                    if field_PK:
                        location_1 = field_name + " "+ field_type + field_AI + field_PK+ field_NN
                    else:
                        location_2 = location_2 + "," + field_name + " " + field_type + field_AI+ field_NN

                values = location_1 + location_2

                sql_create = sql_create.format(table_name, values)

                db.execute_sql(conn, sql_create)

                data = {"code": 0, "message": "创建数据表成功"}
                logger.info("创建数据表成功")
                data = json.dumps(data)

                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "创建数据表失败"}
            logger.error("创建数据表成失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PutWorkManage(View):
    """

    修改创建的表格---表格里面有数据不让更改 没有数据的话可以更改表格
    """

    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            work_code = request.GET.get("work_code")
            table_code = request.GET.get("table_code")
            table_name = request.GET.get("table_name")
            description = request.GET.get("description")
            response_datas = request.GET.get("response_datas")
            create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S ")
            if response_datas:
                response_datas = eval(response_datas)
            sql = """
                         update work_transit set
                         table_name='{0}',work_code='{1}', description ='{2}',
                         create_time= '{3}' where table_code = '{4}'
                         """
            sql_main = sql.format(table_name, work_code, description, create_time,
                                  table_code)
            drs = db.execute_sql(conn, sql_main)

            sql_matter_num = """
                    SELECT max(order_number) FROM field_list
                   """
            dras = db.execute_sql(conn, sql_matter_num)

            if dras:
                sql_num = dras[0][0]
            else:
                sql_num = 0

            sql_check_name = """
            SELECT * FROM {0}
            """
            sql_check_name = sql_check_name.format(table_name)
            ds_nums = db.execute_sql(conn, sql_check_name)
            # print("sartart===========>", ds_nums)
            # ds_num = ds_nums[0][0]

            if ds_nums:
                data = {"code": 1, "message": "数据库表已存在数据,不可操作"}
                logger.error("数据库表已存在数据,不能修改")
                data = json.dumps(data)

                return HttpResponse(data)

            else:
                sql_delete = """
                            drop table if exists {0}
                            """
                sql_delete = sql_delete.format(table_name)
                db.execute_sql(conn, sql_delete)
                sql_matter = """
                              SELECT field_code FROM field_list where table_name = '{0}'
                              """
                sql_matter_format = sql_matter.format(table_name)
                field_dfs = db.execute_sql(conn, sql_matter_format)
                for field_df in field_dfs:
                    sql_delete = """
                                       delete FROM field_list where field_code = '{0}'
                                       """
                    sql_delete_format = sql_delete.format(field_df[0])
                    db.execute_sql(conn, sql_delete_format)
                sql_delete_transit = """
                delete from work_transit where table_code = '{0}'
                """
                sql_delete_transit = sql_delete_transit.format(table_code)
                db.execute_sql(conn, sql_delete_transit)
                sql_transit = """
                    SELECT max(order_number) FROM work_transit;
                    """
                matter_type = db.execute_sql(conn, sql_transit)
                if matter_type[0][0] == None:
                    transit_num = 1
                else:
                    transit_num = matter_type[0][0] + 1

                sql_filed = """
                                SELECT max(order_number) FROM field_list;
                                """
                matter_type = db.execute_sql(conn, sql_filed)
                if matter_type[0][0] == None:
                    field_num = 0
                else:
                    field_num = matter_type[0][0]

                table_code = str("Im_Work_Tran" + str(transit_num))

                sql_insert = """
                                            insert into work_transit(table_code, table_name, work_code,
                                            description,
                                            create_time, order_number)
                                            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')
                                            """
                sql_insert_format = sql_insert.format(table_code, table_name, work_code,
                                                      description, now_time, transit_num)

                drs = db.execute_sql(conn, sql_insert_format)

                for response_data in response_datas:
                    # field_code = response_data.get("field_code")
                    field_name = response_data.get("field_name")
                    field_type = response_data.get("field_type")
                    field_PK = response_data.get("field_PK")
                    field_NN = response_data.get("field_NN")
                    field_AI = response_data.get("field_AI")
                    field_num = field_num + 1
                    field_code = str("Im_Field_" + str(field_num))
                    sql_response = """
                                insert into field_list(field_code,table_name, field_name,
                                field_type, field_PK, field_NN, field_AI, order_number)
                                values('{0}', '{1}', '{2}', '{3}', '{4}','{5}', '{6}', '{7}')
                        """
                    sql_response_format = sql_response.format(field_code, table_name, field_name,
                                                              field_type, field_PK, field_NN, field_AI, field_num)

                    matter_drs = db.execute_sql(conn, sql_response_format)
                sql_create = """
                    CREATE TABLE IF NOT EXISTS {0}({1});
                    """
                location_1 = ""
                location_2 = ""
                for response_data in response_datas:

                    field_name = response_data.get("field_name")
                    field_type = response_data.get("field_type")
                    field_PK = response_data.get("field_PK")
                    field_NN = response_data.get("field_NN")
                    field_AI = response_data.get("field_AI")


                    if field_AI == "True" or field_AI == "true":
                        field_AI = " AUTO_INCREMENT "
                    else:
                        field_AI = ""

                    if field_PK == "True" or field_PK == "true":
                        field_PK = " primary key "
                    else:
                        field_PK = ""
                    if field_NN == "True" or field_NN == "true":
                        field_NN = " not null "
                    else:
                        field_NN = ""
                    if field_type == "VARCHAR":
                        field_type = "varchar(255)"

                    if field_type == "DATETIME":
                        field_type = " DATETIME DEFAULT CURRENT_TIMESTAMP "
                    if field_PK:
                        location_1 = field_name + " " + field_type + field_AI + field_PK  + field_NN
                    else:
                        location_2 = location_2 + "," + field_name + " "  + field_type + field_AI + field_NN

                values = location_1 + location_2

                sql_create = sql_create.format(table_name, values)

                db.execute_sql(conn, sql_create)

                data = {"code": 0, "message": "修改数据表成功"}
                logger.info("修改数据表成功")

                data = json.dumps(data)

                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "修改失败"}
            logger.error("修改失败---->%s"% e)
            data = json.dumps(data)
            return HttpResponse(data)


class DeleteWorkManage(View):
    """

    删除自定义的表格
    """
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            table_code = request.GET.get("table_code")
            # table_name = request.GET.get("table_name")
            sql_ = """
            select table_name from work_transit where table_code = '{0}'
            """
            sql_ = sql_.format(table_code)
            dfs = db.execute_sql(conn, sql_)
            table_name = dfs[0][0]
            response_datas = request.GET.get("response_datas")
            if response_datas:
                response_datas = eval(response_datas)
            # materials_production_code = "Im_Product_Pick_Matter_1"
            # response_datas = [{"materials_code": "Im_Materials_Pick_1"}]
            if response_datas:
                for response_data in response_datas:
                    field_code = dict(response_data).get("field_code")
                    field_name = dict(response_data).get("field_name")
                    sql = """
                       delete from field_list where field_code = '{0}'
                       """
                    sql_format = sql.format(field_code)
                    db.execute_sql(conn, sql_format)

                    sql_delete = """
                    ALTER TABLE {0} DROP COLUMN {1}             
                    """
                    sql_delete = sql_delete.format(table_name, field_name)
                    db.execute_sql(conn, sql_delete)
            else:
                sql_table = """
                select * from {0}
                """
                sql_table = sql_table.format(table_name)
                drs_tables = db.execute_sql(conn, sql_table)
                if drs_tables:
                    data = {"code": 1, "message": "数据库表里面已经存在数据，不能删除"}
                    logger.error("数据库表已存在数据,不能修改")
                    data = json.dumps(data)

                    return HttpResponse(data)
                else:
                    sql_matter = """
                                  SELECT field_code FROM field_list where table_name = '{0}'
                                  """
                    sql_matter_format = sql_matter.format(table_name)
                    field_dfs = db.execute_sql(conn, sql_matter_format)
                    for field_df in field_dfs:
                        sql_delete = """
                           delete FROM field_list where field_code = '{0}'
                           """
                        sql_delete_format = sql_delete.format(field_df[0])
                        db.execute_sql(conn, sql_delete_format)
                    sql = """
                           delete from work_transit where table_code = '{0}'
                           """
                    sql_main = sql.format(table_code)
                    des = db.execute_sql(conn, sql_main)

                    sql_drop = """
                    drop table if exists {0}
                    """
                    sql_drop = sql_drop.format(table_name)
                    db.execute_sql(conn, sql_drop)

                    data = {"code": 0, "message": "删除成功"}
                    logger.info("删除之前自定义表格成功")
                    data = json.dumps(data)
                    return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除失败,%s" % e)
            return HttpResponse(data)


class NoPageProcessMatterDeal(View):
    """

    不分页工站下领料的详情 安装数量返回
    """
    def get(self, request):
        try:
            lid = []
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            matter_code = request.GET.get("matter_code")
            work_id = request.GET.get("work_id")

            if matter_code:
                matter_code_sql = " and matter_code = " + "'" + matter_code + "'"
            else:
                matter_code_sql = ""

            if work_id:
                work_id_sql = " and work_id !=  " + "'" + work_id + "'"
            else:
                work_id_sql = ""

            sql = """
            select * from process_matter_deal where 2 > 1 {0} {1}
            """
            sql = sql.format(matter_code_sql, work_id_sql)
            drs = db.execute_sql(conn, sql)
            for dr in drs:
                dict_data = {}
                # dict_data["process_matter_deal_code"] = dr[0]
                dict_data["work_id"] = dr[1]
                dict_data["matter_code"] = dr[2]
                dict_data["install_number"] = dr[3]
                data_list.append(dict_data)

            for i in data_list:
                if (i['work_id'], i["matter_code"]) not in lid:
                    lid.append((i['work_id'], i["matter_code"]))
            lm = []
            for i in lid:
                lm.append({'work_id': i[0], 'matter_code': i[1], "install_number": 0})

            for i in data_list:
                for o in lm:
                    if i['work_id'] == o['work_id'] and i["matter_code"] == o["matter_code"]:
                        o['install_number'] = o['install_number'] + i['install_number']

            data = {"code": 0, "message": "操作成功", "data": lm}
            logger.info("得到安装数量操作成功")
            data = json.dumps(data)
            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("操作失败---》,%s" % e)
            return HttpResponse(data)


class PackCheckFinishedProduct(View):
    """
    包装前检验是否合格
    """
    def get(self, request):
        try:
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            finished_product_code = request.GET.get("finished_product_code")
            sql_check = """
            select Result from fct where SN = '{0}'
            """
            sql_check = sql_check.format(finished_product_code)
            dr_checks = db.execute_sql(conn, sql_check)
            if dr_checks:
                if dr_checks[0][0] == "PASS":
                    data = {"code": 0, "message": "检验合格"}
                    data = json.dumps(data)
                    return HttpResponse(data)
                else:
                    data = {"code": 1, "message": "检验不合格"}
                    data = json.dumps(data)
                    return HttpResponse(data)

            else:
                data = {"code": 1, "message": "此产品还没有检验，请先检验再包装"}
                data = json.dumps(data)
                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "包装前检验成品操作失败"}
            data = json.dumps(data)
            logger.error("包装前检验成品操作失败->,%s" % e)
            return HttpResponse(data)


class TransitProductQualifiedSearch(View):
    """
    加工过站详情加工站的信息--- 合格和不合格的数量等

    """

    def get(self, request):
        try:
            data_add_int = {}
            data_list = []
            db = DB()
            product_id = request.session.get("session_projectId")
            work_id = request.session.get("session_workId")
            select_table = "product_transit_" + str(work_id)
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            start_time = request.GET.get("start_time")
            end_time = request.GET.get("end_time")

            conn = db.get_connection(product_id)
            product_plan_code = request.GET.get("product_plan_code")
            if product_plan_code:
                product_plan_code_sql = " and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""

            if start_time:
                start_time_sql = " and out_time > " + "'" + start_time + "'"
            else:
                start_time_sql = ""
            if end_time:
                end_time_sql = " and out_time < " + "'" + end_time + "'"
            else:
                end_time_sql = ""

            pass_num = 0
            fail_num = 0
            sql_search = """
                   select * from {0} where 2>1 {1} {2} {3} group by finished_product_code order by out_time desc;
                   """
            sql_search = sql_search.format(select_table, product_plan_code_sql, start_time_sql, end_time_sql)
            dr_searchs = db.execute_sql(conn, sql_search)
            if dr_searchs:
                for dr_search in dr_searchs:
                    dict_data = {}
                    # dict_data["product_transit_code"] = dr_search[0]
                    # dict_data["matter_code"] = dr_search[1]
                    # dict_data["matter_id"] = dr_search[2]
                    dict_data["finished_product_code"] = dr_search[3]
                    dict_data["user_code"] = dr_search[4]
                    dict_data["work_code"] = dr_search[5]
                    dict_data["test_result"] = dr_search[6]
                    if dr_search[6] == "FAIL":
                        fail_num += 1
                    else:
                        pass_num += 1
                    # dict_data["description"] = dr_search[7]
                    if dr_search[8]:
                        dp = dr_search[8]
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S ")
                        dict_data["enter_time"] = dp
                    else:
                        dict_data["enter_time"] = ""
                    ds = dr_search[9]
                    sq = ds.strftime("%Y-%m-%d %H:%M:%S ")
                    dict_data["out_time"] = sq
                    #
                    # dict_data["enter_time"] = dr_search[8]
                    # dict_data["out_time"] = dr_search[9]
                    dict_data["product_plan_code"] = dr_search[10]
                    dict_data["product_name"] = product_id
                    # dict_data["end_product_code"] = dr_search[11]
                    # dict_data["product_code"] = dr_search[12]

                    sql_matter = """
                    select matter_code, matter_id from {0} where finished_product_code = '{1}'
                    """
                    sql_matter = sql_matter.format(select_table, dr_search[3])
                    dfs = db.execute_sql(conn, sql_matter)
                    matter_list = []
                    for df in dfs:
                        matter_dict = {}
                        matter_dict["matter_code"] = df[0]
                        matter_dict["matter_id"] = df[1]
                        matter_list.append(matter_dict)
                        dict_data["matter_list"] = matter_list

                    data_list.append(dict_data)

                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                dfs = int(len(data_list))
                sql_num_int = dfs
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                data_add_int["pass_num"] = pass_num
                data_add_int["fail_num"] = fail_num
                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("调取加工过站详情成功:")
                return HttpResponse(result)

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                data = {"code": 0, "message": "查询没有数据"}
                data = json.dumps(data)
                return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "加工站过站信息查询操作失败"}
            data = json.dumps(data)
            logger.error("加工站过站信息查询操作失败->,%s" % e)
            return HttpResponse(data)


class WorkUnqualifiedResult(View):
    """
    工站和不良原因联系表查询
    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))
            unqualified_result_code = request.GET.get("unqualified_result_code")
            work_id = request.GET.get("work_id")
            if unqualified_result_code:
                unqualified_result_code_sql = " and unqualified_result_code = " + "'" + unqualified_result_code + "'"
            else:
                unqualified_result_code_sql = ""
            if work_id:
                work_id_sql = " and work_id = " + "'" + work_id + "'"
            else:
                work_id_sql = ""


            sql_search = """
                               select * from work_unqualified_result where 2>1 {0} {1};
                               """
            sql_search = sql_search.format(unqualified_result_code_sql, work_id_sql)
            dr_searchs = db.execute_sql(conn, sql_search)
            if dr_searchs:
                for dr_search in dr_searchs:
                    dict_data = {}
                    dict_data["unqualified_result_code"] = dr_search[0]
                    dict_data["work_id"] = dr_search[1]
                    dict_data["unqualified_result_name"] = dr_search[2]
                    dict_data["content"] = dr_search[3]
                    dict_data["process_mode"] = dr_search[4]
                    dict_data["operate_user"] = dr_search[5]
                    if dr_search[6]:
                        dp = dr_search[6]
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                        dict_data["time"] = dp
                    else:
                        dict_data["time"] = ""
                    data_list.append(dict_data)
                data_list.sort(key=lambda x: (x['unqualified_result_code']), reverse=False)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                dfs = int(len(data_list))
                sql_num_int = dfs
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
                result = {"code": 0, "message": "操作成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("调取工站不良原因详情成功:")
                return HttpResponse(result)
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                logger.info("调取工站不良原因详情成功，没有数据:")
                return HttpResponse(result)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "操作失败"}
            data = json.dumps(data)
            logger.error("调取工站不良原因详情操作失败->,%s" % e)
            return HttpResponse(data)

    def post(self, request):
        try:
            product_id = request.session.get("session_projectId")
            json_data = request.body
            str_data = json.loads(json_data)
            db = DB()
            conn = db.get_connection(product_id)

            operate_user_code = request.session.get('session_currentId')       # 当前操作人
            work_id = str_data.get("work_id")
            unqualified_result_name = str_data.get("unqualified_result_name")
            content = str_data.get("content")
            process_mode = str_data.get("process_mode")

            conn_common = db.get_connection("db_common")

            sql_person = """
                        select user_name from person where user_code = '{0}'
                        """
            sql_person = sql_person.format(operate_user_code)
            dr_persons = db.execute_sql(conn_common, sql_person)
            if dr_persons:
                operate_user = dr_persons[0][0]
            else:
                sql_user = """
                select user_name from person where user_code = '{0}'
                """
                sql_user = sql_user.format(operate_user_code)
                dfs = db.execute_sql(conn, sql_user)
                if dfs:
                    operate_user = dfs[0][0]
                else:
                    operate_user = operate_user_code

            sql_filed = """
                       SELECT max(order_number) FROM work_unqualified_result;
                       """
            matter_type = db.execute_sql(conn, sql_filed)
            if matter_type[0][0] == None:
                field_num = 1
            else:
                field_num = matter_type[0][0] + 1
            unqualified_result_code = "F00000" + str(field_num)

            sql_insert_into = """
            insert into work_unqualified_result(unqualified_result_code, work_id, unqualified_result_name,
                                            content,
                                            process_mode, operate_user, order_number)
                                            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')
            """
            sql_insert_into = sql_insert_into.format(unqualified_result_code, work_id, unqualified_result_name,
                                                  content, process_mode, operate_user, field_num)

            drs = db.execute_sql(conn, sql_insert_into)

            data = {"code": 0, "message": "新增不良原因表成功"}
            logger.info("新增不良原因表成功")
            data = json.dumps(data)

            return HttpResponse(data)

        except Exception as e:
            print(e)
            data = {"code": 1, "message": "新增不良原因表失败"}
            logger.error("新增不良原因表失败")
            data = json.dumps(data)
            return HttpResponse(data)


class PutWorkUnqualifiedResult(View):
    def get(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            operate_user = request.GET.get("operate_user")  # 当前操作人
            work_id = request.GET.get("work_id")
            unqualified_result_name = request.GET.get("unqualified_result_name")
            content = request.GET.get("content")
            process_mode = request.GET.get("process_mode")
            unqualified_result_code = request.GET.get("unqualified_result_code")
            sql = """
                   update work_unqualified_result set
                  operate_user='{0}',work_id='{1}',unqualified_result_name='{2}',content='{3}',
                  process_mode='{4}' where unqualified_result_code = '{5}'
                   """
            sql = sql.format(operate_user, work_id, unqualified_result_name, content, process_mode,
                             unqualified_result_code)
            drs = db.execute_sql(conn, sql)
            result = {"code": 0, "message": "操作成功"}
            result = json.dumps(result)
            logger.info("修改不良原因表成功")
            return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("修改不良原因表失败")
            return HttpResponse(result)


class DeleteWorkUnqualifiedResult(View):
    """

    删除工站和不良原因的数据
    """
    def get(self, request):
        try:
            product_id = request.session.get("session_projectId")
            db = DB()
            conn = db.get_connection(product_id)

            unqualified_result_code = request.GET.get("unqualified_result_code")
            sql = """
            delete FROM work_unqualified_result where unqualified_result_code = '{0}'       
            """
            sql_format = sql.format(unqualified_result_code)
            db.execute_sql(conn, sql_format)
            data = {"code": 0, "message": "删除成功"}
            data = json.dumps(data)
            logger.info("删除不良原因成功")
            return HttpResponse(data)
        except Exception as e:
            data = {"code":1, "message": "删除失败"}
            data = json.dumps(data)
            logger.error("删除不良原因失败")
            return HttpResponse(data)


class OneProductInAllWorkStationInfo(View):
    """
    产品在各个工站的一些信息  包括在包装  检验  测试等工站    --> 产品的生命周期
    """

    def get_live_data(self, product_id, finished_product_code):
        func = product_live()
        data_list = func.one_product_live(product_id, finished_product_code)

        print("88888>", data_list)

        return data_list

    def get(self, request):
        try:
            # data_list = []
            data_add_int = {}

            product_id = request.session.get("session_projectId")
            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            finished_product_code = request.GET.get("finished_product_code")

            data_list = self.get_live_data(product_id, finished_product_code)

            print("------------sdsdsd>", data_list)



            data_list.sort(key=lambda x: (x['time']), reverse=False)


            page_result = Page(page, page_size, data_list)
            data = page_result.get_str_json()
            dfs = int(len(data_list))
            sql_num_int = dfs
            if dfs:
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int
            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0
            result = {"code": 0, "message": "调取成功", "data": data_add_int}
            result = json.dumps(result)
            logger.info("生命周期成功:")
            return HttpResponse(result)

        except Exception as e:
            data = {"code": 1, "message": "生命周期失败%s" % e}
            logger.error("生命周期失败%s" % e)
            data = json.dumps(data)
            print(e)
            return HttpResponse(data)


            # conn = db.get_connection(product_id)
            # db = DB()



            # if finished_product_code:
            #     finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            #     sn_sql = " and SN = " + "'" + finished_product_code + "'"
            # else:
            #     finished_product_code_sql = ""
            #     sn_sql = ""
            #
            # sql = """
            #        select * from work_station where work_type = '加工'
            #        """
            # drs = db.execute_sql(conn, sql)
            # jiagong_list = []
            # if drs:
            #     for dr in drs:
            #         jiagong_list.append(dr[1])
            #     for wor_id in jiagong_list:
            #         one_station = "product_transit_" + str(wor_id)
            #         sql_select = """
            #         select * from {0} where 2 > 1 {1} group by finished_product_code
            #         """
            #         sql_select = sql_select.format(one_station, finished_product_code_sql)
            #         dr_oneworks = db.execute_sql(conn, sql_select)
            #         if dr_oneworks:
            #             for dr_onework in dr_oneworks:
            #                 dict_one_data = {}
            #                 dict_one_data["finished_product_code"] = dr_onework[3]
            #                 dict_one_data["user_code"] = dr_onework[4]
            #                 dict_one_data["work_code"] = dr_onework[5]
            #                 dict_one_data["test_result"] = dr_onework[6]
            #                 if dr_onework[9]:
            #                     dp = dr_onework[9]
            #                     dp = dp.strftime("%Y-%m-%d %H:%M:%S")
            #                     dict_one_data["time"] = dp
            #                 else:
            #                     dict_one_data["time"] = ""
            #                 data_list.append(dict_one_data)
            #         else:
            #             pass
            #
            #     sql_other_table = """
            #     SELECT * FROM work_station left join work_transit on work_station.work_code = work_transit.work_code
            #     ;
            #     """
            #     # sql_other_table = sql_other_table.format(sn_sql)
            #     df_tbales = db.execute_sql(conn, sql_other_table)
            #     if df_tbales:
            #         for df_tab in df_tbales:
            #             if df_tab[7]:
            #                 sql_table = """
            #                 select SN, Result, time from {0} where 2 > 1 {1}
            #                 """
            #                 sql_table = sql_table.format(df_tab[7], sn_sql)
            #                 dffs = db.execute_sql(conn, sql_table)
            #                 if dffs:
            #                     for df in dffs:
            #                         da_dict = {}
            #                         da_dict["finished_product_code"] = df[0]
            #                         da_dict["test_result"] = df[1]
            #                         if df[2]:
            #                             dp = df[2]
            #                             dp = dp.strftime("%Y-%m-%d %H:%M:%S")
            #                             da_dict["time"] = dp
            #                         else:
            #                             da_dict["time"] = ""
            #                         da_dict["work_code"] = df_tab[0]
            #                         da_dict["user_code"] = ""
            #                         data_list.append(da_dict)
            #                 else:
            #                     pass
            #     else:
            #         pass
            #
            #
            #
            #     data_list.sort(key=lambda x: (x['time']), reverse=False)
            #     page_result = Page(page, page_size, data_list)
            #     data = page_result.get_str_json()
            #     dfs = int(len(data_list))
            #     sql_num_int = dfs
            #     data_add_int["data"] = data
            #     data_add_int["total"] = sql_num_int
            #     result = {"code": 0, "message": "操作成功", "data": data_add_int}
            #
            #     result = json.dumps(result)
            #     logger.info("调取产品的各个工站信息成功:")
            #     return HttpResponse(result)
            # else:
            #     result = {"code": 0, "message": "项目还未建加工站"}
            #     result = json.dumps(result)
            #     return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("产品的生命周期查询失败")
            return HttpResponse(result)


class NopageWorkUnqualifiedResultName(View):
    """
    不分页返回工站下 不良信息原因内码和名称

    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            # conn = db.get_connection("db_common")
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            work_id = request.GET.get("work_id")
            print("-=->", work_id)
            if work_id:
                work_id_sql = " and work_id = " + "'" + work_id + "'"
            else:
                work_id_sql = ""
            sql = """
            select * from work_unqualified_result where 2>1 {0}
            """
            sql = sql.format(work_id_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["unqualified_result_code"] = dr[0]
                    dict_data["unqualified_result_name"] = dr[2]
                    data_list.append(dict_data)

                data_add_int["data"] = data_list

                result = {"code": 0, "message": "调取成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("不分页返回工站下 不良信息原因内码和名称成功%s"% result)
                return HttpResponse(result)

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("不分页返回工站下 不良信息原因内码和名称失败")
            return HttpResponse(result)


class ProductCodeResponseResult(View):
    """
    根据不合格的成品码 返回他的不良原因码

    """
    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            product_id = request.session.get("session_projectId")

            conn = db.get_connection(product_id)
            finished_product_code = request.GET.get("finished_product_code")
            # finished_product_code = "zz"

            if finished_product_code:
                finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""

            sql_tables = """
            show tables like "unqualified_product_%" 
            """
            un_tables = db.execute_sql(conn, sql_tables)

            if un_tables:
                for un_table in un_tables:
                    sql_search = """
                    select finished_product_code, description from {0} where description like "%F0000%" {1} group by finished_product_code
                    """
                    sql_search = sql_search.format(un_table[0], finished_product_code_sql)
                    dfs = db.execute_sql(conn, sql_search)
                    if dfs:
                        for df in dfs:
                            dict_data = {}
                            dict_data["finished_product_code"] = df[0]
                            dict_data["description"] = df[1]
                            data_list.append(dict_data)
                    else:
                        pass

                if data_list:

                    result = {"code": 0, "message": "操作成功", "data": data_list}
                    result = json.dumps(result)
                    logger.info("根据不合格的成品码 返回他的不良原因码成功%s"% result)
                    return HttpResponse(result)
                else:
                    result = {"code": 0, "message": "此产品没有不良原因码", "data": data_list}
                    result = json.dumps(result)
                    logger.info("根据不合格的成品码 返回他的不良原因码成功, 此产品没有不良原因码%s" % result)
                    return HttpResponse(result)
            else:
                result = {"code": 0, "message": "没有创建加工工站", "data":data_list}
                result = json.dumps(result)
                logger.error("根据不合格的成品码 返回他的不良原因码, 没有创建加工工站")
                return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("根据不合格的成品码 返回他的不良原因码失败%s"% e)
            return HttpResponse(result)



class ModifyInWorkStation(View):

    def get_live_data(self, product_id, finished_product_code):
        func = product_live()
        data_list = func.one_product_live(product_id, finished_product_code)

        return data_list

    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            # conn = db.get_connection("db_common")
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            finished_product_code = request.GET.get("finished_product_code")
            product_plan_code = request.GET.get("product_plan_code")
            status = request.GET.get("status")

            if finished_product_code:
                finished_product_code_sql = " and finished_product_code = " + "'" + finished_product_code + "'"
            else:
                finished_product_code_sql = ""
            if product_plan_code:
                product_plan_code_sql = " and product_plan_code = " + "'" + product_plan_code + "'"
            else:
                product_plan_code_sql = ""
            if status:
                status_sql = " and status = " + "'" + status + "'"
            else:
                status_sql = ""

            sql = """
                   select * from modify_in_workstation where 2>1 {0} {1} {2}
                   """
            sql = sql.format(finished_product_code_sql, product_plan_code_sql, status_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["modify_in_workstation_code"] = dr[0]
                    dict_data["product_name"] = dr[1]
                    dict_data["finished_product_code"] = dr[2]
                    dict_data["work_id"] = dr[3]
                    dict_data["product_plan_code"] = dr[4]
                    dict_data["operate_user"] = dr[5]
                    if dr[6]:
                        dp = dr[6]
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                        dict_data["enter_time"] = dp
                    else:
                        dict_data["enter_time"] = ""
                    if dr[7]:
                        ds = dr[7]
                        ds = ds.strftime("%Y-%m-%d %H:%M:%S")
                        dict_data["out_time"] = ds
                    else:
                        dict_data["out_time"] = ""
                    dict_data["process_method"] = dr[8]
                    dict_data["status"] = dr[9]
                    dict_data["enter_work_code"] = dr[10]
                    data_list.append(dict_data)
                data_list.sort(key=lambda x: (x['enter_time']), reverse=True)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                dfs = int(len(data_list))
                sql_num_int = dfs
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "操作成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("不良品进入维修工站成功%s" % result)
                return HttpResponse(result)

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("不良品进入维修工站失败%s"% e)
            return HttpResponse(result)

    def post(self, request):
        try:
            db = DB()
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)
            json_data = request.body

            str_data = json.loads(json_data)

            finished_product_code = str_data.get("finished_product_code")
            product_plan_code = str_data.get("product_plan_code")
            # enter_work_code = str_data.get("enter_work_code")  # ZIAAAAAAAAAAAAAAAA
            work_id = request.session.get('session_workId')

            data_list = self.get_live_data(product_id, finished_product_code)
            data_list.sort(key=lambda x: (x['time']), reverse=False)
            if data_list:
                enter_work_code = data_list[-1]["work_code"]
            else:

                data = {"code": 1, "message": "此产品没有任何生命周期,没有经过任何工站"}
                logger.info("此产品没有任何生命周期,没有经过任何工站")
                data = json.dumps(data)
                return HttpResponse(data)

            data_list = []
            data_add_int = {}

            sql_work_code = """
            select work_code from work_station where work_id = '{0}'
            """
            sql_work_code = sql_work_code.format(work_id)
            drs = db.execute_sql(conn, sql_work_code)
            if drs:
                work_id = drs[0][0]
            else:
                work_id = work_id

            operate_user = request.session.get('session_currentId')  # 当前操作人
            status = str_data.get("status")

            sql_filed = """
                       SELECT max(order_number) FROM modify_in_workstation;
                       """
            matter_type = db.execute_sql(conn, sql_filed)
            if matter_type[0][0] == None:
                field_num = 1
            else:
                field_num = matter_type[0][0] + 1
            modify_in_workstation_code = "Im_Modi_In_Sta_" + str(field_num)

            sql_check = """
            select status from modify_in_workstation where finished_product_code = '{0}'
            """
            sql_check = sql_check.format(finished_product_code)
            drs_checks = db.execute_sql(conn, sql_check)

            print("===--=-=-=>>>", drs_checks)

            if drs_checks:
                da_list = []
                for dr_check in drs_checks:
                    da_list.append(dr_check[0])

                if "入站" in da_list:
                    result = {"code": 1, "message": "此产品已经存在维修表中,不能重复添加"}
                    result = json.dumps(result)
                    logger.error("此产品已经存在维修表中,不能重复添加%s")
                    return HttpResponse(result)
                else:
                    sql_insert_into = """
                            insert into modify_in_workstation(modify_in_workstation_code, product_name, 
                                                            finished_product_code,
                                                            work_id,
                                                            product_plan_code, operate_user,
                                                             status, enter_work_code, order_number)
                                                            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                                                            '{7}', '{8}')
                                                """
                    sql_insert_into = sql_insert_into.format(modify_in_workstation_code, product_id,
                                                             finished_product_code,
                                                             work_id, product_plan_code,
                                                             operate_user, status, enter_work_code, field_num)
                    drs = db.execute_sql(conn, sql_insert_into)

                    data = {"code": 0, "message": "新增维修成功"}
                    logger.info("新增维修成功")
                    data = json.dumps(data)

                    return HttpResponse(data)

            else:
                sql_insert_into = """
                            insert into modify_in_workstation(modify_in_workstation_code, product_name, 
                                                            finished_product_code,
                                                            work_id,
                                                            product_plan_code, operate_user,
                                                            status, enter_work_code, order_number)
                                                            values('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}',
                                                            '{7}', '{8}')
                            """
                sql_insert_into = sql_insert_into.format(modify_in_workstation_code, product_id, finished_product_code,
                                                         work_id, product_plan_code,
                                                         operate_user,status, enter_work_code, field_num)

                drs = db.execute_sql(conn, sql_insert_into)

                data = {"code": 0, "message": "新增维修成功"}
                logger.info("新增维修成功")
                data = json.dumps(data)

                return HttpResponse(data)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("新增维修成功%s" % e)
            return HttpResponse(result)


class AnalyseWorkStationInfo(View):

    def get(self, request):
        try:
            data_list = []
            data_add_int = {}
            db = DB()
            # conn = db.get_connection("db_common")
            product_id = request.session.get("session_projectId")
            conn = db.get_connection(product_id)

            page = int(request.GET.get("page"))
            page_size = int(request.GET.get("page_size"))

            work_type = request.GET.get("work_type")

            if status:
                status_sql = " and status = " + "'" + status + "'"
            else:
                status_sql = ""

            sql = """
                   select * from modify_in_workstation where 2>1 {0} {1} {2}
                   """
            sql = sql.format(finished_product_code_sql, product_plan_code_sql, status_sql)
            drs = db.execute_sql(conn, sql)
            if drs:
                for dr in drs:
                    dict_data = {}
                    dict_data["modify_in_workstation_code"] = dr[0]
                    dict_data["product_name"] = dr[1]
                    dict_data["finished_product_code"] = dr[2]
                    dict_data["work_id"] = dr[3]
                    dict_data["product_plan_code"] = dr[4]
                    dict_data["operate_user"] = dr[5]
                    if dr[6]:
                        dp = dr[6]
                        dp = dp.strftime("%Y-%m-%d %H:%M:%S")
                        dict_data["enter_time"] = dp
                    else:
                        dict_data["enter_time"] = ""
                    if dr[7]:
                        ds = dr[7]
                        ds = ds.strftime("%Y-%m-%d %H:%M:%S")
                        dict_data["out_time"] = ds
                    else:
                        dict_data["out_time"] = ""
                    dict_data["process_method"] = dr[8]
                    dict_data["status"] = dr[9]
                    dict_data["enter_work_code"] = dr[10]
                    data_list.append(dict_data)
                data_list.sort(key=lambda x: (x['enter_time']), reverse=True)
                page_result = Page(page, page_size, data_list)
                data = page_result.get_str_json()
                dfs = int(len(data_list))
                sql_num_int = dfs
                data_add_int["data"] = data
                data_add_int["total"] = sql_num_int

                result = {"code": 0, "message": "操作成功", "data": data_add_int}
                result = json.dumps(result)
                logger.info("不良品进入维修工站成功%s" % result)
                return HttpResponse(result)

            else:
                data_add_int["data"] = []
                data_add_int["total"] = 0

                result = {"code": 0, "message": "查询没有数据", "data": data_add_int}
                result = json.dumps(result)
                return HttpResponse(result)

        except Exception as e:
            print(e)
            result = {"code": 1, "message": "操作失败", "data": e}
            result = json.dumps(result)
            logger.error("不良品进入维修工站失败%s" % e)
            return HttpResponse(result)

































































































































