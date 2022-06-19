from flask import Flask, render_template, redirect, url_for, request, send_file, session
import pandas as pd
from io import BytesIO
from datetime import datetime

from models import *

app = Flask(__name__)
app.secret_key = str(datetime.now()).strip()

form_infos = ['sexo','idade', 'massa', 'altura', 'atividade', 'exercicio', 'tempo_exercicio', 'dias_exercicio', 'dieta_preferida', 'objetivo']
    

@app.route('/', methods=['POST', 'GET'])
def input():
    
    if request.method == 'POST' and all(item in request.form for item in form_infos):
        return redirect(url_for("output"))
   
    else:
        exercicios = dict_met_exercicios.keys()
        atividades = dict_met_atividades.keys()
        sexos = SEXO_CHOICES
        objetivos = OBJETIVOS_CHOICES
        dietas = df_dieta['Dietas']

        context = {'exercicios': sorted(exercicios),
                   'atividades': atividades,
                   'sexos': sexos,
                   'objetivos': objetivos,
                   'dietas': dietas
                   }

        return render_template('input.html', **context)


@app.route('/resultados', methods=['POST', 'GET'])
def output():

    if request.method == 'POST':

        session['sexo'] = request.form.get('sexo')
        session['idade'] = int(request.form.get('idade').replace(',', '.'))
        session['massa'] = float(request.form.get('massa').replace(',', '.'))
        session['altura'] = float(request.form.get('altura').replace(',', '.'))

        session['atividade'] = request.form.get('atividade')
        session['exercicio'] = request.form.get('exercicio')
        session['tempo_exercicio'] = float(request.form.get('tempo_exercicio').replace(',', '.'))
        session['dias_exercicio'] = int(request.form.get('dias_exercicio').replace(',', '.'))
        session['dieta_preferida'] = request.form.get('dieta_preferida')
        session['objetivo'] = request.form.get('objetivo')

        bmr = get_bmr(session['altura'], session['massa'], session['idade'], session['sexo'])
        eat = get_eat(session['exercicio'], session['tempo_exercicio'], session['dias_exercicio'], session['massa'], bmr)
        neat = get_neat(session['atividade'], session['massa'], bmr)
        tdee = get_tdee(bmr, eat, neat)
        tef = get_tef(tdee)

        calorias_dieta = get_calorias_dieta(session['objetivo'], tdee)
        dias_para_objetivo = get_dias_para_objetivo(session['objetivo'], calorias_dieta, session['massa'])

        proteinas_dieta = get_proteinas_dieta(session['dieta_preferida'], calorias_dieta)
        carboidratos_dieta = get_carboidratos_dieta(session['dieta_preferida'], calorias_dieta)
        gorduras_dieta = get_gorduras_dieta(session['dieta_preferida'], calorias_dieta)

        context = {'bmr': int(round(bmr, 0)),
                   'eat': int(round(eat, 0)),
                   'neat': int(round(neat, 0)),
                   'tdee': int(round(tdee, 0)),
                   'tef': int(round(tef, 0)),
                   'calorias_dieta': int(round(calorias_dieta, 0)),
                   'objetivo': session['objetivo'],
                   'dias_para_objetivo': dias_para_objetivo,
                   'proteinas_dieta': int(round(proteinas_dieta, 0)),
                   'carboidratos_dieta': int(round(carboidratos_dieta, 0)),
                   'gorduras_dieta': int(round(gorduras_dieta, 0))
        }

        return render_template('output.html', **context)

    else:
        return redirect(url_for("input"))



if __name__ == '__main__':
    app.run(debug=True)


