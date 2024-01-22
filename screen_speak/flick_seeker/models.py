from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext as _


class User(AbstractUser):
    # プロフィール画像を保存するフィールド
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    # UserManager を追加
    objects = UserManager()
    
    def __str__(self):
        return self.username

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
    