import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Layout from './components/Layout';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Movies from './pages/Movies';
import MovieDetail from './pages/MovieDetail';
import Booking from './pages/Booking';
import Profile from './pages/Profile';
import AdminMovies from './pages/admin/Movies';
import AdminBookings from './pages/admin/Bookings';
import AdminUsers from './pages/admin/Users';
import AdminReports from './pages/admin/Reports';
import { AuthProvider } from './contexts/AuthContext';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<Layout />}>
              <Route index element={<Home />} />
              <Route path="login" element={<Login />} />
              <Route path="register" element={<Register />} />
              <Route path="movies" element={<Movies />} />
              <Route path="movies/:id" element={<MovieDetail />} />
              <Route path="booking/:showtimeId" element={<Booking />} />
              <Route path="profile" element={<Profile />} />
              <Route path="admin/movies" element={<AdminMovies />} />
              <Route path="admin/bookings" element={<AdminBookings />} />
              <Route path="admin/users" element={<AdminUsers />} />
              <Route path="admin/reports" element={<AdminReports />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App; 