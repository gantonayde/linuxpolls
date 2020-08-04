from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from articles.models import Comment, Post

admin.site.site_header = 'LinuxPolls Admin Panel'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'enable_comments')
    list_filter = ("status", )
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [CommentsInline]
    summernote_fields = ('content', )
