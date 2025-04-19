import React, { useState, useEffect } from 'react';
import {
  Container,
  Box,
  Typography,
  Button,
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
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Alert,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { Download, Delete } from '@mui/icons-material';
import axios from 'axios';
import { format } from 'date-fns';
import { vi } from 'date-fns/locale';

const Reports = () => {
  const [reports, setReports] = useState([]);
  const [openDialog, setOpenDialog] = useState(false);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/reports/');
      setReports(response.data);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setError('Không thể tải danh sách báo cáo');
    }
  };

  const handleCreateReport = async () => {
    if (!startDate || !endDate) {
      setError('Vui lòng chọn khoảng thời gian');
      return;
    }

    if (startDate > endDate) {
      setError('Ngày bắt đầu phải nhỏ hơn ngày kết thúc');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/api/reports/', {
        start_date: format(startDate, 'yyyy-MM-dd'),
        end_date: format(endDate, 'yyyy-MM-dd'),
      });
      setReports([...reports, response.data]);
      setOpenDialog(false);
      setSuccess('Tạo báo cáo thành công');
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setError('Tạo báo cáo thất bại');
    }
  };

  const handleDownloadReport = async (reportId) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/reports/${reportId}/download/`, {
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${reportId}.xlsx`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      setError('Tải báo cáo thất bại');
    }
  };

  const handleDeleteReport = async (reportId) => {
    try {
      await axios.delete(`http://localhost:8000/api/reports/${reportId}/`);
      setReports(reports.filter((report) => report.id !== reportId));
      setSuccess('Xóa báo cáo thành công');
      setTimeout(() => setSuccess(''), 3000);
    } catch (error) {
      setError('Xóa báo cáo thất bại');
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Quản lý báo cáo</Typography>
        <Button variant="contained" onClick={() => setOpenDialog(true)}>
          Tạo báo cáo mới
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      <Grid container spacing={3}>
        {reports.map((report) => (
          <Grid item xs={12} key={report.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <Box>
                    <Typography variant="h6">
                      Báo cáo từ {format(new Date(report.start_date), 'dd/MM/yyyy')} đến{' '}
                      {format(new Date(report.end_date), 'dd/MM/yyyy')}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Tạo ngày: {format(new Date(report.created_at), 'dd/MM/yyyy HH:mm')}
                    </Typography>
                  </Box>
                  <Box>
                    <IconButton
                      color="primary"
                      onClick={() => handleDownloadReport(report.id)}
                      sx={{ mr: 1 }}
                    >
                      <Download />
                    </IconButton>
                    <IconButton color="error" onClick={() => handleDeleteReport(report.id)}>
                      <Delete />
                    </IconButton>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      <Dialog open={openDialog} onClose={() => setOpenDialog(false)}>
        <DialogTitle>Tạo báo cáo mới</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2 }}>
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={vi}>
              <DatePicker
                label="Ngày bắt đầu"
                value={startDate}
                onChange={setStartDate}
                renderInput={(params) => <TextField {...params} fullWidth sx={{ mb: 2 }} />}
              />
              <DatePicker
                label="Ngày kết thúc"
                value={endDate}
                onChange={setEndDate}
                renderInput={(params) => <TextField {...params} fullWidth />}
              />
            </LocalizationProvider>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Hủy</Button>
          <Button onClick={handleCreateReport} variant="contained">
            Tạo báo cáo
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Reports; 