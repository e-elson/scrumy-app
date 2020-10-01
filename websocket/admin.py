from django.contrib import admin
from .models import ChatMessage, Connection

# Register your models here.

admin.site.register(Connection)
admin.site.register(ChatMessage)
