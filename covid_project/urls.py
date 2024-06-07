"""
URL configuration for covid_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler400, handler403, handler404, handler500

admin.site.site_header = "Covid-19 Tracker"
admin.site.index_title = "Welcome to covid-19 Tracker"
admin.site.site_title = "Covid-19 Tracker"

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('covid_app.urls'))
]

handler404 = 'covid_app.views.error_404'

