from flask import Flask, request, render_template, redirect, url_for
from __main__ import app
from .login import obtener_id_preceptor
from .models import db, Asistencia, Curso, Estudiante


@app.route('/informe', methods=['GET'])
def informe():

    preceptor = obtener_id_preceptor()

    if not preceptor:
        return redirect(url_for('login'))

    cursos_preceptor = Curso.query.filter_by(idpreceptor=preceptor.id).all()
    curso_id = request.args.get('curso_id', None)

    if not curso_id:
        return render_template('informe.html', cursos=cursos_preceptor)
    
    estudiantes = Estudiante.query.filter_by(idcurso=curso_id).order_by(Estudiante.nombre, Estudiante.apellido).all()
    informe = []
    # Obtener el objeto Curso correspondiente al ID recibido
    for estudiante in estudiantes:
        asistencias = Asistencia.query.filter_by(idestudiante=estudiante.id).all()
        aula = aula_justificada = aula_injustificada = 0
        fisica = fisica_justificada = fisica_injustificada = 0

        for asistencia in asistencias:
            if asistencia.codigoclase == 1:
                if asistencia.asistio == 's':
                    aula += 1
                elif asistencia.asistio == 'n':
                    if asistencia.justificacion:
                        aula_justificada += 1
                    else:
                        aula_injustificada += 1
            elif asistencia.codigoclase == 2:
                if asistencia.asistio == 's':
                    fisica += 1
                elif asistencia.asistio == 'n':
                    if asistencia.justificacion:
                        fisica_justificada += 1
                    else:
                        fisica_injustificada += 1
        total = aula_injustificada + aula_justificada + (fisica_injustificada + fisica_justificada) / 2

        

        informe.append({
            'estudiante': estudiante,
            'asistencia_fecha': asistencia.fecha,
            'aula': aula,
            'aula_justificada': aula_justificada,
            'aula_injustificada': aula_injustificada,
            'edu_fisica': fisica,
            'fisica_justificada': fisica_justificada,
            'fisica_injustificada': fisica_injustificada,
            'total': total
        })


    return render_template('informe.html', informe=informe, cursos=cursos_preceptor)