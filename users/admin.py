from django.contrib import admin
from .models import Interests, Message, Profile
# Register your models here.
admin.site.register(Profile)
admin.site.register(Interests)
admin.site.register(Message)
