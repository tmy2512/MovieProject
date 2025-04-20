from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'name', 'report_type', 'start_date', 'end_date', 
                 'created_by', 'created_at', 'updated_at', 'data')
        read_only_fields = ('id', 'created_at', 'updated_at')

class ReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('name', 'report_type', 'start_date', 'end_date') 