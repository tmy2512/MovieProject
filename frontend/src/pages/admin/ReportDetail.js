import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Button,
  Alert,
} from '@mui/material';
import { Download } from '@mui/icons-material';
import axios from 'axios';
import { format } from 'date-fns';
import { vi } from 'date-fns/locale';

const ReportDetail = () => {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchReport();
  }, [id]);

  const fetchReport = async () => {
    try {
      const [reportResponse, summaryResponse] = await Promise.all([
        axios.get(`http://localhost:8000/api/reports/${id}/`),
        axios.get(`http://localhost:8000/api/reports/${id}/summary/`),
      ]);
      setReport(reportResponse.data);
      setSummary(summaryResponse.data);
    } catch (error) {
      console.error('Error fetching report:', error);
      setError('Không thể tải thông tin báo cáo');
    }
  };

  const handleDownload = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/api/reports/${id}/download/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${id}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setError('Tải báo cáo thất bại');
    }
  };

  if (!report || !summary) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">
          Báo cáo từ {format(new Date(report.start_date), 'dd/MM/yyyy')} đến{' '}
          {format(new Date(report.end_date), 'dd/MM/yyyy')}
        </Typography>
        <Button
          variant="contained"
          startIcon={<Download />}
          onClick={handleDownload}
        >
          Tải báo cáo
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tổng doanh thu
              </Typography>
              <Typography variant="h4" color="primary">
                {summary.total_revenue.toLocaleString('vi-VN')} VNĐ
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Số vé đã bán
              </Typography>
              <Typography variant="h4" color="primary">
                {summary.total_tickets}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Số suất chiếu
              </Typography>
              <Typography variant="h4" color="primary">
                {summary.total_showtimes}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Doanh thu theo phim
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Tên phim</TableCell>
                <TableCell align="right">Số vé</TableCell>
                <TableCell align="right">Doanh thu</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {summary.movie_revenue.map((movie) => (
                <TableRow key={movie.movie_id}>
                  <TableCell>{movie.movie_title}</TableCell>
                  <TableCell align="right">{movie.ticket_count}</TableCell>
                  <TableCell align="right">
                    {movie.revenue.toLocaleString('vi-VN')} VNĐ
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>

      <Box sx={{ mt: 4 }}>
        <Typography variant="h5" gutterBottom>
          Doanh thu theo ngày
        </Typography>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Ngày</TableCell>
                <TableCell align="right">Số vé</TableCell>
                <TableCell align="right">Doanh thu</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {summary.daily_revenue.map((day) => (
                <TableRow key={day.date}>
                  <TableCell>{format(new Date(day.date), 'dd/MM/yyyy')}</TableCell>
                  <TableCell align="right">{day.ticket_count}</TableCell>
                  <TableCell align="right">
                    {day.revenue.toLocaleString('vi-VN')} VNĐ
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Box>
    </Container>
  );
};

export default ReportDetail; 