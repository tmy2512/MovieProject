-- Insert sample movies
INSERT INTO movies_movie (id, title, description, release_date, duration, rating, poster_url, trailer_url, created_at, updated_at)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', 'The Dark Knight', 'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.', '2008-07-18', 152, 9.0, 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg', 'https://www.youtube.com/watch?v=EXeTwQWrcwY', NOW(), NOW()),
    
    ('550e8400-e29b-41d4-a716-446655440001', 'Inception', 'A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.', '2010-07-16', 148, 8.8, 'https://m.media-amazon.com/images/M/MV5BMjAxMzY3NjcxNF5BMl5BanBnXkFtZTcwNTI5OTM0Mw@@._V1_.jpg', 'https://www.youtube.com/watch?v=YoHD9XEInc0', NOW(), NOW()),
    
    ('550e8400-e29b-41d4-a716-446655440002', 'Interstellar', 'A team of explorers travel through a wormhole in space in an attempt to ensure humanity''s survival.', '2014-11-07', 169, 8.6, 'https://m.media-amazon.com/images/M/MV5BZjdkOTU3MDktN2IxOS00OGEyLWFmMjktY2FiMmZkNWIyODZiXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg', 'https://www.youtube.com/watch?v=zSWdZVtXT7E', NOW(), NOW());

-- Insert sample genres
INSERT INTO movies_genre (id, name, created_at, updated_at)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440003', 'Action', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440004', 'Sci-Fi', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440005', 'Thriller', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440006', 'Drama', NOW(), NOW());

-- Insert movie-genre relationships
INSERT INTO movies_movie_genres (movie_id, genre_id)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440003'),
    ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440005'),
    ('550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440004'),
    ('550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440005'),
    ('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440004'),
    ('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440006');

-- Insert sample actors
INSERT INTO movies_actor (id, name, profile_picture, created_at, updated_at)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440007', 'Christian Bale', 'https://m.media-amazon.com/images/M/MV5BMTkxNzA0NDYxNF5BMl5BanBnXkFtZTcwNTIxMzUyMg@@._V1_.jpg', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440008', 'Heath Ledger', 'https://m.media-amazon.com/images/M/MV5BMTI2NTY0NzA4MF5BMl5BanBnXkFtZTYwMjE1MDE0._V1_.jpg', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440009', 'Leonardo DiCaprio', 'https://m.media-amazon.com/images/M/MV5BMjI0MTg3MzI0M15BMl5BanBnXkFtZTcwMzQyODU2Mw@@._V1_.jpg', NOW(), NOW()),
    ('550e8400-e29b-41d4-a716-446655440010', 'Matthew McConaughey', 'https://m.media-amazon.com/images/M/MV5BMTg0MDc3ODUwOV5BMl5BanBnXkFtZTcwMTk0NjQyMg@@._V1_.jpg', NOW(), NOW());

-- Insert movie-actor relationships
INSERT INTO movies_movie_actors (movie_id, actor_id)
VALUES 
    ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440007'),
    ('550e8400-e29b-41d4-a716-446655440000', '550e8400-e29b-41d4-a716-446655440008'),
    ('550e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440009'),
    ('550e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440010'); 