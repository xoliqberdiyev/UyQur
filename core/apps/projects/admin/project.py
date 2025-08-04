from django.contrib import admin 

from core.apps.projects.models.project import Project, ProjectFolder



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'start_date', 'end_date']
    search_fields = ['name']
    inlines = []


@admin.register(ProjectFolder)
class ProjectFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']