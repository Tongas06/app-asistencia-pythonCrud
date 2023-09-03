from datetime import datetime
from flask import Flask, request, render_template, redirect, url_for
from __main__ import app
from .models import db, Asistencia, Curso, Estudiante
from .login import obtener_id_preceptor

@app.route('/registrar_asistencia', methods=['GET', 'POST'])
def registrar_asistencia():
    preceptor = obtener_id_preceptor()
    if not preceptor:
        return redirect(url_for('login'))

    curso_id = request.args.get('curso_id', None)
    if not curso_id:
        return redirect(url_for('inicio'))

    curso = Curso.query.filter_by(id=curso_id, idpreceptor=preceptor.id).first()
    if not curso:
        return redirect(url_for('inicio'))
    if request.method == 'POST':
        clase = int(request.form['clase'])
        fecha = request.form['fecha']
        for estudiante in curso.estudiantes:
            # Obtener los datos del formulario y guardar la asistencia en la base de datos
            asistencia = request.form.get(f'asistencia_{estudiante.id}')
            justificacion = request.form.get(f'justificacion_{estudiante.id}')
            
            fecha_a = datetime.strptime(fecha, "%Y-%m-%d")
            dia, mes, ano = fecha_a.day, fecha_a.month, fecha_a.year
            fecha_bien = f"{dia}/{mes}/{ano}"

            registro_existente = Asistencia.query.filter_by(idestudiante=estudiante.id, fecha=fecha_bien, codigoclase=clase).first()
            if registro_existente:
                # Si el registro ya existe, retorna un mensaje de error
                return "Ya se ha registrado la asistencia para este estudiante, aula y tipo de clase en la fecha especificada"
            
            else:


                registro_asistencia = Asistencia(
                    idestudiante=estudiante.id,
                    fecha=fecha_bien,
                    codigoclase=clase,
                    asistio=asistencia,
                    justificacion=justificacion if asistencia == 'n' else ''
                )
                db.session.add(registro_asistencia)
                db.session.commit()
                
        return redirect(url_for('inicio'))

    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
    return render_template('asistencia.html', curso=curso, estudiantes=estudiantes)