from rest_framework.serializers import ModelSerializer
from apps.store.models import Product,Comments,Image
from rest_framework import serializers
from apps.store.models import Category
from apps.adds.models import Banner


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class BannerSerializer(ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','title','description','image']

class CommentsSerializer(ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    user_image = serializers.ImageField(source='user.avatar', read_only=True)
    class Meta:
        model = Comments
        fields = ['id','user','text','user_image']
        extra_kwargs = {
            'id':{
                "read_only": True
            }
        }


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ['product','text']
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class ProductSerializer(ModelSerializer):
    comments = CommentsSerializer(many=True,read_only=True)
    pictures = ImageSerializer(read_only=True,many=True)
    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'image',
            'pictures',
            'price',
            'description',
            'stock',
            'is_available',
            'category',
            'created_date',
            'modified_date',
            'comments',

        ]