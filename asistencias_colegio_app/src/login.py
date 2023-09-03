from flask import Flask, request, render_template, redirect, url_for, session
import hashlib
from __main__ import app
from src.models import db, Preceptor, Padre

def check_pass(password):
    return hashlib.md5(bytes(password, encoding='utf-8')).hexdigest()

def authenticate(email, password, tipo_usuario):
    usuario = None
    if tipo_usuario == 'preceptor':
        usuario = Preceptor.query.filter_by(correo=email).first()
    elif tipo_usuario == 'padre':
        usuario = Padre.query.filter_by(correo=email).first()
    if usuario and usuario.clave == check_pass(password):
        return usuario
    return None


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        user = authenticate(email, password, user_type)
        if user:
            session['user_id'] = user.id
            session['user_type'] = user_type
            return redirect(url_for('inicio'))
        else:
            return "Credenciales incorrectas"
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    tipo_usuario = session.get('user_type', None)
    if not tipo_usuario:
        return redirect(url_for('login'))
    preceptor_actual = None
    cursos = None
    if tipo_usuario == 'preceptor':
        preceptor_actual = obtener_id_preceptor()
        cursos = preceptor_actual.cursos
    return render_template('inicio.html', tipo_usuario=tipo_usuario, cursos=cursos)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

def obtener_id_preceptor():
    if 'user_id' not in session:
        return None
    return Preceptor.query.get(session['user_id'])