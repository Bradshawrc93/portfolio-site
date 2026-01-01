from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import DevlogPost
from markdown import Markdown


def devlog_list(request):
    """List of published devlog posts."""
    posts = DevlogPost.objects.filter(
        status='published',
        published_at__isnull=False
    ).order_by('-published_at')
    
    context = {
        'posts': posts,
    }
    return render(request, 'devlog/list.html', context)


def devlog_detail(request, slug):
    """Devlog post detail page with Markdown rendering."""
    post = get_object_or_404(
        DevlogPost,
        slug=slug,
        status='published',
        published_at__isnull=False
    )
    
    # Convert Markdown to HTML
    md = Markdown(extensions=['fenced_code', 'tables', 'codehilite'])
    content_html = md.convert(post.content_md)
    
    # Get related posts (same project if available)
    related_posts = DevlogPost.objects.filter(
        status='published',
        published_at__isnull=False
    ).exclude(id=post.id)
    
    if post.project:
        related_posts = related_posts.filter(project=post.project)
    
    related_posts = related_posts[:3]
    
    context = {
        'post': post,
        'content_html': content_html,
        'related_posts': related_posts,
    }
    return render(request, 'devlog/detail.html', context)

