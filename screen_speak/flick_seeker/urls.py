from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import top, signup, login_view, signup_confirm, signup_complete, dashboard, movie_list, mypage, my_reviews, my_favorites


app_name = 'flick_seeker'

urlpatterns = [
    path('', top, name='top'),  # ルートURLを 'top' ビューにマッピング
    path('top/', top, name='top'),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('signup_confirm/<str:token>/', signup_confirm, name='signup_confirm'),
    path('signup_complete/<str:token>/', signup_complete, name='signup_complete'),
    path('dashboard/', dashboard, name='dashboard'),
    path('movies/', movie_list, name='movie_list'),
    path('mypage/', mypage, name='mypage'),
    path('my_reviews/', my_reviews, name='my_reviews'),
    path('my_favorites/', my_favorites, name='my_favorites'),
    path('logout/', auth_views.LogoutView.as_view(next_page='flick_seeker:top'), name='logout'),
]