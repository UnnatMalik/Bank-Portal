from django.urls import path
from . import views
urlpatterns = [
    path("",views.stock_home,name='stock_home'),
    path("watchlist/",views.stock_watchlist,name='stock_watchlist'),
    path("details/",views.stock_details,name='stock_details'),
]