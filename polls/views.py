from django.shortcuts import get_object_or_404, render
from django.http import Http404, HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.views import generic
from .models import Question
from polls.models import Choice


def PollsIndex(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    polls = Question.objects.all()
    return render(request,
                  'polls/index.html',
                  {'latest_question_list': latest_question_list,
                  'polls': polls},)

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
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        print('Entering except')
        # return render(request, 'polls/index.html', {
        #     'question': p,
        #     'error_message': "You didn't select a choice.",
        # })
        return HttpResponseServerError("You didn't select a choice.")
    else:
        selected_choice.votes += 1
        selected_choice.save()
        p.update_figure()
        print(p.get_absolute_url())
        return HttpResponseRedirect(p.get_absolute_url())

def greet(request, user_name):
    return HttpResponse("Greetings %s." % user_name)