from tf_keras.models import load_model
from PIL import Image, ImageOps
import numpy as np

np.set_printoptions(suppress=True)
model = load_model("keras_model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()

RECOMENDACIONES_CLINICAS = {
    "acne": "Tratamiento de primera línea incluye retinoides tópicos (ej. adapaleno) y peróxido de benzoilo. En casos moderados/severos se evalúan antibióticos orales (ej. doxiciclina) o isotretinoína. (Literatura clínica de referencia).",
    "actinic keratosis": "Condición precancerosa. Las opciones estándar incluyen crioterapia con nitrógeno líquido, quimioterapia tópica (5-fluorouracilo al 5%) o moduladores inmunológicos (imiquimod). Requiere vigilancia.",
    "bullous": "Las enfermedades ampollares autoinmunes (ej. pénfigo) son urgencias relativas. El tratamiento angular incluye corticosteroides sistémicos (prednisona) y agentes ahorradores de esteroides. Requiere biopsia urgente.",
    "cancer de piel": "Requiere biopsia excisional o por sacabocados urgente. El tratamiento de elección suele ser la escisión quirúrgica con márgenes clínicos o cirugía micrográfica de Mohs. La derivación oncológica es prioritaria.",
    "eczema": "El manejo pilar consiste en la reparación de la barrera cutánea con emolientes y control de brotes con corticosteroides tópicos. Alternativas incluyen inhibidores de calcineurina (tacrolimus).",
    "lichen": "Para el liquen plano, la terapia de primera línea son los corticosteroides tópicos de alta potencia o intralesionales. Casos generalizados pueden requerir fototerapia o esteroides sistémicos.",
    "vasculitis": "Requiere descartar afectación sistémica (renal, pulmonar). El tratamiento abarca desde reposo absoluto y elevación, hasta corticosteroides sistémicos e inmunosupresores en casos severos.",
    "warts": "Tratamientos de primera línea incluyen queratolíticos (ácido salicílico al 17-40%) y crioterapia con nitrógeno líquido. Lesiones recalcitrantes pueden requerir inmunoterapia intralesional."
}

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
    clave_busqueda = enfermedad_principal.lower()
    texto_medico = ""

    for key, value in RECOMENDACIONES_CLINICAS.items():
        if key in clave_busqueda:
            texto_medico = value
            break
            
    
    if not texto_medico:
        texto_medico = "Se requiere evaluación clínica para determinar el tratamiento de soporte específico."

    # 3. ARMADO DEL REPORTE FINAL
    recomendacion = (
        f"Diagnóstico Principal Probable: {enfermedad_principal}"
        f"{texto_medico}"
    )

    return resultados_completos, recomendacion