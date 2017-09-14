from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('tt_user.UserInfo')
    goods=models.ForeignKey('goods.GoodsInfo')
    count=models.IntegerField()
    def __str__(self):
        return self.user.uname