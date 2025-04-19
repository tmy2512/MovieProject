import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  TextField,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';

const steps = ['Chọn ghế', 'Thanh toán', 'Xác nhận'];

const Booking = () => {
  const { showtimeId } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [activeStep, setActiveStep] = useState(0);
  const [showtime, setShowtime] = useState(null);
  const [selectedSeats, setSelectedSeats] = useState([]);
  const [discountCode, setDiscountCode] = useState('');
  const [discount, setDiscount] = useState(0);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const fetchShowtime = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/showtimes/${showtimeId}/`);
        setShowtime(response.data);
      } catch (error) {
        console.error('Error fetching showtime:', error);
        setError('Không thể tải thông tin suất chiếu');
      }
    };

    fetchShowtime();
  }, [showtimeId, user, navigate]);

  const handleSeatSelect = (seat) => {
    if (selectedSeats.includes(seat)) {
      setSelectedSeats(selectedSeats.filter((s) => s !== seat));
    } else {
      setSelectedSeats([...selectedSeats, seat]);
    }
  };

  const handleDiscountApply = async () => {
    try {
      const response = await axios.post('http://localhost:8000/api/discounts/apply/', {
        code: discountCode,
        showtime_id: showtimeId,
      });
      setDiscount(response.data.discount);
      setError('');
    } catch (error) {
      setError('Mã giảm giá không hợp lệ hoặc đã hết hạn');
      setDiscount(0);
    }
  };

  const handleNext = () => {
    if (activeStep === 0 && selectedSeats.length === 0) {
      setError('Vui lòng chọn ít nhất một ghế');
      return;
    }
    setError('');
    setActiveStep((prevStep) => prevStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevStep) => prevStep - 1);
  };

  const handleConfirm = async () => {
    try {
      const bookingData = {
        showtime: showtimeId,
        seats: selectedSeats,
        discount_code: discountCode || null,
      };

      await axios.post('http://localhost:8000/api/bookings/', bookingData);
      setSuccess(true);
    } catch (error) {
      setError('Đặt vé thất bại. Vui lòng thử lại');
    }
  };

  const totalPrice = showtime
    ? selectedSeats.length * showtime.price * (1 - discount)
    : 0;

  if (!showtime) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
        {steps.map((label) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
          </Step>
        ))}
      </Stepper>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {activeStep === 0 && (
        <Grid container spacing={4}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Chọn ghế
                </Typography>
                <Box
                  sx={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(10, 1fr)',
                    gap: 1,
                    mt: 2,
                  }}
                >
                  {Array.from({ length: 100 }, (_, i) => i + 1).map((seat) => (
                    <Button
                      key={seat}
                      variant={selectedSeats.includes(seat) ? 'contained' : 'outlined'}
                      onClick={() => handleSeatSelect(seat)}
                      disabled={showtime.booked_seats.includes(seat)}
                    >
                      {seat}
                    </Button>
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Thông tin đặt vé
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Phim: {showtime.movie.title}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Ngày: {new Date(showtime.start_time).toLocaleDateString('vi-VN')}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Giờ: {new Date(showtime.start_time).toLocaleTimeString('vi-VN')}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Phòng: {showtime.theater}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Số ghế đã chọn: {selectedSeats.length}
                </Typography>
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Tổng tiền: {totalPrice.toLocaleString('vi-VN')} VNĐ
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeStep === 1 && (
        <Grid container spacing={4}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Thanh toán
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <TextField
                    fullWidth
                    label="Mã giảm giá"
                    value={discountCode}
                    onChange={(e) => setDiscountCode(e.target.value)}
                    sx={{ mb: 2 }}
                  />
                  <Button
                    variant="contained"
                    onClick={handleDiscountApply}
                    sx={{ mb: 2 }}
                  >
                    Áp dụng
                  </Button>
                </Box>
                <Typography variant="h6" sx={{ mt: 2 }}>
                  Tổng tiền: {totalPrice.toLocaleString('vi-VN')} VNĐ
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {activeStep === 2 && (
        <Grid container spacing={4}>
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Xác nhận đặt vé
                </Typography>
                <Typography variant="body1" gutterBottom>
                  Bạn có chắc chắn muốn đặt {selectedSeats.length} vé với tổng số tiền{' '}
                  {totalPrice.toLocaleString('vi-VN')} VNĐ?
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
        {activeStep !== 0 && (
          <Button onClick={handleBack} sx={{ mr: 1 }}>
            Quay lại
          </Button>
        )}
        {activeStep === steps.length - 1 ? (
          <Button variant="contained" onClick={handleConfirm}>
            Xác nhận
          </Button>
        ) : (
          <Button variant="contained" onClick={handleNext}>
            Tiếp tục
          </Button>
        )}
      </Box>

      <Dialog open={success} onClose={() => navigate('/')}>
        <DialogTitle>Đặt vé thành công</DialogTitle>
        <DialogContent>
          <Typography>
            Bạn đã đặt vé thành công. Vui lòng kiểm tra email để xem thông tin vé.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => navigate('/')}>Về trang chủ</Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Booking; 