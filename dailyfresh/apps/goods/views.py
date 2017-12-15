from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
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


class DetailView(View):
    """商品详情视图"""
    def get(self, request, sku_id):
        """
        1.根据前端传来的sku_id获取该商品的信息
        2.获取商品的分类信息
        3.获取商品的评论信息
        4.获取新品信息
        5.获取商品的其他规格
        6.组织模板上下文
        7.返回数据
        :param request:
        :return:
        """
        # 获取商品的信息
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return redirect(reverse('goods:index'))
        # 获取商品分类信息
        types = GoodsType.objects.all()
        # 获取商品评论信息
        sku_orders = OrderGoods.objects.filter(sku=sku).exclude(comment='')[:30]
        # 获取新品信息
        new_goods = GoodsSKU.objects.filter(type=sku.type).order_by('-create_time')[:2]

        # 获取商品的其他规格
        same_spu_skus = GoodsSKU.objects.filter(goods=sku.goods).exclude(id=sku_id)
        cart_count = 0

        context = {
            'sku': sku,
            'types': types,
            'sku_orders': sku_orders,
            'new_goods': new_goods,
            'same_spu_skus': same_spu_skus,
            'cart_count': cart_count
        }

        # 返回结果
        return render(request, 'detail.html', context)
