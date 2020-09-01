from django.contrib import admin
from .models import CustomUser, create_event

admin.site.register(CustomUser)
admin.site.register(create_event)