from django.urls import path, re_path
from rest_framework import routers

from . import views
from .views import InOutWarehouseViewSet

url = routers.SimpleRouter()
url.register(r'in_out_warehouse', InOutWarehouseViewSet)
urlpatterns = []
urlpatterns += url.urls