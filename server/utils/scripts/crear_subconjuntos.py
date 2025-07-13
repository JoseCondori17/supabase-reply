import pandas as pd
import os

# Ruta del archivo base
csv_original = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset/spotify_songs.csv"
output_dir = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset"

# Tamaños de subconjuntos
subconjuntos = [10, 100, 500, 1000, 2000]

# Cargar el dataset original
df = pd.read_csv(csv_original)

# Generar y guardar los subconjuntos
for N in subconjuntos:
    subset = df.head(N)
    output_path = os.path.join(output_dir, f"spotify_songs_{N}.csv")
    subset.to_csv(output_path, index=False)
    print(f" Subconjunto de {N} canciones guardado en: {output_path}")
