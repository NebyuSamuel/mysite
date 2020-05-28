from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# custom model manager for status published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset() \
            .filter(status = 'published')

class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(DraftedManager, self).get_queryset() \
            .filter(status = 'draft')

# Post model to handle posts on the blog
class Post(models.Model):
    # default manager
    objects = models.Manager() 
    # custom manager for status published
    published = PublishedManager()
    # custom manager for status draft
    drafted = DraftedManager()
    STATUS_CHOICES = (
        ('draft','Drafted'),
        ('published','Published'),
    )

    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250, unique_for_date = 'publish')
    author = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return reverse("blog:post_detail", args = [
            self.pk,self.publish.year,self.publish.month,self.publish.day,self.slug])
    

# Comment model to handle comments of a post
class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE, related_name = 'comments')
    name = models.CharField(max_length = 80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    active = models.BooleanField(default = True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'




