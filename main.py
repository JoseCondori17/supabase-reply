from server.engine.executor import PinPom
from server.sql.sql_parser import SQLParser
from server.utils.scripts.subset_context import switch_subset
from server.utils.audio import preparar_audio_para_busqueda

sq = SQLParser()
create_db = "CREATE DATABASE ecommerce"
create_schema = "CREATE SCHEMA product"
create_query = """
    CREATE DATABASE university;
    CREATE SCHEMA course;
    CREATE TABLE users (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE,
        created_at TIMESTAMP
    );

    CREATE TABLE book (
        id UUID PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        code VARCHAR(255) UNIQUE,
        created_at TIMESTAMP
    );

    CREATE TABLE author (
        id UUID PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        year DATE UNIQUE,
        created_at TIMESTAMP
    );

    CREATE SCHEMA employee;
    CREATE SCHEMA teach;

    CREATE DATABASE ecommerce;
    CREATE SCHEMA policia;
    CREATE SCHEMA municipio;
    """
drop_table = "DROP TABLE product"
drop_db = "DROP DATABASE users"
create_index = "CREATE INDEX pk_prod ON product USING BTREE(name);"
select_from = "SELECT * FROM users WHERE name='Carlos' and last_name = 'Paucar'"
select_from_le = "SELECT name FROM users WHERE age < 21 and age >= 15 and name = 'Juan'"
select_from_btw = "SELECT name FROM users WHERE age BETWEEN 21 AND 40"
insert_into = """
    INSERT INTO users VALUES
    (1, 'Juan Pérez', 'juan@example.com', '2025-06-20 17:30:00'),
    (2, 'María López', 'maria@example.com', '2025-06-20 17:30:01'),
    (3, 'Carlos Gómez', 'carlos@example.com', '2025-06-20 17:30:02'),
    (4, 'Ana Rodríguez', 'ana@example.com', '2025-06-20 17:30:03'),
    (5, 'Luis Fernández', 'luis@example.com', '2025-06-20 17:30:04'),
    (6, 'Sofía Martínez', 'sofia@example.com', '2025-06-20 17:30:05'),
    (7, 'Pedro Sánchez', 'pedro@example.com', '2025-06-20 17:30:06'),
    (8, 'Elena Díaz', 'elena@example.com', '2025-06-20 17:30:07'),
    (9, 'Miguel Ruiz', 'miguel@example.com', '2025-06-20 17:30:08'),
    (10, 'Laura Hernández', 'laura@example.com', '2025-06-20 17:30:09');
"""
create_uni = """
    CREATE DATABASE university;
    CREATE SCHEMA course;
    CREATE TABLE music_10(
        id INT PRIMARY KEY,
        track_id VARCHAR(22),
        track_album_id VARCHAR(22),
        track_artist VARCHAR(36),
        track_name VARCHAR(94),
        playlist_genre VARCHAR(5),
        playlist_subgenre VARCHAR(25),
        path_download_wav VARCHAR(190),
        lyrics VARCHAR(20000),
        song_url VARCHAR(54),
        album_url VARCHAR(54),
        artist_url VARCHAR(54),
        album_name VARCHAR(145),
        album_date DATE,
        image_url VARCHAR(65)
    );

    CREATE TABLE music_100(
        id INT PRIMARY KEY,
        track_id VARCHAR(22),
        track_album_id VARCHAR(22),
        track_artist VARCHAR(36),
        track_name VARCHAR(94),
        playlist_genre VARCHAR(5),
        playlist_subgenre VARCHAR(25),
        path_download_wav VARCHAR(190),
        lyrics VARCHAR(20000),
        song_url VARCHAR(54),
        album_url VARCHAR(54),
        artist_url VARCHAR(54),
        album_name VARCHAR(145),
        album_date DATE,
        image_url VARCHAR(65)
    );
    
    CREATE TABLE music_500(
        id INT PRIMARY KEY,
        track_id VARCHAR(22),
        track_album_id VARCHAR(22),
        track_artist VARCHAR(36),
        track_name VARCHAR(94),
        playlist_genre VARCHAR(5),
        playlist_subgenre VARCHAR(25),
        path_download_wav VARCHAR(190),
        lyrics VARCHAR(20000),
        song_url VARCHAR(54),
        album_url VARCHAR(54),
        artist_url VARCHAR(54),
        album_name VARCHAR(145),
        album_date DATE,
        image_url VARCHAR(65)
    );
    
    CREATE TABLE music_1000(
        id INT PRIMARY KEY,
        track_id VARCHAR(22),
        track_album_id VARCHAR(22),
        track_artist VARCHAR(36),
        track_name VARCHAR(94),
        playlist_genre VARCHAR(5),
        playlist_subgenre VARCHAR(25),
        path_download_wav VARCHAR(190),
        lyrics VARCHAR(20000),
        song_url VARCHAR(54),
        album_url VARCHAR(54),
        artist_url VARCHAR(54),
        album_name VARCHAR(145),
        album_date DATE,
        image_url VARCHAR(65)
    );
    
    CREATE TABLE music_2000(
        id INT PRIMARY KEY,
        track_id VARCHAR(22),
        track_album_id VARCHAR(22),
        track_artist VARCHAR(36),
        track_name VARCHAR(94),
        playlist_genre VARCHAR(5),
        playlist_subgenre VARCHAR(25),
        path_download_wav VARCHAR(190),
        lyrics VARCHAR(20000),
        song_url VARCHAR(54),
        album_url VARCHAR(54),
        artist_url VARCHAR(54),
        album_name VARCHAR(145),
        album_date DATE,
        image_url VARCHAR(65)
    );

"""
user_table = """
    CREATE TABLE users (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE,
        created_at TIMESTAMP
    );
"""
select_all = "SELECT track_name, path_download_wav FROM music WHERE id = 1439"
delete_from = "DELETE FROM users WHERE age < 21;"

#print(s.parse(query_aud)[0].args)
#print(s._parse_select_from(s.parse(query_aud)[0]))
copy_query = """
    COPY music_10
    FROM 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_10.csv'
    DELIMITER ',';
    
    COPY music_100
    FROM 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_100.csv'
    DELIMITER ',';
    
    COPY music_500
    FROM 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_500.csv'
    DELIMITER ',';
    
    COPY music_1000
    FROM 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_1000.csv'
    DELIMITER ',';
    
    COPY music_2000
    FROM 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs_2000.csv'
    DELIMITER ',';
"""
query_music_cosine = """
    SELECT track_name, path_download_wav
    FROM music_2000
    WHERE path_download_wav <#> 'D:/USUARIO/Downloads/test_audio.mpeg'
    LIMIT 8;
"""
query_in = """
    SELECT *
    FROM music
    WHERE id IN (1,4,6,7)
"""
query_aud = """
    EXPLAIN ANALYZE
    SELECT id, track_name, lyrics
    FROM music_2000
    WHERE lyrics @@ 'dance baby love' AND NOT lyrics @@ 'dance all night'
    LIMIT 5;
"""

create_aud_index = """
    CREATE INDEX idx_lyrics ON music_2000 USING spimi(lyrics);
"""

dbms = PinPom()
result = dbms.execute(query_aud)
for r in result:
    print(r)

#print(dbms.index_service.get_indexes("university", "course", "users"))
#print(sq._parse_create_index(sq.parse(create_index)[0]))
#c = dbms.catalog_service.load_catalog()
#print(c)
#dbms.execute(create_query)
#print(dbms.database_service.get_databases_name())
#print(dbms.catalog_service.get_databases())