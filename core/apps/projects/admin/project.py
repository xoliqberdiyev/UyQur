from django.contrib import admin 

from core.apps.projects.models.project import Project, ProjectFolder, ProjectLocation



@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'location', 'start_date', 'end_date']
    search_fields = ['name']


@admin.register(ProjectFolder)
class ProjectFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(ProjectLocation)
class ProjectLocation(admin.ModelAdmin):
    list_display = ['id','address', 'latitude', 'longitude']