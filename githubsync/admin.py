from django.contrib import admin
from .models import RepoSnapshot, RepoActivityPoint, UserContributionDay


@admin.register(RepoSnapshot)
class RepoSnapshotAdmin(admin.ModelAdmin):
    list_display = ('repo_full_name', 'language', 'stars', 'forks', 'open_issues', 'fetched_at', 'updated_at')
    list_filter = ('language', 'fetched_at')
    search_fields = ('repo_full_name', 'description')
    readonly_fields = ('fetched_at', 'updated_at')
    ordering = ('-fetched_at',)


@admin.register(RepoActivityPoint)
class RepoActivityPointAdmin(admin.ModelAdmin):
    list_display = ('repo_full_name', 'day', 'commits')
    list_filter = ('day', 'repo_full_name')
    search_fields = ('repo_full_name',)
    ordering = ('-day', 'repo_full_name')
    date_hierarchy = 'day'


@admin.register(UserContributionDay)
class UserContributionDayAdmin(admin.ModelAdmin):
    list_display = ('username', 'day', 'count')
    list_filter = ('username', 'day')
    search_fields = ('username',)
    ordering = ('-day', 'username')
    date_hierarchy = 'day'

