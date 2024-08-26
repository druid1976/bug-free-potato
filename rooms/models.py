from django.db import models

# Create your models here.

class Rooms(models.Model):
    room_name = models.CharField(max_length=50)
    building_name = models.CharField(max_length=100)
    floor_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.room_name} is at the {self.building_name}, on {self.floor_name}"