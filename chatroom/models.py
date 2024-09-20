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
    file = models.FileField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'


class NotificationRoom(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)