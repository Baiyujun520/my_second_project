from django.shortcuts import render
from django.views.generic import View
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from order.models import OrderGoods

# Create your views here.


class IndexView(View):
    '''首页类视图'''
    def get(self, request):
        """
        首页展示，获取所有的商品信息
        :param request:
        :return:
        """
        # 1.获取首页商品分类信息
        types = GoodsType.objects.all()
        # 获取首页轮播图信息
        goods_banners = IndexGoodsBanner.objects.all().order_by('index')
        # 获取首页促销活动信息
        promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

        for type in types:
            image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
            title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
            type.image_banners = image_banners
            type.title_banners = title_banners
        context = {
            'types': types,
            'goods_banners': goods_banners,
            'promotion_banners': promotion_banners
        }

        return render(request, 'index.html', context)
