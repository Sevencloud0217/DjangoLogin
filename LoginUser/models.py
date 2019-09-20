from django.db import models
class LoginUser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)
    username = models.CharField(max_length=32,null=True,blank=True)
    phone_number = models.CharField(max_length=11,null=True,blank=True)
    photo = models.ImageField(upload_to='images',null=True,blank=True)
    age = models.IntegerField(null=True,blank=True)
    gender = models.CharField(null=True,blank=True,max_length=4)
    address = models.TextField(null=True,blank=True)
    #null 针对数据库 表示可以为空 即在数据库的存储中可以为空
    #black 针对表单 ，表示在表单字段中可以不用填，但针对数据可不影响
    class Meta:
        db_table="LoginUser"
class Goods(models.Model):
    goods_number = models.CharField(max_length=11)
    goods_name = models.CharField(max_length=32)
    goods_price = models.FloatField()
    goods_count = models.IntegerField()
    goods_location = models.CharField(max_length=254)
    goods_safe_data = models.IntegerField()
    goods_pro_time = models.DateField(auto_now=True,verbose_name='生产日期')
    class Meta:
        db_table = 'Goods'

# Create your models here.
