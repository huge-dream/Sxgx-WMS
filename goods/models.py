from django.db import models

class ListModel(models.Model):
    goods_code = models.CharField(max_length=255, verbose_name="Goods Code")
    goods_desc = models.CharField(max_length=255, verbose_name="Goods Description")
    light_guidance = models.BooleanField(default=False, verbose_name="光指引")
    goods_supplier = models.CharField(max_length=255, verbose_name="Goods Supplier", null=True, blank=True)
    goods_weight = models.FloatField(default=0, verbose_name="Goods Weight", null=True, blank=True)
    goods_w = models.FloatField(default=0, verbose_name="Goods Width", null=True, blank=True)
    goods_d = models.FloatField(default=0, verbose_name="Goods Depth", null=True, blank=True)
    goods_h = models.FloatField(default=0, verbose_name="Goods Height", null=True, blank=True)
    unit_volume = models.FloatField(default=0, verbose_name="Unit Volume", null=True, blank=True)
    goods_unit = models.CharField(max_length=255, verbose_name="Goods Unit", null=True, blank=True)
    goods_class = models.CharField(max_length=255, verbose_name="Goods Class", null=True, blank=True)
    goods_brand = models.CharField(max_length=255, verbose_name="Goods Brand", null=True, blank=True)
    goods_color = models.CharField(max_length=255, verbose_name="Goods Color", null=True, blank=True)
    goods_shape = models.CharField(max_length=255, verbose_name="Goods Shape", null=True, blank=True)
    goods_specs = models.CharField(max_length=255, verbose_name="Goods Specs", null=True, blank=True)
    goods_origin = models.CharField(max_length=255, verbose_name="Goods Origin", null=True, blank=True)
    safety_stock = models.BigIntegerField(default=0, verbose_name="Goods Safety Stock", null=True, blank=True)
    goods_cost = models.FloatField(default=0, verbose_name="Goods Cost", null=True, blank=True)
    goods_price = models.FloatField(default=0, verbose_name="Goods Price", null=True, blank=True)
    creater = models.CharField(max_length=255, verbose_name="Who created")
    bar_code = models.CharField(max_length=255, verbose_name="Bar Code")
    openid = models.CharField(max_length=255, verbose_name="Openid")
    is_delete = models.BooleanField(default=False, verbose_name='Delete Label')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'goods'
        verbose_name = 'Goods List'
        verbose_name_plural = "Goods List"
        ordering = ['-id']
