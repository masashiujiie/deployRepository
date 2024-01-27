import uuid  # 一意のID生成のためのライブラリ
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView  # Djangoの標準ログインビュー
from django.shortcuts import render  # HTMLテンプレートをレンダリングするための関数
from django.shortcuts import render, redirect  # レンダリングとリダイレクトのための関数
from django.contrib.auth.decorators import login_required  # ログイン要求のデコレータ
from django.shortcuts import get_object_or_404  # オブジェクトを取得、なければ404エラーを返す
from .models import Movie, Review, Favorite  # アプリケーションのモデルをインポート
from .forms import CustomUserCreationForm, PasswordForm  # カスタムユーザー作成フォーム
from django.urls import reverse_lazy  # 遅延評価URLリバース関数
from django.contrib import messages  # メッセージフレームワーク
from django.contrib.auth import get_user_model  # ユーザーモデルを取得する関数
from django.db import IntegrityError  # データベース整合性エラー
from django.http import HttpResponse  # HTTPレスポンスを生成する関数
import pdb
import logging

User = get_user_model()  # 現在アクティブなユーザーモデルを取得


def top(request):
    # トップページのビュー。'top.html' テンプレートをレンダリングして表示
    return render(request, 'top.html')

def signup(request):
    logging.debug("signupビューが呼び出されました。リクエストメソッド: %s", request.method)
    
    # サインアップ（ユーザー登録）ページのビュー
    if request.method == 'POST':
        # フォームからのPOSTリクエストを処理
        form = CustomUserCreationForm(request.POST) 
        logging.debug("POSTデータ: %s", request.POST)
        print("Form Received:", form.is_valid(), form.errors)  # フォームの有効性とエラーを確認
        if form.is_valid():
            logging.debug("フォームは有効です。")
            
            # フォームのデータが有効な場合、一時的なトークンを生成しセッションに保存
            token = uuid.uuid4().hex
            # ユーザー情報（パスワード除外）とトークンをセッションに保存
            request.session['signup_data'] = {
                'username': form.cleaned_data.get('username'),
                'email': form.cleaned_data.get('email'),
                'token': token,
            }
            logging.debug("リダイレクト前のセッションデータ: %s", request.session['signup_data'])
            # signup_confirm ページにリダイレクト
            return redirect('flick_seeker:signup_confirm', token=token)
        else:
            logging.debug("フォームは無効です。エラー: %s", form.errors)

            print("Redirecting to signup_confirm")
    else:
        # GETリクエストの場合、空のフォームを表示
        form = CustomUserCreationForm()

    # signup.html を表示
    return render(request, 'signup.html', {'form': form})

class CustomLoginView(LoginView):
    # カスタムログインビュー。ログインページ用のクラスベースビュー
    template_name = 'login.html'  # 使用するテンプレートを指定
    redirect_authenticated_user = True  # 既に認証されているユーザーはリダイレクト
    success_url = reverse_lazy('flick_seeker:dashboard')  # ログイン成功後のリダイレクト先を指定

login_view = CustomLoginView.as_view()

def signup_confirm(request, token):
    # セッションからサインアップデータを取得
    signup_data = request.session.get('signup_data')
    # セッション内のトークンとURLのトークンが一致するか検証
    if signup_data and signup_data.get('token') == token:
        if request.method == 'POST':
            # パスワード入力フォームからのPOSTリクエストを処理
            password_form = PasswordForm(request.POST)
            if password_form.is_valid():
                # パスワードが有効な場合、セッションに保存してsignup_completeにリダイレクト
                signup_data['password'] = password_form.cleaned_data.get('password')
                request.session['signup_data'] = signup_data
                return redirect('flick_seeker:signup_complete', token=token)
        else:
            # GETリクエストの場合、パスワード入力フォームを表示
            password_form = PasswordForm()
        # トークンが一致する場合、ユーザー情報を確認ページに表示
        context = {
            'username': signup_data.get('username'),
            'email': signup_data.get('email'),
            'token': token,  # トークンもフォームに渡す
            'password_form': PasswordForm(),  # パスワード専用のフォームを追加
        }
        return render(request, 'signup_confirm.html', context)
    else:
        # トークンが一致しない場合、エラーメッセージを表示
        return HttpResponse("無効なアクセスです。", status=403)
    
def signup_complete(request, token):
    # サインアップ完了ページのビュー。セッションのトークンとPOSTされたトークンを照合
    if request.method == 'POST':
        # POSTリクエストからtokenを取得
        signup_data = request.session.get('signup_data', {})
        post_token = request.POST.get('token')
                
        # セッションのトークンとPOSTされたトークンが一致するか確認 
        if signup_data and signup_data.get('token') == post_token:             
            try:
                 # トークンが一致する場合、ユーザーをデータベースに保存
                user = User.objects.create_user(
                    username=signup_data.get('username'),
                    email=signup_data.get('email'),
                    password=signup_data.get('password') # フォームから直接パスワードを取得
                 )
                  # セッションから取得したパスワードでユーザーのパスワードを設定
                user.set_password(signup_data.get('password'))
                user.save()
                
                 # 登録成功後、セッションからサインアップデータを削除
                del request.session['signup_data']
                
                # ユーザー保存後、サインアップ完了ページにリダイレクト
                return redirect('flick_seeker:login')  
            except IntegrityError:
                # ユーザー名が重複しているなどの問題が発生した場合
                return HttpResponse("ユーザー登録に失敗しました。既に存在するユーザー名です。", status=400)
            except Exception as e:
                logging.error("ユーザーの保存中にエラーが発生しました: %s", e)
                # ユーザー保存中のエラーを処理
                return HttpResponse("ユーザーの保存中にエラーが発生しました。エラー内容: {}".format(e), status=500)
        else:
            # トークンが一致しない場合、エラーメッセージを表示
            return HttpResponse("無効なアクセスです。", status=403)
    else:
        # POSTメソッドでない場合、エラーメッセージを表示
        return HttpResponse("許可されていないメソッドです。", status=405)

@login_required(login_url='screen_speak:login')
def dashboard(request):
    # ダッシュボードページのビュー（ログインが必要）
    return render(request, 'dashboard.html')

def movie_list(request):
    # 映画一覧ページのビュー。データベースから映画のリストを取得し表示
    movies = Movie.objects.all()[:3]  # 最初の3件だけを取得
    return render(request, 'movie_list.html', {'movies': movies})

def movie_detail(request, movie_id):
    # 映画詳細ページのビュー。指定されたIDの映画の詳細情報を表示
    movie = get_object_or_404(Movie, pk=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})

def search(request):
    # 検索ページのビュー。ユーザーのクエリに基づいて映画を検索
    query = request.GET.get('query', '')
    # 検索クエリに基づく映画の検索処理はここに記述（省略）
    
@login_required
def mypage(request):
    # マイページのビュー。ログインユーザーの情報を表示
    user = request.user

    # マイページに必要なデータを辞書に格納
    context = {
        'user': user,
        # 他の必要なデータを追加
    }

    return render(request, 'mypage.html', context)

@login_required
def my_reviews(request):
    # ユーザーのレビュー一覧ページのビュー。ログインユーザーのレビューを表示（モデルによって異なる）
    print("Logged in user:", request.user)  # デバッグ出力
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'my_reviews.html', {'reviews': reviews})

@login_required
def my_favorites(request):
    # ユーザーのお気に入り映画一覧ページのビュー。ログインユーザーのお気に入り映画を表示（モデルによって異なる）
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'my_favorites.html', {'favorites': favorites})