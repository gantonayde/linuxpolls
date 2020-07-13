from django.urls import path
from polls import views

app_name = 'polls'

urlpatterns = [  
    path('', views.PollsIndex, name='index'),
    path('<int:question_id>/', views.PollDetails, name='detail'),
    path('<int:question_id>/vote/', views.ajax_vote, name='vote'),
    # ex: /polls/user_name/
    path('<str:user_name>/', views.greet, name='greet')
]