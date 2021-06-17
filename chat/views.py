from chat.serializers import  ChatSerializer, ThreadSerializer
from django.http import Http404, HttpResponse
from django.views.generic.edit import FormMixin
from django.views.generic import DetailView, ListView
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.generics import  CreateAPIView,  RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from .models import Thread, ChatMessage
from django.db.models import Q


class InboxView(ListView):
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView( FormMixin, DetailView):
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ChatListView(APIView):
    serializer_class = ChatSerializer
    permission_classes = (permissions.AllowAny,)
    def get(self, request, username):
        try:
            qlookup = Q(first = request.user, second__username=username) | Q(second = request.user, first__username=username)
            thread = Thread.objects.get(qlookup)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            data_res = ChatMessage.objects.order_by('timestamp').filter(thread=thread)
            serializer = ChatSerializer(data_res, context={'request': request}, many=True).data

            return Response(serializer)
  
class Chatlistlast30(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = ChatSerializer
    def get(self, request, username):
        try:
            qlookup = Q(first = request.user, second__username=username) | Q(second = request.user, first__username=username)
            thread = Thread.objects.get(qlookup)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            data_res = ChatMessage.objects.order_by('timestamp').filter(thread=thread)[:30]
            serializer = ChatSerializer(data_res, context={'request': request}, many=True).data

            return Response(serializer) 
            


class Chatlistall(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    serializer_class = ChatSerializer
    def get(self, request, username):
        try:
            qlookup = Q(first = request.user, second__username=username) | Q(second = request.user, first__username=username)
            thread = Thread.objects.get(qlookup)
        except Thread.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            data_res = ChatMessage.objects.order_by('timestamp').filter(thread=thread)
            serializer = ChatSerializer(data_res, context={'request': request}, many=True).data

            return Response(serializer)

class ThreadListView(APIView):
    permission_classes=(permissions.IsAuthenticated,)
    def get(self, request, user):
        if request.method == 'GET':
            qlookup = Q(first = user) | Q(second = user)
            qyeryset = Thread.objects.filter(Q(first = user) | Q(second = user))
            serializer = ThreadSerializer(qyeryset, context={'request': request}, many=True).data
            return Response(serializer)
        
        return Response(status=status.HTTP_404_NOT_FOUND)



class ThreadDetailView(RetrieveUpdateDestroyAPIView):
    queryset= Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (permissions.IsAuthenticated,)

class Chatimgupload(CreateAPIView):
    queryset= ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

class ChatDelete(APIView):
    queryset= ChatMessage.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def delete(self, request, thread, pk):
        # try:
        #     thread = Thread.objects.get(id=thread)
        # except Thread.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            data_res = ChatMessage.objects.get(thread=thread, id=pk)
            data_res.delete()
            return HttpResponse("Message Deleted")
        else:
            return HttpResponse("Message already deleted")

            


class ThreadCreateView(CreateAPIView):
    queryset= Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = (permissions.IsAuthenticated,)


