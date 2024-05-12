from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('sign_up', sign_up),
    path('login', user_login),
    path('', main_page),
    path('logout', user_logout),
]
