from datetime import datetime
from flask import Flask, request, render_template
from __main__ import app
from .models import db, Asistencia, Estudiante


def listado(curso_id, fecha, codigoclase):
    fecha_a = datetime.strptime(fecha, "%Y-%m-%d")
    dia, mes, ano = fecha_a.day, fecha_a.month, fecha_a.year
    fecha_bien = f"{dia}/{mes}/{ano}"
    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).all()

    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).all()

    lista = []

    for estudiante in estudiantes:
        asistencia = Asistencia.query.filter_by(idestudiante=estudiante.id, fecha=fecha_bien, codigoclase=codigoclase).first()

        if asistencia:
            print(f"Asistencia: {asistencia.asistio}")
        else:
            print("Asistencia no encontrada")
        
        lista.append({
            'nombre': estudiante.nombre,
            'apellido': estudiante.apellido,
            'asistio': asistencia.asistio if asistencia else ''
        })
    
    lista.sort(key=lambda x: (x['apellido'], x['nombre']))
    return lista

@app.route('/listado_asistencia', methods=['GET', 'POST'])
def listado_asistencia():
    curso_id = int(request.args.get('curso_id'))
    
    if request.method == 'POST':
        fecha = request.form['fecha']
        codigoclase = request.form['codigoclase']
        
        lista = listado(curso_id, fecha, codigoclase)
        
        return render_template('listado.html', lista=lista, curso_id=curso_id)
    
    return render_template('listado_form.html', curso_id=curso_id)