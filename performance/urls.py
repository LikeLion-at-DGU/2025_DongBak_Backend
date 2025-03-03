from django.urls import path, include
from rest_framework import routers

from .views import *

from django.conf.urls.static import static
from django.conf import settings

app_name = "performance"

defalut_router = routers.SimpleRouter(trailing_slash=False)
defalut_router.register("home", PerformanceViewSet, basename="home")

urlpatterns = [
    path('', include(defalut_router.urls)),
    path('upload-performance-data', PerformanceDataView.as_view(), name='upload_performance_data')
]