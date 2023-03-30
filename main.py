# Importando os pacotes
import pandas as pd
import csv
import random

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime


app = Flask(__name__)

@app.route('/bot', methods= ['POST'])
def bot():

    # read in data
    df = pd.read_csv("/Users/leticia/geek-bot/geek-bot-env/UnimedMedicos.csv", sep=";")
    

    # incoming message
    incoming_msg = request.values.get('Body', '').upper()
    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    resp = MessagingResponse()
    msg = resp.message()

    if 'OI' in incoming_msg:
        reply = ('''Olá, aqui é a Júlia, assistente virtual da Unimed Araruama. *Digite a especialidade desejada*\n
Caso não saiba o nome da especialidade, digite *Ajuda*.''')
        msg.body(reply)
        messages.append(incoming_msg) # add incoming message to the list
        return str(resp)
    
    if 'AJUDA' in incoming_msg:
        lista_especialidades = df['Especialidade'].unique()
        #reply = str (lista_especialidades)
        results = f'''Essas são as especialidades disponíveis\n\n'''
        for i in range(len(lista_especialidades)):
            especialidades = f'''{lista_especialidades[i]}\n'''
            results = results + especialidades
        reply = str(results)
        messages.append(incoming_msg) # add incoming message to the list
    
    if incoming_msg in list(df['Especialidade']):
        tabela = (df[['Nome', 'Endereço', 'Telefone']].loc[df['Especialidade'] == incoming_msg]).reset_index()
        #results = tabela.Nome[0], tabela.Endereço[0], tabela.Telefone[0]

        if len(tabela) > 10:
            total_medicos = list(range(len(tabela)))
            random_list = random.sample(total_medicos, k=10)
            results = f'''Esses foram os profissionais encontrados\n'''
            for i in random_list:
                medico = f'''{i} - {tabela.Nome[i]}, {tabela.Endereço[i]}, {tabela.Telefone[i]}\n\n'''
                results = results + medico
                reply = str(results)
        else:
            results = f'''Esses foram os profissionais encontrados\n'''
            for i in range(len(tabela)):
                medico = f'''{i} - {tabela.Nome[i]}, {tabela.Endereço[i]}, {tabela.Telefone[i]}\n\n'''
                results = results + medico
                reply = str(results)
        messages.append(incoming_msg) # add incoming message to the list

    msg.body(reply)

    # write incoming messagens to CSV file
    with open('messages.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([incoming_msg, date_time])

    return str(resp)


@app.route('/')
def index():
    return "Sim, o Flask está funcionando :)"

if __name__ == '__main__':
    app.run()