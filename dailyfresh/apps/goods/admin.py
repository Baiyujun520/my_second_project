from django.contrib import admin
from goods.models import GoodsSKU, GoodsImage, IndexGoodsBanner, IndexPromotionBanner, GoodsType
# Register your models here.
admin.site.register(GoodsSKU)
admin.site.register(GoodsImage)
admin.site.register(IndexGoodsBanner)
admin.site.register(IndexPromotionBanner)
admin.site.register(GoodsType)