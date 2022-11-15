from .models import UpdateVersion as uv
from django.conf import settings
from django.http import JsonResponse
from pyupdater.client import Client
from client_config import ClientConfig
from time import sleep

def print_status_info(info):
    context = {}
    context['total'] = info.get(u'total')
    context['downloaded'] = info.get(u'downloaded')
    context['status'] = info.get(u'status')
    print(context)

def update(request):
    APP_NAME = settings.APP_NAME
    APP_VERSION = settings.APP_VERSION
    client = Client(ClientConfig(), refresh=True, progress_hooks=[print_status_info])
    app_update = client.update_check(APP_NAME, APP_VERSION)
    if app_update is not None:
        app_update.download(background=True)
    else:
        return JsonResponse({
            "count": 0,
            "next": "null",
            "previous": "null",
            "results": 'success'
        })
    while True:
        if app_update.is_downloaded():
            app_update.extract_overwrite()
            break
        else:
            sleep(0.5)
    return JsonResponse({
        "count": 0,
        "next": "null",
        "previous": "null",
        "results": 'success'
    })