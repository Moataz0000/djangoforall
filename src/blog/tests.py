import pytest
from .models import Post







@pytest.mark.django_db 
def test_post_name():
    post = Post.objects.create(title='hello world', content='Some content')
    assert post.title == 'hello world'
