from django.contrib import admin

# Register your models here.
from .models import Comment, BlogPost

admin.site.register(BlogPost)
admin.site.register(Comment)