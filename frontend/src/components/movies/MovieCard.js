import { Card, CardMedia, CardContent, Typography, Button } from '@mui/material';
import { Link } from 'react-router-dom';

function MovieCard({ movie }) {
  return (
    <Card>
      <CardMedia component="img" height="350" image={movie.poster_url} alt={movie.title} />
      <CardContent>
        <Typography variant="h6">{movie.title}</Typography>
        <Typography variant="body2" color="text.secondary">{movie.genre}</Typography>
        <Button component={Link} to={`/movies/${movie.id}`} variant="contained" fullWidth sx={{ mt: 2 }}>
          View Details
        </Button>
      </CardContent>
    </Card>
  );
}

export default MovieCard;