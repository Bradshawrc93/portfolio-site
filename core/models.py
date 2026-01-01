from django.db import models
from django.urls import reverse


class Project(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('planning', 'Planning'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    repo_full_name = models.CharField(
        max_length=200,
        help_text="GitHub repo in format: owner/repo (e.g., bradshawrc93/project-name)"
    )
    tagline = models.CharField(max_length=300, help_text="Short description")
    stack = models.CharField(
        max_length=500,
        help_text="Comma-separated tech stack (e.g., Python, Django, PostgreSQL)"
    )
    demo_url = models.URLField(blank=True, null=True, help_text="Optional demo/live site URL")
    featured = models.BooleanField(default=False, help_text="Show on homepage")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    sort_order = models.IntegerField(default=0, help_text="Lower numbers appear first")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    def get_stack_list(self):
        """Return stack as a list of strings."""
        return [s.strip() for s in self.stack.split(',') if s.strip()]

