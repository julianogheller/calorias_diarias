import pandas as pd

SEXO_CHOICES = ('Masculino', 'Feminino')
OBJETIVOS_CHOICES = ('Emagrecer', 'Manter o Peso', 'Ganhar Massa')
FATOR_DIETA_BULK = 0.1
FATOR_DIETA_CUT = 0.15

dict_met_exercicios = {
    '--Sedentário--': 0,
    'Ciclismo': 6,
    'Aeróbicos': 6.25,
    'Dança': 6,
    'Corrida': 8,
    'Caminhada': 4,
    'Surf': 4,
    'Natação': 7.5,
    'Basquete': 6.25,
    'Vôlei': 4.5,
    'Tênis': 6.5, 
    'Futebol': 7.25, 
    'Patinação': 7, 
    'Skate': 5,
    'Hipismo': 4.25, 
    'Handebol': 7.25, 
    'Golf': 4,
    'Futebol Americano': 6.5, 
    'Ginástica': 5.25,
    'Artes Marciais': 6.5,
    'Musculação': 4.75
}

dict_met_atividades = {                               
    'Trabalho Sentado': 2.5, 
    'Moderada': 4.25,
    'Trabalho Braçal': 6.75,
    'Atleta Profissional': 8
}                                     # valores retirados de uma média da tabela de MET para atividades cotidianas separadas em 3 grupos de intensidade
                                   
df_dieta = pd.DataFrame({
    'Dietas': ['Low Carb', 'Balanceada', 'High Carb'],
    'Proteínas': [0.40, 0.30, 0.30],
    'Carboidratos': [0.20, 0.35, 0.50],
    'Gorduras': [0.40, 0.35, 0.20]})


def get_bmr(altura, massa, idade, sexo): # taxa metabólica basal (calorias usadas pelo corpo só para sobreviver)
    
    bmr = (altura * 625) + (massa * 9.99) - (idade * 4.92)
    
    if sexo == "Masculino":
        bmr += 5

    elif sexo == "Feminino":
        bmr -= 161
    
    return bmr


def get_eat(exercicio, tempo_exercicio, dias_exercicio, massa, bmr):  # termogênese ativa de exercício (calorias usadas fazendo exercícios)
    
    met = dict_met_exercicios[exercicio]

    eat = met * massa * (tempo_exercicio/60) * (dias_exercicio/7)

    return eat

def get_neat(atividade, massa, bmr):  # termogênese ativa de não-exercício (calorias usadas fazendo movimentos comuns - ex: subir escada, caminhar na rua)
    
    met = dict_met_atividades[atividade]
    
    neat = met * massa * (5/7) * 8 * 60 * 3.5 / bmr

    return neat


def get_tdee(bmr, eat, neat): # gasto energético diário total (soma de todos os gastos calóricos)
   
    tdee = (bmr + eat + neat)/0.9
   
    return tdee

def get_tef(tdee):  # efeito térmico do alimento (calorias usadas pelo corpo só para digerir os alimentos)
   
    tef = tdee * 0.1
   
    return tef


def get_calorias_dieta(objetivo, tdee):
    
    if objetivo == "Ganhar Massa":
        calorias_dieta = tdee * (1 + FATOR_DIETA_BULK)

    elif objetivo == "Manter o Peso":
        calorias_dieta = tdee
    
    else:
        calorias_dieta = tdee * (1 - FATOR_DIETA_CUT)
    
    return calorias_dieta


def get_dias_para_objetivo(objetivo, calorias_dieta, massa):
    if objetivo == "Ganhar Massa":
        dias_para_objetivo = 6_000 / (calorias_dieta * FATOR_DIETA_BULK)
        return f'ganhar 1kg de músculo a cada {int(round(dias_para_objetivo, 0))} dias'
    elif objetivo == "Manter o Peso":
        return f'manter os {int(round(massa, 0))} kg'
    else:
        dias_para_objetivo = 7_700 / (calorias_dieta * FATOR_DIETA_CUT)
        return f'perder 1kg de gordura a cada {int(round(dias_para_objetivo, 0))} dias'


def get_proteinas_dieta(dieta_preferida, calorias_dieta):
    proteinas_dieta = calorias_dieta * (df_dieta['Proteínas'].where(df_dieta['Dietas'] == dieta_preferida).sum()) / 4
    return proteinas_dieta

def get_carboidratos_dieta(dieta_preferida, calorias_dieta):
    carboidratos_dieta = calorias_dieta * (df_dieta['Carboidratos'].where(df_dieta['Dietas'] == dieta_preferida).sum()) / 4
    return carboidratos_dieta

def get_gorduras_dieta(dieta_preferida, calorias_dieta):
    gorduras_dieta = calorias_dieta * (df_dieta['Gorduras'].where(df_dieta['Dietas'] == dieta_preferida).sum()) / 9
    return gorduras_dieta
