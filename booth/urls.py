from django.urls import path, include
from rest_framework import routers

from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "booth"

defalut_router = routers.SimpleRouter(trailing_slash=False)
defalut_router.register("home", BoothViewSet, basename="home")

food_truck_router = routers.SimpleRouter(trailing_slash=False)
food_truck_router.register("foodtruck", FoodTruckViewSet, basename="foodtruck")

urlpatterns = [
    path("", include(defalut_router.urls)),
    path("", include(food_truck_router.urls)),
    path("search", SearchView.as_view(), name='search')
]