# %%
import os
import sys
import json
import pandas as pd
import numpy as np
from server.utils.extract_audio_functions import *

dataset = "./server/utils/dataset/spotify_songs.csv"
scaler = "./server/utils/scaler.joblib"
kmeans = "./server/utils/Kmeans.joblib"
histogram = "./server/utils/histogramas_acusticos.json"
funciones = "./server/utils/extract_audio_functions.py"

archivos = [dataset, scaler, kmeans, histogram, funciones]
directorios = ["./audios_temp", "./audios_wav", "./dataset"]

# METODOS UTILES PARA PROCESAR EL AUDIO 

# Funciones para usar al procesar
def extraer_mfcc_por_path(path, scaler) -> list[list[float]]:
    mfcc_test = extract_mfcc(path)
    return scaler.transform(mfcc_test)

def sacar_histograma_con_id(id, json_path="./server/utils/histogramas_acusticos.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(str(id))  
    except FileNotFoundError:
        print(f"[ERROR] Archivo {json_path} no encontrado.")
    except Exception as e:
        print(f"[ERROR] {e}")
def normalizar_distancias(recomendaciones):
    distancias = np.array([distancia for _, distancia in recomendaciones])
    min_d = np.min(distancias)
    max_d = np.max(distancias)
    similitudes = 1 - (distancias - min_d) / (max_d - min_d)

    recomendaciones_normalizadas = [
        (id, float(sim)) for (id, _), sim in zip(recomendaciones, similitudes)
    ]
    return recomendaciones_normalizadas

def insertar_csv(name, id, path_wav, csv_path="./dataset/spotify_songs.csv"):
    df = pd.read_csv(csv_path)

    nueva_fila = {
        'track_id': '',
        'track_artist': '',
        'track_name': name,
        'path_download': '',
        'id': str(id),
        'path_download_wav': "./"+path_wav.replace("\\", "/")

    }

    df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.to_csv(csv_path, index=False)

def max_key(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if not data:
            return 0

        ultima_clave = list(data.keys())[-1]
        return int(ultima_clave) if ultima_clave.isdigit() else 0

    except FileNotFoundError:
        return 0
    except Exception as e:
        print(f"Error al leer {json_path}: {e}")
        return 0

#--------------- TEST adudio MP3 --------------
#para poder hacer recomendacion de audio necesita path
# para el SQL 
def obtener_recomendaciones_por_audio_mp3(path_mp3,k=5,tipo="coseno"):
    """
        recibe un path mp3 : C:/dowload/coldplay.mpeg    ->  no guarda este audio lo deja como temp.wav

        retorna: dict -> key(id):value(score)

        Examples:
            Call function and add params to functions
            obtener_recomendaciones_por_audio_mp3(audio,k=5,tipo="manhatan")
    """
    directorio='./server/utils/audios_temp'
    
    path_salida = directorio+"/temp.wav"
    path_mp3_salida_wav=os.path.abspath(path_salida)
    #process
    transform_mp3_to_wav(path_mp3,path_mp3_salida_wav)
    scaler = cargar_objeto("./server/utils/scaler.joblib")
    kmeans_model = cargar_objeto("./server/utils/Kmeans.joblib")
    mfcc_normalizado=extraer_mfcc_por_path(path_mp3_salida_wav,scaler)

    histograma = histogram_audio(mfcc_normalizado, kmeans_model)

    if   tipo=="coseno":
        recomendaciones= knn_cosine(histograma, k=k)
    elif tipo=="manhatan":
        recomendaciones= knn_manhattan(histograma,k=k)
        recomendaciones= normalizar_distancias(recomendaciones)
    elif tipo=="euclidiana":
        recomendaciones= knn_lineal(histograma,k=k)
        recomendaciones= normalizar_distancias(recomendaciones)
    else :
        print("[ERROR] Tipo de distancia no soportada. Usando distancia euclidiana por defecto.")
        return None    
    recomendaciones_dict=dict(recomendaciones)
    return recomendaciones_dict

# review

# -- RECOMENDACION POR ID --      (el usuario selecciona un audio del dataset y debajo le salen musicas recomendadas k=5)

def obtener_recomendaciones_por_song_id(id,tipo=None,k=5):
    """
    Examples:
        Call function and add params to functions
        obtener_recomendaciones_por_song_id(2003, tipo="euclidiana", k=5)
    Return:
        - dict -> key:value
    """
    histograma=sacar_histograma_con_id(id)

    if   tipo=="coseno":
        recomendaciones= knn_cosine(histograma, k=k)
    elif tipo=="manhatan":
        recomendaciones= knn_manhattan(histograma,k=k)
        recomendaciones= normalizar_distancias(recomendaciones)
    elif tipo=="euclidiana":
        recomendaciones= knn_lineal(histograma,k=k)
        recomendaciones= normalizar_distancias(recomendaciones)
    else :
        print("[ERROR] Tipo de distancia no soportada. Usando distancia euclidiana por defecto.")
        return None   
        
    recomendaciones_dict=dict(recomendaciones)
    return recomendaciones_dict

# ---- INSERT AUDIO ---- 

def insert_audio(path_mp3: str, id: str = None, json_path: str = "./server/utils/histogramas_acusticos.json"):
    """
    recibe un path mp3 : C:/dowload/coldplay.mpeg 
    id : id del audio que se insertara 
    
    Inserta un nuevo audio: 
    extrae MFCC, genera su histograma y lo guarda en JSON, ademas guarda su nombre.wav.
    """
    name=os.path.basename(path_mp3)
    name=name.replace(".mpeg","")
    name_wav=os.path.join('audios_wav',name+".wav")
    path_wav = os.path.abspath(name_wav)

    #insert en audios_wav
    transform_mp3_to_wav(path_mp3, path_wav, tiempo_recorte=30)

    scaler = cargar_objeto("./scaler.joblib")
    kmeans_model = cargar_objeto("./Kmeans.joblib")

    mfcc = extract_mfcc(path_wav)
    mfcc_normalizado = scaler.transform(mfcc)
    hist = histogram_audio(mfcc_normalizado, kmeans_model)

    #insert histogramas
    try:
        with open("./server/utils/histogramas_acusticos.json") as f:
            diccionario = json.load(f)
    except FileNotFoundError:
        diccionario = {}
    diccionario[id] = hist.tolist()
    guardar_json(diccionario, json_path)

    #TODO :POR AHORA INSERT CSV   -> DEBE INSERTAR EN TABLA 
    insertar_csv(name,id,name_wav)

    print("[DEBUG]  isertado el audio ",name," id: ",id ,"correctamente")

##############################################################################################################
# CONSTRUCCION DEL INDICE INVERTIDO 
# construir_indice_invertido_por_hist()

# KNN CON INDICE INVERTIDO


# hist = sacar_histograma_con_id(2003)

# res = knn_index_inverted(hist,k=5)