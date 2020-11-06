from django.test import TestCase
from .models import Cash, Purchase
from django.contrib.auth.models import User

# Create your tests here.
class PurchaseTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username="Jiggy")
        Purchase.objects.create(my_user=user1, stock="NFLX", shares=5, price=100.00)
        Purchase.objects.create(my_user=user1, stock="NFLX", shares=5, price=-100.00)
        Purchase.objects.create(my_user=user1, stock="NFLX", shares=-5, price=100.00)
        Purchase.objects.create(my_user=user1, stock="NETFLX", shares=5, price=100.00)

    def test_valid_purchase(self):
        user1 = User.objects.get(username="Jiggy")
        p = Purchase.objects.get(my_user=user1, stock="NFLX", shares=5, price=100.00)
        self.assertTrue(p.is_valid_purchase())

    def test_invalid_purchase_stock(self):
        user1 = User.objects.get(username="Jiggy")
        p = Purchase.objects.get(my_user=user1, stock="NETFLX", shares=5, price=100.00)
        self.assertFalse(p.is_valid_purchase())

    def test_invalid_purchase_shares(self):
        user1 = User.objects.get(username="Jiggy")
        p = Purchase.objects.get(my_user=user1, stock="NFLX", shares=-5, price=100.00)
        self.assertFalse(p.is_valid_purchase())

    def test_invalid_purchase_price(self):
        user1 = User.objects.get(username="Jiggy")
        p = Purchase.objects.get(my_user=user1, stock="NFLX", shares=5, price=-100.00)
        self.assertFalse(p.is_valid_purchase())