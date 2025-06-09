from rest_framework.routers import DefaultRouter

from .viewsets import CartViewSet, OrderViewSet

router = DefaultRouter()

router.register("cart", CartViewSet)
router.register("order", OrderViewSet, basename="order")

urlpatterns = [] + router.urls
