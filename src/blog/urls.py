from . import views
from django.urls import re_path, path



app_name = 'blog'

urlpatterns = [
    path('posts/', views.post_list, name='posts_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('posts/search/', views.post_search, name='post_search'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    re_path(r'^(?P<slug>[-a-zA-Z0-9 _ءاأإآؤئبتثجحخدذرزسشصضطظعغفقكلمنهويةى٠١٢٣٤٥٦٧٨٩]+)/$', views.post_detail, name='post_detail'),
    re_path(r'post/comment/(?P<post_slug>[-a-zA-Z0-9 _ءاأإآؤئبتثجحخدذرزسشصضطظعغفقكلمنهويةى٠١٢٣٤٥٦٧٨٩]+)/$', views.post_comment, name='post_comment'),
]
