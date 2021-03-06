from channels.generic.websocket import AsyncWebsocketConsumer  # Tutorial Parte 2 WebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    # Tutorial PT1
    # def connect(self):
    #     self.accept()
    #
    # def disconnect(self, code):
    #     pass
    #
    # def receive(self, text_data=None, bytes_data=None):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))
    # def connect(self):
    #     self.room_name = self.scope['url_route']['kwargs']['room_name']
    #     self.room_group_name = 'chat_%s' % self.room_name
    #
    #     # Entrar al room
    #     async_to_sync(self.channel_layer.group_add)(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #
    #     self.accept()
    #
    # def disconnect(self, code):
    #     # Salir de room
    #     async_to_sync(self.channel_layer.group_discard)(
    #         self.room_group_name,
    #         self.channel_name
    #     )
    #
    # # Recibir mensaje del WebSocket
    # def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']
    #
    #     # Enviar mensaje al grupo
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message',
    #             'message': message
    #         }
    #     )
    #
    # # Recibir mensaje del grupo
    # def chat_message(self, event):
    #     message = event['message']
    #
    #     # Enviar mensaje al WebSocket
    #     self.send(text_data=json.dumps({
    #         'message': message
    #     }))

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.user_name = self.scope['url_route']['kwargs']['user_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Entrar en sala
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        # Salir de sala
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Recibir mensaje del WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Enviar mensaje a sala
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user': self.user_name,
                'message': message
            }
        )

    # Recibir mensaje de la sala
    async def chat_message(self, event):
        user = event['user']
        message = event['message']

        # Enviar mensaje a WebSocket
        await self.send(text_data=json.dumps({
            'user': user,
            'message': message
        }))
