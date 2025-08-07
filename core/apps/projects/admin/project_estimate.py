from django.contrib import admin

from core.apps.projects.models.project_estimate import ProjectEstimate, EstimateWork, EstimateProduct


@admin.register(ProjectEstimate)
class ProjectEstimateAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name']


@admin.register(EstimateWork)
class EstimateWorkAdmin(admin.ModelAdmin):
    list_display = ['id', 'number', 'name', 'price', 'quantity']

    
@admin.register(EstimateProduct)
class EstimateProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'price', 'quantity']
