from django.urls import path  # DjangoのURLパターンを定義するためのモジュールから、path関数をインポート
from django.contrib.auth import views as auth_views  # Djangoの認証システム関連のビューをインポート
from django.urls import path, include  # URLパス関連の機能をインポート
from .views import top, signup, login_view, signup_confirm, signup_complete, dashboard, movie_list, mypage, my_reviews, my_favorites  # アプリケーションのビュー関数をインポート

app_name = 'flick_seeker'  # アプリケーションの名前空間を設定

urlpatterns = [
    path('', top, name='top'),  # ルートURL ('/') を 'top' ビューにマッピング
    path('top/', top, name='top'),  # '/top/' URL を 'top' ビューにマッピング
    path('signup/', signup, name='signup'),  # '/signup/' URL を 'signup' ビューにマッピング
    path('login/', login_view, name='login'),  # '/login/' URL を 'login_view' ビューにマッピング
    path('signup_confirm/<str:token>/', signup_confirm, name='signup_confirm'),  # '/signup_confirm/' URL を 'signup_confirm' ビューにマッピング、トークンをパラメータとして受け取る
    path('signup_complete/<str:token>/', signup_complete, name='signup_complete'),  # '/signup_complete/' URL を 'signup_complete' ビューにマッピング、トークンをパラメータとして受け取る
    path('dashboard/', dashboard, name='dashboard'),  # '/dashboard/' URL を 'dashboard' ビューにマッピング
    path('movies/', movie_list, name='movie_list'),  # '/movies/' URL を 'movie_list' ビューにマッピング
    path('mypage/', mypage, name='mypage'),  # '/mypage/' URL を 'mypage' ビューにマッピング
    path('my_reviews/', my_reviews, name='my_reviews'),  # '/my_reviews/' URL を 'my_reviews' ビューにマッピング
    path('my_favorites/', my_favorites, name='my_favorites'),  # '/my_favorites/' URL を 'my_favorites' ビューにマッピング
    path('logout/', auth_views.LogoutView.as_view(next_page='flick_seeker:top'), name='logout'),  # '/logout/' URL を Djangoのログアウトビューにマッピング、ログアウト後は 'top' ビューにリダイレクト
]
