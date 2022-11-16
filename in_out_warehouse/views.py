from rest_framework import serializers, status
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
    goods_code = serializers.CharField(read_only=True, source='good.goods_code')
    goods_desc = serializers.CharField(read_only=True, source='good.goods_desc')
    binset_name = serializers.CharField(read_only=True, source='binset.bin_name')
    type_label = serializers.CharField(read_only=True, source='get_type_display')

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
    filter_fields = ['type']
    search_fields = ['good__goods_code', 'good__goods_desc']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        创建
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # 写这里
        if serializer.instance.type == 0:
            # 入库
            pass
        else:
            # 出库
            pass
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
