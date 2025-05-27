import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async as sync_to_async
from django.core.serializers.json import DjangoJSONEncoder
from .models import Order
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("order_updates", self.channel_name)
        logger.info(f"New WebSocket connection: {self.channel_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_updates", self.channel_name)
        logger.info(f"WebSocket disconnected: {self.channel_name}, code: {close_code}")

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')

            if message_type == 'change_status':
                await self.handle_status_change(data)

        except json.JSONDecodeError:
            logger.error("Invalid JSON received")
            await self.send_error("Invalid message format")
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send_error("Internal server error")

    async def handle_status_change(self, data):
        try:
            order_id = data['order_id']
            new_status = data['new_status']

            # Validate and update order
            current_status = await self.get_order_status(order_id)
            if not await self.validate_status_transition(current_status, new_status):
                await self.send_error(f"Invalid status transition from {current_status} to {new_status}")
                return

            order_data = await self.update_order_status(order_id, new_status)
            await self.broadcast_order_update(order_data, "status_changed")

        except Order.DoesNotExist:
            await self.send_error(f"Order {order_id} not found")
        except Exception as e:
            logger.error(f"Status change failed: {str(e)}")
            await self.send_error("Failed to update order status")

    async def broadcast_order_update(self, order_data, event_type):
        """Broadcast order updates to all clients"""
        await self.channel_layer.group_send(
            "order_updates",
            {
                "type": "order_update",
                "message": {
                    "event_type": event_type,
                    "order": order_data,
                    "timestamp": timezone.now().isoformat()
                }
            }
        )

    async def order_update(self, event):
        """Send order updates to WebSocket client"""
        try:
            await self.send(text_data=json.dumps(event, cls=DjangoJSONEncoder))
        except Exception as e:
            logger.error(f"Failed to send update: {str(e)}")

    async def send_error(self, message):
        """Send error message to client"""
        await self.send(text_data=json.dumps({
            "type": "error",
            "message": message,
            "timestamp": timezone.now().isoformat()
        }))

    @sync_to_async
    def get_order_status(self, order_id):
        return Order.objects.values_list('status', flat=True).get(id=order_id)

    @sync_to_async
    def validate_status_transition(self, current_status, new_status):
        valid_transitions = {
            'Pending': ['Processing', 'Cancelled'],
            'Processing': ['Shipped', 'Cancelled'],
            'Shipped': ['Delivered'],
            'Delivered': [],
            'Cancelled': []
        }
        return new_status in valid_transitions.get(current_status, [])

    @sync_to_async
    def update_order_status(self, order_id, new_status):
        order = Order.objects.select_related('user').get(id=order_id)
        order.status = new_status
        order.save()

        return {
            "id": order.id,
            "status": order.status,
            "customer_name": order.customer_name or "Guest",
            "phone": order.phone,
            "city": order.city,
            "address": order.address,
            "user": order.user.username if order.user else None,
            "created_at": order.created_at.isoformat(),
            "updated_at": timezone.now().isoformat()
        }