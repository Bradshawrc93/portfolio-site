# Debugging sync_github Issues

If you're not seeing commits or README after running `sync_github`, check the following:

## 1. Verify Data Was Saved

Run these commands in Render Shell to check if data exists:

```python
# Check if snapshot exists
python manage.py shell
>>> from githubsync.models import RepoSnapshot
>>> from core.models import Project
>>> project = Project.objects.first()
>>> print(f"Project repo: {project.repo_full_name}")
>>> snapshot = RepoSnapshot.objects.filter(repo_full_name=project.repo_full_name).first()
>>> if snapshot:
...     print(f"Snapshot exists: {snapshot.repo_full_name}")
...     print(f"Has README: {bool(snapshot.readme_content)}")
...     print(f"README length: {len(snapshot.readme_content) if snapshot.readme_content else 0}")
... else:
...     print("No snapshot found")

# Check activity data
>>> from githubsync.models import RepoActivityPoint
>>> from django.utils import timezone
>>> from datetime import timedelta
>>> today = timezone.now().date()
>>> cutoff = today - timedelta(days=90)
>>> activity = RepoActivityPoint.objects.filter(repo_full_name=project.repo_full_name, day__gte=cutoff)
>>> print(f"Activity points: {activity.count()}")
>>> if activity.exists():
...     print(f"First point: {activity.first().day} - {activity.first().commits} commits")
```

## 2. Check Sync Command Output

When you run `python manage.py sync_github`, look for:
- ✅ "Syncing X projects..."
- ✅ "Processing [repo]..."
- ❌ Any error messages
- ❌ "Stats calculation in progress" warnings (means GitHub is still calculating)

## 3. Common Issues

### GitHub API Rate Limits
- Without GITHUB_TOKEN: 60 requests/hour
- With GITHUB_TOKEN: 5000 requests/hour
- If you hit rate limits, wait an hour or add GITHUB_TOKEN

### Commit Activity Delayed
- GitHub's `/stats/commit_activity` endpoint can return 202 (accepted) if stats are being calculated
- Wait a few minutes and try again
- The command will show: "Stats calculation in progress for [repo]"

### Repository Name Case Sensitivity
- Make sure `repo_full_name` in your Project matches GitHub exactly
- Format: `username/repo-name` (e.g., `bradshawrc93/python-coding-challenges`)

### README Not Found
- Repository might not have a README.md file
- README might be in a different location (README.txt, README, etc.)
- The sync command only fetches README.md from the root

## 4. Re-run Sync

If data is missing, try:
```bash
python manage.py sync_github
```

Make sure to wait a moment if you see "Stats calculation in progress" messages.

