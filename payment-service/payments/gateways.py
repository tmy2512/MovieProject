from abc import ABC, abstractmethod
import hashlib
import hmac
import urllib.parse
from typing import Dict, Any
from datetime import datetime
import requests
from django.conf import settings

class PaymentGateway(ABC):
    @abstractmethod
    def create_payment(self, amount: float, order_info: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    def verify_payment(self, payment_data: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def process_refund(self, transaction_id: str, amount: float, reason: str) -> Dict[str, Any]:
        pass

class VNPayGateway(PaymentGateway):
    def __init__(self):
        self.merchant_id = settings.VNPAY['MERCHANT_ID']
        self.merchant_password = settings.VNPAY['MERCHANT_PASSWORD']
        self.payment_url = settings.VNPAY['PAYMENT_URL']
        self.return_url = settings.VNPAY['RETURN_URL']

    def _create_signature(self, data: Dict[str, str]) -> str:
        # Sắp xếp các tham số theo thứ tự alphabet
        sorted_items = sorted(data.items())
        
        # Tạo chuỗi query string
        query_string = "&".join([f"{k}={v}" for k, v in sorted_items])
        
        # Tạo chữ ký bằng HMAC-SHA512
        h = hmac.new(
            self.merchant_password.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha512
        )
        return h.hexdigest()

    def create_payment(self, amount: float, order_info: str) -> Dict[str, Any]:
        # Chuẩn bị dữ liệu thanh toán
        payment_data = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'pay',
            'vnp_TmnCode': self.merchant_id,
            'vnp_Amount': str(int(amount * 100)),  # Số tiền * 100 (VNĐ)
            'vnp_CurrCode': 'VND',
            'vnp_TxnRef': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_OrderInfo': order_info,
            'vnp_OrderType': 'billpayment',
            'vnp_Locale': 'vn',
            'vnp_ReturnUrl': self.return_url,
            'vnp_IpAddr': '127.0.0.1',  # IP của khách hàng
            'vnp_CreateDate': datetime.now().strftime('%Y%m%d%H%M%S'),
        }

        # Tạo chữ ký
        payment_data['vnp_SecureHash'] = self._create_signature(payment_data)

        # Tạo URL thanh toán
        query_string = urllib.parse.urlencode(payment_data)
        payment_url = f"{self.payment_url}?{query_string}"

        return {
            'payment_url': payment_url,
            'transaction_id': payment_data['vnp_TxnRef']
        }

    def verify_payment(self, payment_data: Dict[str, Any]) -> bool:
        # Tách secure hash từ dữ liệu
        secure_hash = payment_data.pop('vnp_SecureHash', None)
        if not secure_hash:
            return False

        # Tạo chữ ký từ dữ liệu nhận được
        calculated_hash = self._create_signature(payment_data)

        # So sánh chữ ký
        return secure_hash == calculated_hash

    def process_refund(self, transaction_id: str, amount: float, reason: str) -> Dict[str, Any]:
        # Chuẩn bị dữ liệu hoàn tiền
        refund_data = {
            'vnp_Version': '2.1.0',
            'vnp_Command': 'refund',
            'vnp_TmnCode': self.merchant_id,
            'vnp_TransactionType': '03',  # Hoàn tiền toàn phần
            'vnp_TxnRef': transaction_id,
            'vnp_Amount': str(int(amount * 100)),
            'vnp_OrderInfo': reason,
            'vnp_TransactionNo': datetime.now().strftime('%Y%m%d%H%M%S'),
            'vnp_CreateBy': 'System',
        }

        # Tạo chữ ký
        refund_data['vnp_SecureHash'] = self._create_signature(refund_data)

        # Gửi yêu cầu hoàn tiền đến VNPay
        try:
            response = requests.post(
                'https://sandbox.vnpayment.vn/merchant_webapi/api/transaction',
                json=refund_data
            )
            return response.json()
        except requests.RequestException:
            return {'error': 'Không thể kết nối đến VNPay'} 