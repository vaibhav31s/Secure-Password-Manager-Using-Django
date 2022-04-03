from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse
from . import views
urlpatterns = [
   path('', views.index,name="index"),
   path('login',views.logins,name="login"),
   path('signup',views.signup,name="signup"),
   path('add',views.add,name="add"),
   path('signout',views.signout,name="signout")
   

] 
