from django.contrib import admin 

from core.apps.projects.models.project import ProjectDepartment, Project


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