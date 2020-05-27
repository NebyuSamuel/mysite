from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# custom model manager for status published
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset() \
            .filter(status = 'Published')

# custom model manager for status drafted
class DraftedManager(models.Manager):
    def get_queryset(self):
        return super(DraftedManager,self).get_queryset() \
            .filter(status = 'Drafted')


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
