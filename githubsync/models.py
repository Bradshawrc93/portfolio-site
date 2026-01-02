from django.db import models


class RepoSnapshot(models.Model):
    """Cache GitHub repository metadata."""
    repo_full_name = models.CharField(max_length=200, unique=True, db_index=True)
    description = models.TextField(blank=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    stars = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    open_issues = models.IntegerField(default=0)
    pushed_at = models.DateTimeField(null=True, blank=True)
    readme_content = models.TextField(blank=True, help_text="README.md content from repository")
    updated_at = models.DateTimeField(auto_now=True)
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fetched_at']

    def __str__(self):
        return self.repo_full_name


class RepoActivityPoint(models.Model):
    """Cache daily commit counts for a repository."""
    repo_full_name = models.CharField(max_length=200, db_index=True)
    day = models.DateField(db_index=True)
    commits = models.IntegerField(default=0)

    class Meta:
        unique_together = [['repo_full_name', 'day']]
        ordering = ['-day']
        indexes = [
            models.Index(fields=['repo_full_name', '-day']),
        ]

    def __str__(self):
        return f"{self.repo_full_name} - {self.day} ({self.commits} commits)"


class UserContributionDay(models.Model):
    """Cache daily contribution counts for a GitHub user (current year)."""
    username = models.CharField(max_length=100, db_index=True)
    day = models.DateField(db_index=True)
    count = models.IntegerField(default=0)

    class Meta:
        unique_together = [['username', 'day']]
        ordering = ['-day']
        indexes = [
            models.Index(fields=['username', '-day']),
        ]

    def __str__(self):
        return f"{self.username} - {self.day} ({self.count} contributions)"

