from django.contrib import admin
from .models import Project, Image



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'created']
    readonly_fields = ['slug']
    
    

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['project']    
    
    
    
  