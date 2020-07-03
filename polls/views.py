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
from django.forms.formsets import formset_factory


def PollsIndex(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    questions = Question.objects.all()

    return render(request,
                  'polls/index.html',
                  {'latest_question_list': latest_question_list,
                  'questions': questions,
                  },)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/index.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     print("In vote")
#     try:
#         print("Trying")
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         print("In except")
#         # Redisplay the question voting form.
#         return render(request, 'polls/index.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes = F('votes') + 1
#         selected_choice.save()
#         question.update_figure()
#         # Always return an HttpResponseRedirect after successfully dealing
#         # with POST data. This prevents data from being posted twice if a
#         # user hits the Back button.
#         return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

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

    if request.method == 'POST':
        print("INDEX POST")
        
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
    print('starting ajax_vote')
    try:
        print('Entering try')
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        #if voted:
        #    return JsonResponse("You have already voted", status=400)
    except (KeyError, Choice.DoesNotExist):
        print('Entering except')
        # return render(request, 'polls/index.html', {
        #     'question': p,
        #     'error_message': "You didn't select a choice.",
        # })
        return JsonResponse("Choice does not exist.", safe=False, status=400)
    else:
        print('Entering else...success!')
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        question.update_figure()
        plot = question.plot_set.get(question_id=question_id)
        plotly_plot = plot.figure
        id_data = list(question.choice_set.all().values('question_id', 'id'))
       # return JsonResponse(data)
        return JsonResponse({'id_data': id_data, 'plotly_plot': plotly_plot})
        #return HttpResponse("Successfully voted.")
        #return HttpResponseRedirect(p.get_absolute_url())

def greet(request, user_name):
    return HttpResponse("Greetings %s." % user_name)