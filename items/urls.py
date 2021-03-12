from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.http import HttpResponse
from rest_framework.decorators import api_view

from items import views

urlpatterns = [
    path('', views.index, name='item_view'),
    path('search', views.search, name='search_item'),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\n"
                                               "Disallow: /*?\n"
                                               "Disallow: /admin/\n"
                                               "Sitemap: https://albionprofits.tk/static/items/data/sitemap.xml",
                                               content_type="text/plain"), name="robots_file"),
    url('api/albion/prices/cities', views.two_city_compare, name='two_cities'),
    path('info', views.info, name='info_page'),
    path('api', views.development, name='api_info'),
    path('changelog', views.changelog, name='changelog_page'),
    path('accounts/profile', views.profile, name='account_profile')
]