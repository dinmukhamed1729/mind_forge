from django.contrib import admin
from .models import Task, TestCase, Tag, Difficulty

admin.site.register(Task)
admin.site.register(TestCase)
admin.site.register(Tag)
admin.site.register(Difficulty)
