from categories.admin import CategoryAdmin as BaseCategoryAdmin
from categories.models import Category
from django.contrib import admin
from django.db.models import Count
from django_summernote.admin import SummernoteModelAdmin

from articles.models import Post

admin.site.site_header = 'LinuxPolls Admin Panel'


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'slug', 'status', 'created_on',
                    'enable_comments', 'carousel')
    list_filter = ('status', 'category')
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title', )}
    summernote_fields = ('content', )

    actions = ['add_to_carousel', 'remove_from_carousel',
               'allow_comments', 'disable_comments']

    def add_to_carousel(self, request, queryset):
        for post in queryset:
            if not post.carousel:
                post.carousel = True
                post.save()

    def remove_from_carousel(self, request, queryset):
        for post in queryset:
            if post.carousel:
                post.carousel = False
                post.save()

    def allow_comments(self, request, queryset):
        for post in queryset:
            if not post.enable_comments:
                post.enable_comments = True
                post.save()

    def disable_comments(self, request, queryset):
        for post in queryset:
            if post.enable_comments:
                post.enable_comments = False
                post.save()


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

    def has_delete_permission(self, request, queryset):
        return False


admin.site.unregister(Category)
@admin.register(Category)
class CategoryAdmin(BaseCategoryAdmin):
    list_display = ('name', 'alternate_title', 'active',
                    'post_count')
    inlines = [PostsInline]

    def get_queryset(self, request):
        queryset = super(BaseCategoryAdmin, self).get_queryset(request)
        queryset = queryset.annotate(post_count=Count("post"))
        return queryset

    def post_count(self, obj):
        return obj.post_count

    post_count.admin_order_field = 'post_count'
