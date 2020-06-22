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



def PostList(request):

    search_terms = request.GET.get("q")
    print(search_terms)
   # query = ""
   ## if request.GET:
        
       # query = request.GET['q']
       # query = str(query)

    
    #plot_div = add_figure(Question.objects.get(pk=2),1)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
   # object_list = get_article_queryset(query)
    if search_terms:
        object_list = Post.objects.filter(Q(title__icontains=search_terms) | Q(content__icontains=search_terms)).order_by('-created_on')
    else:
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

    main_question = get_object_or_404(Question, pk=1)
    
    return render(request,
                  'index.html',
                  {'page': page,
                   'post_list': post_list,
                   'latest_question_list': latest_question_list,
                   'main_question': main_question,
        })

    # return render(request,
    #               'index.html',
    #               {'page': page,
    #                'post_list': post_list,
    #                'latest_question_list': latest_question_list,
    #                'main_question': main_question},)

def Articles(request):
 
    #plot_div = add_figure(Question.objects.get(pk=2),1)
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    
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

def About(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    return render(request,
                  'about.html',
                  {'latest_question_list': latest_question_list},)

def post_detail(request, slug):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
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


