from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from .forms import CreateUserForm, QuoteForm, BuyForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .helpers import lookup, usd


@login_required(login_url='login')
def index(request):
    # If no user is signed in, return to login page:     
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("login"))
    return render(request, "spondulator/index.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":

            # Attempt to sign user in
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            # Check if authentication successful
            if user is not None:
                login(request, user)
                messages.success(request, username + "has successfuly logged in.")
                return redirect("index")
            else:
                messages.info(request, "Username OR password is incorrect")
                return render(request, "spondulator/login.html")
        else:
            return render(request, "spondulator/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfuly.")
    return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:        
        form = CreateUserForm()
        if request.method == "POST":
            form = CreateUserForm(request.POST)
            if form.is_valid():
                # Attempt to create new user
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, "Account was created for " + username)
                
                return redirect("login")
        
        return render(request, "spondulator/register.html", {
            'form': form
        })

@login_required(login_url='login')
def quote(request):
    """Get stock quote."""
    if request.method == "POST":

        # Ensure quote symbol was submitted
        # if not request.form.get("symbol"):
        #     return apology("must provide symbol", 400)

        form = QuoteForm(request.POST)

        if form.is_valid():
            stock_data = lookup(form.cleaned_data["symbol"])

            # Ensure it is valid symbol
            if not stock_data:
                return render(request, "spondulator/quote.html", {
                    "form": form,
                    "message": "Invalid Symbol !!"
                })

            return render(request, "spondulator/quoted.html", {
                "name": stock_data["name"], 
                "symbol": stock_data["symbol"], 
                "price": usd(stock_data["price"]),
            })

    else:
        return render(request, "spondulator/quote.html", {
            "form": QuoteForm()
        })

@login_required(login_url='login')
def buy(request):
    return render(request, "spondulator/buy.html", {
            "form": BuyForm()
        })

