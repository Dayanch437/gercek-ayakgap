from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from apps.cart.models import Cart, CartItem, Order
from apps.store.models import Product
from apps.utils.enums import CartStatus


class CartItemSerializer(ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.FloatField(source='product.price', read_only=True)
    total = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product','product_name','price', 'quantity','total']

    def  create(self, validated_data):
        user = self.context['request'].user
        cart = Cart.objects.get(user=user,status=CartStatus.PENDING)
        product = validated_data['product']
        quantity = validated_data['quantity']
        try:
            product = Product.objects.get(pk=product)
            if product.stock < quantity:
                raise serializers.ValidationError('Not enough stock')

        except product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist')

        cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
        return cart_item

    def get_total(self, obj):
        price = obj.product.price
        quantity = obj.quantity
        total = price * quantity
        return f"{price} x {quantity} = {total}"


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, required=False)
    total_price = serializers.SerializerMethodField()
    user = serializers.CharField(source='user.username', read_only=True)
    def to_representation(self, instance):
        data = super().to_representation(instance)
        items = data.get('items', [])

        combined = {}
        for item in items:
            product_id = item['product']
            if product_id in combined:
                combined[product_id]['quantity'] += item['quantity']
            else:
                combined[product_id] = item

        data['items'] = list(combined.values())
        return data

    def get_total_price(self, obj):
        return sum(
            (item.product.price if item.product else 0) * item.quantity
            for item in obj.items.all()
        )
    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'items','total_price']
        extra_kwargs = {
            'status': {'read_only': True},
            'user': {'required': False,'read_only':True}
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user, status=CartStatus.PENDING)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart





class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'city', 'address', 'phone','status']
        extra_kwargs = {
            "user":{
            "read_only":True
            },
            "cart":{
                "read_only":True
            }
        }

    def create(self, validated_data):

        request = self.context.get('request')

        user = request.user if request and request.user.is_authenticated else None
        cart = Cart.objects.filter(user=user, status=CartStatus.PENDING).first()
        if not cart:
            raise serializers.ValidationError("No pending cart found for this user.")
        order = Order.objects.create(user=user, cart=cart, **validated_data)
        # Mark the cart as completed
        cart.status = CartStatus.COMPLETED
        cart.save()
        return order
