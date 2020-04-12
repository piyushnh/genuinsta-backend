from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

from apps.restaurants.models import Order

class OrderListConsumer(WebsocketConsumer):
    def connect(self):
        self.name = self.scope['url_route']['kwargs']['restaurant_id']
        self.group_name = 'restaurant_%s' % self.name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.group_name,
    #         {
    #             'type': 'order_placed',
    #             'message': message
    #         }
    #     )

    # Receive message from room group
    def order_placed(self, event):

        # print('sksu')
        order = event['order']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'order': order
        }))

class OrderConsumer(WebsocketConsumer):
    def connect(self):
        self.name = self.scope['url_route']['kwargs']['order_id']
        self.group_name = 'order_%s' % self.name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': message['type'],
                # 'message': message
            }
        )

    # Receive message from room group
    def order_accepted(self, event):

        print('Order Accepted')

        # # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'order': order
        # }))

    def order_ready(self, event):

        print('Order Ready')
        # order = event['order']

        # # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'order': order
        # }))
