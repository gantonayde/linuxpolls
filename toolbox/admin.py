from django.contrib import admin
from toolbox.models import IP2LocationDBUpdate, FAQs

@admin.register(IP2LocationDBUpdate) 
class IP2LocationDBUpdate(admin.ModelAdmin):
    list_display = ('db_code', 'created_on', 'updated_on', 'status')

@admin.register(FAQs)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('title', 'body')
    search_fields = ['title', 'body']