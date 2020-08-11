from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from toolbox.models import IP2LocationDBUpdate, FAQs


@admin.register(IP2LocationDBUpdate)
class IP2LocationDBUpdate(admin.ModelAdmin):
    list_display = ('db_code', 'created_on', 'updated_on', 'status')


@admin.register(FAQs)
class FAQAdmin(SummernoteModelAdmin):
    list_display = ('title', 'body')
    search_fields = ['title', 'body']
    summernote_fields = ('body', )
