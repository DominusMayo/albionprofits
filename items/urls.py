from django.urls import path
from django.conf.urls import url
from django.http import HttpResponse

from items import views

urlpatterns = [
    path('', views.index, name='item_view'),
    path('search', views.search, name='search_item'),
    url(r'^robots.txt', lambda x: HttpResponse("User-Agent: *\n"
                                               "Disallow: /*?\n"
                                               "Disallow: /admin/\n"
                                               "Sitemap: static/items/data/sitemap.xml", content_type="text/plain"), name="robots_file"),
]