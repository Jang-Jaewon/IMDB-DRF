from django.contrib import admin

from .models import StreamPlatform, Content, Review


admin.site.register(StreamPlatform)
admin.site.register(Content)
admin.site.register(Review)