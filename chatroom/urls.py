# chat/urls.py
from django.urls import path
from .views import *
from chatroom.views import *

app_name = "chatroom"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("<str:room_name>/", RoomsView.as_view(), name="room"),
    path("upload/<str:room_name>/", FileTransporter.as_view(), name="transport_file"),
]
