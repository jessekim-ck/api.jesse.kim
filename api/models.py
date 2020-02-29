from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    parent_category_id = models.ForeignKey(
        "self",
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )

    @property
    def num_posts(self):
        posts = Post.objects.filter(category_id=self)
        return len(posts)

    @property
    def children_categories(self):
        children = Category.objects.filter(parent_category_id=self)
        return children

    @property
    def num_total_posts(self):
        num = self.num_posts

        for child in self.children_categories:
            num = num + child.num_posts
            for grand_child in child.children_categories:
                num = num + grand_child.num_posts
                for grand_grand_child in grand_child.children_categories:
                    num = num + grand_grand_child.num_posts
                    for grand_grand_grand_child in grand_grand_child.children_categories:
                        num = num + grand_grand_grand_child.num_posts

        return num

    def __str__(self):
        return self.title


class Post(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    text = models.TextField()
    category_id = models.ForeignKey(
        Category,
        default=None,
        null=True,
        blank=True,
        on_delete=models.CASCADE
    )
    writer_id = models.ForeignKey(
        User,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )
    is_private = models.BooleanField(default=False)

    @property
    def num_comments(self):
        comments = Comment.objects.filter(post_id=self)
        return len(comments)

    def __str__(self):
        return self.title


class Comment(models.Model):
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    nickname = models.CharField(max_length=200, null=True, blank=True)
    text = models.TextField()
    post_id = models.ForeignKey(
        Post,
        null=False,
        blank=False,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.post_id.title


class DayLog(models.Model):

    class Evaluation(models.IntegerChoices):
        terrible = 1
        bad = 2
        soso = 3
        good = 4
        excellent = 5

    date = models.DateField(default=timezone.datetime.today)
    sleep_from = models.DateTimeField(default=None)
    sleep_to = models.DateTimeField(default=None)
    condition = models.IntegerField(choices=Evaluation.choices, default=None)
    achievement = models.IntegerField(choices=Evaluation.choices, default=None)
    memo = models.TextField(default="")

    @property
    def sleep_minutes(self):
        if self.sleep_from is not None and self.sleep_to is not None:
            minutes = int((sleep_to - sleep_from).total_seconds/60)
            return minutes
        else:
            return None
