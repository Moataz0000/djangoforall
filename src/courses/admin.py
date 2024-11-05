from django.contrib import admin
from .models import Course, File,Video, Subject


@admin.register(Subject)    
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'created'] 
    readonly_fields = ['slug']   


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'created']
    list_filter  = ['created', 'status']
    readonly_fields = ['slug']
    
    
    
@admin.register(File)    
class FileAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']    
    
    
@admin.register(Video)    
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'course']    