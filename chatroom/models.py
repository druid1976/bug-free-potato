from django.db import models
from accounts.models import CustomUser
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    room_maker = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'


class NotificationRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)