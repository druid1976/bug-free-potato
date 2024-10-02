from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from .forms import FileForm
from .models import *

# Create your views here.


class IndexView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request):
        rooms = Room.objects.all()
        # rooms_json = rooms.
        return render(request, 'chatroom/index.html', {"rooms": rooms})


class RoomsView(LoginRequiredMixin, View):
    login_url = 'accounts:login'

    def get(self, request, room_name):

        messages = Message.objects.filter(room__name=room_name)
        files = File.objects.filter(room__name=room_name)
        nameNurl = [(file.name, file.url) for file in files]
        return render(request, 'chatroom/room.html', {
            "room_name": room_name,
            'messages': messages,
            'nameNurl': nameNurl,
        })


# HTTP ÜZERİNDEN FİLE YÜKLEMEK

class FileTransporter(View):
    form_class = FileForm

    def post(self, request, *args, **kwargs):

        room_name = request.POST['room_name']
        form = FileForm(request.POST, request.FILES)

        if form.is_valid():
            room = Room.objects.get(name=room_name)
            file = form.save(commit=False)
            file.owner = request.user
            file.room = room
            file.save()

            return JsonResponse({
                    'file_url': file.file.url,
                    'user': request.user.username,
            })
        return JsonResponse({'error': 'Invalid Form'})
