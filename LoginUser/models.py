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
# Create your models here.
