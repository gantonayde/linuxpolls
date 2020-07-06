from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.views import generic
from .models import Question
from polls.models import Choice
from django.forms.models import model_to_dict, modelformset_factory
from .plots import add_bokeh_figure
from django.core import serializers
from polls.plots import add_figure_scatter, add_plotly_fig
from .forms import VotingForm, QForm
from polls.forms import AnswerFormSet, ChoiceForm, QChoicesForm, QuestionForm, QuestionFormSet
from django import forms
from django.forms import widgets
import json
import urllib
from .tools import get_answered_polls, last_day_of_month

def PollsIndex(request):
    questions = Question.objects.all()
    answered_polls = get_answered_polls(request)
    template = 'polls/index.html'
    context = {'questions': questions,
               'answered_polls': answered_polls}
    return render(request, template, context)


def PollDetails(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    answered_polls = get_answered_polls(request)
    template = 'polls/details.html'
    context = {'question': question,
               'answered_polls': answered_polls}
    return render(request, template, context)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/index.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'


def form_vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    print('starting form_vote')

    if request.method == 'POST':
        print("Checking request")
        voting_form = QuestionForm(data=request.POST)
        print(voting_form)
        if voting_form.is_valid():
            print("Valid voting form found")
            selected_choice = p.choice_set.get(pk=request.POST['choice_text'])
            print("selected_choice:", selected_choice)
            print("selected_choice votes:", selected_choice.votes)

    
        
        # if form.is_valid():
        #     pk = form.cleaned_data['choice_text']
        #     selected_choice = p.choice_set.get(pk=pk)
        #     selected_choice.votes += 1
        #     selected_choice.save()
    try:
        print('Entering try')
        print(request.POST['choice_text'])
        selected_choice = p.choice_set.get(pk=request.POST['choice_text'])
    except (KeyError, Choice.DoesNotExist):
        print('Entering except')
        # return render(request, 'polls/index.html', {
        #     'question': p,
        #     'error_message': "You didn't select a choice.",
        # })
        #return HttpResponse("Choice not selected.")
        return HttpResponseServerError("You didn't select a choice.")
    else:
        print('Entering else...success!')
        selected_choice.votes += 1
        selected_choice.save()
        p.update_figure()
        data = list(p.choice_set.all().values('question_id', 'id', 'votes'))
        graph = add_bokeh_figure(p)
        graph1 = add_figure_scatter(p)
        graph3 = add_plotly_fig(p)
        
        #print(graph)
        #for plot in p.plot_set.all():
        #     print(plot.div)
        #     data = {}
        #     data['div'] = plot.div
        #     data['script'] = plot.script
       # return JsonResponse(data)
        return JsonResponse({'graph': graph, 'data': data, 'plt': graph3})
        #return HttpResponse("Successfully voted.")
        #return HttpResponseRedirect(p.get_absolute_url())

def ajax_vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    id_data = list(question.choice_set.all().values('question_id', 'id'))
    print('starting ajax_vote')

    if request.COOKIES.get('q_voted'):
        value = urllib.parse.unquote_plus(request.COOKIES['q_voted'])
        cookie_value = json.loads(value)
        print(cookie_value)   
        for q_id in cookie_value['question_id']:
            if q_id == question_id:
                return JsonResponse({'id_data': id_data}, status=400)   
    else:
        cookie_value = {'question_id': []}

    try:
        print('Entering try...selecting choice')
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        print('Entering except...choice does not exist')
        return JsonResponse("Choice does not exist.", safe=False, status=400)
    else:
        print('Entering else...success!')
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        question.update_figure()
        plot = question.plot_set.get(question_id=question_id)
        plotly_plot = plot.figure
        
        # Set to True to enable cookies
        enable_cookie = False
        if enable_cookie:
            response = JsonResponse({'id_data': id_data, 'plotly_plot': plotly_plot})
            cookie_value['question_id'].append(question_id)
            response.set_cookie("q_voted", value=json.dumps(cookie_value), expires=last_day_of_month())
            return response
        else:
            return JsonResponse({'id_data': id_data, 'plotly_plot': plotly_plot})

def greet(request, user_name):
    return HttpResponse("Greetings %s." % user_name)