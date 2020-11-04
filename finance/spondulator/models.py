#from django.conf import settings
from django.db import models

from django.contrib.auth.models import User


class Cash(models.Model):
    # By default related name will be cash
    my_user = models.OneToOneField(User, on_delete=models.CASCADE, )
    in_hand_money: models.IntegerField(default=10000)
    net_profit: models.IntegerField(default=0)

# class Purchase(models.Model):
#     my_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
#     stock: models.CharField(max_length=5)
#     shares: models.IntegerField()
#     price: models.FloatField()
#     bought_at: models.DateTimeField(auto_now_add=True)
