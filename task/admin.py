from django.contrib import admin
from .models import Category, Task, Note, Article


admin.site.register(Category)
admin.site.register(Task)
admin.site.register(Note)
admin.site.register(Article)
