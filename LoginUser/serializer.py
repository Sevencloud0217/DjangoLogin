from rest_framework import serializers
from LoginUser.models import *
class GoodsSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Goods ##遍历的对象
        fields = [
            "id",
            "goods_number",
            "goods_name",
            "goods_price",
            "goods_count",
            "goods_location",
            "goods_safe_data",
            "goods_status",
            "goods_pro_time",
        ]