from rest_framework import viewsets, permissions
from .models import Report
from .serializers import ReportSerializer, ReportCreateSerializer

class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Report.objects.filter(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return ReportCreateSerializer
        return ReportSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user) 