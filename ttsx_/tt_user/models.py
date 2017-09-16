from django.db import models

# Create your models here.

class UserInfoManager(models.Manager):
    # def get_queryset(self):
    #     return super().get_queryset().filter(isValid=True)

    def create(self, uname, upwd, uemail):
        user = UserInfo()
        user.uname = uname
        user.upwd = upwd
        user.uemail = uemail
        user.isValid = True
        user.isActive = False
        return user

class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    isValid=models.BooleanField(default=True)
    isActive=models.BooleanField(default=False)
    users = UserInfoManager()
    class Meta:
        db_table = 'user_info'

class UserAddressInfo(models.Model):
    uname=models.CharField(max_length=20)
    uaddr_detail=models.CharField(max_length=100)
    uphone=models.CharField(max_length=11)
    user=models.ForeignKey('UserInfo')
    ucode = models.CharField(default='', max_length=6)
    class Meta:
        db_table = 'user_address'