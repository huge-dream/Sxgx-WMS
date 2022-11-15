from django.db import models

class UpdateVersion(models.Model):
    update_version = models.SmallIntegerField(default=0, verbose_name='update check')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create Time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update Time')
    extra1 = models.CharField(default='', max_length=255, verbose_name="extra1")
    extra2 = models.CharField(default='', max_length=255, verbose_name="extra2")
    extra3 = models.CharField(default='', max_length=255, verbose_name="extra3")
    extra4 = models.CharField(default='', max_length=255, verbose_name="extra4")
    extra5 = models.CharField(default='', max_length=255, verbose_name="extra5")
    extra6 = models.CharField(default='', max_length=255, verbose_name="extra6")
    extra7 = models.CharField(default='', max_length=255, verbose_name="extra7")
    extra8 = models.CharField(default='', max_length=255, verbose_name="extra8")
    extra9 = models.CharField(default='', max_length=255, verbose_name="extra9")
    extra10 = models.CharField(default='', max_length=255, verbose_name="extra10")

    class Meta:
        db_table = 'updateversion'
        verbose_name = 'Update Version'
        verbose_name_plural = "Update Version"
        ordering = ['-id']