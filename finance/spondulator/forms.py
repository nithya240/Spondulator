from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class QuoteForm(forms.Form):
    symbol = forms.CharField(label="Symbol ", max_length=5)
    error_css_class = 'error'
    required_css_class = 'bold'

class BuyForm(forms.Form):
    symbol = forms.CharField(label="Symbol", max_length=5)
    shares = forms.IntegerField(label="Shares", min_value=1)
    error_css_class = 'error'
    required_css_class = 'bold'


#
# Error: So we will create Sell Form in html only
#
# class SellForm(forms.Form):

#     stocks = []

#     def __init__(self, stocks, *args, **kwargs):
#         super(SellForm, self).__init__(*args, **kwargs)
#         self.stocks = stocks

#     CHOICES = ()
#     for stock in stocks:
#         another_choice = ('stock', 'stock')
#         CHOICES += another_choice

#     # CHOICES = (
#     #     (11, 'Credit Card'),
#     #     (12, 'Student Loans'),
#     #     (13, 'Taxes'),
#     # )

#     symbol = forms.ChoiceField(label=stocks[0], choices=CHOICES)
#     shares = forms.IntegerField(label="Shares ", min_value=0)