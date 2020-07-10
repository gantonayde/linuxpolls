from django.contrib import admin
from django.forms.models import BaseInlineFormSet, ModelForm
# Register your models here.
from .models import Question, Choice, Plot, Vote
from django.utils import timezone 


@admin.register(Vote) 
class VoteAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice','voted_on','ip_address')
    list_filter = ("question",)

@admin.register(Plot) 
class PlotAdmin(admin.ModelAdmin):
    list_display = ('question', 'plot_type','created_on','update')
    list_filter = ("plot_type",)

class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial. 
        By always returning true even unchanged inlines will get validated and saved."""
        return True

class Figureinline(admin.StackedInline):
    model = Plot
    extra = 0
    form = AlwaysChangedModelForm
    #exclude = ['graph']

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1
   # verbose_name = 'Name'
   # verbose_name_plural = 'Names'
    
    #fieldsets = [ (None,  {'fields': ['choice_text', 'votes']}) ]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Question',               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Poll on focus', {'fields': ['on_focus']}),
        ('Poll in carousel', {'fields': ['carousel']})
    ]
    inlines = [ChoiceInline, Figureinline]
    list_display = ('question_text', 'pub_date', 'was_published_recently', )
    list_filter = ['pub_date']
    search_fields = ['question_text']
    actions = ['reset_poll_votes','update_figure']

    def reset_poll_votes(self, request, queryset):
        #queryset.update(pub_date=timezone.now())
       for question in queryset:
           question.reset_votes()

    def update_figure(self, request, queryset):
        for question in queryset:
            question.update_figure()

