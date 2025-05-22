
from django.urls import reverse

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async as sync_to_async
import json
from .models import Order

class OrderConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("order_updates", self.channel_name)

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("order_updates", self.channel_name)

    async def receive(self, text_data):
        # print('Received WebSocket message:', text_data)
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type')

        if message_type == 'change_status':
            order_id = text_data_json['order_id']
            new_status = text_data_json['new_status']
            # print(f'Updating order {order_id} to status: {new_status}')  # Log the update

            # Update the order status in the database
            order_data = await self.update_order_status(order_id, new_status)

            # Notify the group about the updated order
            await self.channel_layer.group_send(
                "order_updates",
                {
                    "type": "order_update",
                    "message": order_data,  # Include the serialized order data
                },
            )



    async def order_update(self, event):
        # print('Broadcasting order update:', event)  # Log the broadcast
        await self.send(text_data=json.dumps(event))

    @sync_to_async
    def update_order_status(self, order_id, new_status):
        order = Order.objects.get(id=order_id)
        # print(f'Current status of order {order_id}: {order.status}')  # Log the current status
        order.status = new_status
        order.save()
        # print(f'Updated status of order {order_id} to: {order.status}')  # Log the updated status
        user = order.user.username
        return {
            "id": order.id,
            "status": order.status,
            "city": order.city,
            "address": order.address,
            "phone": order.phone,
            "user": user,
        }
