from django.db import models
from django.urls import reverse
from core.models import Project


class DevlogPost(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content_md = models.TextField(help_text="Markdown content")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    published_at = models.DateTimeField(blank=True, null=True)
    project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='devlog_posts'
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('devlog_detail', kwargs={'slug': self.slug})

    def get_tags_list(self):
        """Return tags as a list of strings."""
        return [t.strip() for t in self.tags.split(',') if t.strip()]

    @property
    def is_published(self):
        return self.status == 'published' and self.published_at is not None

