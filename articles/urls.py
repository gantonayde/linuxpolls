from . import views
from django.urls import path
#
urlpatterns = [
    path('', views.PostList, name='home'), 
    path('about/', views.About , name='about'),
    path('search/', views.Search , name='search'),
    path('articles/', views.Articles, name='articles_list'),   
    path('articles/<slug:slug>/', views.post_detail, name='post_detail'),  
    
]
