from django.contrib import admin 

from core.apps.projects.models.project import ProjectDepartment, Project, ProjectFolder


class ProjectDepartmentInline(admin.TabularInline):
    model = ProjectDepartment
    extra = 0


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'start_date', 'end_date']
    search_fields = ['name']
    inlines = [ProjectDepartmentInline]


@admin.register(ProjectDepartment)
class ProjectDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'project']
    search_fields = ['name']


@admin.register(ProjectFolder)
class ProjectFolderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']