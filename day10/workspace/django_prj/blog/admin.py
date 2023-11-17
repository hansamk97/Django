from django.contrib import admin
from .models import Post, Category, Tag, Comment

# Register your models here.
# admin화면에 post를 볼 수 있도록 한다.
admin.site.register(Post)
admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    # prepopulated_fields : 장고 제공기능, 
    # 다른 필드의 값을 가지고 와서 자동으로 채울수 있도록 함
    prepopulated_fields = {'slug' : ('name',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}

admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag,TagAdmin)