from django.contrib import admin
from django.forms.models import ModelForm
from polls.models import Question, Choice, Plot, Vote


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice', 'voted_on', 'ip_address',
                    'country_code', 'city')
    list_filter = ("question", )


@admin.register(Plot)
class PlotAdmin(admin.ModelAdmin):
    list_display = ('question', 'plot_type', 'created_on',
                    'allow_updates', 'carousel')
    list_filter = ('question', 'plot_type', 'carousel')

    actions = ['add_to_carousel', 'remove_from_carousel']

    def add_to_carousel(self, request, queryset):
        for plot in queryset:
            if not plot.carousel:
                plot.carousel = True
                plot.save()
    
    def remove_from_carousel(self, request, queryset):
        for plot in queryset:
            if plot.carousel:
                plot.carousel = False
                plot.save()


class AlwaysChangedModelForm(ModelForm):
    def has_changed(self):
        """ Should returns True if data differs from initial.
        By always returning true even unchanged inlines will
        get validated and saved."""
        return True


class Figureinline(admin.StackedInline):
    model = Plot
    extra = 0
    form = AlwaysChangedModelForm
    # exclude = ['graph']


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 1

# verbose_name = 'Name'
# verbose_name_plural = 'Names'

# fieldsets = [ (None,  {'fields': ['choice_text', 'votes']}) ]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [('Question', {
        'fields': ['question_text']
    }), ('Poll on focus', {
        'fields': ['on_focus']
    })]
    inlines = [ChoiceInline, Figureinline]
    list_display = (
        'question_text',
        'created_on',
        'was_published_recently',
    )
    list_filter = ['created_on']
    search_fields = ['question_text']
    actions = ['reset_poll_votes', 'update_figure']

    def reset_poll_votes(self, request, queryset):
        for question in queryset:
            question.reset_votes()

    def update_figure(self, request, queryset):
        for question in queryset:
            question.update_figure()
