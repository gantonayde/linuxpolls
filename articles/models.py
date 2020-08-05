from django.db import models
from django.contrib.auth.models import User
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Category(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

    def __str__(self):
        return self.title


STATUS = ((0, "Draft"), (1, "Publish"))


class Post(models.Model, HitCountMixin):
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=False, null=True)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    updated_on = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='postimages', blank=True)
    summary = models.CharField(max_length=400, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    enable_comments = models.BooleanField(default=True)
    hitcount = GenericRelation(HitCount, object_id_field='object_pk')

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80, default='Anonymous')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        if len(self.body) > 10:
            comment_body = (' ').join(self.body.split()[:3])
        else:
            comment_body = self.body
        return f'Comment {comment_body} by {self.name}'
