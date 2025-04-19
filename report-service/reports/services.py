from datetime import datetime, timedelta
from django.db.models import Sum, Count
from .models import RevenueReport, MovieRevenue, DailyRevenue, TheaterRevenue, ShowtimeRevenue
import requests
from decimal import Decimal

class ReportService:
    @staticmethod
    def fetch_booking_data(start_date, end_date):
        """Lấy dữ liệu đặt vé từ booking service"""
        try:
            response = requests.get(
                'http://booking-service:8001/api/bookings/',
                params={
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
            return response.json()
        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def fetch_showtime_data(showtime_ids):
        """Lấy thông tin suất chiếu từ showtime service"""
        try:
            response = requests.get(
                'http://showtime-service:8002/api/showtimes/',
                params={'ids': ','.join(map(str, showtime_ids))}
            )
            return response.json()
        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def fetch_movie_data(movie_ids):
        """Lấy thông tin phim từ movie service"""
        try:
            response = requests.get(
                'http://movie-service:8003/api/movies/',
                params={'ids': ','.join(map(str, movie_ids))}
            )
            return response.json()
        except requests.exceptions.RequestException:
            return []

    @staticmethod
    def generate_revenue_report(start_date, end_date):
        """Tạo báo cáo doanh thu"""
        # Lấy dữ liệu đặt vé
        bookings = ReportService.fetch_booking_data(start_date, end_date)
        if not bookings:
            return None

        # Tạo báo cáo chính
        report = RevenueReport.objects.create(
            start_date=start_date,
            end_date=end_date
        )

        # Tổng hợp dữ liệu
        showtime_ids = set()
        movie_ids = set()
        daily_revenues = {}
        theater_revenues = {}
        movie_revenues = {}
        showtime_revenues = {}

        for booking in bookings:
            showtime_id = booking['showtime']
            showtime_ids.add(showtime_id)
            
            # Tổng hợp theo ngày
            date = booking['created_at'][:10]
            if date not in daily_revenues:
                daily_revenues[date] = {'tickets': 0, 'revenue': Decimal('0')}
            daily_revenues[date]['tickets'] += 1
            daily_revenues[date]['revenue'] += Decimal(str(booking['total_amount']))

            # Tổng hợp theo suất chiếu
            if showtime_id not in showtime_revenues:
                showtime_revenues[showtime_id] = {
                    'tickets': 0,
                    'revenue': Decimal('0'),
                    'movie_id': booking['movie_id'],
                    'theater_id': booking['theater_id']
                }
            showtime_revenues[showtime_id]['tickets'] += 1
            showtime_revenues[showtime_id]['revenue'] += Decimal(str(booking['total_amount']))

        # Lấy thông tin suất chiếu
        showtimes = ReportService.fetch_showtime_data(list(showtime_ids))
        for showtime in showtimes:
            movie_ids.add(showtime['movie'])
            theater_id = showtime['theater']

            # Tổng hợp theo rạp
            if theater_id not in theater_revenues:
                theater_revenues[theater_id] = {
                    'tickets': 0,
                    'revenue': Decimal('0'),
                    'name': showtime['theater_name']
                }
            theater_revenues[theater_id]['tickets'] += showtime_revenues[showtime['id']]['tickets']
            theater_revenues[theater_id]['revenue'] += showtime_revenues[showtime['id']]['revenue']

            # Tổng hợp theo phim
            movie_id = showtime['movie']
            if movie_id not in movie_revenues:
                movie_revenues[movie_id] = {
                    'tickets': 0,
                    'revenue': Decimal('0'),
                    'title': showtime['movie_title']
                }
            movie_revenues[movie_id]['tickets'] += showtime_revenues[showtime['id']]['tickets']
            movie_revenues[movie_id]['revenue'] += showtime_revenues[showtime['id']]['revenue']

        # Lưu doanh thu theo ngày
        for date, data in daily_revenues.items():
            DailyRevenue.objects.create(
                report=report,
                date=date,
                ticket_count=data['tickets'],
                revenue=data['revenue']
            )

        # Lưu doanh thu theo rạp
        for theater_id, data in theater_revenues.items():
            TheaterRevenue.objects.create(
                report=report,
                theater_id=theater_id,
                theater_name=data['name'],
                ticket_count=data['tickets'],
                revenue=data['revenue']
            )

        # Lưu doanh thu theo phim
        for movie_id, data in movie_revenues.items():
            MovieRevenue.objects.create(
                report=report,
                movie_id=movie_id,
                movie_title=data['title'],
                ticket_count=data['tickets'],
                revenue=data['revenue']
            )

        # Lưu doanh thu theo suất chiếu
        for showtime_id, data in showtime_revenues.items():
            showtime = next(s for s in showtimes if s['id'] == showtime_id)
            ShowtimeRevenue.objects.create(
                report=report,
                showtime_id=showtime_id,
                movie_title=showtime['movie_title'],
                theater_name=showtime['theater_name'],
                start_time=showtime['start_time'],
                ticket_count=data['tickets'],
                revenue=data['revenue']
            )

        # Cập nhật tổng doanh thu
        report.total_revenue = sum(d['revenue'] for d in daily_revenues.values())
        report.total_tickets = sum(d['tickets'] for d in daily_revenues.values())
        report.total_showtimes = len(showtime_ids)
        report.save()

        return report

    @staticmethod
    def get_report_summary(report_id):
        """Lấy thông tin tổng hợp của báo cáo"""
        report = RevenueReport.objects.get(id=report_id)
        
        return {
            'total_revenue': report.total_revenue,
            'total_tickets': report.total_tickets,
            'total_showtimes': report.total_showtimes,
            'movie_revenue': [
                {
                    'movie_id': mr.movie_id,
                    'movie_title': mr.movie_title,
                    'ticket_count': mr.ticket_count,
                    'revenue': mr.revenue
                }
                for mr in report.movie_revenues.all()
            ],
            'daily_revenue': [
                {
                    'date': dr.date,
                    'ticket_count': dr.ticket_count,
                    'revenue': dr.revenue
                }
                for dr in report.daily_revenues.all()
            ],
            'theater_revenue': [
                {
                    'theater_id': tr.theater_id,
                    'theater_name': tr.theater_name,
                    'ticket_count': tr.ticket_count,
                    'revenue': tr.revenue
                }
                for tr in report.theater_revenues.all()
            ]
        } 