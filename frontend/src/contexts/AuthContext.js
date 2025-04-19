import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';
import jwtDecode from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const decoded = jwtDecode(token);
        setUser(decoded);
      } catch (err) {
        localStorage.removeItem('token');
      }
    }
    setLoading(false);
  }, []);

  const login = async (email, password) => {
    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email,
        password,
      });
      const { access, refresh } = response.data;
      localStorage.setItem('token', access);
      localStorage.setItem('refresh', refresh);
      const decoded = jwtDecode(access);
      setUser(decoded);
      setError(null);
      return true;
    } catch (err) {
      setError(err.response?.data?.message || 'Đăng nhập thất bại');
      return false;
    }
  };

  const register = async (userData) => {
    try {
      await axios.post('http://localhost:8000/api/users/', userData);
      return true;
    } catch (err) {
      setError(err.response?.data?.message || 'Đăng ký thất bại');
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('refresh');
    setUser(null);
  };

  const refreshToken = async () => {
    try {
      const refresh = localStorage.getItem('refresh');
      const response = await axios.post('http://localhost:8000/api/token/refresh/', {
        refresh,
      });
      const { access } = response.data;
      localStorage.setItem('token', access);
      const decoded = jwtDecode(access);
      setUser(decoded);
      return true;
    } catch (err) {
      logout();
      return false;
    }
  };

  const value = {
    user,
    loading,
    error,
    login,
    register,
    logout,
    refreshToken,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 