from apps.cart.models import Cart
from .serializers import CartSerializer, OrderSerializer
from rest_framework import viewsets
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    tags=['cart'],
    description='cart'
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]  # Only logged-in users can access
    http_method_names = ['get', 'post']
