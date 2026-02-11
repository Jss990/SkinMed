from tf_keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

def procesar_imagen_ia(ruta_imagen):
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(ruta_imagen).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    
    resultados_completos = []
    for i in range(len(class_names)):
        nombre_clase = class_names[i].strip()[2:] 
        porcentaje = round(prediction[0][i] * 100, 2)
        
        resultados_completos.append({
            'enfermedad': nombre_clase,
            'confianza': porcentaje
        })
    
    resultados_completos = sorted(resultados_completos, key=lambda x: x['confianza'], reverse=True)
    enfermedad_principal = resultados_completos[0]['enfermedad']
    recomendacion = f"Se ha detectado una alta coincidencia visual con {enfermedad_principal}. Se sugiere agendar cita presencial para confirmación clínica."

    return resultados_completos, recomendacion