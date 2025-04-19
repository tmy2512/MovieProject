import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  Container,
  Grid,
  Typography,
  Box,
  Card,
  CardContent,
  Button,
  Chip,
  Divider,
  Rating,
} from '@mui/material';
import { PlayArrow, AccessTime, CalendarToday } from '@mui/icons-material';
import axios from 'axios';

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [showtimes, setShowtimes] = useState([]);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const [movieResponse, showtimesResponse] = await Promise.all([
          axios.get(`http://localhost:8000/api/movies/${id}/`),
          axios.get(`http://localhost:8000/api/showtimes/?movie=${id}`),
        ]);
        setMovie(movieResponse.data);
        setShowtimes(showtimesResponse.data);
      } catch (error) {
        console.error('Error fetching movie details:', error);
      }
    };

    fetchMovie();
  }, [id]);

  if (!movie) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={4}>
          <Card>
            <Box
              component="img"
              src={movie.poster_url}
              alt={movie.title}
              sx={{
                width: '100%',
                height: 'auto',
                objectFit: 'cover',
              }}
            />
          </Card>
        </Grid>
        <Grid item xs={12} md={8}>
          <Box>
            <Typography variant="h3" gutterBottom>
              {movie.title}
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Rating value={movie.rating} readOnly precision={0.5} />
              <Typography variant="body1" sx={{ ml: 1 }}>
                {movie.rating}/10
              </Typography>
            </Box>
            <Box sx={{ mb: 2 }}>
              {movie.genres.map((genre) => (
                <Chip
                  key={genre}
                  label={genre}
                  sx={{ mr: 1, mb: 1 }}
                  color="primary"
                  variant="outlined"
                />
              ))}
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <AccessTime sx={{ mr: 1 }} />
              <Typography variant="body1">{movie.duration} phút</Typography>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <CalendarToday sx={{ mr: 1 }} />
              <Typography variant="body1">
                {new Date(movie.release_date).toLocaleDateString('vi-VN')}
              </Typography>
            </Box>
            <Typography variant="h6" gutterBottom>
              Mô tả
            </Typography>
            <Typography variant="body1" paragraph>
              {movie.description}
            </Typography>
            <Typography variant="h6" gutterBottom>
              Diễn viên
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mb: 2 }}>
              {movie.cast.map((actor) => (
                <Chip
                  key={actor.id}
                  label={actor.name}
                  variant="outlined"
                  size="small"
                />
              ))}
            </Box>
          </Box>
        </Grid>
      </Grid>

      <Divider sx={{ my: 4 }} />

      <Typography variant="h4" gutterBottom>
        Lịch chiếu
      </Typography>
      <Grid container spacing={2}>
        {showtimes.map((showtime) => (
          <Grid item xs={12} sm={6} md={4} key={showtime.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {new Date(showtime.start_time).toLocaleDateString('vi-VN')}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {new Date(showtime.start_time).toLocaleTimeString('vi-VN', {
                    hour: '2-digit',
                    minute: '2-digit',
                  })}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Phòng: {showtime.theater}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  Giá vé: {showtime.price.toLocaleString('vi-VN')} VNĐ
                </Typography>
                <Button
                  component={Link}
                  to={`/booking/${showtime.id}`}
                  variant="contained"
                  startIcon={<PlayArrow />}
                  fullWidth
                >
                  Đặt vé
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default MovieDetail; 