from server.engine.executor import PinPom
from server.sql.sql_parser import SQLParser

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
    CREATE TABLE users (
        id INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE,
        created_at TIMESTAMP
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
select_all = "SELECT email FROM users;"
delete_from = "DELETE FROM users WHERE age < 21;"
query_aud = """
    SELECT title, artist, lyric
    FROM Audio
    WHERE lyric @@ 'amor en tiempos de guerra'
    LIMIT 10;
"""
#print(s.parse(query_aud)[0].args)
#print(s._parse_select_from(s.parse(query_aud)[0]))
dbms = PinPom()
dbms.execute("SELECT name FROM users WHERE name='Juan Pérez'")
#print(dbms.index_service.get_indexes("university", "course", "users"))
#print(sq._parse_create_index(sq.parse(create_index)[0]))
#c = dbms.catalog_service.load_catalog()
#print(c)
#dbms.execute(create_query)
#print(dbms.database_service.get_databases_name())
#print(dbms.catalog_service.get_databases())