import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.consumer import SyncConsumer
from channels.db import database_sync_to_async
import channels_redis
from .models import Thread, ChatMessage
from DocPlus.models import User

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        
        other_user = self.scope['url_route']['kwargs']['username']
        me = self.scope['user']
        thread_obj = await self.get_thread(me, other_user)
        self.thread_obj = thread_obj
        chat_room = f"thread_{thread_obj.id}"
        self.chat_room = chat_room
        await self.channel_layer.group_add(
            self.chat_room, self.channel_name
        )
        
        await self.send({
                'type': 'websocket.accept'
            })

    async def websocket_receive(self, event):
        front_text = event.get('text', None)
        if front_text is not None:
            loaded_dict_data = json.loads(front_text)
            msg = loaded_dict_data.get('message')
            user = self.scope['user']
            sec_user = self.scope['url_route']['kwargs']['username']
            username = 'default'
            if user.is_authenticated:
                username = user.username
            await self.send({
            "type": "websocket.send",
            "text":  msg
        })  
        await self.channel_layer.group_send(
            self.chat_room,{
            'type' : 'chat_message',
            'message': msg,
        })
        myResponse = {
                'message'  : msg,
                'username' : username
                }
                
        await self.create_chat_message(user, msg, sec_user)           
               
       
    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text":  event["message"]
            
        })
    
    async def websocket_disconnect(self, event):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    @database_sync_to_async
    def get_thread(self, user, other_username):
        return Thread.objects.get_or_new(user, other_username)

    @database_sync_to_async
    def create_chat_message(self, me, msg, other):
        thread_obj = self.thread_obj
        return ChatMessage.objects.create(thread=thread_obj, user=me, message=msg, recuser=other)
