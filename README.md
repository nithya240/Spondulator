# Spondulator - The Financial Education System

Spondulator is a stock market learning tool designed and developed to help people make better financial decisions in life. By using this application, the users will not only be able to make the better financial decisions in life but will also gain the confidence to invest in the real-world stock market game and win the same.

## Description:

 Spondulator provides a better way to learn the stock market by experiencing the same in the virtual environment, which seems to be intimidating to do so in the real world with the help of real money. The system gives some initial amount of virtual money to the users to play with, using which they can look up for the stock data, buy the stock, as well as sell it. The application also shows the calculated profit or loss on the total committed money. The IBM Watson Cloud technology is used to perform sentiment analysis about any company from different news sources which is then classified into positive, negative or neutral category in order to make an informed decision. This can also help to make an investment decision around the company’s future value. It is a distributed system which uses the third party API from the IEX cloud to fetch real-time stock value, as well as the IBM Watson Discovery service to get latest news about any company. 

## Configuration and Running:

Steps to create new Django Project and new app inside it:
1. django-admin startproject PROJECT_NAME
2. cd PROJECT_NAME
3. python manage.py startapp APP_NAME
4. Add the APP_NAME in settings.py in list of INSTALLED_APPS
5. Register urls in project level urls.py (default one), as well as in app level urls.py after creating the urls.py in your app.

After cloning the spondular in your pc, remove db.sqlite3, pycache, and migrations folder as well from all sub folders of django project.

NOTE: Name of our django project is finance and the app inside it is spondulator.
Once removing above files, run the following commands in your terminal:
1. python manage.py makemigrations spondulator
2. python manage.py migrate
3. python manage.py runserver

NOTE: You can visit to "/admin" app to see the models i.e. tables in our database and modify the same from the admin panel only which is a Django default app.
 

## Development Tools:

* Languages: HTML 5, CSS 3, Python

* Library: Bootstrap 4

* Framework: Django

* API's: IBM Watson Discovery service, IEX Cloud API

* Tools: Trello, Visual Studio Code, Git


