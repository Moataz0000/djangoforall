from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.template.loader import render_to_string


class Subject(models.Model):
    title = models.CharField(max_length=250, unique=True, help_text='make sure this field be Unique.')
    slug  = models.SlugField(max_length=250, unique=True) 
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created']
        verbose_name_plural = "Subjects"
        
        
    def __str__(self) -> str:
        return self.title  
    
    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)     
    
    
    
    

class Course(models.Model):
    STATUS = (
        ('U', 'Unavailable'),
        ('A', 'Available'),
    )
    
    title = models.CharField(max_length=500)  
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subjects', null=True)
    slug   = models.SlugField(max_length=500, blank=True, null=True)
    content = models.TextField()  
    image = models.ImageField(upload_to='courses', default='no_picture.jpg')  
    status = models.CharField(choices=STATUS, default='A', max_length=1)  
    course_url = models.URLField(null=True)

    created = models.DateTimeField(default=timezone.now)  

    def __str__(self):
        return self.title  
    
    def save(self, *args ,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)    
    
    def get_course_url(self):
        return reverse('courses:course_details', args=[self.slug])
    
    
    



class ItemBase(models.Model):
    title = models.CharField(max_length=500, db_index=True)
    created = models.DateTimeField(timezone.now, db_index=True), 
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='%(class)s_related')
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return self.title  
    
    def render(self):
        return render_to_string(
            f'courses/content/{self._meta.model_name}.html',  # This will look for templates like file.html or video.html
            {'item': self}
        )


class File(ItemBase):
    file = models.FileField(upload_to='courses')
    
    
class Video(ItemBase):
    file = models.URLField()