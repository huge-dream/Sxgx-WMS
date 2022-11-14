from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from in_out_warehouse.models import ListModel
from utils.page import MyPageNumberPagination


class InOutWarehouseSerializer(ModelSerializer):
    """
    出入库表-序列化器
    """

    class Meta:
        model = ListModel
        fields = "__all__"
        read_only_fields = ["id"]


class InOutWarehouseCreateSerializer(ModelSerializer):
    """
    出入库表-新增-序列化器
    """
    class Meta:
        model = ListModel
        fields = "__all__"
        read_only_fields = ["id"]



class InOutWarehouseViewSet(ModelViewSet):
    """
    出入库表-接口
    """
    queryset = ListModel.objects.all()
    serializer_class = InOutWarehouseSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter, ]
    ordering_fields = ['id', "create_time", "update_time", ]

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    # def create(self,request):
    #     print(request.data)
    #     return Response([], status=200)

