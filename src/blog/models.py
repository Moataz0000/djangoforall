from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from django.conf import settings
from taggit.managers import TaggableManager
from django_ckeditor_5.fields import CKEditor5Field
from .utils import arabic_slugify










class Manager(models.Manager):
    def get_active_posts(self):
        return self.filter(active=True)

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, allow_unicode=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts', default='no_picture.jpg', blank=True)
    content = CKEditor5Field('Content', config_name='default')
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=False)

    tags = TaggableManager()
    objects = Manager()

    def __str__(self):
        return f'Post: {self.title} by {self.author}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_post_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})


    
    
    class Meta:
        ordering = ['-created'] 
        indexes = [
            models.Index(fields=['title','slug']),
            models.Index(fields=['content']),
        ]
        
        
        
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments') 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_comments')   
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now) 
    updated = models.DateTimeField(auto_now=True)
    active  = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return f'Comment by {self.user} on {self.post}'    
    
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])
        ]
        
        
        
        
class Subscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    class Meta:
        indexes = [
            models.Index(fields=['email'])
        ]
                