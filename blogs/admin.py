from django.contrib import admin

from blogs.models import Blog, Review, Tag

# Register your models here.

admin.site.register(Blog)
admin.site.register(Review)
admin.site.register(Tag)
