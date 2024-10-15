from django.contrib import admin
from social.models import Post, Comment

# Register your models here.
admin.site.register([Post, Comment])
