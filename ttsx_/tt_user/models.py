from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    isValid=models.BooleanField(default=True)
    isActive=models.BooleanField(default=False)
    def __str__(self):
        return self.uname

class UserAddressInfo(models.Model):
    uname=models.CharField(max_length=20)
    uaddress=models.CharField(max_length=100)
    uphone=models.CharField(max_length=11)
    user=models.ForeignKey('UserInfo')