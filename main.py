# Importando os pacotes
import pandas as pd
import csv
import random

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from datetime import datetime


app = Flask(__name__)

messages = [] 

# Criando a rota
@app.route('/bot', methods= ['POST'])
def bot():

    # lendo os dados dos especialistas
    df = pd.read_csv("/Users/leticia/geek-bot/geek-bot-env/UnimedMedicos.csv", sep=";")
    

    # Recebendo a mensagem
    incoming_msg = request.values.get('Body', '').upper() #Salvando o corpo da mensagem recebida 
    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S") #Salvando as informações de data e hora da mensagem recebida

    resp = MessagingResponse()
    msg = resp.message()

    if 'OI' in incoming_msg:
        reply = ('''Olá, aqui é a Júlia, assistente virtual da Unimed Araruama. *Digite a especialidade desejada*\n
Caso não saiba o nome da especialidade, digite *Ajuda*.''') # Resposta que iremos retornar caso seja mandado um "Oi"
        msg.body(reply)
        return str(resp) # Retornando a resposta
    
    if 'AJUDA' in incoming_msg:
        lista_especialidades = df['Especialidade'].unique() #Pegando os valores únicos da variável "Especialidade"
        results = f'''Essas são as especialidades disponíveis\n\n''' #Colocando numa variável o início da mensagem a ser enviada e ir pra próxima linha
        for i in range(len(lista_especialidades)): # De acordo com a quantidade de especialidades
            especialidades = f'''{lista_especialidades[i]}\n''' # Vou pegar o nome de cada especialidade e ir pra próxima linha
            results = results + especialidades # E ir adicionando numa variável
        reply = str(results) # Retornando a resposta
        messages.append(incoming_msg) # Adicionando a interação realizada
    
    if incoming_msg in list(df['Especialidade']): # Se a mensagem recebida for uma Especialidade
        tabela = (df[['Nome', 'Endereço', 'Telefone']].loc[df['Especialidade'] == incoming_msg]).reset_index() #Crio uma tabela apenas com as variáveis que quero retornar daquela especialidade específica

        if len(tabela) > 10: # Como algumas especialidades tinham muitas opções, aquelas com muitos especialistas, escolhi mostrar apenas 10
            total_medicos = list(range(len(tabela))) # Faço uma lista com todos os médicos daquela especialidade
            random_list = random.sample(total_medicos, k=10) # para não ser injusta e mostrar apenas os 10 primeiros, crio uma amostra aleatória com 10 especialistas
            results = f'''Esses foram os profissionais encontrados\n''' #Colocando numa variável o início da mensagem a ser enviada e ir pra próxima linha
            for i in random_list: # Para cada entrada da lista
                medico = f'''{i} - {tabela.Nome[i]}, {tabela.Endereço[i]}, {tabela.Telefone[i]}\n\n''' #Colo em ordem, Nome, Endereço e Telefone
                results = results + medico
                reply = str(results) # Retornando a resposta
        else: # Se tiver menos que 10 especialistas, faz a mesma coisa que o anterior, porém retornando todos
            results = f'''Esses foram os profissionais encontrados\n'''
            for i in range(len(tabela)):
                medico = f'''{i} - {tabela.Nome[i]}, {tabela.Endereço[i]}, {tabela.Telefone[i]}\n\n'''
                results = results + medico
                reply = str(results)# Retornando a resposta
        messages.append(incoming_msg) # Adicionando a interação realizada

    msg.body(reply)

    # Salvando as interações num arquivo CSV
    with open('messages.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([incoming_msg, date_time])

    return str(resp)


@app.route('/')
def index():
    return "Sim, o Flask está funcionando :)"

if __name__ == '__main__':
    app.run()