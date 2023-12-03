from django.urls import path
from . import views
from .views import (search_api)

app_name = 'home'

urlpatterns = [
     path('', views.home, name='home'),
     path('search-api/', views.search_api, name='search_api'),
]