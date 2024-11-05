from django.shortcuts import render, get_object_or_404
from .models import Course, Subject
from django.db.models import Count






def list_courses(request, subject_slug=None):
    courses = Course.objects.filter(status='A')
    subject = None
    
    if subject_slug:
        subject = get_object_or_404(Subject, slug=subject_slug)
        courses = courses.filter(subject=subject)

    # Get all subjects and annotate with course count
    subjects = Subject.objects.annotate(course_count=Count('subjects'))
    courses_count = Course.objects.count()
    
    context = {
        'courses': courses,
        'subject': subject,
        'subjects': subjects,  # Pass the subjects to the context
        'courses_count':courses_count
    }
    
    return render(request, 'courses/course_list.html', context)






def course_details(request, slug):
    course = get_object_or_404(Course, slug=slug)
    context = {
        'course': course
    }
    
    return render(request, 'courses/course_detail.html', context)