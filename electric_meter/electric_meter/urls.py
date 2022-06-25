"""electric_meter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path("index", views.index),
    path("", views.index),
    path('recognition', login_required(views.recognition)),
    path('pic_upload', login_required(views.pic_upload)),
    path("info_upload", login_required(views.info_upload)),
    path("info_list", login_required(views.info_list)),
    path("to_excel", login_required(views.to_excel)),
    path(r'user', views.user_view),
    path(r'user_oper', views.user_oper),
    path(r'logout', views.logout_view),
]
