"""
Management command to sync GitHub data.

Fetches:
1. Repository snapshots for all Project repos
2. Last 90 days of commit activity per repo
3. Current year contributions for user bradshawrc93
"""

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import os
from core.models import Project
from githubsync.models import RepoSnapshot, RepoActivityPoint, UserContributionDay


class Command(BaseCommand):
    help = 'Sync GitHub repository data and user contributions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='bradshawrc93',
            help='GitHub username for contribution data (default: bradshawrc93)',
        )

    def handle(self, *args, **options):
        username = options['username']
        github_token = os.environ.get('GITHUB_TOKEN')
        
        headers = {'Accept': 'application/vnd.github.v3+json'}
        if github_token:
            headers['Authorization'] = f'token {github_token}'
        
        base_url = 'https://api.github.com'
        
        self.stdout.write(self.style.SUCCESS('Starting GitHub sync...'))
        
        # 1. Sync repository snapshots and activity for all projects
        projects = Project.objects.all()
        self.stdout.write(f'Syncing {projects.count()} projects...')
        
        for project in projects:
            self.stdout.write(f'  Processing {project.repo_full_name}...')
            
            # Fetch repo snapshot
            try:
                repo_url = f'{base_url}/repos/{project.repo_full_name}'
                response = requests.get(repo_url, headers=headers, timeout=10)
                response.raise_for_status()
                repo_data = response.json()
                
                # Parse pushed_at datetime
                pushed_at_str = repo_data.get('pushed_at')
                pushed_at = None
                if pushed_at_str:
                    try:
                        pushed_at = datetime.fromisoformat(pushed_at_str.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        pass
                
                # Update or create RepoSnapshot
                snapshot, created = RepoSnapshot.objects.update_or_create(
                    repo_full_name=project.repo_full_name,
                    defaults={
                        'description': repo_data.get('description', '') or '',
                        'language': repo_data.get('language', ''),
                        'stars': repo_data.get('stargazers_count', 0),
                        'forks': repo_data.get('forks_count', 0),
                        'open_issues': repo_data.get('open_issues_count', 0),
                        'pushed_at': pushed_at,
                    }
                )
                
                # Fetch commit activity (last 90 days)
                stats_url = f'{base_url}/repos/{project.repo_full_name}/stats/commit_activity'
                stats_response = requests.get(stats_url, headers=headers, timeout=30)
                
                if stats_response.status_code == 200:
                    commit_activity = stats_response.json()
                    
                    # Process last 90 days (approximately 13 weeks)
                    today = timezone.now().date()
                    cutoff_date = today - timedelta(days=90)
                    
                    # Clear old activity points for this repo
                    RepoActivityPoint.objects.filter(
                        repo_full_name=project.repo_full_name,
                        day__lt=cutoff_date
                    ).delete()
                    
                    # Process commit activity (array of weeks)
                    for week_data in commit_activity[-13:]:  # Last 13 weeks
                        if not week_data or 'days' not in week_data:
                            continue
                        
                        week_start_timestamp = week_data.get('week', 0)
                        week_start = datetime.fromtimestamp(week_start_timestamp).date()
                        
                        # Process each day in the week
                        for day_offset, day_commits in enumerate(week_data.get('days', [])):
                            day = week_start + timedelta(days=day_offset)
                            
                            # Only store if within last 90 days
                            if day >= cutoff_date and day <= today:
                                RepoActivityPoint.objects.update_or_create(
                                    repo_full_name=project.repo_full_name,
                                    day=day,
                                    defaults={'commits': day_commits}
                                )
                elif stats_response.status_code == 202:
                    self.stdout.write(
                        self.style.WARNING(f'  Stats calculation in progress for {project.repo_full_name}')
                    )
                
            except requests.exceptions.RequestException as e:
                self.stdout.write(
                    self.style.WARNING(f'  Error fetching {project.repo_full_name}: {e}')
                )
                continue
        
        # 2. Fetch user contributions for current year
        self.stdout.write(f'Syncing contributions for {username}...')
        
        try:
            events_url = f'{base_url}/users/{username}/events/public'
            all_contributions = {}
            
            # Get current year range
            now = timezone.now()
            year_start = datetime(now.year, 1, 1).date()
            year_end = datetime(now.year, 12, 31).date()
            
            # Clear old contribution days for this user
            UserContributionDay.objects.filter(
                username=username,
                day__lt=year_start
            ).delete()
            
            # Fetch events (limited - GitHub API pagination)
            # Note: This is a simplified version using events API
            page = 1
            per_page = 100
            max_pages = 10  # Limit to avoid rate limits
            
            while page <= max_pages:
                response = requests.get(
                    events_url,
                    headers=headers,
                    params={'page': page, 'per_page': per_page},
                    timeout=10
                )
                
                if response.status_code != 200:
                    break
                
                events = response.json()
                if not events:
                    break
                
                for event in events:
                    created_at_str = event.get('created_at')
                    if not created_at_str:
                        continue
                    
                    try:
                        event_date = datetime.fromisoformat(created_at_str.replace('Z', '+00:00')).date()
                    except (ValueError, AttributeError):
                        continue
                    
                    # Only count events from current year
                    if year_start <= event_date <= year_end:
                        # Count PushEvent and other contribution events
                        event_type = event.get('type', '')
                        if event_type in ['PushEvent', 'CreateEvent', 'PullRequestEvent', 'IssuesEvent']:
                            all_contributions[event_date] = all_contributions.get(event_date, 0) + 1
                
                # Check if we've gone past current year
                if events:
                    try:
                        last_event_date = datetime.fromisoformat(events[-1]['created_at'].replace('Z', '+00:00')).date()
                        if last_event_date < year_start:
                            break
                    except (ValueError, AttributeError, KeyError):
                        pass
                
                page += 1
            
            # Store contribution days
            for day, count in all_contributions.items():
                UserContributionDay.objects.update_or_create(
                    username=username,
                    day=day,
                    defaults={'count': count}
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'  Synced {len(all_contributions)} days of contributions'
                )
            )
            
        except requests.exceptions.RequestException as e:
            self.stdout.write(
                self.style.WARNING(f'  Error fetching contributions: {e}')
            )
        
        self.stdout.write(self.style.SUCCESS('GitHub sync completed!'))

