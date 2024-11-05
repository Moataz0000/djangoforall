from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse


class Project(models.Model):
    title = models.CharField(max_length=255)
    slug  = models.SlugField(max_length=255)
    main_image = models.ImageField(upload_to='projects', default='no_picture.jpg', blank=True)
    description = CKEditor5Field('Content', config_name='default') 
    github_url = models.URLField()
    deploy_url = models.URLField(blank=True, null=True)
    created    = models.DateTimeField(default=timezone.now) 
    
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title) 
        return super().save(*args, **kwargs)   
    
    def get_project_url(self):
        return reverse('portfolio:project_detail', args=[self.slug])
    class Meta:
        ordering = ['-created']
    



class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects', default='no_picture.jpg') 
    
    def __str__(self) -> str:
        return self.project.title       