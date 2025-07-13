import json
import pandas as pd
import os

# Ruta del archivo original de histogramas
ruta_histograma_total = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/histogramas_acusticos.json"

# Directorio donde están los CSV y donde guardaremos los nuevos JSON
directorio_dataset = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/dataset"

directorio_hist = "C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/histogramas"

# Cargar todos los histogramas
with open(ruta_histograma_total, 'r') as f:
    histogramas_totales = json.load(f)

# Para cada subconjunto (ya creado como CSV)
for N in [10, 100, 500, 1000, 2000]:
    ruta_csv = os.path.join(directorio_dataset, f"spotify_songs_{N}.csv")
    ruta_json_salida = os.path.join(directorio_hist, f"hists_{N}.json")

    # Leer los IDs del CSV
    df = pd.read_csv(ruta_csv)
    ids_en_csv = df["id"].astype(str).tolist()

    # Filtrar los histogramas
    histogramas_filtrados = {
        k: v for k, v in histogramas_totales.items() if k in ids_en_csv
    }

    # Guardar el nuevo JSON
    with open(ruta_json_salida, 'w') as f_out:
        json.dump(histogramas_filtrados, f_out, indent=4)

    print(f" Histograma guardado: {ruta_json_salida} ({len(histogramas_filtrados)} entradas)")
