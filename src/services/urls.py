from django.urls import path
from . import views


app_name = 'services'

urlpatterns = [
    path('order-service/', views.service, name='service'),
    path('success/', views.success, name='success'),  

]