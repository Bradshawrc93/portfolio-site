from django.contrib import admin
from django.utils.html import format_html
from .models import DevlogPost


@admin.register(DevlogPost)
class DevlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'published_at', 'project', 'created_at', 'preview_link')
    list_filter = ('status', 'published_at', 'created_at', 'project')
    search_fields = ('title', 'content_md', 'tags')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status',)
    date_hierarchy = 'published_at'
    ordering = ('-published_at', '-created_at')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content_md', 'status', 'published_at')
        }),
        ('Metadata', {
            'fields': ('project', 'tags')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')
    
    def preview_link(self, obj):
        if obj.is_published:
            return format_html(
                '<a href="{}" target="_blank">View</a>',
                obj.get_absolute_url()
            )
        return '-'
    preview_link.short_description = 'Preview'
    
    def save_model(self, request, obj, form, change):
        # Auto-set published_at if status is published and it's not set
        if obj.status == 'published' and not obj.published_at:
            from django.utils import timezone
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

