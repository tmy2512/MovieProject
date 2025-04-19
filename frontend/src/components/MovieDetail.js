import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  Box,
  Chip,
} from '@mui/material';
import axios from 'axios';

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await axios.get(`http://localhost:8001/movies/${id}/`);
        setMovie(response.data);
      } catch (error) {
        console.error('Error fetching movie:', error);
      }
    };

    fetchMovie();
  }, [id]);

  if (!movie) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Card>
        <Grid container>
          <Grid item xs={12} md={4}>
            <CardMedia
              component="img"
              height="600"
              image={movie.poster_url}
              alt={movie.title}
            />
          </Grid>
          <Grid item xs={12} md={8}>
            <CardContent>
              <Typography variant="h3" component="h1" gutterBottom>
                {movie.title}
              </Typography>
              <Box sx={{ mb: 2 }}>
                <Chip label={movie.genre} color="primary" sx={{ mr: 1 }} />
                <Chip label={`${movie.duration} min`} sx={{ mr: 1 }} />
                <Chip label={`Rating: ${movie.rating}`} />
              </Box>
              <Typography variant="h6" gutterBottom>
                Director: {movie.director}
              </Typography>
              <Typography variant="body1" paragraph>
                {movie.description}
              </Typography>
              <Typography variant="h6" gutterBottom>
                Cast:
              </Typography>
              <Typography variant="body1" paragraph>
                {movie.cast}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Release Date: {new Date(movie.release_date).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Grid>
        </Grid>
      </Card>
    </Container>
  );
};

export default MovieDetail; 