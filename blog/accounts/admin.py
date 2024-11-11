from django.contrib import admin

# UserAdmin...カスタムユーザーモデルを管理サイトで扱うためのクラス
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
# class CustomUserAdmin(admin.ModelAdmin):
    '''
        管理ページのレコード一覧に表示するカラムを設定するクラス
    '''
    #レコード一覧にidとusernameを表示
    list_display = ("date_joined", 'id', 'username', 'email')

    #表示するカラムにリンクを設定
    list_display_links = ('id', 'username')

 # Django管理サイトにCustomUser、CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)