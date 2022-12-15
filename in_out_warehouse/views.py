import time

import binascii
import serial
from django.db import transaction
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
from staff.models import ListModel as staff

class InOutWarehouseSerializer(ModelSerializer):
    """
    出入库表-序列化器
    """
    goods_desc = serializers.SerializerMethodField()
    type_label = serializers.CharField(read_only=True, source='get_type_display')
    dept_name = serializers.SerializerMethodField()

    def get_dept_name(self,instance):
        staff_name = instance.creater
        staff_detail = staff.objects.filter(staff_name=staff_name).first()
        if staff_detail:
            return staff_detail.dept
        return None

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.order_by('-create_time')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        if isinstance(self.request.data, list):
            return serializer_class(many=True, *args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)

    @transaction.atomic # 添加入库事物
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

    @action(methods=['get'], detail=False, permission_classes=[])
    def get_serial(self, request):
        state = int(request.query_params.get('state',1))
        light_guide_sign = request.query_params.get('light_guide_sign')
        # 2. 如果状态为1，直接调用指定位置
        # 3. 如果状态为2，查询结果
        try:
            with serial.Serial(port="COM3", baudrate=9200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                timeout=2, rtscts=False) as ser:
                ser.write(b'81')
                time.sleep(0.5)
                init_light_guide_sign = 'FF 01 00 07 00 01 09'  # 初始点位
                print("light_guide_sign", light_guide_sign)
                if light_guide_sign.isnumeric():  # 数字时执行
                    ser.write(light_guide_sign.encode())
                    time.sleep(0.5)
                    return Response(data={
                        "state": 0  # 返回0不操作，返回1进行下一个判断
                    }, status=status.HTTP_200_OK)
                if state == 1:
                    ser.write(bytes.fromhex(init_light_guide_sign))
                    time.sleep(0.5)
                    ser.write(bytes.fromhex(light_guide_sign))
                elif state == 2:
                    ser.write(bytes.fromhex(light_guide_sign))
                    time.sleep(3)
                    ser.flushInput()  # 清空缓冲区
                    while True:
                        if ser.in_waiting:
                            data = ser.read_all().decode('gbk')
                            print("data", data)
                            # 接收到后，回归原点
                            ser.write(bytes.fromhex(init_light_guide_sign))
                            time.sleep(1)
                            ser.write(b'80')
                            time.sleep(0.5)
                            # 数据的接收
                            return Response(data={
                                "state": 1  # 返回0不操作，返回1进行下一个判断
                            }, status=status.HTTP_200_OK)
                elif state == 3:
                    # 位置移动
                    ser.write(bytes.fromhex(light_guide_sign))
                    time.sleep(0.5)
                    ser.write(bytes.fromhex('FF 01 00 00 00 00 01'))  # 停止移动
                elif state == 4:
                    ser.write(bytes.fromhex(light_guide_sign))  # 直接执行
                return Response(data={
                    "state": 0  # 返回0不操作，返回1进行下一个判断
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response(data={
                "state": -1  # 返回0不操作，返回1进行下一个判断
            }, status=status.HTTP_200_OK)
