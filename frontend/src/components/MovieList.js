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

const SAMPLE_MOVIES = [
  {
    id: 1,
    title: "Sample Movie",
    description: "This is a sample movie description. Enjoy the show!",
    duration: 120,
    release_date: "2024-01-01",
    rating: 8.5,
    genre: "Action",
    director: "Jane Doe",
    cast: "John Smith, Alice Johnson",
    poster_url: "https://via.placeholder.com/400x600?text=Sample+Movie"
  }
  // You can add more sample movies here if you want
];

const MovieList = () => {
  const [movies, setMovies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        const response = await axios.get('http://localhost:8001/movies/');
        setMovies(response.data);
      } catch (error) {
        setError('Error fetching movies');
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, []);

  // Use sample data if movies is empty after loading
  const displayMovies = (!loading && Array.isArray(movies) && movies.length === 0)
    ? SAMPLE_MOVIES
    : (Array.isArray(movies) ? movies : []);

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

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Now Showing
      </Typography>
      <Grid container spacing={4}>
        {displayMovies.map((movie) => (
          <Grid item key={movie.id} xs={12} sm={6} md={4}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column', transition: '0.3s', '&:hover': { boxShadow: 6 } }}>
              <CardMedia
                component="img"
                height="400"
                image={movie.poster_url}
                alt={movie.title}
              />
              <CardContent>
                <Typography gutterBottom variant="h5" component="div">
                  {movie.title}
                </Typography>
                <Box sx={{ mb: 1 }}>
                  <Chip label={movie.genre} color="primary" sx={{ mr: 1 }} />
                  <Chip label={`Rating: ${movie.rating}`} sx={{ mr: 1 }} />
                  <Chip label={new Date(movie.release_date).getFullYear()} />
                </Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                  {movie.description.substring(0, 100)}...
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