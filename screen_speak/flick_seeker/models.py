from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext as _


# CustomUserManagerを表すモデル
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # カスタムユーザーモデルのためのユーザー作成メソッド
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        # スーパーユーザー作成メソッド
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    # プロフィール画像を保存するフィールド
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # UserManager を追加
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email

# 映画情報を表すモデル
class Movie(models.Model):
    # 映画のタイトル
    title = models.CharField(max_length=255)
    # 映画のあらすじ
    plot = models.TextField()
    # 監督の名前
    director = models.CharField(max_length=255)
    # 出演者
    cast = models.CharField(max_length=255)
    # 公開年度
    release_year = models.PositiveIntegerField()
    # 作成日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時（自動で現在の日時が設定され、更新時に更新される）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# レビュー情報を表すモデル
class Review(models.Model):
    # レビューを書いたユーザー
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # レビュー対象の映画
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 評価スコア
    rating = models.PositiveIntegerField()
    # レビューコメント
    comment = models.TextField()
    # 作成日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)
    # 更新日時（自動で現在の日時が設定され、更新時に更新される）
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

# ハッシュタグを表すモデル
class Hashtag(models.Model):
    # ハッシュタグのラベル
    label = models.CharField(max_length=255)
    # 作成日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.label

# レビューとハッシュタグの関連を表すモデル
class ReviewHashtag(models.Model):
    # レビューへの外部キー
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # ハッシュタグへの外部キー
    hashtag = models.ForeignKey(Hashtag, on_delete=models.CASCADE)
    # 作成日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.review.user.username} - {self.hashtag.label}'

# お気に入り映画情報を表すモデル
class FavoriteMovie(models.Model):
    # ユーザーへの外部キー
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 映画への外部キー
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # 登録日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.movie.title}'

# レビューリアクション情報を表すモデル
class ReviewReaction(models.Model):
    # ユーザーへの外部キー
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # レビューへの外部キー
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # リアクションの種類
    rating_type = models.CharField(max_length=255)
    # 登録日時（自動で現在の日時が設定される）
    created_at = models.DateTimeField(auto_now_add=True)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # 同じ映画に対する重複したお気に入りを防ぐ
    