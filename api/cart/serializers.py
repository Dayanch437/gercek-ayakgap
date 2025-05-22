from rest_framework import serializers
from apps.cart.models import Cart, CartItem, Order
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from apps.store.models import Product
from apps.utils.enums import CartStatus

class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
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


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, required=False)
    class Meta:
        model = Cart
        fields = ['id', 'user', 'status', 'items']
        extra_kwargs = {
            'status': {'read_only': True},
            'user': {'required': False,
                     'read_only':True}

        }

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        user = self.context['request'].user
        cart, created = Cart.objects.get_or_create(user=user, status=CartStatus.PENDING)
        for item_data in items_data:
            CartItem.objects.create(cart=cart, **item_data)
        return cart




class OrderSerializer(serializers.ModelSerializer):
    cart = serializers.SerializerMethodField()  # Get user's pending cart ID
    user = serializers.SerializerMethodField()  # Get user's username

    class Meta:
        model = Order
        fields = ['id', 'user', 'cart', 'city', 'address', 'phone','status']

    def get_user(self, obj):
        """Returns the username of the order owner."""
        return obj.user.username if obj.user else None

    def get_cart(self, obj):
        """Returns the cart ID if available."""
        return obj.cart.id if obj.cart else None

    def create(self, validated_data):
        """Assigns user and pending cart to the order automatically."""
        request = self.context.get('request')
        user = request.user if request and request.user.is_authenticated else None
        cart = Cart.objects.filter(user=user, status=CartStatus.PENDING).first()

        if not cart:
            raise serializers.ValidationError("No pending cart found for this user.")

        # Create an order and link it to the user's pending cart
        order = Order.objects.create(user=user, cart=cart, **validated_data)

        # Mark the cart as completed
        cart.status = CartStatus.COMPLETED
        cart.save()

        return order

