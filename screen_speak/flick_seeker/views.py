import uuid
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Movie, Review, Favorite
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import HttpResponse

User = get_user_model()

def top(request):
    # トップページのビュー
    return render(request, 'top.html')

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # 一時的なトークンを生成
            token = uuid.uuid4().hex
            # ユーザー情報（パスワード除外）とトークンをセッションに保存
            request.session['signup_data'] = {
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'token': token,
            }
            # signup_confirm ページにリダイレクト
            return redirect('flick_seeker:signup_confirm', token=token)
    else:
        form = CustomUserCreationForm()

    # signup.html を表示
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    # カスタムログインビュー
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('flick_seeker:dashboard')  # ログイン成功後のリダイレクト先

login_view = CustomLoginView.as_view()

def signup_confirm(request, token):
    # セッションからサインアップデータを取得
    signup_data = request.session.get('signup_data')
    # セッション内のトークンとURLのトークンが一致するか検証
    if signup_data and signup_data.get('token') == token:
        # 確認ページにユーザー情報を表示
        context = {
            'username': signup_data.get('username'),
            'email': signup_data.get('email'),
            'token': token,  # トークンもフォームに渡す
        }
        return render(request, 'signup_confirm.html', context)
    else:
        # トークンが一致しない場合はエラーを表示
        return HttpResponse("無効なアクセスです。", status=403)
    
def signup_complete(request, token):
    if request.method == 'POST':
        # POSTリクエストからtokenを取得
        post_token = request.POST.get('token')
        print(f"POST token: {post_token}")
        signup_data = request.session.get('signup_data', None)
        print(f"Session token: {signup_data.get('token') if signup_data else 'No signup_data in session'}")
        
        # セッションデータとPOSTされたトークンが一致するか確認 
        if signup_data and signup_data.get('token') == post_token: 
            try:
                # Userモデルのcreate_userメソッドでユーザーを作成
                user = User.objects.create_user(
                    email=signup_data.get('email'),
                    password=signup_data.POST('password') # フォームから直接パスワードを取得
                )
                user.save()
                # 保存後のログを出力します（デバッグ用）
                print(f"User {user.email} saved successfully")
                
                # サインアップ完了後の処理
                return redirect('flick_seeker:signup_complete')  
            except Exception as e:
                # エラーハンドリングを追加
                print(f"Error saving user: {e}")
                return HttpResponse("ユーザーの保存中にエラーが発生しました。", status=500)
        else:
            return HttpResponse("無効なアクセスです。", status=403)
    else:
        return HttpResponse("許可されていないメソッドです。", status=405)

@login_required(login_url='screen_speak:login')
def dashboard(request):
    # ダッシュボードページのビュー（ログインが必要）
    return render(request, 'dashboard.html')

def movie_list(request):
    # 映画一覧ページのビュー
    movies = Movie.objects.all()[:3]  # 最初の3件だけを取得
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    # 映画詳細ページのビュー
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def search(request):
    # 検索ページのビュー
    query = request.GET.get('query', '')
    # 検索クエリを使って映画の一覧を取得するクエリを作成（例）
    
@login_required
def mypage(request):
    # ログイン中のユーザー情報を取得
    user = request.user

    # マイページに必要なデータを辞書に格納
    context = {
        'user': user,
        # 他の必要なデータを追加
    }

    return render(request, 'mypage.html', context)

@login_required
def my_reviews(request):
    # ログインユーザーのレビューを取得（モデルによって異なる）
    print("Logged in user:", request.user)  # デバッグ出力
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'my_reviews.html', {'reviews': reviews})

@login_required
def my_favorites(request):
    # ログインユーザーのお気に入り映画を取得（モデルによって異なる）
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'my_favorites.html', {'favorites': favorites})