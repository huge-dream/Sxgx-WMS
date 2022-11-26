import sys

from django.http import StreamingHttpResponse, JsonResponse
from django.conf import settings
from wsgiref.util import FileWrapper
from rest_framework.exceptions import APIException
import mimetypes, os

def robots(request):
    path = settings.BASE_DIR + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def favicon(request):
    path = str(settings.BASE_DIR) + '/static/img/logo.png'
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def css(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def js(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def statics(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def fonts(request):
    path = str(settings.BASE_DIR) + '/templates/dist/spa' + request.path_info
    content_type, encoding = mimetypes.guess_type(path)
    resp = StreamingHttpResponse(FileWrapper(open(path, 'rb')), content_type=content_type)
    resp['Cache-Control'] = "max-age=864000000000"
    return resp

def myip(request):
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    print(s.getsockname()[0])
    ip = s.getsockname()[0]
    s.close()
    return JsonResponse({"ip": ip})

import socket
import webbrowser
import pandas as pd

def initfolder():
    upload_folder = os.path.exists(os.path.join(settings.BASE_DIR, 'media/' + "upload_example"))
    if upload_folder is False:
        os.makedirs(os.path.join(settings.BASE_DIR, 'media/' + "/upload_example"))

    customer_cn_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/customer_cn.xlsx")
    customer_en_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/customer_en.xlsx")
    goodslist_cn_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/goodslist_cn.xlsx")
    goodslist_en_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/goodslist_en.xlsx")
    supplier_cn_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/supplier_cn.xlsx")
    supplier_en_path = os.path.join(settings.BASE_DIR, 'media/' + "/upload_example/supplier_en.xlsx")
    customer_cn_file = os.path.exists(customer_cn_path)
    customer_en_file = os.path.exists(customer_en_path)
    goodslist_cn_file = os.path.exists(goodslist_cn_path)
    goodslist_en_file = os.path.exists(goodslist_en_path)
    supplier_cn_file = os.path.exists(supplier_cn_path)
    supplier_en_file = os.path.exists(supplier_en_path)
    if not customer_cn_file:
        customer_cn = pd.DataFrame({"客户名称": [], "客户城市": [], "详细地址": [], "联系电话": [], "负责人": [], "客户等级": []})
        df = customer_cn.set_index("客户名称")
        df.to_excel(customer_cn_path)

    if not customer_en_file:
        customer_en = pd.DataFrame(
            {"Customer Name": [], "Customer City": [], "Customer Address": [], "Customer Contact": [],
             "Customer Manager": [], "Customer Level": []})
        df = customer_en.set_index("Customer Name")
        df.to_excel(customer_en_path)

    if not goodslist_cn_file:
        goodslist_cn = pd.DataFrame(
            {"商品编码": [], "商品描述": [], "商品供应商": [], "商品单位重量": [], "商品单位长度": [], "商品单位宽度": [], "商品单位高度": [], "最小单位体积": [],
             "商品单位": [], "商品类别": [], "商品品牌": [], "商品颜色": [], "商品形状": [], "商品规格": [], "商品产地": [], "商品成本": [],
             "商品价格": []})
        df = goodslist_cn.set_index("商品编码")
        df.to_excel(goodslist_cn_path)

    if not goodslist_en_file:
        goodslist_en = pd.DataFrame(
            {"Goods Code": [], "Goods Description": [], "Goods Supplier": [], "Goods Weight": [], "Goods Width": [],
             "Goods Depth": [], "Goods Height": [], "Unit Volume": [], "Goods Unit": [], "Goods Class": [],
             "Goods Brand": [], "Goods Color": [], "Goods Shape": [], "Goods Specs": [], "Goods Origin": [],
             "Goods Cost": [], "Goods Price": []})
        df = goodslist_en.set_index("Goods Code")
        df.to_excel(goodslist_en_path)

    if not supplier_cn_file:
        supplier_cn = pd.DataFrame({"供应商名称": [], "供应商城市": [], "详细地址": [], "联系电话": [], "负责人": [], "供应商等级": []})
        df = supplier_cn.set_index("供应商名称")
        df.to_excel(supplier_cn_path)

    if not supplier_en_file:
        supplier_en = pd.DataFrame(
            {"Supplier Name": [], "Supplier City": [], "Supplier Address": [], "Supplier Contact": [],
             "Supplier Manager": [], "Supplier Level": []})
        df = supplier_en.set_index("Supplier Name")
        df.to_excel(supplier_en_path)

def initcheck():
    if sys.argv[1] == 'runserver':
        initfolder()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        baseurl = "http://" + ip + ":8000"
        path = os.path.join(settings.BASE_DIR, 'templates/dist/spa/statics/baseurl.txt')
        if os.path.exists(path):
            os.remove(path)
        with open(path, 'w') as f:
            f.write(str(baseurl))
        f.close()
        # webbrowser.open(baseurl)
