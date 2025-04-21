import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Button,
  CircularProgress,
  Alert,
  Chip,
  Box
} from '@mui/material';
import { Link } from 'react-router-dom';
import axios from 'axios';

const MovieList = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get('http://localhost:8001/api/movies/', {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          }
        });
        setMovies(response.data);
        setError(null);
      } catch (error) {
        console.error('Error fetching movies:', error);
        setError('Error fetching movies. Please try again later.');
        setMovies([]);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, textAlign: 'center' }}>
        <CircularProgress />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="error">{error}</Alert>
      </Container>
    );
  }

  if (!movies || movies.length === 0) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4 }}>
        <Alert severity="info">No movies available at the moment.</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Now Showing
      </Typography>
      <Grid container spacing={4}>
        {movies.map((movie) => (
          <Grid item key={movie.id} xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: '0.3s', '&:hover': { boxShadow: 6 } }}>
              <CardMedia
                component="img"
                height="400"
                image={movie.poster_url || 'https://via.placeholder.com/400x600?text=No+Poster'}
                alt={movie.title}
                onError={(e) => {
                  e.target.src = 'https://via.placeholder.com/400x600?text=No+Poster';
                }}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  {movie.title}
                </Typography>
                <Box sx={{ mb: 1 }}>
                  {movie.genre.split(',').map((g, index) => (
                    <Chip 
                      key={index} 
                      label={g.trim()} 
                      color="primary" 
                      sx={{ mr: 1, mb: 1 }} 
                    />
                  ))}
                  <Chip label={`Rating: ${movie.rating}`} sx={{ mr: 1, mb: 1 }} />
                  <Chip label={new Date(movie.release_date).getFullYear()} sx={{ mb: 1 }} />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {movie.description.length > 150 
                    ? `${movie.description.substring(0, 150)}...` 
                    : movie.description}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  <strong>Director:</strong> {movie.director}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  <strong>Cast:</strong> {movie.cast}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  <strong>Duration:</strong> {movie.duration} min
                </Typography>
                <Button
                  component={Link}
                  to={`/movies/${movie.id}`}
                  variant="contained"
                  color="primary"
                  sx={{ mt: 2 }}
                  fullWidth
                >
                  View Details
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default MovieList;