from django.contrib import admin
from .models import Post, Comment, Subscription



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    readonly_fields = ['slug']
    list_display = ['title', 'slug', 'created', 'author', 'active']
    search_fields = ['title','author']
    list_filter = ['created', 'active']
    # form = PostForm
    
    
    
    
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created', 'post', 'active', 'updated']
    list_filter  = ['created', 'active']
    search_fields = ['user', 'body']     
    
    

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_on']    