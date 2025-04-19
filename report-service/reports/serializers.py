from rest_framework import serializers
from .models import (
    RevenueReport,
    MovieRevenue,
    TheaterRevenue,
    DailyRevenue,
    ExportHistory
)

class MovieRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieRevenue
        fields = '__all__'

class TheaterRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheaterRevenue
        fields = '__all__'

class DailyRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyRevenue
        fields = '__all__'

class ExportHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExportHistory
        fields = '__all__'

class RevenueReportSerializer(serializers.ModelSerializer):
    movie_revenues = MovieRevenueSerializer(many=True, read_only=True)
    theater_revenues = TheaterRevenueSerializer(many=True, read_only=True)
    daily_revenues = DailyRevenueSerializer(many=True, read_only=True)
    exports = ExportHistorySerializer(many=True, read_only=True)

    class Meta:
        model = RevenueReport
        fields = '__all__'

class RevenueReportCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RevenueReport
        fields = ['start_date', 'end_date']

    def validate(self, attrs):
        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError(
                "Ngày bắt đầu không thể sau ngày kết thúc"
            )
        return attrs 