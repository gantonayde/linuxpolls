from .models import Question, Choice
from django import forms
from django_select2 import forms as s2forms
from django.forms import modelformset_factory, widgets
from django.forms.models import inlineformset_factory


class QChoicesForm(forms.ModelForm):
    class Meta:
        model = Choice
        exclude = ('__all__',)
class QuestionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "question_text__icontains",     
    ]

class QuestionForm(forms.ModelForm):
    #choice_text =  forms.ModelChoiceField(queryset=Choice.objects.all(),
                                                         #     empty_label=None,
                                                        #      widget=widgets.Select)
    class Meta:
        model = Choice
        fields = ('id','choice_text',)        
    #question = forms.ModelChoiceField(queryset=Question.objects.all())
class ChoiceForm(forms.ModelForm):
     #question = forms.ModelChoiceField(queryset=Question.objects.filter(id=1))
     
    class Meta:
         model = Choice
         fields = ["question", "choice_text",]
        
    choice_text =  forms.ModelChoiceField(queryset=Choice.objects.none(),
                                                              empty_label=None,
                                                              widget=widgets.Select)
    
    question =  forms.ModelChoiceField(queryset=Question.objects.none())

QuestionFormSet = modelformset_factory(Choice, fields=('__all__'))

AnswerFormSet = inlineformset_factory(Question, Choice, extra=0, can_delete=False,
                                        fields=('choice_text',))

class QForm(forms.Form):
    qs = forms.ModelChoiceField(queryset=Choice.objects.filter(question__pk=1).order_by('id'))


# iterable 
GEEKS_CHOICES =( 
    ("1", "One"), 
    ("2", "Two"), 
    ("3", "Three"), 
    ("4", "Four"), 
    ("5", "Five"), 
)

class VotingForm(forms.Form):
    chosen_answer = forms.ChoiceField(choices=GEEKS_CHOICES, label='Choice', required=False,
                                                     widget=forms.Select(
                                                        attrs={
                                                             'class': 'form-control'
                                                         }
                                                     ))
    # other_book_name = forms.CharField(label='Other', max_length=100, required=False,
    #                                   widget=forms.TextInput(
    #                                     attrs={
    #                                           'class': 'form-control',
    #                                           'placeholder': 'Did we miss something?'
    #                                       }
    #                                   ))

   # def __init__(self, *args, **kwargs):
   #      super().__init__(*args, **kwargs)
    #     unique_books_names = Vote.objects.order_by('book_name').values_list('book_name', flat=True).distinct()
   #      self.fields['chosen_books_options'].choices = [(book_name, book_name) for book_name in unique_books_names]

