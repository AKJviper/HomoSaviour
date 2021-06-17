from django.http.response import HttpResponse
from rest_framework import serializers
from .models import ChatMessage, Thread

from django.http import Http404

class ChatMessageSerializer(serializers.ModelSerializer):
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username = self.context['view'].kwargs.get('username')
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def create(self, validated_data):
        thread = self.get_object()
        user = self.request.user
        message = validated_data("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return HttpResponse('Message Instance Created')


    class Meta:
        model = Thread 
        fields = '__all__'

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'

class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thread
        fields = '__all__'
