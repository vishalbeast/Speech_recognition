from django.contrib import admin
from.models import Chat
# Register your models here.



@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('message', 'created', 'user',)
    search_fields = ['message']