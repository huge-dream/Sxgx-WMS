from django.apps import AppConfig
from django.db.models.signals import post_migrate

class StaffConfig(AppConfig):
    name = 'staff'