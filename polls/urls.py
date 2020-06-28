from django.urls import path

from . import views
app_name = 'polls'
urlpatterns = [  
    path('polls/', views.PollsIndex, name='index'),
    path('polls/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('polls/<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('polls/<int:question_id>/ajaxvote/', views.ajax_vote, name='vote'),
    # ex: /polls/user_name/
    path('<str:user_name>/', views.greet, name='greet')
]