from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .views import index



handler404 = 'src.views.custom_404_view'


urlpatterns = [
    path('', index, name='index'),
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),

    path('djangoforall-admin/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # Apps
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('courses/',include('courses.urls', namespace='courses')),
    path('portfolio/', include('portfolio.urls', namespace='portfolio')),
    path('services/', include('services.urls', namespace='services'))
]




urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)