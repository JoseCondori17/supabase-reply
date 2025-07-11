from server.utils.extract_audio_functions import *
import pandas as pd
import json

dataset_file = "../../../utils/spotify_songs.csv"
scaler_file = "../../../utils/scaler.joblib"
kmeans_file = "../../../utils/Kmeans.joblib"
histogram_file = "../../../utils/histogramas_acusticos.json"
audio_dir = "../../../audio"

def extraer_mfcc_por_path(path, scaler) -> list[list[float]]:
    mfcc_test = extract_mfcc(path)
    return scaler.transform(mfcc_test)

##########################################################################################
#para poder hacer recomendacion de audio necesita path
# para el SQL
def obtener_recomendaciones_por_audio_mp3(path_mp3,k=5,tipo="coseno"):
    """
        recibe un path mp3 : C:/dowload/coldplay.mpeg    ->  no guarda este audio lo deja como temp.wav
        retorna: array [(id1:score1),(id2:score2),...]
    """
    directorio=audio_dir
    
    path_salida = directorio+"/temp.wav"
    path_mp3_salida_wav=os.path.abspath(path_salida)
    
    #process
    transform_mp3_to_wav(path_mp3,path_mp3_salida_wav)
    scaler = cargar_objeto(scaler_file)
    kmeans_model = cargar_objeto(kmeans_file)
    mfcc_normalizado=extraer_mfcc_por_path(path_mp3_salida_wav,scaler)

    histograma = histogram_audio(mfcc_normalizado, kmeans_model)

    if   tipo=="coseno":
        recomendaciones= knn_cosine(histograma, k=k)
    elif tipo=="manhatan":
        recomendaciones= knn_manhattan(histograma,k=k)
    else : 
        recomendaciones= knn_lineal(histograma,k=k) # distancia euclidiana   
    recomendaciones_dict=dict(recomendaciones)
    return recomendaciones_dict

##########################################################################################
# -- RECOMENDACION POR ID --      
# (el usuario selecciona un audio del dataset y debajo le salen musicas recomendadas k=5)
def sacar_histograma_con_id(id, json_path="../../../utils/histogramas_acusticos.json"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get(str(id))  
    except FileNotFoundError:
        print(f"[ERROR] Archivo {json_path} no encontrado.")
    except Exception as e:
        print(f"[ERROR] {e}")
    
def obtener_recomendaciones_por_song_id(id,tipo,k=5):
    histograma=sacar_histograma_con_id(id)

    if   tipo=="coseno":
        recomendaciones= knn_cosine(histograma, k=k)
    elif tipo=="manhatan":
        recomendaciones= knn_manhattan(histograma,k=k)
    else : 
        recomendaciones= knn_lineal(histograma,k=k) # distancia euclidiana   
    recomendaciones_dict=dict(recomendaciones)
    return recomendaciones_dict

##########################################################################################
# ---- INSERT AUDIO ---- 
def insertar_csv(name, id, path_wav, csv_path="../../../utils/spotify_songs.csv"):
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

def insert_audio(path_mp3: str, id: str = None, json_path: str = "../../../utils/histogramas_acusticos.json"):
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

    scaler = cargar_objeto(scaler_file)
    kmeans_model = cargar_objeto(kmeans_file)

    mfcc = extract_mfcc(path_wav)
    mfcc_normalizado = scaler.transform(mfcc)
    hist = histogram_audio(mfcc_normalizado, kmeans_model)

    #insert histogramas
    try:
        with open(histogram_file) as f:
            diccionario = json.load(f)
    except FileNotFoundError:
        diccionario = {}
    diccionario[id] = hist.tolist()
    guardar_json(diccionario, json_path)

    #TODO :POR AHORA INSERT CSV   -> DEBE INSERTAR EN TABLA 
    insertar_csv(name,id,name_wav)

    print("[DEBUG]  isertado el audio ",name," id: ",id ,"correctamente")

