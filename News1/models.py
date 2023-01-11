from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.user}'

    def update_rating(self):
        post = Post.post_rating.value_from_object('id')
        article = Post.article_rating.value_from_object('id')
        comment = Comment.comment_rating.value_from_object('id')
        self.auth_rating = 3 * post + article + comment
        self.save()
        print(f'Рейтинг = {self.auth_rating}')


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.name_category}'


class Post(models.Model):
    news = "NW"
    article = "AR"
    post_chose = [(news, "Новость"), (article, "Статья")]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_time = models.DateTimeField(auto_now_add=True)
    pc_chose = models.CharField(max_length=2, choices=post_chose, default=article)
    title = models.TextField()
    post_text = models.TextField()
    post_rating = models.FloatField(default=0.0)
    article_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.title}'

    def like_post(self):
        self.post_rating += 1
        self.save()

    def like_article(self):
        self.article_rating += 1
        self.save()

    def dislike_post(self):
        self.post_rating -= 1
        self.save()

    def dislike_article(self):
        self.article_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[:125:]+"..."


class PostCategory(models.Model):
    pc_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    pc_category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pc_post}'


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_dt = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.comment_text}'

    def like_comment(self):
        self.comment_rating += 1
        self.save()

    def dislike_comment(self):
        self.comment_rating -= 1
        self.save()