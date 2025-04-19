import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

// Movie Service
export const movieService = {
    // Phim
    getMovies: () => axios.get(`${API_URL}/movies/`),
    getMovieDetail: (id) => axios.get(`${API_URL}/movies/${id}/`),
    createMovie: (data) => axios.post(`${API_URL}/movies/`, data),
    updateMovie: (id, data) => axios.put(`${API_URL}/movies/${id}/`, data),
    deleteMovie: (id) => axios.delete(`${API_URL}/movies/${id}/`),
    searchMovies: (query) => axios.get(`${API_URL}/movies/search/?q=${query}`),
    filterMovies: (params) => axios.get(`${API_URL}/movies/filter/`, { params }),
    getUpcomingMovies: () => axios.get(`${API_URL}/movies/upcoming/`),
    getNowShowingMovies: () => axios.get(`${API_URL}/movies/now-showing/`),
    
    // Thể loại
    getGenres: () => axios.get(`${API_URL}/genres/`),
    getGenreDetail: (id) => axios.get(`${API_URL}/genres/${id}/`),
    createGenre: (data) => axios.post(`${API_URL}/genres/`, data),
    getMoviesByGenre: (id) => axios.get(`${API_URL}/genres/${id}/movies/`),
    
    // Diễn viên
    getActors: () => axios.get(`${API_URL}/actors/`),
    getActorDetail: (id) => axios.get(`${API_URL}/actors/${id}/`),
    createActor: (data) => axios.post(`${API_URL}/actors/`, data),
    getMoviesByActor: (id) => axios.get(`${API_URL}/actors/${id}/movies/`),
};

// Showtime Service
export const showtimeService = {
    // Suất chiếu
    getShowtimes: () => axios.get(`${API_URL}/showtimes/`),
    getShowtimeDetail: (id) => axios.get(`${API_URL}/showtimes/${id}/`),
    createShowtime: (data) => axios.post(`${API_URL}/showtimes/`, data),
    updateShowtime: (id, data) => axios.put(`${API_URL}/showtimes/${id}/`, data),
    deleteShowtime: (id) => axios.delete(`${API_URL}/showtimes/${id}/`),
    getShowtimesByMovie: (movieId) => axios.get(`${API_URL}/showtimes/movie/${movieId}/`),
    getShowtimesByTheater: (theaterId) => axios.get(`${API_URL}/showtimes/theater/${theaterId}/`),
    getShowtimesByDate: (date) => axios.get(`${API_URL}/showtimes/date/${date}/`),
    getShowtimesByDateRange: (startDate, endDate) => axios.get(`${API_URL}/showtimes/range/?start_date=${startDate}&end_date=${endDate}`),
    getAvailableShowtimes: (movieId, date) => axios.get(`${API_URL}/showtimes/available/?movie_id=${movieId}&date=${date}`),
    
    // Rạp
    getTheaters: () => axios.get(`${API_URL}/theaters/`),
    getTheaterDetail: (id) => axios.get(`${API_URL}/theaters/${id}/`),
    createTheater: (data) => axios.post(`${API_URL}/theaters/`, data),
    
    // Phòng chiếu
    getRooms: () => axios.get(`${API_URL}/rooms/`),
    getRoomDetail: (id) => axios.get(`${API_URL}/rooms/${id}/`),
    createRoom: (data) => axios.post(`${API_URL}/rooms/`, data),
    getRoomsByTheater: (theaterId) => axios.get(`${API_URL}/rooms/theater/${theaterId}/`),
};

// Booking Service
export const bookingService = {
    // Đặt vé
    getBookings: () => axios.get(`${API_URL}/bookings/`),
    getBookingDetail: (id) => axios.get(`${API_URL}/bookings/${id}/`),
    createBooking: (data) => axios.post(`${API_URL}/bookings/`, data),
    updateBooking: (id, data) => axios.put(`${API_URL}/bookings/${id}/`, data),
    deleteBooking: (id) => axios.delete(`${API_URL}/bookings/${id}/`),
    cancelBooking: (id) => axios.post(`${API_URL}/bookings/${id}/cancel/`),
    getBookingsByUser: (userId) => axios.get(`${API_URL}/bookings/user/${userId}/`),
    getBookingsByShowtime: (showtimeId) => axios.get(`${API_URL}/bookings/showtime/${showtimeId}/`),
    checkSeatAvailability: (data) => axios.post(`${API_URL}/bookings/check-seat/`, data),
    calculatePrice: (data) => axios.post(`${API_URL}/bookings/calculate-price/`, data),
    processPayment: (data) => axios.post(`${API_URL}/bookings/payment/`, data),
    
    // Vé
    getTickets: () => axios.get(`${API_URL}/tickets/`),
    getTicketDetail: (id) => axios.get(`${API_URL}/tickets/${id}/`),
    createTicket: (data) => axios.post(`${API_URL}/tickets/`, data),
    getTicketsByBooking: (bookingId) => axios.get(`${API_URL}/tickets/booking/${bookingId}/`),
    
    // Ghế
    getSeats: () => axios.get(`${API_URL}/seats/`),
    getSeatDetail: (id) => axios.get(`${API_URL}/seats/${id}/`),
    createSeat: (data) => axios.post(`${API_URL}/seats/`, data),
    getSeatsByRoom: (roomId) => axios.get(`${API_URL}/seats/room/${roomId}/`),
    getAvailableSeats: (showtimeId) => axios.get(`${API_URL}/seats/available/?showtime_id=${showtimeId}`),
};

// Report Service
export const reportService = {
    getReports: () => axios.get(`${API_URL}/reports/`),
    getReportDetail: (id) => axios.get(`${API_URL}/reports/${id}/`),
    createReport: (data) => axios.post(`${API_URL}/reports/`, data),
    deleteReport: (id) => axios.delete(`${API_URL}/reports/${id}/`),
    downloadReport: (id) => axios.get(`${API_URL}/reports/${id}/download/`, { responseType: 'blob' }),
    getReportSummary: (id) => axios.get(`${API_URL}/reports/${id}/summary/`),
    exportReport: (id) => axios.get(`${API_URL}/reports/${id}/export/`),
    getRevenueByRange: (startDate, endDate) => axios.get(`${API_URL}/reports/revenue/range/?start_date=${startDate}&end_date=${endDate}`),
}; 