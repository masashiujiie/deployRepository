from django.db import models  # Djangoのデータベースモデルを定義するためのモジュールをインポート
from django.contrib.auth.models import AbstractUser, BaseUserManager  # Djangoのユーザーモデル(AbstractUser)とユーザーマネージャ(BaseUserManager)をインポート
from django.utils.translation import gettext as _  # Djangoの翻訳関数をインポートし、gettextとして別名を付ける

# カスタムユーザーマネージャを定義するクラス
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        # ユーザー作成メソッド。email が無い場合はエラーを発生させる
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **extra_fields):
        # スーパーユーザー作成メソッド。is_staff と is_superuser を強制的に True に設定
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)

# ユーザーモデル
class User(AbstractUser):
    username = models.CharField(_('username'), max_length=150, unique=True, null=False)  # ユーザー名フィールド
    email = models.EmailField(_('email address'), unique=True)  # emailアドレスフィールド
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  # プロフィール画像フィールド
    
    USERNAME_FIELD = 'email'  # ユーザー名としてemailを使用
    REQUIRED_FIELDS = ['username']  # 必須フィールドを設定

    objects = CustomUserManager()  # カスタムユーザーマネージャを使用
    
    def __str__(self):
        # ユーザーの文字列表現
        return self.email

# 映画モデル
class Movie(models.Model):
    title = models.CharField(max_length=255)  # タイトルフィールド
    plot = models.TextField()  # あらすじフィールド
    director = models.CharField(max_length=255)  # 監督フィールド
    cast = models.CharField(max_length=255)  # 出演者フィールド
    release_year = models.PositiveIntegerField()  # 公開年フィールド
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時（自動で現在の日時が設定され、更新時に更新される）

    def __str__(self):
        # 映画の文字列表現
        return self.title

# レビューモデル
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー外部キー
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # 映画外部キー
    rating = models.PositiveIntegerField()  # 評価スコアフィールド
    comment = models.TextField()  # コメントフィールド
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）
    updated_at = models.DateTimeField(auto_now=True)  # 更新日時（自動で現在の日時が設定され、更新時に更新される）

    def __str__(self):
        # レビューの文字列表現
        return f'{self.user.username} - {self.movie.title}'

# ハッシュタグモデル
class Hashtag(models.Model):
    label = models.CharField(max_length=255)  # ラベルフィールド
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）

    def __str__(self):
        # ハッシュタグの文字列表現
        return self.label

# レビューとハッシュタグの関連モデル
class ReviewHashtag(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)  # レビュー外部キー
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)  # ハッシュタグ外部キー
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）

    def __str__(self):
        # レビューとハッシュタグの関連の文字列表現
        return f'{self.review.user.username} - {self.hashtag.label}'

# お気に入り映画モデル
class FavoriteMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー外部キー
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # 映画外部キー
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）

    def __str__(self):
        # お気に入り映画の文字列表現
        return f'{self.user.username} - {self.movie.title}'

# レビューリアクションモデル
class ReviewReaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー外部キー
    review = models.ForeignKey(Review, on_delete=models.CASCADE)  # レビュー外部キー
    rating_type = models.CharField(max_length=255)  # リアクションの種類フィールド
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）

# お気に入りモデル
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # ユーザー外部キー
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)  # 映画外部キー
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時（自動で現在の日時が設定される）

    class Meta:
        unique_together = ('user', 'movie')  # 同じ映画に対する重複したお気に入りを防止
