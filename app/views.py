import os
from .models import Chat
import speech_recognition as sr
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def home(request):
    chats = Chat.objects.all()
    all_users = User.objects.filter(messages__isnull=False).distinct()
    ctx = {
        'home': 'active',
        'chat': chats,
        'allusers': all_users
    }
    if request.user.is_authenticated:    
        return render(request, 'app/chat.html', ctx)
    else:
        return render(request, 'app/base.html', None)


def upload(request):
    #customHeader = request.META['HTTP_MYCUSTOMHEADER']

    filename = str(Chat.objects.count())
    filename = filename + "name" + ".wav"
    uploadedFile = open(filename, "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    # Speech recognizer
    r = sr.Recognizer()
    speech = sr.AudioFile(filename)
    with speech as source:
        audio = r.record(source)
    msg = r.recognize_google(audio)
    os.remove(filename)
    chat_message = Chat(user=request.user, message=msg)
    if msg != '':
        chat_message.save()
    return redirect('/')


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        print('Our value = ', msg)
        chat_message = Chat(user=request.user, message=msg)
        if msg != '':
            chat_message.save()
        return JsonResponse({'msg': msg, 'user': chat_message.user.username})
    else:
        return HttpResponse('Request should be POST.')


def messages(request):
    chat = Chat.objects.all()
    return render(request, 'app/messages.html', {'chat': chat})