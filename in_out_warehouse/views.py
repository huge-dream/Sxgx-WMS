from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from in_out_warehouse.models import ListModel
from utils.page import MyPageNumberPagination

from stock.models import StockListModel, StockBinModel
from binset.models import ListModel as binsetmodel
from goods.models import ListModel as goodsmodel

from rest_framework.exceptions import APIException
from binset.models import ListModel as BinsetModel

class InOutWarehouseSerializer(ModelSerializer):
    """
    出入库表-序列化器
    """
    goods_desc = serializers.SerializerMethodField()
    type_label = serializers.CharField(read_only=True, source='get_type_display')

    def get_goods_desc(self,instance):
        goods_code = instance.goods_code
        goods_detail = goodsmodel.objects.filter(goods_code=goods_code).first()
        if goods_detail:
            return goods_detail.goods_desc
        return None

    class Meta:
        model = ListModel
        fields = "__all__"
        read_only_fields = ["id"]


class WarehouseSerializer(ModelSerializer):
    """
    根据商品编码查询库位和剩余数量
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
    filter_fields = "__all__"
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
        for stock_data in serializer.data:
            bin_detail = binsetmodel.objects.filter(bin_name=stock_data.get('bin_name')).first()
            goods_detail = goodsmodel.objects.filter(goods_code=stock_data.get('goods_code')).first()
            if stock_data.get('type') == 0:
                goods_qty = StockListModel.objects.filter(goods_code=goods_detail.goods_code).first()
                if goods_qty is not None:
                    goods_qty_add_detail = goods_qty
                    goods_qty_add_detail.goods_qty = goods_qty_add_detail.goods_qty + int(stock_data.get('number'))
                    goods_qty_add_detail.save()
                else:
                    StockListModel.objects.create(openid=self.request.auth.openid,
                                                  goods_code=goods_detail.goods_code,
                                                  goods_desc=goods_detail.goods_desc,
                                                  goods_qty=int(stock_data.get('number'))
                                                  )
                bin_qty = StockBinModel.objects.filter(bin_name=bin_detail.bin_name, goods_code=goods_detail.goods_code)
                if bin_qty.exists():
                    bin_qty_add_detail = bin_qty.first()
                    bin_qty_add_detail.goods_qty = bin_qty_add_detail.goods_qty + int(stock_data.get('number'))
                    bin_qty_add_detail.save()
                else:
                    StockBinModel.objects.create(openid=self.request.auth.openid,
                                                 bin_name=bin_detail.bin_name,
                                                 goods_code=goods_detail.goods_code,
                                                 goods_desc=goods_detail.goods_desc,
                                                 goods_qty=int(stock_data.get('number')),
                                                 )
            else:
                goods_qty = StockListModel.objects.filter(goods_code=goods_detail.goods_code)
                if goods_qty.exists():
                    goods_qty_add_detail = goods_qty.first()
                    goods_qty_add_detail.goods_qty = goods_qty_add_detail.goods_qty - int(stock_data.get('number'))
                    if goods_qty_add_detail.goods_qty < 0:
                        raise APIException({"detail": "出库数量不能大于现有数量"})
                    else:
                        goods_qty_add_detail.save()
                else:
                    raise APIException({"detail": "该货物库存不存在"})
                bin_qty = StockBinModel.objects.filter(bin_name=bin_detail.bin_name, goods_code=goods_detail.goods_code)
                if bin_qty.exists():
                    bin_qty_add_detail = bin_qty.first()
                    bin_qty_add_detail.goods_qty = bin_qty_add_detail.goods_qty - int(stock_data.get('number'))
                    if bin_qty_add_detail.goods_qty < 0:
                        raise APIException({"detail": "出库数量不能大于现有数量"})
                    elif bin_qty_add_detail.goods_qty == 0:
                        bin_qty_add_detail.delete()
                    else:
                        bin_qty_add_detail.save()
                else:
                    raise APIException({"detail": "该货物库存不存在"})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'],detail=False)
    def code_to_detail(self,request):
        params = request.query_params
        goods_code = params.get('goods_code')
        queryset = StockBinModel.objects.filter(goods_code__icontains=goods_code).values('goods_qty','bin_name')
        bin_name_list = [item.get('bin_name') for item in queryset]
        bin_set = BinsetModel.objects.filter(bin_name__in=bin_name_list).values('id','bin_name')
        bin_set_dict = { item.get('bin_name'):item.get('id') for item in bin_set }
        for item in queryset:
            if not item.get('bin_name'):
                continue
            item['bin_id'] = bin_set_dict.get(item.get('bin_name'),'')
        return Response(queryset, status=status.HTTP_200_OK)