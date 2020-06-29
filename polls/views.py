from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.views import generic
from .models import Question
from polls.models import Choice
from django.forms.models import model_to_dict
from .plots import add_bokeh_figure
from django.core import serializers
import pygal
from polls.plots import add_figure_scatter, add_plotly_fig


def PollsIndex(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    questions = Question.objects.all()
    print(latest_question_list)
    
    
    graph = pygal.Line()
    graph.title = '% Change Coolness of programming languages over time.'
    graph.x_labels = ['2011','2012','2013','2014','2015','2016']
    
    graph.add('Python',  [15, 31, 89, 200, 356, 900])
    graph.add('Java',    [15, 45, 76, 80,  91,  95])

    bar_chart = pygal.StackedBar()
    bar_chart.add('Fibonacci', [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55])
    bar_chart.add('Padovan', [1, 1, 1, 2, 2, 3, 4, 5, 7, 9, 12])
    bar_chart.render()
    graph_data = bar_chart.render_data_uri()
    
    return render(request,
                  'polls/index.html',
                  {'latest_question_list': latest_question_list,
                  'questions': questions,
                  'graph_data': graph_data},)

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/index.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print("In vote")
    try:
        print("Trying")
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        print("In except")
        # Redisplay the question voting form.
        return render(request, 'polls/index.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        question.update_figure()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def ajax_vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    print('starting ajax_vote')
    try:
        print('Entering try')
        print(request.POST['choice'])
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
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

def greet(request, user_name):
    return HttpResponse("Greetings %s." % user_name)