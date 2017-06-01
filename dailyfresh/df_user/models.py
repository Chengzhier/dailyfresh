from django.db import models

# Create your models here.


class login(models.Model):
    uname = models.CharField(max_length=20)
    upaswd = models.CharField(max_length=20)


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    ushou = models.CharField(max_length=20,default='')
    uemail = models.CharField(max_length=30)
    uaddress = models.CharField(max_length=100,default='')
    utel = models.CharField(max_length=11,default='')
    ucode = models.CharField(max_length=6,default= '')



