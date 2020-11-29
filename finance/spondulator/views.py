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

from .helpers import lookup, usd, lookInCloud
from .models import Cash, Purchase

from django.db.models import Sum

import json



@login_required(login_url='login')
def index(request):
    cash = request.user.cash.in_hand_money
    
    # Query to be fired
    # SELECT stock, SUM(shares) FROM purchase WHERE id = user_id GROUP BY stock ORDER BY stock
    # purchases = request.user.purchases.all()
    # purchases = Purchase.objects.values('stock').annotate(total_shares=Sum('shares')).order_by('stock')

    purchases = request.user.purchases.all()
    grouped_purchases = purchases.values('stock').annotate(total_shares=Sum('shares')).order_by('stock')

    total = cash
    # Modifying list of purchases and adding new key-values to each purchase obj
    for purchase in grouped_purchases:
        stock_data = lookup(purchase["stock"])
        purchase["stock"] = stock_data["symbol"]
        purchase["price"] = usd(stock_data["price"])
        purchase["name"] = stock_data["name"]
        purchase["sum"] = usd(purchase["total_shares"] * stock_data["price"])
        total = float(total) + float(purchase["total_shares"] * stock_data["price"])

    return render(request, "spondulator/index.html", {
        "total": usd(total),
        "cash": usd(cash),
        "purchases": grouped_purchases
    })


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
                # messages.success(request, username + "has successfuly logged in.")
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
    """Buy shares of stock"""
    if request.method == "POST":
        form = BuyForm(request.POST)

        if form.is_valid():

            stock_symbol = form.cleaned_data["symbol"]
            total_shares = form.cleaned_data["shares"]
            
            stock_data = lookup(stock_symbol)

            # Ensure it is valid symbol
            if not stock_data:
                return render(request, "spondulator/buy.html", {
                    "form": form,
                    "message": "Invalid Symbol !!"
                })

            # Ensure user has enough cash to purchase shares
            stock_price = stock_data["price"]
            total_cost = float(stock_price) * int(total_shares)

            if float(request.user.cash.in_hand_money) < total_cost:
                return render(request, "spondulator/buy.html", {
                    "form": form,
                    "message": "Sorry you don't have enough cash !!"
                })

            # Commit a transaction for the user and insert data in Purchase table
            transaction = Purchase(my_user=request.user, stock=stock_symbol, shares=total_shares, price=stock_price)
            transaction.save()

            # Update in_hand_money for cash table for the given user
            request.user.cash.in_hand_money -= total_cost
            request.user.cash.save()

            messages.success(request, str(total_shares) + " shares of " + stock_symbol + " was bought !!")
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "spondulator/buy.html", {
            "form": BuyForm()
        })


@login_required(login_url='login')
def sell(request):
    """Sell shares of stock"""

    if request.method == "POST":
        stock_symbol = request.POST.get("symbol")
        total_shares = request.POST.get("shares")

        # Ensure quote symbol was submitted
        if not stock_symbol:
            return render(request, "spondulator/sell.html", {
                    "message": "Must Provide Symbol !!"
                })

        # Ensure total no of shares was submitted
        if not total_shares:
            return render(request, "spondulator/sell.html", {
                    "message": "Missing Shares !!"
                })

        # Ensure total no of shares is number
        if not total_shares.isnumeric():
            return render(request, "spondulator/sell.html", {
                    "message": "Invalid Input !!"
                })

        # Ensure total no of shares is greater than 1 by server
        if int(total_shares) < 1:
            return render(request, "spondulator/sell.html", {
                    "message": "Invalid Input !!"
                })

        purchases = request.user.purchases.all()
        # Grouped_purchases = purchases.values('stock').annotate(total_shares=Sum('shares'))
        grouped_purchases = purchases.filter(stock=stock_symbol).annotate(total_shares=Sum('shares'))

        total_shares = int(total_shares)

        if len(grouped_purchases) == 0:
            return render(request, "spondulator/sell.html", {
                    "message": "You don't have this stock !!"
                })

        if total_shares > grouped_purchases[0].total_shares:
            return render(request, "spondulator/sell.html", {
                    "message": "Too many shares !!"
                })

        # Lookup for stock & know it's current val nd then sell it
        stock_data = lookup(stock_symbol)

        # Update shares column in purchase table
        transaction = Purchase(my_user=request.user, stock=stock_symbol, shares=-total_shares, price=stock_data["price"])
        transaction.save()

        # Update in_hand_money for cash table for the given user
        request.user.cash.in_hand_money += stock_data["price"]*total_shares
        request.user.cash.save()

        messages.success(request, str(total_shares) + " shares of " + stock_symbol + " was sold !!")
        return HttpResponseRedirect(reverse("index"))
    else:
        purchases = request.user.purchases.all()
        stocks = set()
        for purchase in purchases:
            stock = purchase.stock
            stocks.add(stock)
        return render(request, "spondulator/sell.html", {
            "stocks": stocks
        })

@login_required(login_url='login')
def history(request):
    """Show history of transactions"""
    purchases = request.user.purchases.all()
    return render(request, "spondulator/history.html", {
        "purchases": purchases
    })


def company(request):
    if request.method == "POST":

        form = QuoteForm(request.POST)
        if form.is_valid():
            stock_data = lookup(form.cleaned_data["symbol"])

            # Ensure it is valid symbol
            if not stock_data:
                return render(request, "spondulator/company.html", {
                    "form": form,
                    "message": "Invalid Symbol !!"
                })

            company_info = lookInCloud(form.cleaned_data["symbol"])

            title = json.dumps(company_info["results"][0]["title"], indent=2)

            articles = company_info["results"]
            #news_list = company_info["results"]
            #news = [news_list[x:x+3] for x in range(0, len(news_list), 3)]
            # news = [{}] * len(articles)

            # obj = {}

            positive = 0
            negative = 0
            neutral = 0
            for article in articles:
                article["posted"] = json.dumps(article.get("publication_date", None), indent=2).strip('"')
                article["author"] = json.dumps(article.get("author", None), indent=2).strip('"')
                article["sentiment"] = json.dumps(article["enriched_text"]["sentiment"]["document"].get("label", None), indent=2).strip('"')
                article["title"] = json.dumps(article.get("title", None), indent=2).strip('"')
                article["url"] = json.dumps(article.get("url", None), indent=2)

                if article["author"] == "null":
                    article["author"] = "None"

                if article.get('sentiment') == "positive":
                    positive += 1

                elif article.get('sentiment') == "negative":
                    negative += 1

                else:
                    neutral += 1
               

            return render(request, "spondulator/company.html", {
                "form": form,
                "flag": True,
                "name": stock_data["name"],
                "title": title,
                "articles": articles,
                "positive": positive,
                "negative": negative,
                "neutral": neutral
            })
            
    return render(request, "spondulator/company.html", {
        "form": QuoteForm(),
    })


# <form action="{% url 'company' %}" method="post">
#         {% csrf_token %}
#         {{ form }}
#         <input type="submit" placeholder="Get Insights">
#     </form>