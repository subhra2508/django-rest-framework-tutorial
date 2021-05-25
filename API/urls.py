"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from restapi.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('stucreate/', student_create),

    # function based api views
    # path('studentapi/', student_api),
    # path('studentapi/<str:pk>/', student_api),

    # classBased api views
    # path('studentapi/', StudentAPI.as_view()),
    # path('studentapi/<str:pk>/', StudentAPI.as_view()),

    # using genericviews and mixin
    # path('studentapi/', StudentList.as_view()),
    # path('studentapi/', StudentCreate.as_view()),
    # path('studentapi/<str:pk>/', StudentRetrive.as_view()),
    # path('studentapi/<str:pk>/', StudentUpdate.as_view()),
    # path('studentapi/<str:pk>/', StudentDestroy.as_view()),
    path('studentapi/', LCStudentAPI.as_view()),
    path('studentapi/<str:pk>/', RUDStudentAPI.as_view()),
]
#  path('stuinfo/<str:pk>/', student_details),
#  path('stuinfo/', student_list),
