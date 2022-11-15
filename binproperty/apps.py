from django.apps import AppConfig
from django.db.models.signals import post_migrate

class BinpropertyConfig(AppConfig):
    name = 'binproperty'