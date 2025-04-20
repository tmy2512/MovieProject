import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Grid, Card, Button, Box, Typography, Chip, Paper, CardMedia, CardContent } from '@mui/material';
import styled from 'styled-components';
import axios from 'axios';

const MovieDetailContainer = styled(Container)`
  padding: 2rem 0;
`;

const MoviePoster = styled.img`
  width: 100%;
  height: auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const MovieTitle = styled(Typography)`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: #333;
`;

const MovieInfo = styled(Box)`
  margin-bottom: 1.5rem;
`;

const InfoLabel = styled.span`
  font-weight: bold;
  margin-right: 0.5rem;
`;

const GenreTag = styled(Chip)`
  margin: 0.25rem;
`;

const ActorCard = styled(Card)`
  margin: 1rem;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
`;

const ActorImage = styled(CardMedia)`
  height: 200px;
  object-fit: cover;
`;

const TrailerContainer = styled(Paper)`
  margin: 2rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
`;

const MovieDetail = () => {
  const { id } = useParams();
  const [movie, setMovie] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_MOVIE_SERVICE_URL}/api/movies/${id}/`);
        setMovie(response.data);
        setLoading(false);
      } catch (err) {
        setError('Failed to fetch movie details');
        setLoading(false);
      }
    };

    fetchMovie();
  }, [id]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>{error}</div>;
  if (!movie) return <div>Movie not found</div>;

  return (
    <MovieDetailContainer>
      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <MoviePoster src={movie.poster_url} alt={movie.title} />
        </Grid>
        <Grid item xs={12} md={8}>
          <MovieTitle variant="h1">{movie.title}</MovieTitle>
          <MovieInfo>
            <Typography>
              <InfoLabel>Rating:</InfoLabel>
              <span>{movie.rating}/10</span>
            </Typography>
            <Typography>
              <InfoLabel>Release Date:</InfoLabel>
              <span>{new Date(movie.release_date).toLocaleDateString()}</span>
            </Typography>
            <Typography>
              <InfoLabel>Duration:</InfoLabel>
              <span>{Math.floor(movie.duration / 60)}h {movie.duration % 60}m</span>
            </Typography>
            <Typography>
              <InfoLabel>Genres:</InfoLabel>
              {movie.genres.map(genre => (
                <GenreTag key={genre.id} label={genre.name} />
              ))}
            </Typography>
          </MovieInfo>
          <Typography paragraph>{movie.description}</Typography>
          <Button variant="contained" href={movie.trailer_url} target="_blank">
            Watch Trailer
          </Button>
        </Grid>
      </Grid>

      <TrailerContainer>
        <Typography variant="h3">Trailer</Typography>
        <Box sx={{ position: 'relative', paddingTop: '56.25%' }}>
          <iframe
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              border: 0
            }}
            src={movie.trailer_url.replace('watch?v=', 'embed/')}
            title="Movie Trailer"
            allowFullScreen
          />
        </Box>
      </TrailerContainer>

      <Typography variant="h3">Cast</Typography>
      <Grid container spacing={2}>
        {movie.actors.map(actor => (
          <Grid item xs={12} sm={6} md={3} key={actor.id}>
            <ActorCard>
              <ActorImage component="img" image={actor.profile_picture} alt={actor.name} />
              <CardContent>
                <Typography variant="h6">{actor.name}</Typography>
              </CardContent>
            </ActorCard>
          </Grid>
        ))}
      </Grid>
    </MovieDetailContainer>
  );
};

export default MovieDetail; 