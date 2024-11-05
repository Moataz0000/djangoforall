from django.shortcuts import render, get_object_or_404
from .models import Project, Image




def portfolio(request):
    # استخدام prefetch_related لجلب الصور المرتبطة بكل مشروع
    projects = Project.objects.prefetch_related('images').all()
    return render(request, 'portfolio/projects.html', context={'projects': projects})



def project_detail(request, slug):
    # استخدام prefetch_related لجلب الصور المرتبطة بالمشروع
    project = get_object_or_404(Project.objects.prefetch_related('images'), slug=slug)
    return render(request, 'portfolio/project_detail.html', context={'project': project})





def about_me(request):
    return render(request, 'portfolio/aboutme.html')