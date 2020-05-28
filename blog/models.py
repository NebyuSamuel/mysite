from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

# custom model manager for status published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset() \
            .filter(status = 'published')

# custom model manager for status drafted
class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(DraftedManager,self).get_queryset() \
            .filter(status = 'draft')


# Create your models here.
class Post(models.Model):
    # default manager
    objects = models.Manager() 
    # custom manager for status published
    published = PublishedManager()
    # custom manager for status drafted
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
            self.publish.year,self.publish.month,self.publish.day,self.slug
        ])
    

