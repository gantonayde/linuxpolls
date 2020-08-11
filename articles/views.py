import json
import urllib

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from articles.models import Post
from polls.models import Question, Plot
from toolbox.models import FAQs
from toolbox.tools import get_popular


def Index(request):
    latest_question_list = Question.objects.order_by('-created_on')[:5]
    carousel_articles = Post.objects.filter(status=1, carousel=True).order_by('-created_on')[:4]
    carousel_plots = Plot.objects.filter(carousel=True).order_by('-created_on')[:4]
    popular_articles = get_popular(Post, days=7, obj_number=5)

    polls_on_focus = Question.objects.filter(on_focus=True)
    if request.COOKIES.get('q_voted'):
        cookie_value = urllib.parse.unquote_plus(request.COOKIES['q_voted'])
        cookie_value = json.loads(cookie_value)
        answered_polls = [q_id for q_id in cookie_value['question_id']]
    else:
        answered_polls = []
    polls_on_focus = polls_on_focus.exclude(id__in=answered_polls)

    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 7)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)

    return render(request,
                  'index.html',
                  {'page': page_number,
                   'post_list': post_list,
                   'polls_on_focus': polls_on_focus,
                   'carousel_articles': carousel_articles,
                   'carousel_plots': carousel_plots,
                   'latest_question_list': latest_question_list,
                   'popular_articles': popular_articles,
                   })


def Articles(request):
    latest_question_list = Question.objects.order_by('-created_on')[:5]
    popular_articles = get_popular(Post, days=7, obj_number=5)
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 10)
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)
    return render(request,
                  'articles/index.html',
                  {'page': page_number,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list,
                   'popular_articles': popular_articles, })


def Search(request):
    latest_question_list = Question.objects.order_by('-created_on')[:5]
    popular_articles = get_popular(Post, days=7, obj_number=5)
    search_terms = request.GET.get("s")
    if search_terms:
        object_list = Post.objects.filter(Q(title__icontains=search_terms) |
                                          Q(content__icontains=search_terms)
                                          ).order_by('-created_on')
        if not object_list:
            print("No matches")
    else:
        object_list = Post.objects.none()

    paginator = Paginator(object_list, 10)  # 3 posts in each page
    page_number = request.GET.get('page')
    post_list = paginator.get_page(page_number)

    return render(request,
                  'search.html',
                  {'page': page_number,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list,
                   'popular_articles': popular_articles,
                   'search_terms': search_terms},)


def About(request):
    latest_question_list = Question.objects.order_by('-created_on')[:5]
    popular_articles = get_popular(Post, days=7, obj_number=5)
    frequently_asked_questions = FAQs.objects.all()
    return render(request,
                  'about.html',
                  {'latest_question_list': latest_question_list,
                   'popular_articles': popular_articles,
                   'faqs': frequently_asked_questions},)


def post_detail(request, slug):
    latest_question_list = Question.objects.order_by('-created_on')[:5]
    popular_articles = get_popular(Post, days=7, obj_number=5)
    template_name = 'articles/details.html'
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post,
        'latest_question_list': latest_question_list,
        'popular_articles': popular_articles,
    }
    return render(request, template_name, context)
