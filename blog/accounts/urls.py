from django.urls import path
from .import views

from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    #サインアップページのビューの呼び出し
    #「http(s)://<ホスト名>/signup/」へのアクセスに対して、
    #viewsモジュールのSignUpViewをインスタンス化する
    path('signup/',views.SignUpView.as_view(), name='signup'),
    #サインアップ完了ページのビューの呼び出し
    path('signup_success/',views.SignUpSuccessView.as_view(), name='signup_success'),
    #ログインページの表示
    path('login/',auth_views.LoginView.as_view(template_name='login.html'), name='login'), 
    path('logout/',auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    
]