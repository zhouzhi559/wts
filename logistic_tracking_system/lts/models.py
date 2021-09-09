from django.db import models

# Create your models here.


# class CustomInfo(models.Model):
#
#     nid = models.AutoField(primary_key=True)
#     custom_id = models.CharField(max_length=8, unique=True, null=False, verbose_name="客户编号")
#     custom_name = models.CharField(max_length=64, null=True, verbose_name="客户名称")
#     custom_address = models.CharField(max_length=64, null=True, verbose_name="客户地址")
#     custom_telephone = models.CharField(max_length=11, null=True, verbose_name="客户电话")
#     create_time = models.DateField(verbose_name='创建时间', auto_now_add=True)
#
#     class Meta:
#         db_table ="custom_info"
#         verbose_name = "客户信息表"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.custom_name
#
#
# class Order(models.Model):
#
#     nid = models.AutoField(primary_key=True)
#     order_id = models.CharField(max_length=8, unique=True, null=False, verbose_name="订单编号")
#     order_status = models.CharField(max_length=8, unique=True, null=False, verbose_name="订单编号")
#
#

