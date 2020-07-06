from django.db import models
from django.contrib.auth.models import User


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    summary = models.CharField(max_length=400, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
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

class FAQs(models.Model):
    title = models.CharField(max_length=200, help_text='Enter question title')
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
   
    class Meta :
       ordering = ['-created_on']
       verbose_name = 'FAQ'
       verbose_name_plural = 'FAQs'
       

    def __str__(self):
       return self.title