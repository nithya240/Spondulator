from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class QuoteForm(forms.Form):
    symbol = forms.CharField(label="Symbol ", max_length=5)

class BuyForm(forms.Form):
    symbol = forms.CharField(label="Symbol ", max_length=5)
    shares = forms.IntegerField(label="Shares ", min_value=1)