  
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from DocPlus.filesize import ContentTypeRestrictedFileField



class ThreadManager(models.Manager):
    def by_user(self, user):
        qlookup = Q(first=user) | Q(second=user)
        qlookup2 = Q(first=user) & Q(second=user)
        qs = self.get_queryset().filter(qlookup).exclude(qlookup2).distinct()
        return qs

    def get_or_new(self, user, other_username): # get_or_create
        username = user.username
        if username == other_username:
            return None
        qlookup1 = Q(first__username=username) & Q(second__username=other_username)
        qlookup2 = Q(first__username=other_username) & Q(second__username=username)
        qs = self.get_queryset().filter(qlookup1 | qlookup2).distinct()
        if qs.count() == 1:
            return qs.first()
        elif qs.count() > 1:
            return qs.order_by('timestamp').first()
        else:
            Klass = user.__class__
            user2 = Klass.objects.get(username=other_username)
            if user != user2:
                obj = self.model(
                        first=user, 
                        second=user2
                    )
                obj.save()
                return obj, True
            return None, False


class Thread(models.Model):
    first        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_first')
    first_fullname = models.CharField(max_length=35, blank=True,null=True)
    firstuser = models.CharField(max_length=35, blank=True,null=True)
    second       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_thread_second')
    second_fullname = models.CharField(max_length=35, blank=True,null=True)
    seconduser = models.CharField(max_length=35, blank=True,null=True)
    updated      = models.DateTimeField(auto_now=True)
    timestamp    = models.DateTimeField(auto_now_add=True)
    
    objects      = ThreadManager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.first_fullname = self.first.first_name +" "+ self.first.last_name
            self.second_fullname = self.second.first_name +" "+ self.second.last_name
            self.firstuser = self.first.username
            self.seconduser = self.second.username
        super(Thread, self).save(*args, **kwargs)
    @property
    def room_group_name(self):
        return f'chat_{self.id}'

    def broadcast(self, msg=None):
        if msg is not None:
            # broadcast_msg_to_chat(msg, group_name=self.room_group_name, user='admin')
            return True
        return False

    def __str__(self):
        return "%s %s" % (self.firstuser, self.seconduser)



class ChatMessage(models.Model):
    thread      = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.SET_NULL)
    user        = models.ForeignKey(User, verbose_name='sender', on_delete=models.CASCADE , related_name='sender_name')
    recuser       = models.CharField(max_length=30, null=True, blank=True, verbose_name='receiver')
    image       = models.ImageField(null = True, blank=True, upload_to="images/messages")
    file = ContentTypeRestrictedFileField(
        upload_to='pdf/',
        content_types=['application/pdf', 'application/zip'],
        max_upload_size=5242880,
        null = True, blank=True,
    )
    message     = models.TextField(null=True, blank=True, default="")
    timestamp   = models.DateTimeField(auto_now_add=True)