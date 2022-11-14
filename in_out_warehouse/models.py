from django.db import models
from goods.models import ListModel as GoodModel

class ListModel(models.Model):
    good = models.ForeignKey(GoodModel,db_constraint=False,on_delete=models.CASCADE,verbose_name="商品")
    number = models.IntegerField(default=0,blank=True,verbose_name="数量")
    TYPE_ENUM = (
        (0,'入库'),
        (1,'出库')
    )
    type = models.SmallIntegerField(choices=TYPE_ENUM,default=0,blank=True,verbose_name="类型")
    creater = models.CharField(max_length=255, verbose_name="Who created")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Create Time")
    update_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name="Update Time")

    class Meta:
        db_table = 'in_out_warehouse'
        verbose_name = '出入库表'
        verbose_name_plural = "出入库表"