import React from 'react';
import { AppBar, Toolbar, Typography, Button, IconButton, Box, Menu, MenuItem } from '@mui/material';
import { Link } from 'react-router-dom';
import MovieIcon from '@mui/icons-material/Movie';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';

const pages = [
  { label: 'Home', path: '/' },
  { label: 'Movies', path: '/movies' },
  { label: 'Showtimes', path: '/showtimes' },
  { label: 'Booking', path: '/booking' }
];

const Navbar = () => {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleMenu = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <AppBar position="static" color="primary" enableColorOnDark>
      <Toolbar>
        <MovieIcon sx={{ mr: 1 }} />
        <Typography variant="h6" component={Link} to="/" sx={{ flexGrow: 1, color: 'inherit', textDecoration: 'none', fontWeight: 700 }}>
          Movie Theater
        </Typography>
        <Box sx={{ display: { xs: 'none', md: 'flex' } }}>
          {pages.map((page) => (
            <Button
              key={page.label}
              color="inherit"
              component={Link}
              to={page.path}
              sx={{ mx: 1 }}
            >
              {page.label}
            </Button>
          ))}
          <IconButton color="inherit" component={Link} to="/profile">
            <AccountCircle />
          </IconButton>
        </Box>
        {/* Mobile menu */}
        <Box sx={{ display: { xs: 'flex', md: 'none' } }}>
          <IconButton color="inherit" onClick={handleMenu}>
            <MenuIcon />
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
            transformOrigin={{ vertical: 'top', horizontal: 'right' }}
          >
            {pages.map((page) => (
              <MenuItem key={page.label} component={Link} to={page.path} onClick={handleClose}>
                {page.label}
              </MenuItem>
            ))}
            <MenuItem component={Link} to="/profile" onClick={handleClose}>
              Profile
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;