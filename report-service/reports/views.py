from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import RevenueReport, ExportHistory
from .serializers import (
    RevenueReportSerializer,
    RevenueReportCreateSerializer,
    ExportHistorySerializer
)
from .services import generate_revenue_report, export_report_to_excel
import os
from django.http import FileResponse
from django.conf import settings

class RevenueReportViewSet(viewsets.ModelViewSet):
    queryset = RevenueReport.objects.all()
    serializer_class = RevenueReportSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RevenueReportCreateSerializer
        return RevenueReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Tạo báo cáo mới
        report = RevenueReport.objects.create(
            start_date=serializer.validated_data['start_date'],
            end_date=serializer.validated_data['end_date'],
            status='PENDING'
        )
        
        # Bắt đầu quá trình tạo báo cáo
        if generate_revenue_report(report):
            return Response(
                RevenueReportSerializer(report).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Không thể tạo báo cáo'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['post'])
    def export(self, request, pk=None):
        report = self.get_object()
        
        # Tạo thư mục exports nếu chưa tồn tại
        exports_dir = os.path.join(settings.BASE_DIR, 'exports')
        os.makedirs(exports_dir, exist_ok=True)
        
        # Xuất báo cáo ra Excel
        if export_report_to_excel(report):
            # Lưu lịch sử xuất
            export = ExportHistory.objects.create(
                report=report,
                file_type='EXCEL',
                file_url=f'/exports/report_{report.id}.xlsx'
            )
            
            return Response(
                ExportHistorySerializer(export).data,
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'Không thể xuất báo cáo'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        report = self.get_object()
        export = report.exports.filter(file_type='EXCEL').first()
        
        if not export:
            return Response(
                {'error': 'Không tìm thấy file xuất'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        file_path = os.path.join(settings.BASE_DIR, export.file_url.lstrip('/'))
        
        if not os.path.exists(file_path):
            return Response(
                {'error': 'File không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=f'report_{report.id}.xlsx'
        )

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """API lấy tổng quan doanh thu"""
        # Lấy thời gian mặc định (30 ngày gần nhất)
        end_date = timezone.now().date()
        start_date = end_date - timezone.timedelta(days=30)
        
        # Lấy báo cáo gần nhất trong khoảng thời gian
        report = RevenueReport.objects.filter(
            start_date__gte=start_date,
            end_date__lte=end_date,
            status='COMPLETED'
        ).order_by('-created_at').first()
        
        if not report:
            return Response(
                {'error': 'Không tìm thấy báo cáo'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        return Response(RevenueReportSerializer(report).data) 