from server.sql.sql_parser import SQLParser
from server.engine.executor import PinPom

s = SQLParser()
create_db = "CREATE DATABASE ecommerce"
create_schema = "CREATE SCHEMA product"
create_query = """
    CREATE DATABASE university;
    CREATE SCHEMA course;
    CREATE TABLE users (
        UUID INT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE,
        created_at TIMESTAMP
    );
    """
    
drop_table = "DROP TABLE product"
drop_db = "DROP DATABASE users"
create_index = "CREATE INDEX pk_prod ON product USING BTREE(name);"
select_from = "SELECT * FROM users WHERE name='Carlos' and last_name = 'Paucar'"
select_from_le = "SELECT name FROM users WHERE age < 21 and age >= 15"
select_from_btw = "SELECT name FROM users WHERE age BETWEEN 21 AND 40"
insert_into = "INSERT INTO users VALUES (1, 'Juan', 'Pedro'), (2, 'Mar', 'Lima');"
delete_from = "DELETE FROM users WHERE age < 21;"
#s.parse(select_from)

dbms = PinPom()
dbms.execute(create_query)