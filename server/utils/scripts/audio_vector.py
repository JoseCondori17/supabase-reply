import psycopg2
import json

# Cargar histogramas ya calculados
with open("C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/histogramas_acusticos.json", "r", encoding="utf-8") as f:
    histogramas = json.load(f)

# Conexión a PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# Puedes cambiar esto por music_10, music_100, etc.
tabla = "music_total"

for id_str, vector in histogramas.items():
    id_int = int(id_str)
    vector_json = json.dumps(vector)
    cur.execute(f"""
        UPDATE {tabla}
        SET audio_vector = %s
        WHERE id = %s
    """, (vector_json, id_int))

conn.commit()
cur.close()
conn.close()
print(" Columnas audio_vector rellenadas.")
