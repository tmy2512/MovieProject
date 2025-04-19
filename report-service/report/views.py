from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from .models import RevenueReport
from .serializers import RevenueReportSerializer, RevenueReportCreateSerializer
from .services import ReportService
import pandas as pd
from io import BytesIO
from datetime import datetime

class RevenueReportViewSet(viewsets.ModelViewSet):
    queryset = RevenueReport.objects.all()
    serializer_class = RevenueReportSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return RevenueReportCreateSerializer
        return RevenueReportSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        
        report = ReportService.generate_revenue_report(start_date, end_date)
        if not report:
            return Response(
                {'error': 'Không thể tạo báo cáo'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        return Response(
            RevenueReportSerializer(report).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        try:
            summary = ReportService.get_report_summary(pk)
            return Response(summary)
        except RevenueReport.DoesNotExist:
            return Response(
                {'error': 'Báo cáo không tồn tại'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        try:
            report = self.get_object()
            summary = ReportService.get_report_summary(pk)
            
            # Tạo DataFrame cho từng loại dữ liệu
            df_movie = pd.DataFrame(summary['movie_revenue'])
            df_daily = pd.DataFrame(summary['daily_revenue'])
            df_theater = pd.DataFrame(summary['theater_revenue'])
            
            # Tạo Excel writer
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                # Tổng quan
                pd.DataFrame({
                    'Tổng doanh thu': [summary['total_revenue']],
                    'Tổng số vé': [summary['total_tickets']],
                    'Tổng số suất chiếu': [summary['total_showtimes']]
                }).to_excel(writer, sheet_name='Tổng quan', index=False)
                
                # Doanh thu theo phim
                df_movie.to_excel(writer, sheet_name='Doanh thu theo phim', index=False)
                
                # Doanh thu theo ngày
                df_daily.to_excel(writer, sheet_name='Doanh thu theo ngày', index=False)
                
                # Doanh thu theo rạp
                df_theater.to_excel(writer, sheet_name='Doanh thu theo rạp', index=False)
            
            # Tạo response
            output.seek(0)
            response = HttpResponse(
                output.getvalue(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = f'attachment; filename=report_{pk}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            return response
            
        except RevenueReport.DoesNotExist:
            return Response(
                {'error': 'Báo cáo không tồn tại'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        """Xuất báo cáo dưới dạng JSON"""
        try:
            summary = ReportService.get_report_summary(pk)
            return Response(summary)
        except RevenueReport.DoesNotExist:
            return Response(
                {'error': 'Báo cáo không tồn tại'}, 
                status=status.HTTP_404_NOT_FOUND
            ) 