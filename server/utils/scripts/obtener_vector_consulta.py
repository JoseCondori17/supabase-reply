from server.utils.audio import (
    transform_mp3_to_wav,
    extraer_mfcc_por_path,
    cargar_objeto,
    histogram_audio
)
# Rutas
mp3_path = 'D:/USUARIO/Downloads/test_audio.mpeg'
wav_path = 'C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/audios_temp/temp.wav'

# Convertir a wav
transform_mp3_to_wav(mp3_path, wav_path)

# Cargar modelos
scaler = cargar_objeto("C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/scaler.joblib")
kmeans = cargar_objeto("C:/Users/USUARIO/PycharmProjects/supabase-reply/server/utils/Kmeans.joblib")

# MFCCs
mfcc = extraer_mfcc_por_path(wav_path, scaler)

# Histograma
vector_del_test_audio = histogram_audio(mfcc, kmeans).tolist()
print(vector_del_test_audio)
