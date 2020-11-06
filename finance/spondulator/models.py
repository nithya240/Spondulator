#from django.conf import settings
from django.db import models

from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


class Cash(models.Model):
    # By default related name will be cash
    my_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cash")
    in_hand_money = models.IntegerField(default=10000)
    net_profit = models.IntegerField(default=0)

    def __str__(self):
        return f"Currently, the {self.my_user.username} has cash = {self.in_hand_money} in hand and net profit/loss = {self.net_profit}"

# Autometically creating Cash instance whenever new User is created
@receiver(post_save, sender=User, dispatch_uid='add_cash_for_new_user')
def add_cash(sender, instance, created, **kwargs):
    user = instance
    if created:
        cash = Cash(my_user=user)
        cash.save()

class Purchase(models.Model):
    my_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")
    stock = models.CharField(max_length=5, null=True)
    shares = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    bought_at = models.DateTimeField(auto_now_add=True, null=True)

    # Adding a Test Case 
    def is_valid_purchase(self):
        return self.shares > 0 and self.price > 0 and (len(self.stock) > 0 and len(self.stock) <= 5)
