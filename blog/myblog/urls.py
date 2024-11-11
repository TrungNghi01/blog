from django.urls import path

from . import views

app_name = 'myblog'

urlpatterns = [
    # url Index (Home)
    path('', views.IndexView.as_view(), name='index'),

    # url tìm kiếm theo danh mục (category search)
    path("search/<int:category>", views.CategorySearchView.as_view(), name="category-search",),

    # url About Us
    path('about/', views.AboutView.as_view(), name='about'),

    # url Blog Contact (email)
    path('contact/', views.ContactView.as_view(), name='contact'),

    # url Post Detail
    path('post-detail/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

    # url Create Post
    path('create-post/', views.CreatePostView.as_view(), name="create-post"),
    path('create-post-done/', views.CreatePostDoneView.as_view(), name="myblog/create-post-done"),

    # url posted by category
    path('posted-by-category/<int:category>', views.PostedByCategoryView.as_view(), name='posted-by-category'),

    # url posted by category
    path('posted-by-user/<int:user>/', views.PostedByUserView.as_view(), name='posted-by-user'),
    
    # url Delete Post
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete-post'),
    path('delete-post-done/', views.DeletePostDoneView.as_view(), name='myblog/delete-post-done'),

    # url My page
    path('mypage/', views.MypageView.as_view(), name='mypage'),

    # url
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='edit-post'),
]
