from django.contrib import admin
from .models import Post, Category

# Register your models here.
# admin화면에 post를 볼 수 있도록 한다.
admin.site.register(Post)
admin.site.register(Category)