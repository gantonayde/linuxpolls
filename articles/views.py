from django.views import generic
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q
from .models import Post
from .forms import CommentForm

from polls.models import Question, Choice
from polls.plots import add_figure
from django.http import HttpResponseRedirect
from django.urls import reverse


latest_question_list = Question.objects.order_by('-pub_date')[:5]


def Index(request):
    polls_on_focus = Question.objects.order_by('-pub_date')[:5]
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    
    return render(request,
                  'index.html',
                  {'page': page,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list,
                   'polls_on_focus': polls_on_focus,
        })


def Articles(request):

    object_list = Post.objects.filter(status=1).order_by('-created_on')
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'articles/index.html',
                  {'page': page,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list},)

def Search(request):

    search_terms = request.GET.get("s")
    if search_terms:
        object_list = Post.objects.filter(Q(title__icontains=search_terms) | 
                                          Q(content__icontains=search_terms)).order_by('-created_on')
        if not object_list:
            print("No matches")
    else:
        print("else")
        object_list = Post.objects.none()
    print(search_terms)
    paginator = Paginator(object_list, 3)  # 3 posts in each page
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
        print(post_list)
    except PageNotAnInteger:
            # If page is not an integer deliver the first page
        post_list = paginator.page(1)
        for i in post_list:
            print(i,post_list)
    except EmptyPage:
        # If page is out of range deliver last page of results
        post_list = paginator.page(paginator.num_pages)
    return render(request,
                  'search.html',
                  {'page': page,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list,
                   'search_terms': search_terms},)

def About(request):
    
    return render(request,
                  'about.html',
                  {'latest_question_list': latest_question_list},)

def post_detail(request, slug):

    template_name = 'articles/details.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form,
                                           'latest_question_list': latest_question_list})




def get_article_queryset(query=None):
    print("Using get_article_queryset")
    queryset = []
    queries = query.split(" ")
    print(queries)
    for q in queries:
        posts = Post.objects.filter(
            Q(title__icontains=q),
            Q(content__icontains=q)
        ).distinct()

        for post in posts:
            queryset.append(post)
    return list(set(queryset))


