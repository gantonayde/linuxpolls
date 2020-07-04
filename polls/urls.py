from django.urls import path

from . import views
app_name = 'polls'
urlpatterns = [  
    path('', views.PollsIndex, name='index'),
    path('<int:question_id>/', views.PollDetails, name='detail'),
    path('<int:question_id>/results/', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.ajax_vote, name='vote'),
    path('<int:question_id>/formvote/', views.form_vote, name='formvote'),
    # ex: /polls/user_name/
    path('<str:user_name>/', views.greet, name='greet')
]