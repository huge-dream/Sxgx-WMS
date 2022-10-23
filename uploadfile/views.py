from rest_framework import viewsets, views
import pandas as pd
import numpy as np
from django.utils import timezone
from django.db.models import Q
from utils.datasolve import data_validate
from utils.datasolve import is_number
from utils.datasolve import sumOfList
from utils.datasolve import transportation_calculate
from utils.md5 import Md5
from goods.models import ListModel as goodslist
from goodsunit.models import ListModel as goodsunit
from goodsclass.models import ListModel as goodsclass
from goodsbrand.models import ListModel as goodsbrand
from goodscolor.models import ListModel as goodscolor
from goodsshape.models import ListModel as goodsshape
from goodsspecs.models import ListModel as goodsspecs
from goodsorigin.models import ListModel as goodsorigin
from goods import files as goodsfiles
from goods.models import ListModel as goods
from stock.models import StockListModel as stocklist
from supplier.models import ListModel as supplier
from supplier import files as supplierfiles
from customer.models import ListModel as customer
from customer import files as customerfiles
from payment.models import TransportationFeeListModel as freight
from capital.models import ListModel as capital
from scanner.models import ListModel as scanner
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from staff.models import ListModel as staff
from asn.models import AsnListModel
from asn.models import AsnDetailModel
from asn.serializers import ASNListPostSerializer
from asn.serializers import ASNDetailPostSerializer
from asn import files as asnfiles
from warehouse.models import ListModel as warehouse
from payment.models import TransportationFeeListModel as transportation
from dn.models import DnListModel
from dn.models import DnDetailModel
from dn.serializers import DNListPostSerializer
from dn.serializers import DNDetailPostSerializer
from dn import files as dnfiles
from utils import makepdf
from traceback import format_exc


class GoodlistfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return goodslist.objects.all()
        else:
            return goodslist.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = goodsfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = goodsfiles.en_data_header()
        else:
            data_header = goodsfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                self.get_queryset().delete()
                goodsunit.objects.all().delete()
                goodsclass.objects.all().delete()
                goodsbrand.objects.all().delete()
                goodscolor.objects.all().delete()
                goodsshape.objects.all().delete()
                goodsspecs.objects.all().delete()
                goodsorigin.objects.all().delete()
                scanner.objects.filter(openid=self.request.auth.openid, mode='GOODS').delete()
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('SKU')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if str(data_list[i][3]) == 'nan':
                            data_list[i][3] = 'N/A'
                        if not is_number(str(data_list[i][4])):
                            data_list[i][4] = 0
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        if not is_number(str(data_list[i][6])):
                            data_list[i][6] = 0
                        if not is_number(str(data_list[i][7])):
                            data_list[i][7] = 0
                        if str(data_list[i][8]) == 'nan':
                            data_list[i][8] = 'N/A'
                        if not is_number(str(data_list[i][9])):
                            data_list[i][9] = 0
                        if str(data_list[i][8]) == 'nan':
                            data_list[i][8] = 'N/A'
                        if str(data_list[i][11]) == 'nan':
                            data_list[i][11] = 'N/A'
                        if not is_number(str(data_list[i][12])):
                            data_list[i][12] = 0
                        if not is_number(str(data_list[i][13])):
                            data_list[i][13] = 0
                        bar_code = Md5.md5(str(data_list[i][0]).strip())
                        goodslist.objects.create(goods_code=str(data_list[i][0]).strip(),
                                                 goods_desc=str(data_list[i][1]).strip(),
                                                 goods_supplier=str(data_list[i][2]).strip(),
                                                 goods_weight=data_list[i][4],
                                                 goods_w=data_list[i][5],
                                                 goods_d=data_list[i][6],
                                                 goods_h=data_list[i][7],
                                                 unit_volume=data_list[i][9],
                                                 goods_unit=str(data_list[i][10]).strip(),
                                                 goods_class=str(data_list[i][3]).strip(),
                                                 goods_brand='N/A',
                                                 goods_color='N/A',
                                                 goods_shape=str(data_list[i][8]).strip(),
                                                 goods_specs=str(data_list[i][11]).strip(),
                                                 goods_origin='N/A',
                                                 goods_cost=data_list[i][12],
                                                 goods_price=data_list[i][13],
                                                 bar_code=bar_code,
                                                 creater=str(staff_name)
                                                 )
                        scanner.objects.create(openid=self.request.auth.openid, mode="GOODS",
                                               code=str(data_list[i][0]).strip(),
                                               bar_code=bar_code)
                goods_supplier_list = df.drop_duplicates(subset=[data_header.get('goods_supplier')], keep='first').loc[
                                      :,
                                      data_header.get('goods_supplier')].values
                for i in goods_supplier_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if supplier.objects.filter(supplier_name=str(i).strip()).exists():
                        pass
                    else:
                        supplier.objects.create(supplier_name=str(i).strip(),
                                                supplier_city="Supplier City",
                                                supplier_address="Supplier Address",
                                                supplier_contact="Supplier Contact",
                                                supplier_manager="Supplier Manager",
                                                creater=str(staff_name)
                                                )
                goods_unit_list = df.drop_duplicates(subset=[data_header.get('goods_unit')], keep='first').loc[:,
                                    data_header.get('goods_unit')].values
                for i in goods_unit_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsunit.objects.filter(goods_unit=str(i).strip()).exists():
                        pass
                    else:
                        goodsunit.objects.create(goods_unit=str(i).strip(), creater=str(staff_name))
                goods_class_list = df.drop_duplicates(subset=[data_header.get('goods_class')], keep='first').loc[:,
                                    data_header.get('goods_class')].values
                for i in goods_class_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsclass.objects.filter(goods_class=str(i).strip()).exists():
                        pass
                    else:
                        goodsclass.objects.create(goods_class=str(i).strip(), creater=str(staff_name))
                goods_shape_list = df.drop_duplicates(subset=[data_header.get('goods_shape')], keep='first').loc[:,
                                    data_header.get('goods_shape')].values
                for i in goods_shape_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsshape.objects.filter(goods_shape=str(i).strip()).exists():
                        pass
                    else:
                        goodsshape.objects.create(goods_shape=str(i).strip(), creater=str(staff_name))
                goods_specs_list = df.drop_duplicates(subset=[data_header.get('goods_specs')], keep='first').loc[:,
                                    data_header.get('goods_specs')].values
                for i in goods_specs_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsspecs.objects.filter(goods_specs=str(i).strip()).exists():
                        pass
                    else:
                        goodsspecs.objects.create(goods_specs=str(i).strip(), creater=str(staff_name))
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class SupplierfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return supplier.objects.all()
        else:
            return supplier.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = supplierfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = supplierfiles.en_data_header()
        else:
            data_header = supplierfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                self.get_queryset().delete()
                df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('supplier_name')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if str(data_list[i][4]) == 'nan':
                            data_list[i][4] = 'N/A'
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        supplier.objects.create(supplier_name=str(data_list[i][0]).strip(),
                                                supplier_city=str(data_list[i][1]).strip(),
                                                supplier_address=str(data_list[i][2]).strip(),
                                                supplier_contact=data_list[i][3],
                                                supplier_manager=str(data_list[i][4]).strip(),
                                                supplier_level=data_list[i][5],
                                                creater=str(staff_name)
                                                )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class CustomerfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return customer.objects.all()
        else:
            return customer.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = customerfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = customerfiles.en_data_header()
        else:
            data_header = customerfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                self.get_queryset().delete()
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('customer_name')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if str(data_list[i][4]) == 'nan':
                            data_list[i][4] = 'N/A'
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        customer.objects.create(customer_name=str(data_list[i][0]).strip(),
                                                customer_city=str(data_list[i][1]).strip(),
                                                customer_address=str(data_list[i][2]).strip(),
                                                customer_contact=data_list[i][3],
                                                customer_manager=str(data_list[i][4]).strip(),
                                                customer_level=data_list[i][5],
                                                creater=str(staff_name)
                                                )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class CapitalfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return capital.objects.filter(openid=self.request.auth.openid)
        else:
            return capital.objects.filter().none()

    def post(self, request, *args, **kwargs):
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                self.get_queryset().delete()
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                data_list = df.drop_duplicates(keep='first', inplace=True)
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if not is_number(str(data_list[i][1])):
                            data_list[i][1] = 0
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = 0
                        capital.objects.create(openid=self.request.auth.openid,
                                               capital_name=str(data_list[i][0]).strip(),
                                               capital_qty=data_list[i][1],
                                               capital_cost=data_list[i][2],
                                               creater=str(staff_name)
                                               )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class FreightfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return freight.objects.filter(openid=self.request.auth.openid)
        else:
            return freight.objects.filter().none()

    def post(self, request, *args, **kwargs):
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                self.get_queryset().delete()
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                data_list = df.drop_duplicates(keep='first', inplace=True).values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                        if str(data_list[i][0]) == 'nan':
                            data_list[i][0] = 'N/A'
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = 0
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if not is_number(str(data_list[i][4])):
                            data_list[i][4] = 0
                        if str(data_list[i][5]) == 'nan':
                            data_list[i][5] = 'N/A'
                        freight.objects.create(openid=self.request.auth.openid,
                                               send_city=str(data_list[i][0]).strip(),
                                               receiver_city=str(data_list[i][1]).strip(),
                                               weight_fee=data_list[i][2],
                                               volume_fee=data_list[i][3],
                                               min_payment=data_list[i][4],
                                               transportation_supplier=str(data_list[i][5]).strip(),
                                               creater=str(staff_name)
                                               )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class AsnlistfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pass

class DnlistfileViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pass


class GoodlistfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return goodslist.objects.all()
        else:
            return goodslist.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = goodsfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = goodsfiles.en_data_header()
        else:
            data_header = goodsfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('SKU')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if str(data_list[i][3]) == 'nan':
                            data_list[i][3] = 'N/A'
                        if not is_number(str(data_list[i][4])):
                            data_list[i][4] = 0
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        if not is_number(str(data_list[i][6])):
                            data_list[i][6] = 0
                        if not is_number(str(data_list[i][7])):
                            data_list[i][7] = 0
                        if str(data_list[i][8]) == 'nan':
                            data_list[i][8] = 'N/A'
                        if not is_number(str(data_list[i][9])):
                            data_list[i][9] = 0
                        if str(data_list[i][8]) == 'nan':
                            data_list[i][8] = 'N/A'
                        if str(data_list[i][11]) == 'nan':
                            data_list[i][11] = 'N/A'
                        if not is_number(str(data_list[i][12])):
                            data_list[i][12] = 0
                        if not is_number(str(data_list[i][13])):
                            data_list[i][13] = 0
                        if goodslist.objects.filter(goods_code=str(data_list[i][0]).strip()).exists():
                            pass
                        else:
                            bar_code = Md5.md5(str(data_list[i][0]).strip())
                            goodslist.objects.create(goods_code=str(data_list[i][0]).strip(),
                                                    goods_desc=str(data_list[i][1]).strip(),
                                                    goods_supplier=str(data_list[i][2]).strip(),
                                                    goods_weight=data_list[i][4],
                                                    goods_w=data_list[i][5],
                                                    goods_d=data_list[i][6],
                                                    goods_h=data_list[i][7],
                                                    unit_volume=data_list[i][9],
                                                    goods_unit=str(data_list[i][10]).strip(),
                                                    goods_class=str(data_list[i][3]).strip(),
                                                    goods_brand='N/A',
                                                    goods_color='N/A',
                                                    goods_shape=str(data_list[i][8]).strip(),
                                                    goods_specs=str(data_list[i][11]).strip(),
                                                    goods_origin='N/A',
                                                    goods_cost=data_list[i][12],
                                                    goods_price=data_list[i][13],
                                                    bar_code=bar_code,
                                                    creater=str(staff_name)
                                                    )
                            scanner.objects.create(openid=self.request.auth.openid, mode="GOODS",
                                                   code=str(data_list[i][0]).strip(),
                                                   bar_code=bar_code)
                goods_supplier_list = df.drop_duplicates(subset=[data_header.get('goods_supplier')], keep='first').loc[:,
                                      data_header.get('goods_supplier')].values
                for i in goods_supplier_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if supplier.objects.filter(supplier_name=str(i).strip()).exists():
                        pass
                    else:
                        supplier.objects.create(supplier_name=str(i).strip(),
                                                supplier_city="Supplier City",
                                                supplier_address="Supplier Address",
                                                supplier_contact="Supplier Contact",
                                                supplier_manager="Supplier Manager",
                                                creater=str(staff_name)
                                                )
                goods_unit_list = df.drop_duplicates(subset=[data_header.get('goods_unit')], keep='first').loc[:,
                                    data_header.get('goods_unit')].values
                for i in goods_unit_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsunit.objects.filter(goods_unit=str(i).strip()).exists():
                        pass
                    else:
                        goodsunit.objects.create(goods_unit=str(i).strip(), creater=str(staff_name))
                goods_class_list = df.drop_duplicates(subset=[data_header.get('goods_class')], keep='first').loc[:,
                                    data_header.get('goods_class')].values
                for i in goods_class_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsclass.objects.filter(goods_class=str(i).strip()).exists():
                        pass
                    else:
                        goodsclass.objects.create(goods_class=str(i).strip(), creater=str(staff_name))
                goods_shape_list = df.drop_duplicates(subset=[data_header.get('goods_shape')], keep='first').loc[:,
                                    data_header.get('goods_shape')].values
                for i in goods_shape_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsshape.objects.filter(goods_shape=str(i).strip()).exists():
                        pass
                    else:
                        goodsshape.objects.create(goods_shape=str(i).strip(), creater=str(staff_name))
                goods_specs_list = df.drop_duplicates(subset=[data_header.get('goods_specs')], keep='first').loc[:,
                                    data_header.get('goods_specs')].values
                for i in goods_specs_list:
                    if str(i) == 'nan':
                        i = 'N/A'
                    if goodsspecs.objects.filter(goods_specs=str(i).strip()).exists():
                        pass
                    else:
                        goodsspecs.objects.create(goods_specs=str(i).strip(), creater=str(staff_name))
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class SupplierfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return supplier.objects.all()
        else:
            return supplier.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = supplierfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = supplierfiles.en_data_header()
        else:
            data_header = supplierfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('supplier_name')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if str(data_list[i][4]) == 'nan':
                            data_list[i][4] = 'N/A'
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        if supplier.objects.filter(supplier_name=str(data_list[i][0]).strip(),
                                                   supplier_city=str(data_list[i][1]).strip(),
                                                   supplier_address=str(data_list[i][2]).strip(),
                                                   supplier_contact=data_list[i][3],
                                                   supplier_manager=str(data_list[i][4]).strip(),
                                                   supplier_level=data_list[i][5],
                                                   creater=str(staff_name)
                                                   ).exists():
                            pass
                        else:
                            supplier.objects.create(supplier_name=str(data_list[i][0]).strip(),
                                                    supplier_city=str(data_list[i][1]).strip(),
                                                    supplier_address=str(data_list[i][2]).strip(),
                                                    supplier_contact=data_list[i][3],
                                                    supplier_manager=str(data_list[i][4]).strip(),
                                                    supplier_level=data_list[i][5],
                                                    creater=str(staff_name)
                                                    )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class CustomerfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return customer.objects.all()
        else:
            return customer.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = customerfiles.cn_data_header()
        elif lang == 'en-us':
            data_header = customerfiles.en_data_header()
        else:
            data_header = customerfiles.en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                df.drop_duplicates(keep='first', inplace=True)
                data_list = df.drop_duplicates(subset=[data_header.get('customer_name')], keep='first').values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if str(data_list[i][2]) == 'nan':
                            data_list[i][2] = 'N/A'
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if str(data_list[i][4]) == 'nan':
                            data_list[i][4] = 'N/A'
                        if not is_number(str(data_list[i][5])):
                            data_list[i][5] = 0
                        if customer.objects.filter(customer_name=str(data_list[i][0]).strip(),
                                                   customer_city=str(data_list[i][1]).strip(),
                                                   customer_address=str(data_list[i][2]).strip(),
                                                   customer_contact=data_list[i][3],
                                                   customer_manager=str(data_list[i][4]).strip(),
                                                   customer_level=data_list[i][5],
                                                   ).exists():
                            pass
                        else:
                            customer.objects.create(customer_name=str(data_list[i][0]).strip(),
                                                    customer_city=str(data_list[i][1]).strip(),
                                                    customer_address=str(data_list[i][2]).strip(),
                                                    customer_contact=data_list[i][3],
                                                    customer_manager=str(data_list[i][4]).strip(),
                                                    customer_level=data_list[i][5],
                                                    creater=str(staff_name)
                                                    )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class CapitalfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return capital.objects.filter(openid=self.request.auth.openid)
        else:
            return capital.objects.filter().none()

    def post(self, request, *args, **kwargs):
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                data_list = df.drop_duplicates(keep='first', inplace=True)
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                    if str(data_list[i][0]) == 'nan':
                        continue
                    else:
                        if not is_number(str(data_list[i][1])):
                            data_list[i][1] = 0
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = 0
                        if capital.objects.filter(openid=self.request.auth.openid,
                                                   capital_name=str(data_list[i][0]).strip(),
                                                   capital_qty=data_list[i][1],
                                                   capital_cost=data_list[i][2],
                                                   ).exists():
                            pass
                        else:
                            capital.objects.create(openid=self.request.auth.openid,
                                                   capital_name=str(data_list[i][0]).strip(),
                                                   capital_qty=data_list[i][1],
                                                   capital_cost=data_list[i][2],
                                                   creater=str(staff_name)
                                                   )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class FreightfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return freight.objects.filter(openid=self.request.auth.openid)
        else:
            return freight.objects.filter().none()

    def post(self, request, *args, **kwargs):
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(openid=self.request.auth.openid,
                                              id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            if excel_type in ['xlsx', 'xls', 'csv']:
                if excel_type == 'csv':
                    df = pd.read_csv(files)
                else:
                    df = pd.read_excel(files)
                data_list = df.drop_duplicates(keep='first', inplace=True).values
                for d in range(len(data_list)):
                    data_validate(str(data_list[d]))
                for i in range(len(data_list)):
                        if str(data_list[i][0]) == 'nan':
                            data_list[i][0] = 'N/A'
                        if str(data_list[i][1]) == 'nan':
                            data_list[i][1] = 'N/A'
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = 0
                        if not is_number(str(data_list[i][3])):
                            data_list[i][3] = 0
                        if not is_number(str(data_list[i][4])):
                            data_list[i][4] = 0
                        if str(data_list[i][5]) == 'nan':
                            data_list[i][5] = 'N/A'
                        if freight.objects.filter(openid=self.request.auth.openid,
                                                  send_city=str(data_list[i][0]).strip(),
                                                  receiver_city=str(data_list[i][1]).strip(),
                                                  weight_fee=data_list[i][2],
                                                  volume_fee=data_list[i][3],
                                                  min_payment=data_list[i][4],
                                                  transportation_supplier=str(data_list[i][5]).strip()
                                                  ).exists():
                            pass
                        else:
                            freight.objects.create(openid=self.request.auth.openid,
                                                   send_city=str(data_list[i][0]).strip(),
                                                   receiver_city=str(data_list[i][1]).strip(),
                                                   weight_fee=data_list[i][2],
                                                   volume_fee=data_list[i][3],
                                                   min_payment=data_list[i][4],
                                                   transportation_supplier=str(data_list[i][5]).strip(),
                                                   creater=str(staff_name)
                                                   )
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class AsnlistfileAddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return AsnListModel.objects.all()
        else:
            return AsnListModel.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = asnfiles.list_cn_data_header()
        elif lang == 'en-us':
            data_header = asnfiles.list_en_data_header()
        else:
            data_header = asnfiles.list_en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            from datetime import datetime 
            dt = datetime.now()
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            warehouse_id = warehouse.objects.all().first().pk
            if excel_type in ['xlsx', 'xls', 'csv']:
                try:
                    if excel_type == 'csv':
                        df = pd.read_csv(files)
                    else:
                        df = pd.read_excel(files)
                    df.drop_duplicates(keep='first', inplace=True)
                    # data_list = df.drop_duplicates(subset=[data_header.get('goods_code')], keep='first').values
                    data_list = df.drop_duplicates(subset=['序号 No.'], keep='first').values
                    for d in range(len(data_list)):
                        data_validate(str(data_list[d]))
                    data = self.request.data
                    patch_number_list = []
                    for i in range(len(data_list)):
                        if str(data_list[i][1]) == 'nan':
                            continue
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = 0
                        if not is_number(str(data_list[i][4])):
                            data_list[i][4] = int(warehouse_id)
                        if str(data_list[i][3]) == 'nan':
                            data_list[i][3] = str(dt.strftime('%Y%m%d%H%M%S%f'))
                        warehouse_openid = warehouse.objects.filter(pk=int(data_list[i][4])).first().openid
                        supplier_name = supplier.objects.all().first().supplier_name
                        if AsnListModel.objects.filter(openid=warehouse_openid,
                                                    patch_number=str(data_list[i][3])).exists():
                            data['asn_code'] = str(AsnListModel.objects.filter(openid=warehouse_openid,
                                                                            patch_number=str(data_list[i][3])).first().asn_code)
                        else:
                            qs_set = AsnListModel.objects.filter(is_delete=False)
                            order_day = str(timezone.now().strftime('%Y%m%d'))
                            if len(qs_set) > 0:
                                asn_last_code = qs_set.order_by('-id').first().asn_code
                                if str(asn_last_code[3:11]) == order_day:
                                    order_create_no = str(int(asn_last_code[11:]) + 1)
                                    data['asn_code'] = 'ASN' + order_day + order_create_no
                                else:
                                    data['asn_code'] = 'ASN' + order_day + '1'
                            else:
                                data['asn_code'] = 'ASN' + order_day + '1'
                            data['openid'] = warehouse_openid
                            data['bar_code'] = Md5.md5(data['asn_code'])
                            data['supplier'] = supplier_name
                            data['creater'] = str(staff_name)
                            serializer = ASNListPostSerializer(data=data)
                            serializer.is_valid(raise_exception=True)
                            serializer.save()
                            scanner.objects.create(openid=warehouse_openid, mode="ASN", code=data['asn_code'], 
                                                bar_code=data['bar_code'])
                        n = 'N/A'
                        if goodslist.objects.filter(goods_code=str(data_list[i][1]).strip()).exists():
                            pass
                        else:
                            bar_code = Md5.md5(str(data_list[i][1]).strip())
                            goodslist.objects.create(goods_code=str(data_list[i][1]).strip(),
                                                    goods_desc=n,
                                                    goods_supplier=n,
                                                    goods_weight=0,
                                                    goods_w=0,
                                                    goods_d=0,
                                                    goods_h=0,
                                                    unit_volume=0,
                                                    goods_unit=n,
                                                    goods_class=n,
                                                    goods_brand=n,
                                                    goods_color=n,
                                                    goods_shape=n,
                                                    goods_specs=n,
                                                    goods_origin=n,
                                                    goods_cost=0,
                                                    goods_price=0,
                                                    bar_code=bar_code,
                                                    creater=str(staff_name))
                            scanner.objects.create(openid=warehouse_openid,
                                                code=str(data_list[i][1]).strip(),
                                                bar_code=bar_code)
                        check_data = {
                            'openid': warehouse_openid,
                            'asn_code': data['asn_code'],
                            'supplier': supplier_name,
                            'goods_code': str(data_list[i][1]).strip(),
                            'goods_qty': int(data_list[i][2]),
                            'patch_number': str(data_list[i][3]),
                            'warehouse_id': int(data_list[i][4]),
                            'creater': str(staff_name)
                        }
                        serializer = ASNDetailPostSerializer(data=check_data)
                        serializer.is_valid(raise_exception=True)
                        post_data_list = []
                        weight_list = []
                        volume_list = []
                        cost_list = []
                        goods_detail = goods.objects.filter(goods_code=str(data_list[i][1]).strip(),
                                                            is_delete=False).first()
                        goods_weight = round(goods_detail.goods_weight * int(data_list[i][2]) / 1000, 4)
                        goods_volume = round(goods_detail.unit_volume * int(data_list[i][2]), 4)
                        goods_cost = round(goods_detail.goods_cost * int(data_list[i][2]), 2)
                        if stocklist.objects.filter(openid=warehouse_openid, goods_code=str(data_list[i][1]).strip()).exists():
                            goods_qty_change = stocklist.objects.filter(openid=warehouse_openid,
                                                    goods_code=str(data_list[i][1]).strip()).first()
                            goods_qty_change.goods_qty = goods_qty_change.goods_qty + int(data_list[i][2])
                            goods_qty_change.asn_stock = goods_qty_change.asn_stock + int(data_list[i][2])
                            goods_qty_change.save()
                        else:
                            stocklist.objects.create(openid=warehouse_openid,
                                                    goods_code=str(data_list[i][1]).strip(),
                                                    goods_desc=goods_detail.goods_desc,
                                                    goods_qty=int(data_list[i][2]),
                                                    asn_stock=int(data_list[i][2]))
                        post_data = AsnDetailModel(**check_data,
                                                goods_desc=str(goods_detail.goods_desc),
                                                goods_weight=goods_weight,
                                                goods_volume=goods_volume,
                                                goods_cost=goods_cost)
                        post_data_list.append(post_data)
                        weight_list.append(goods_weight)
                        volume_list.append(goods_volume)
                        cost_list.append(goods_cost)
                        total_weight = sumOfList(weight_list, len(weight_list))
                        total_volume = sumOfList(volume_list, len(volume_list))
                        total_cost = sumOfList(cost_list, len(cost_list))
                        supplier_city = supplier.objects.filter(supplier_name=supplier_name,
                                                                is_delete=False).first().supplier_city
                        warehouse_city = warehouse.objects.filter(openid=warehouse_openid).first().warehouse_city
                        transportation_fee = transportation.objects.filter(
                            Q(openid=warehouse_openid, send_city__icontains=supplier_city, receiver_city__icontains=warehouse_city,
                            is_delete=False) | Q(openid='init_data', send_city__icontains=supplier_city, receiver_city__icontains=warehouse_city,
                                                is_delete=False))
                        transportation_res = {
                            "detail": []
                        }
                        if len(transportation_fee) >= 1:
                            transportation_list = []
                            for k in range(len(transportation_fee)):
                                transportation_cost = transportation_calculate(total_weight,
                                                                            total_volume,
                                                                            transportation_fee[k].weight_fee,
                                                                            transportation_fee[k].volume_fee,
                                                                            transportation_fee[k].min_payment)
                                transportation_detail = {
                                    "transportation_supplier": transportation_fee[k].transportation_supplier,
                                    "transportation_cost": transportation_cost
                                }
                                transportation_list.append(transportation_detail)
                            transportation_res['detail'] = transportation_list
                        AsnDetailModel.objects.bulk_create(post_data_list, batch_size=100)
                        AsnListModel.objects.filter(openid=warehouse_openid, asn_code=data['asn_code']).update(
                            supplier=supplier_name, total_weight=total_weight, total_volume=total_volume,
                            total_cost=total_cost, transportation_fee=transportation_res,
                            patch_number=str(data_list[i][3]), warehouse_id=int(data_list[i][4]))
                        patch_number_list.append(data_list[i][3])
                    patch_number_list = set(patch_number_list)
                    for i in patch_number_list:
                        all_data = AsnDetailModel.objects.filter(patch_number=i)
                        all_goods = {}
                        for detail in all_data:
                            if detail.goods_code in all_goods:
                                all_goods[detail.goods_code] += detail.goods_qty
                            else:
                                all_goods[detail.goods_code] = detail.goods_qty
                        iter_data = []
                        for k,v in all_goods.items():
                            d = all_data.filter(goods_code=k).first()
                            d.goods_qty = v
                            iter_data.append(d)
                        pdf_data = list()
                        for j in range(len(iter_data)):
                            warehouse_addr = warehouse.objects.filter(pk=iter_data[i].warehouse_id).first().warehouse_city.split('-')
                            d = dict()
                            d['id'] = j + 1
                            d['patch_number'] = iter_data[j].patch_number
                            d['brand'] = 'MADE IN CHINA'
                            d['barcode'] = goods.objects.filter(goods_code=iter_data[j].goods_code).first().bar_code
                            d['total'] = iter_data[j].goods_qty
                            d['goods_code'] = iter_data[j].goods_code
                            d['address'] = warehouse_addr[1]
                            d['country'] = warehouse_addr[0]
                            pdf_data.append(d)
                        # makepdf.generate_pdf.delay(pdf_data, i)
                        # makepdf.generate_pdf(pdf_data, i)
                        makepdf.generate_pdf.push(pdf_data, i)
                        makepdf.generate_pdf.consume()
                    return Response({"detail": "success"}, status=200)
                except:
                    raise APIException({"detail": "Upload Failed"})
            else:
                raise APIException({"detail": "Can Not Support This File Type"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})

class DnlistfileaddViewSet(views.APIView):
    """
        create:
            Upload One Excel（post）
    """
    pagination_class = []

    def get_queryset(self):
        if self.request.user:
            return DnListModel.objects.all()
        else:
            return DnListModel.objects.filter().none()

    def get_lang(self):
        if self.request.user:
            lang = self.request.META.get('HTTP_LANGUAGE')
        else:
            lang = 'en-us'
        if lang == 'zh-hans':
            data_header = dnfiles.dnlist_cn_data_header()
        elif lang == 'en-us':
            data_header = dnfiles.dnlist_en_data_header()
        else:
            data_header = dnfiles.dnlist_en_data_header()
        return data_header

    def post(self, request, *args, **kwargs):
        data_header = self.get_lang()
        files = self.request.FILES.get('file')
        if files:
            excel_type = files.name.split('.')[1]
            staff_name = staff.objects.filter(id=self.request.META.get('HTTP_OPERATOR')).first().staff_name
            warehouse_id = warehouse.objects.all().first().pk
            if excel_type in ['xlsx', 'xls', 'csv']:
                try:
                    if excel_type == 'csv':
                        df = pd.read_csv(files)
                    else:
                        df = pd.read_excel(files)
                    df.drop_duplicates(keep='first', inplace=True)
                    data_list = df.drop_duplicates(subset=[data_header.get('SKU')], keep='first').values
                    for d in range(len(data_list)):
                        data_validate(str(data_list[d]))
                    data = self.request.data
                    for i in range(len(data_list)):
                        if str(data_list[i][0]) == 'nan':
                            continue
                        if not is_number(str(data_list[i][1])):
                            data_list[i][1] = 0
                        if not is_number(str(data_list[i][2])):
                            data_list[i][2] = int(warehouse_id)
                        warehouse_openid = warehouse.objects.filter(pk=data_list[i][2]).first().openid
                        customer_name = customer.objects.all().first().customer_name
                        qs_set = DnListModel.objects.filter(openid=warehouse_openid, is_delete=False)
                        order_day = str(timezone.now().strftime('%Y%m%d'))
                        if len(qs_set) > 0:
                            dn_last_code = qs_set.order_by('-id').first().dn_code
                            if dn_last_code[2:10] == order_day:
                                order_create_no = str(int(dn_last_code[10:]) + 1)
                                data['dn_code'] = 'DN' + order_day + order_create_no
                            else:
                                data['dn_code'] = 'DN' + order_day + '1'
                        else:
                            data['dn_code'] = 'DN' + order_day + '1'
                        data['openid'] = warehouse_openid
                        data['bar_code'] = Md5.md5(str(data['dn_code']))
                        data['warehouse_id'] = int(data_list[i][2])
                        data['customer'] = customer_name
                        data['creater'] = str(staff_name)
                        serializer = DNListPostSerializer(data=data)
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                        scanner.objects.create(openid=warehouse_openid, mode="DN", code=data['dn_code'], 
                                            bar_code=data['bar_code'])
                        n = 'N/A'
                        if goodslist.objects.filter(goods_code=str(data_list[i][0]).strip()).exists():
                            pass
                        else:
                            bar_code = Md5.md5(str(data_list[i][0]).strip())
                            goodslist.objects.create(goods_code=str(data_list[i][0]).strip(),
                                                    goods_desc=n,
                                                    goods_supplier=n,
                                                    goods_weight=0,
                                                    goods_w=0,
                                                    goods_d=0,
                                                    goods_h=0,
                                                    unit_volume=0,
                                                    goods_unit=n,
                                                    goods_class=n,
                                                    goods_brand=n,
                                                    goods_color=n,
                                                    goods_shape=n,
                                                    goods_specs=n,
                                                    goods_origin=n,
                                                    goods_cost=0,
                                                    goods_price=0,
                                                    bar_code=bar_code,
                                                    creater=str(staff_name))
                            scanner.objects.create(openid=warehouse_openid,
                                                code=str(data_list[i][0]).strip(),
                                                bar_code=bar_code)
                        check_data = {
                            'openid': warehouse_openid,
                            'dn_code': str(data['dn_code']),
                            'customer': customer_name,
                            'goods_code': str(data_list[i][0]),
                            'goods_qty': int(data_list[i][1]),
                            'warehouse_id': int(data_list[i][2]),
                            'creater': str(staff_name)
                        }
                        serializer = DNDetailPostSerializer(data=check_data)
                        serializer.is_valid(raise_exception=True)
                        post_data_list = []
                        weight_list = []
                        volume_list = []
                        cost_list = []
                        goods_detail = goods.objects.filter(goods_code=str(data_list[i][0]),
                                                            is_delete=False).first()
                        goods_weight = round(goods_detail.goods_weight * int(data_list[i][1]) / 1000, 4)
                        goods_volume = round(goods_detail.unit_volume * int(data_list[i][1]), 4)
                        goods_cost = round(goods_detail.goods_price * int(data_list[i][1]), 2)
                        if stocklist.objects.filter(openid=warehouse_openid, goods_code=str(data_list[i][0]),
                                                    can_order_stock__gte=0).exists():
                            goods_qty_change = stocklist.objects.filter(openid=warehouse_openid,
                                                                        goods_code=str(data_list[i][0])).first()
                            goods_qty_change.dn_stock = goods_qty_change.dn_stock + int(data_list[i][1])
                            goods_qty_change.save()
                        else:
                            stocklist.objects.create(openid=warehouse_openid,
                                                    goods_code=str(data_list[i][0]),
                                                    goods_desc=goods_detail.goods_desc,
                                                    dn_stock=int(data_list[i][1]))
                        post_data = DnDetailModel(openid=warehouse_openid,
                                                dn_code=str(data['dn_code']),
                                                customer=customer_name,
                                                goods_code=str(data_list[i][0]),
                                                goods_desc=str(goods_detail.goods_desc),
                                                goods_qty=int(data_list[i][1]),
                                                goods_weight=goods_weight,
                                                goods_volume=goods_volume,
                                                goods_cost=goods_cost,
                                                creater=str(staff_name))
                        weight_list.append(goods_weight)
                        volume_list.append(goods_volume)
                        cost_list.append(goods_cost)
                        post_data_list.append(post_data)
                        total_weight = sumOfList(weight_list, len(weight_list))
                        total_volume = sumOfList(volume_list, len(volume_list))
                        total_cost = sumOfList(cost_list, len(cost_list))
                        customer_city = customer.objects.filter(customer_name=customer_name,
                                                                is_delete=False).first().customer_city
                        warehouse_city = warehouse.objects.filter(openid=warehouse_openid).first().warehouse_city
                        transportation_fee = transportation.objects.filter(
                            Q(openid=warehouse_openid, send_city__icontains=warehouse_city, receiver_city__icontains=customer_city,
                            is_delete=False) | Q(openid='init_data', send_city__icontains=warehouse_city, receiver_city__icontains=customer_city,
                                                is_delete=False))
                        transportation_res = {
                            "detail": []
                        }
                        if len(transportation_fee) >= 1:
                            transportation_list = []
                            for k in range(len(transportation_fee)):
                                transportation_cost = transportation_calculate(total_weight,
                                                                            total_volume,
                                                                            transportation_fee[k].weight_fee,
                                                                            transportation_fee[k].volume_fee,
                                                                            transportation_fee[k].min_payment)
                                transportation_detail = {
                                    "transportation_supplier": transportation_fee[k].transportation_supplier,
                                    "transportation_cost": transportation_cost
                                }
                                transportation_list.append(transportation_detail)
                            transportation_res['detail'] = transportation_list
                        DnDetailModel.objects.bulk_create(post_data_list, batch_size=100)
                        DnListModel.objects.filter(openid=warehouse_openid, dn_code=str(data['dn_code'])).update(
                            customer=customer_name, total_weight=total_weight, total_volume=total_volume,
                            total_cost=total_cost, transportation_fee=transportation_res)
                    return Response({"detail": "success"}, status=200)
                except:
                    raise APIException({"detail": "Upload Failed"})
        else:
            raise APIException({"detail": "Please Select One File"})
        return Response({"detail": "success"})
