from django.utils.safestring import mark_safe
import markdown
from django import template
from ..models import Post


register = template.Library()


@register.filter(name='markdown')
def markdown_format(text):
    extensions = ['extra', 'codehilite', 'fenced_code']
    return mark_safe(markdown.markdown(text, extensions=extensions))


@register.simple_tag
def total_posts():
    count = Post.objects.filter(active=True).count()
    return count



@register.simple_tag
def show_latest_posts(count=5):
    return Post.objects.filter(active=True).order_by('-created')[:count]