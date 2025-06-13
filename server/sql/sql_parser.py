from sqlglot import parse as parse_glot
from sqlglot.dialects.postgres import Postgres
from dataclasses import dataclass

@dataclass
class SQLParser:
    
    def parse(self, sql: str) -> dict[str, any]:
        exprs = parse_glot(sql, dialect=Postgres)
        for expr in exprs:
            metadata = {}
            # review the doc and create types for dml or ddl

s = SQLParser()
create_query = """
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255) UNIQUE,
        created_at TIMESTAMP DEFAULT NOW()
    );
    """
s.parse(create_query)