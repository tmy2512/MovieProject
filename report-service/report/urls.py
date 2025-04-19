from django.urls import path
from . import views

urlpatterns = [
    # API tạo và quản lý báo cáo
    path('reports/', views.RevenueReportViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='report-list'),
    
    path('reports/<int:pk>/', views.RevenueReportViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy'
    }), name='report-detail'),
    
    # API tải báo cáo
    path('reports/<int:pk>/download/', views.RevenueReportViewSet.as_view({
        'get': 'download'
    }), name='report-download'),
    
    # API lấy thông tin tổng hợp
    path('reports/<int:pk>/summary/', views.RevenueReportViewSet.as_view({
        'get': 'summary'
    }), name='report-summary'),
    
    # API xuất báo cáo
    path('reports/<int:pk>/export/', views.RevenueReportViewSet.as_view({
        'get': 'export'
    }), name='report-export'),
    
    # API thống kê doanh thu
    path('reports/revenue/range/', views.RevenueReportViewSet.as_view({
        'get': 'revenue_by_range'
    }), name='report-revenue-range'),
] 