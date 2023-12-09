from django.urls import path
from . import views
from .views import (search_api, user_feed)

app_name = 'home'

urlpatterns = [
     path('', user_feed, name='home'),
     path('search-api/', views.search_api, name='search_api'),
]