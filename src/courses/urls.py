from django.urls import path
from . import views


app_name = 'courses'


urlpatterns = [
    path('',views.list_courses, name='list_courses'),
    path('course/<slug:slug>/',views.course_details, name='course_details'),
    path('<slug:subject_slug>/', views.list_courses, name='course_list_by_subject'),  # For courses by subject

]