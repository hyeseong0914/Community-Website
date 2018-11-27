from django.contrib import admin
from .models import Board, Comment
# Register your models here.

class BoardAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'content')

admin.site.register(Board, BoardAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'content')

admin.site.register(Comment, CommentAdmin)