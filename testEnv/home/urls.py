from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('post/', views.PostView.as_view(), name='post'),
    path('blog-datil/<int:pk>/', views.DetailContentView.as_view(), name = 'detail_content'),
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
    path('create-post-done/', views.CreatePostDoneView.as_view(), name='myblog/create-post-done'),
]