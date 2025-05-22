from apps.store.models import Category
from apps.adds.models import Banner
from apps.store.models import Product, Comments
from .serializers import CategorySerializer, CommentCreateSerializer, BannerSerializer
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action


@extend_schema(
    tags=["Banner"],
    summary="BannerViewSet",
    responses=BannerSerializer,
)
class BannerViewSet(ReadOnlyModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer



class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']



    @action(detail=False, methods=['get'], url_path=r'category/(?P<category_id>\d+)')
    def products_by_category(self, request, category_id=None):
        products = Product.objects.filter(category_id=category_id)
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class LastestProductsViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-created_date')[:6]
    serializer_class = ProductSerializer
    permission_classes = (AllowAny,)
    http_method_names = ['get']


class CommentViewSet(ModelViewSet):
    queryset = Comments.objects.all().order_by("-created_date")
    serializer_class = CommentCreateSerializer
    http_method_names = ['post']

