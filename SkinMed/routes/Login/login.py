from flask import render_template, redirect, url_for, request, session
from . import login_bp 

usuarioDoc = "Doctor Chuy"
contraseña = "doc.123"

@login_bp.route('/login', methods=['POST'])
def login():
    usuario_ingresado = request.form['username']
    contraseña_ingresada = request.form['password']

    if usuario_ingresado == usuarioDoc and contraseña_ingresada == contraseña:
 
        return redirect(url_for('Redirections.machineIa'))
    else:

        return redirect(url_for('Redirections.loginn')) 

