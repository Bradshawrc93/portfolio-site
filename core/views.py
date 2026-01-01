from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Project
from devlog.models import DevlogPost
from githubsync.models import RepoSnapshot, RepoActivityPoint, UserContributionDay
from datetime import date, timedelta


def home(request):
    """Homepage with profile, heatmap, summary, activity feed, and projects."""
    featured_projects = Project.objects.filter(featured=True, status='active')[:6]
    
    # Get latest devlog posts
    latest_devlog = DevlogPost.objects.filter(
        status='published',
        published_at__isnull=False
    ).order_by('-published_at')[:10]
    
    # Combine into activity feed (devlog posts as activity items)
    latest_activity = []
    for post in latest_devlog:
        latest_activity.append({
            'type': 'Devlog',
            'title': post.title,
            'url': post.get_absolute_url(),
            'date': post.published_at.strftime('%b %d, %Y') if post.published_at else '',
        })
    
    # Get heatmap data
    username = 'bradshawrc93'
    year = timezone.now().year
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    
    contribution_days = UserContributionDay.objects.filter(
        username=username,
        day__gte=year_start,
        day__lte=year_end
    ).order_by('day')
    
    heatmap_dict = {contrib.day: contrib.count for contrib in contribution_days}
    heatmap_data = []
    contribution_counts = [c.count for c in contribution_days] if contribution_days else [0]
    max_count = max(contribution_counts) if contribution_counts else 1
    
    current_date = year_start
    while current_date <= year_end:
        count = heatmap_dict.get(current_date, 0)
        heatmap_data.append((current_date, count))
        current_date += timedelta(days=1)
    
    context = {
        'featured_projects': featured_projects,
        'latest_activity': latest_activity,
        'heatmap_data': heatmap_data,
        'year': year,
        'max_count': max_count,
        'has_heatmap_data': len(heatmap_data) > 0,
    }
    return render(request, 'core/home.html', context)


def project_list(request):
    """Projects list page with contribution heatmap."""
    projects = Project.objects.filter(status='active').order_by('sort_order', 'title')
    
    # Get contribution heatmap data for current year
    username = 'bradshawrc93'
    year = timezone.now().year
    year_start = date(year, 1, 1)
    year_end = date(year, 12, 31)
    
    contribution_days = UserContributionDay.objects.filter(
        username=username,
        day__gte=year_start,
        day__lte=year_end
    ).order_by('day')
    
    # Build heatmap data structure as a list of (day, count) tuples
    # Include all days in the year for proper grid display
    heatmap_dict = {contrib.day: contrib.count for contrib in contribution_days}
    heatmap_data = []
    contribution_counts = [c.count for c in contribution_days] if contribution_days else [0]
    max_count = max(contribution_counts) if contribution_counts else 1
    
    current_date = year_start
    while current_date <= year_end:
        count = heatmap_dict.get(current_date, 0)
        heatmap_data.append((current_date, count))
        current_date += timedelta(days=1)
    
    context = {
        'projects': projects,
        'heatmap_data': heatmap_data,
        'year': year,
        'max_count': max_count,
        'has_heatmap_data': len(heatmap_data) > 0,
    }
    return render(request, 'core/project_list.html', context)


def project_detail(request, slug):
    """Project detail page with repo activity chart and related devlog posts."""
    project = get_object_or_404(Project, slug=slug, status='active')
    
    # Get repo snapshot
    try:
        snapshot = RepoSnapshot.objects.get(repo_full_name=project.repo_full_name)
    except RepoSnapshot.DoesNotExist:
        snapshot = None
    
    # Get last 90 days of activity
    today = timezone.now().date()
    cutoff_date = today - timedelta(days=90)
    
    activity_points = RepoActivityPoint.objects.filter(
        repo_full_name=project.repo_full_name,
        day__gte=cutoff_date,
        day__lte=today
    ).order_by('day')
    
    # Build activity data
    activity_data = []
    max_commits = 1
    for point in activity_points:
        activity_data.append({
            'day': point.day,
            'commits': point.commits,
        })
        max_commits = max(max_commits, point.commits)
    
    # Get related devlog posts
    related_posts = DevlogPost.objects.filter(
        project=project,
        status='published',
        published_at__isnull=False
    )[:5]
    
    context = {
        'project': project,
        'snapshot': snapshot,
        'activity_data': activity_data,
        'max_commits': max_commits,
        'has_activity_data': len(activity_data) > 0,
        'related_posts': related_posts,
    }
    return render(request, 'core/project_detail.html', context)

