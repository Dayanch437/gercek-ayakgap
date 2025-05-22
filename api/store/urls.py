from rest_framework import routers
from api.store.viewsets import ProductViewSet, CategoryViewSet, CommentViewSet, BannerViewSet, LastestProductsViewSet



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'comments', CommentViewSet)
router.register('banner',BannerViewSet)
router.register('latest-products', LastestProductsViewSet,basename='latest-products')

urlpatterns = router.urls