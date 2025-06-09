from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.adds.models import Banner, Contact
from apps.store.models import Category, Comment, Image, Product, Rating


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','description','image']


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
        extra_kwargs = {
            'user': {'read_only': True}
        }

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']

        if Rating.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Dine bir gezek baha berip bilyaniz !")
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        return Rating.objects.create(user=user, **validated_data)



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


            'average_rating',
            'stars',
            'comments',
        ]