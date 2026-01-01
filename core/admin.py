from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'repo_full_name', 'status', 'featured', 'sort_order', 'created_at')
    list_filter = ('status', 'featured', 'created_at')
    search_fields = ('title', 'tagline', 'repo_full_name', 'stack')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'sort_order', 'status')
    ordering = ('sort_order', 'title')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'tagline', 'repo_full_name')
        }),
        ('Details', {
            'fields': ('stack', 'demo_url', 'status', 'featured', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')

