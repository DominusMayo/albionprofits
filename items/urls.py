from django.urls import path

from items import views

urlpatterns = [
    path('', views.index, name='item_view'),
    path('search', views.search, name='search_item')
]