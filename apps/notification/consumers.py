from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
import json

class NotificationConsumer(JsonWebsocketConsumer):
    def connect(self):
        try:
            self.user = self.scope['user']
            # print('user')
            # print(self.user)
            self.group_name = self.user.group_name
            # self.group_name = 'random_group'
            print(self.group_name)
            print('socket connected')

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.group_name,
                self.channel_name
            )

            self.accept()
        except Exception as e:
            print(e)
            self.close()

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
                'type': 'order_placed',
                'message': message
            }
        )

    # Receive message from room group
    def notify(self, event):

        try:
            print('received')
            request_data = json.dumps(event['request_data'])
            # data = {
            #     'type': 'FRIEND_REQUEST',
            #     'data': request_data
            # }
            print(request_data)
            # Send message to WebSocket
            self.send(text_data=request_data)
        except Exception as e:
            print(e)
            self.close()