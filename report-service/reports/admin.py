from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'report_type', 'start_date', 'end_date', 'created_by', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('name', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at') 