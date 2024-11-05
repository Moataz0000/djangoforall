from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Subscription
from .forms import CommentForm, SubscriptionForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q 
import unicodedata
from django.contrib import messages
from django.core.paginator import Paginator


    
def post_list(request, tag_slug=None):
    queryset = Post.objects.get_active_posts().select_related('author').prefetch_related('tags')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        queryset = queryset.filter(tags__in=[tag])

    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)  

    context = {
        'posts': page_obj.object_list,  
        'page_obj': page_obj, 
        'tag': tag,
    }

    return render(request, 'blog/posts.html', context)





def post_detail(request, slug):
    qs = get_object_or_404(Post.objects.select_related('author').prefetch_related('tags', 'comments'), slug=slug, active=True)
    comments = qs.comments.filter(active=True)
    form = CommentForm()

    post_tags_ids = qs.tags.values_list('id', flat=True)

    similar_posts = Post.objects.filter(active=True, tags__in=post_tags_ids).exclude(id=qs.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', 'created')

    context = {
        'post_detail': qs,
        'comments': comments,
        'form': form,
        'related_posts': similar_posts,
    }

    return render(request, 'blog/post_detail.html', context)



    
@require_POST    
def post_comment(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug, active=True)
    comment = None
    form = CommentForm(data=request.POST)
    
    if form.is_valid():
        comment = form.save(commit=False)  # Don't save yet
        comment.post = post
        comment.user = request.user  # Assign the current user
        comment.save()  # Now save with the user assigned
    
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    
    return render(request, 'blog/comment.html', context)






def normalize_text(text):
    """ Normalize text for better search results """
    return unicodedata.normalize('NFC', text)

def post_search(request):
    query = request.GET.get('query')
    results = []

    if query:
        # Normalize the query to improve search matching
        normalized_query = normalize_text(query)

        search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B') + SearchVector('slug', weight='C')
        search_query = SearchQuery(normalized_query, search_type='plain')

        results = Post.objects.get_active_posts().annotate(
            # Calculate similarity for both title and content
            similarity=TrigramSimilarity('title', normalized_query) + TrigramSimilarity('content', normalized_query),
            rank=SearchRank(search_vector, search_query)
        ).filter(
            Q(similarity__gt=0.1) | Q(rank__gte=0.1)  
        ).order_by('-rank', '-similarity')

    context = {
        'query': query,
        'results': results
    }
    return render(request, 'blog/search.html', context)




def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not Subscription.objects.filter(email=email).exists():
                Subscription.objects.create(email=email)
                
                messages.success(request, 'You\'re subscribed now.' )
                return redirect('blog:posts_list')
            else:
                messages.warning(request, 'You are already subcribed.')
                return redirect('blog:posts_list')

    return render(request, 'blog/posts.html')