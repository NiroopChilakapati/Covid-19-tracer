
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name = 'covid_project'),
    path('stats', stats, name = 'covid_project'),
    path('Recovery & Resources', resorse, name= 'covid_project'),
    path('about', about, name= 'covid_project'),
    path('contact', contact, name= 'covid_project'),
    path('privacy', privacy , name = 'covid_project'),
    path('adminlogin', adminlogin, name='adminlogin'),
    path('welcome', welcome, name='welcome'),
    path('contactdet', contactdet, name='contactdet'),
    path('logout', custom_logout, name='logout'),
    path('get-country/', get_country ),
    path('login/', login_view,name='login'),
    path('signup/', signup_view,name='signup')



]