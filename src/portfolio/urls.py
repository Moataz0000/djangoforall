from django.urls import path
from . import views


app_name = 'portfolio'


urlpatterns = [
    path('projects/', views.portfolio, name='projects'),
    path('project-detail/<slug:slug>/', views.project_detail, name='project_detail'),
    path('about-me/', views.about_me, name='about_me')
]