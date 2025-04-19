import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

@api_view(['POST'])
def login(request):
    """Đăng nhập và lấy token"""
    try:
        response = requests.post(
            f"{settings.USER_SERVICE_URL}/api/users/login/",
            json=request.data
        )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến user service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

class CustomTokenRefreshView(TokenRefreshView):
    """Làm mới token"""
    def post(self, request, *args, **kwargs):
        try:
            response = requests.post(
                f"{settings.USER_SERVICE_URL}/api/token/refresh/",
                json=request.data
            )
            return Response(response.json(), status=response.status_code)
        except requests.RequestException:
            return Response(
                {'error': 'Không thể kết nối đến user service'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def movie_list(request):
    """Quản lý phim"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.MOVIE_SERVICE_URL}/api/movies/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.post(
                f"{settings.MOVIE_SERVICE_URL}/api/movies/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến movie service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def movie_detail(request, pk):
    """Chi tiết phim"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.MOVIE_SERVICE_URL}/api/movies/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        elif request.method == 'PUT':
            response = requests.put(
                f"{settings.MOVIE_SERVICE_URL}/api/movies/{pk}/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.delete(
                f"{settings.MOVIE_SERVICE_URL}/api/movies/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến movie service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def showtime_list(request):
    """Quản lý suất chiếu"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.post(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến showtime service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def showtime_detail(request, pk):
    """Chi tiết suất chiếu"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        elif request.method == 'PUT':
            response = requests.put(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{pk}/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.delete(
                f"{settings.SHOWTIME_SERVICE_URL}/api/showtimes/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến showtime service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def booking_list(request):
    """Quản lý đặt vé"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.BOOKING_SERVICE_URL}/api/bookings/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.post(
                f"{settings.BOOKING_SERVICE_URL}/api/bookings/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến booking service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def booking_detail(request, pk):
    """Chi tiết đặt vé"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.BOOKING_SERVICE_URL}/api/bookings/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        elif request.method == 'PUT':
            response = requests.put(
                f"{settings.BOOKING_SERVICE_URL}/api/bookings/{pk}/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.delete(
                f"{settings.BOOKING_SERVICE_URL}/api/bookings/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến booking service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def payment_list(request):
    """Quản lý thanh toán"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}/api/payments/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.post(
                f"{settings.PAYMENT_SERVICE_URL}/api/payments/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến payment service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def payment_detail(request, pk):
    """Chi tiết thanh toán"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.PAYMENT_SERVICE_URL}/api/payments/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        elif request.method == 'PUT':
            response = requests.put(
                f"{settings.PAYMENT_SERVICE_URL}/api/payments/{pk}/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.delete(
                f"{settings.PAYMENT_SERVICE_URL}/api/payments/{pk}/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến payment service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def report_list(request):
    """Quản lý báo cáo"""
    try:
        if request.method == 'GET':
            response = requests.get(
                f"{settings.REPORT_SERVICE_URL}/api/reports/",
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        else:
            response = requests.post(
                f"{settings.REPORT_SERVICE_URL}/api/reports/",
                json=request.data,
                headers={'Authorization': f"Bearer {request.auth}"}
            )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến report service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_detail(request, pk):
    """Chi tiết báo cáo"""
    try:
        response = requests.get(
            f"{settings.REPORT_SERVICE_URL}/api/reports/{pk}/",
            headers={'Authorization': f"Bearer {request.auth}"}
        )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến report service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_export(request, pk):
    """Xuất báo cáo"""
    try:
        response = requests.post(
            f"{settings.REPORT_SERVICE_URL}/api/reports/{pk}/export/",
            headers={'Authorization': f"Bearer {request.auth}"}
        )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến report service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_download(request, pk):
    """Tải báo cáo"""
    try:
        response = requests.get(
            f"{settings.REPORT_SERVICE_URL}/api/reports/{pk}/download/",
            headers={'Authorization': f"Bearer {request.auth}"}
        )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến report service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def report_summary(request):
    """Tổng quan báo cáo"""
    try:
        response = requests.get(
            f"{settings.REPORT_SERVICE_URL}/api/reports/summary/",
            headers={'Authorization': f"Bearer {request.auth}"}
        )
        return Response(response.json(), status=response.status_code)
    except requests.RequestException:
        return Response(
            {'error': 'Không thể kết nối đến report service'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        ) 