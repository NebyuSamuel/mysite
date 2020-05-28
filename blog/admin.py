from django.contrib import admin
from .models import Post,Comment
# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title','slug','author','publish','status')
    list_filter = ('author','publish','status')
    search_fields = ('title','body')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('-publish',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','body','created','active',)
    list_filter = ('active','created','updated',)
    search_fields = ('name','email','body',)
    ordering = ('-created',)