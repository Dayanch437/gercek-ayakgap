from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.adds.models import Banner
from apps.store.models import Category, Comment, Image, Product, Rating


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
        model = Comment
        fields = ['id','user','text','user_image']
        extra_kwargs = {
            'id':{
                "read_only": True
            }
        }


class CommentCreateSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['product','text']
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'user', 'product', 'stars', 'comment', 'created_date']
        read_only_fields = ['user']

class ProductSerializer(ModelSerializer):
    comments = CommentsSerializer(many=True,read_only=True)
    pictures = ImageSerializer(read_only=True,many=True)
    rating_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()


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

            'rating_count',
            'average_rating',
            'comments',
        ]

        def get_average_rating(self, obj):
            return obj.average_rating['average']

        def get_rating_count(self, obj):
            return obj.average_rating['count']

