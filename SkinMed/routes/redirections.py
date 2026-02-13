from flask import Blueprint, render_template, request
import os

from .Machine.ia_predictor import procesar_imagen_ia

redirections_bp = Blueprint('Redirections', __name__)

@redirections_bp.route('/Loginn')
def loginn():
    return render_template('login.html')

@redirections_bp.route('/machine', methods=['GET', 'POST'])
def machineIa():
    if request.method == 'POST':
        if 'imagen_piel' not in request.files:
            return "No se subió ninguna imagen"
            
        file = request.files['imagen_piel']
        if file.filename == '':
            return "No seleccionaste ningún archivo"

        if file:
            ruta_imagen = os.path.join('static/uploads', file.filename)
            file.save(ruta_imagen)

            resultados, recomendacion = procesar_imagen_ia(ruta_imagen)

            return render_template('diagnostico.html', 
                        resultados=resultados, 
                        recomendacion=recomendacion,
                        nombre_imagen=file.filename)

    return render_template('diagnostico.html')

