from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.cart.models import Cart, Order

from .serializers import CartSerializer, OrderSerializer


@extend_schema(tags=["cart"], description="cart")
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return (
            Cart.objects.filter(user=self.request.user)
            .prefetch_related("items__product")
            .select_related("user")
        )


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related("user")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can access
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
