from .viewsets import CartViewSet, OrderViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('cart', CartViewSet)
router.register('order', OrderViewSet,basename='order')



urlpatterns = [

] + router.urls

