from django.contrib import admin
from .models import Discussion, Topic, Comment

# Register your models here.
admin.site.register(Topic)
admin.site.register(Discussion)
admin.site.register(Comment)