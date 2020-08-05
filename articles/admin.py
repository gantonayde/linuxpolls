from django.contrib import admin
from django.db.models import Count
from django_summernote.admin import SummernoteModelAdmin

from articles.models import Category, Comment, Post

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
    list_display = ('title', 'category', 'slug', 'status', 'created_on',
                    'enable_comments')
    list_filter = ('status', 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    inlines = [CommentsInline]
    summernote_fields = ('content', )


class PostsInline(admin.TabularInline):
    model = Post
    extra = 0
    fields = ('title', 'created_on', 'updated_on', 'status',
              'enable_comments')
    ordering = ('-created_on', )
    readonly_fields = ('title', 'created_on', 'updated_on', 'status',
                       'enable_comments')

    def has_add_permission(self, request, queryset):
        return False


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'updated_on', 'post_count')
    list_filter = ('title', 'created_on', 'updated_on',)
    inlines = [PostsInline]

    def get_queryset(self, request):
        queryset = super(CategoryAdmin, self).get_queryset(request)
        queryset = queryset.annotate(post_count=Count("post"))
        return queryset

    def post_count(self, obj):
        return obj.post_count
