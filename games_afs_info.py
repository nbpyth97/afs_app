from codecs import utf_8_decode, utf_8_encode
from email.encoders import encode_noop
import PyPDF2 as pydf
import unidecode
import pandas as pd
import tabula as read_pdf
from collections import defaultdict
from datetime import datetime

import glob
import os
from pathlib import Path

path = os.getcwd() # get current working directory

time_creation=''
file_name=''

path = "{}\games_info".format(os.getcwd()) # get current working directory

for files in os.listdir(path):
    if 'pdf' in files:
        c_time = os.path.getctime("{0}\\{1}".format(path,files))

        # convert creation timestamp into DateTime object
        dt_c = datetime.fromtimestamp(c_time)
        
        if str(dt_c) > time_creation:
            time_creation = str(dt_c)
            file_name = files
            
print('Created on:', dt_c)
print(file_name)

file_path = "{0}\\{1}".format(path,file_name) #file path
pdf_file = open(file_path,'rb')

pdf_reader = pydf.PdfFileReader(pdf_file)
x= pdf_reader.numPages

lista=[]
lista_games=[]

for i in (range(x)):
    pdf_obj=pdf_reader.getPage(i)
    
    text=pdf_obj.extractText()
    text = text.split('\n')
    lista.append(text)

start_date = lista[0][2]
end_date = lista[0][4]

for i in range(len(lista)):
    if i == 0:
        lista_games = [lista[0][5:]]
    else:
        lista_games.append(lista[i])

#--------------The Deleter--------------
deletewords = ['jogo','árbitro','função',"página","nota informativa","n.:","data:"]
deletewords = [name.upper() for name in deletewords]

middle_list=[]
new_list_of_games=[]
a=0

for n in range(len(lista_games)):
    for m in range(len(lista_games[n])):
        middle_list.append(lista_games[n][m].upper())
        if m == len(lista_games[n])-1:
            new_list_of_games.append(middle_list.copy())
            middle_list.clear()


for i in range(len(new_list_of_games)):
    for words in new_list_of_games[i]:
        for deleter in deletewords:
            if deleter == words:
                new_list_of_games[i].remove(words)
#------------------------------------------

#--------------The Finder 1--------------
stopwords = ['seniores','juniores','juvenis','iniciados','benjamins',
             'infantis','feminino','Fut7','CD Juvenil Feminino Fut7',
            ' Sub15','Feminino','Sub22']

competition_list=[]
stopwords=[name.upper() for name in stopwords]

for i in range(len(new_list_of_games)):
    for words in new_list_of_games[i]:
        for stop in stopwords:
            if stop in words:
                competition_list.append(words)


competition_list = [*set(competition_list)]
print("Número de Competições",len(competition_list))
#------------------------------------------

#--------------By Competition--------------
dictionary_of_competitions=defaultdict(list)
dictionary_of_games=defaultdict(list)

competition_checker=''
a=0

for i in range(len(new_list_of_games)):
    for words in new_list_of_games[i]:
        if words in competition_list:
            competition_checker=''
            if words in dictionary_of_competitions.keys():
                competition_checker = competition_checker + words
            else:
                dictionary_of_competitions["{}".format(words)] = []
                competition_checker = competition_checker + words
            
            continue
        
        dictionary_of_competitions[competition_checker].append(words)
#------------------------------------------

#--------------Take Futsal Out--------------
football_competitions={}

for i in dictionary_of_competitions.keys():
    if "FUTSAL" in i:
        pass
    else:
        football_competitions[i] = []
        football_competitions[i].append(dictionary_of_competitions[i])
#------------------------------------------

#--------------Games with 2 or 1 Referees--------------
referee2_1_list=['benjamins','infantis','feminino','Fut7',
                 'Feminino','CD Juvenil Feminino Fut7',
                 ' Sub15']

referee2_1_list=[i.upper() for i in referee2_1_list]

each_game_referee2_1_middle = []
each_game_referee2_1 = []

dict_games_2_1referees={}

for i in football_competitions.keys():
    for age_rank in referee2_1_list:
        if age_rank in i:
            for games_info in football_competitions[i]:
                for data in games_info:
                    each_game_referee2_1_middle.append(data)
                    if "-{} ".format(datetime.today().year) in data:
                        each_game_referee2_1.append(each_game_referee2_1_middle.copy())
                        each_game_referee2_1_middle.clear()
                if len(each_game_referee2_1)>0:
                    dict_games_2_1referees[i] = each_game_referee2_1
                    each_game_referee2_1=[]
#------------------------------------------

dict_games_2_referees= {}
dict_games_1_referee = dict_games_2_1referees.copy()

for i in dict_games_2_1referees:
    if "FUT9" in i:
        dict_games_2_referees[i] = dict_games_1_referee[i]
        dict_games_1_referee.pop(i)

#--------------Count Games with 2 Referees--------------
count_games_2_referees = 0 

for keys in dict_games_2_referees:
    for i in dict_games_2_referees[keys]:
        count_games_2_referees+=1

print("Número de Jogos com 2 árbitros:",count_games_2_referees)
#------------------------------------------

#--------------Count Games with 1 Referees--------------
count_games_1_referee = 0 

for keys in dict_games_1_referee:
    for i in dict_games_1_referee[keys]:
        count_games_1_referee+=1

count_games_1_referee
print('Número de Jogos com 1 árbitro:',count_games_1_referee)
#------------------------------------------

#--------------Games with 3 Referees--------------
referee3_list=['seniores','juniores','juvenis','iniciados','sub22']
referee3_list=[i.upper() for i in referee3_list]
referee3_list.append('TAÇA A.F.S. SOUSA MARQUES')

each_game_referee3_middle = []
each_game_referee3 = []

dict_games_3referees={}

#games with 3 referees:
for i in football_competitions.keys():
    for age_rank in referee3_list:
        if age_rank in i:
            for games_info in football_competitions[i]:
                for data in games_info:
                    each_game_referee3_middle.append(data)
                    if "ARBITRO ASSISTENTE 2" == data:
                        each_game_referee3.append(each_game_referee3_middle.copy())
                        each_game_referee3_middle.clear()
                if len(each_game_referee3)>0:
                    dict_games_3referees[i] = each_game_referee3
                    each_game_referee3=[]
print(football_competitions)
#------------------------------------------

###########FALTA VER JOGOS DA TAÇA###########
#############################################

count_games_3_referee = 0 

for keys in dict_games_3referees:
    for i in dict_games_3referees[keys]:
        count_games_3_referee+=1

print('Número de Jogos com 3 árbitros:',count_games_3_referee)

def referee_1():
    
    competition_keys_checker = ''
    codigo_jogo = defaultdict(list)

    jogos_info_1_referee = {}
    i=0

    for competition_keys in dict_games_1_referee.keys():
        for competition_games in dict_games_1_referee[competition_keys]:
            for list_info in competition_games:
                i+=1
                
                if list_info == 'ARBITRO':
                    if i == 4 and competition_games[i-4] == 'ÁRBITRO': 
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]
                        
                        try:
                            campo = competition_games[i].split('-')[0]
                            local = competition_games[i].split('-')[1]
                        except:
                            campo = competition_games[i]

                        codigo_jogo[codigo] = [] 
                        
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)
                        
                        continue

                    if i == 4 and competition_games[i-4] != 'ÁRBITRO':
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]
                        
                        
                        try:
                            campo = competition_games[i].split('-')[0]
                            local = competition_games[i].split('-')[1]
                        except:
                            campo = competition_games[i]

                        codigo_jogo[codigo] = [] 
                        
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)
                        
                        continue
                        
                    if i == 5:
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]
                    
                        try:
                            campo = competition_games[i].split('-')[0]
                            local = competition_games[i].split('-')[1]
                        except:
                            campo = competition_games[i]
                        
                        codigo_jogo[codigo] = []
                        
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)
                        
                        continue
                        
                    else:
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]

                        try:
                            campo = competition_games[i].split('-')[0]
                            local = competition_games[i].split('-')[1]
                        except:
                            campo = competition_games[i]

                        codigo_jogo[codigo] = [] 
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)
                        

            i=0
        jogos_info_1_referee[competition_keys] = codigo_jogo
        codigo_jogo = defaultdict(list)
    
    return jogos_info_1_referee    



def referee_2():
    
    competition_keys_checker = ''
    codigo_jogo = defaultdict(list)

    jogos_info_2_referee = {}
    i=0

    for competition_keys in dict_games_2_referees.keys():
        for competition_games in dict_games_2_referees[competition_keys]:
            for list_info in competition_games:
                i+=1
                if list_info == 'ARBITRO':
                    if i == 4 and competition_games[i-4] == 'ÁRBITRO': 
                        #dados do jogo:
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_2 = competition_games[-3].split(' ')
                        arbitro_2 = ' '.join(arbitro_2[1:])
                        n_arbitro_2 = competition_games[-3].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]

                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:
                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None


                        codigo_jogo[codigo] = []

                        #appends:
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_2)
                        codigo_jogo[codigo].append(n_arbitro_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)   

                        continue

                    if i == 4 and competition_games[i-4] != 'ÁRBITRO':
                        #dados do jogo:
                        codigo = competition_games[i-4].split(' ')[0]
                        equipas = competition_games[i-4].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_2 = competition_games[-3].split(' ')
                        arbitro_2 = ' '.join(arbitro_2[1:])
                        n_arbitro_2 = competition_games[-3].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]

                        codigo_jogo[codigo] = []

                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:

                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #appends:
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_2)
                        codigo_jogo[codigo].append(n_arbitro_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)   

                        continue

                    if i == 5 and competition_games[i-5] == 'ÁRBITRO':
                        #dados do jogo:
                        codigo = competition_games[i-4].split(' ')[0]
                        equipas = competition_games[i-4].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_2 = competition_games[-3].split(' ')
                        arbitro_2 = ' '.join(arbitro_2[1:])
                        n_arbitro_2 = competition_games[-3].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]

                        codigo_jogo[codigo] = []

                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:

                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #appends:
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_2)
                        codigo_jogo[codigo].append(n_arbitro_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)   


                        continue

                    else:
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_2 = competition_games[-3].split(' ')
                        arbitro_2 = ' '.join(arbitro_2[1:])
                        n_arbitro_2 = competition_games[-3].split(' ')[0]
                        dia = competition_games[-1].split(' ')[0]
                        hora = competition_games[-1].split(' ')[1]

                        codigo_jogo[codigo] = []  

                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:

                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #appends:
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_2)
                        codigo_jogo[codigo].append(n_arbitro_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)                    


            i=0
        jogos_info_2_referee[competition_keys] = codigo_jogo
        codigo_jogo = defaultdict(list)
    
    return jogos_info_2_referee


def referee_3(): 
    i=0
    n=0
    jogos_info_3_referee={}
    codigo_jogo = defaultdict(list)
    competition_game_check=[]

    for competition_keys in dict_games_3referees.keys():
        for competition_games in dict_games_3referees[competition_keys]:
            for list_info in competition_games:
                i+=1
                if list_info == 'ARBITRO':
                    if i == 4 and competition_games[i-4] == 'ÁRBITRO':
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_assistente_2 = competition_games[-2].split(' ')
                        arbitro_assistente_2 = ' '.join(arbitro_assistente_2[1:])
                        n_arbitro_assistente_2 = competition_games[-2].split(' ')[0]

                        #--------------Arbitro Assistentes--------------:
                        for inside_info in competition_games:
                            if competition_games == competition_game_check:
                                pass
                            else:
                                if inside_info == 'ARBITRO ASSISTENTE 1':
                                    competition_game_check = competition_games.copy()
                                    arbitro_assistente_1 = competition_games[n-1].split(' ')
                                    arbitro_assistente_1 = ' '.join(arbitro_assistente_1[1:])
                                    n_arbitro_assistente_1 = competition_games[n-1].split(' ')[0]
                                    dia = competition_games[n+1].split(' ')[0]
                                    hora = competition_games[n+1].split(' ')[1]
                                    n=0
                                n+=1
                        n=0

                        competition_game_check = []
                        codigo_jogo[codigo] = []

                        #--------------Campo e local--------------:
                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:
                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #--------------Appends--------------:
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_assistente_1)
                        codigo_jogo[codigo].append(n_arbitro_assistente_1)
                        codigo_jogo[codigo].append(arbitro_assistente_2)
                        codigo_jogo[codigo].append(n_arbitro_assistente_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)

                        continue


                    if i == 4 and competition_games[i-4] != 'ÁRBITRO':
                        codigo = competition_games[i-4].split(' ')[0]
                        equipas = competition_games[i-4].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_assistente_2 = competition_games[-2].split(' ')
                        arbitro_assistente_2 = ' '.join(arbitro_assistente_2[1:])
                        n_arbitro_assistente_2 = competition_games[-2].split(' ')[0]

                        #--------------Arbitro Assistentes--------------:
                        for inside_info in competition_games:
                            if competition_games == competition_game_check:
                                pass
                            else:
                                if inside_info == 'ARBITRO ASSISTENTE 1':
                                    competition_game_check = competition_games.copy()
                                    arbitro_assistente_1 = competition_games[n-1].split(' ')
                                    arbitro_assistente_1 = ' '.join(arbitro_assistente_1[1:])
                                    n_arbitro_assistente_1 = competition_games[n-1].split(' ')[0]
                                    dia = competition_games[n+1].split(' ')[0]
                                    hora = competition_games[n+1].split(' ')[1]
                                    n=0
                                n+=1
                        n=0

                        competition_game_check = []
                        codigo_jogo[codigo] = []

                        #--------------Campo e local--------------:
                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:
                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #--------------Appends--------------:           
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_assistente_1)
                        codigo_jogo[codigo].append(n_arbitro_assistente_1)
                        codigo_jogo[codigo].append(arbitro_assistente_2)
                        codigo_jogo[codigo].append(n_arbitro_assistente_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)

                        continue

                    if i == 5 and competition_games[i-5] == 'ÁRBITRO':
                        codigo = competition_games[i-4].split(' ')[0]
                        equipas = competition_games[i-4].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_assistente_2 = competition_games[-2].split(' ')
                        arbitro_assistente_2 = ' '.join(arbitro_assistente_2[1:])
                        n_arbitro_assistente_2 = competition_games[-2].split(' ')[0]

                        #--------------Arbitro Assistentes--------------:
                        for inside_info in competition_games:
                            if competition_games == competition_game_check:
                                pass
                            else:
                                if inside_info == 'ARBITRO ASSISTENTE 1':
                                    competition_game_check = competition_games.copy()
                                    arbitro_assistente_1 = competition_games[n-1].split(' ')
                                    arbitro_assistente_1 = ' '.join(arbitro_assistente_1[1:])
                                    n_arbitro_assistente_1 = competition_games[n-1].split(' ')[0]
                                    dia = competition_games[n+1].split(' ')[0]
                                    hora = competition_games[n+1].split(' ')[1]
                                    n=0
                                n+=1
                        n=0

                        competition_game_check = []
                        codigo_jogo[codigo] = []

                        #--------------Campo e local--------------:
                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:

                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #--------------Appends--------------:           
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_assistente_1)
                        codigo_jogo[codigo].append(n_arbitro_assistente_1)
                        codigo_jogo[codigo].append(arbitro_assistente_2)
                        codigo_jogo[codigo].append(n_arbitro_assistente_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)

                        continue

                    else:
                        codigo = competition_games[i-3].split(' ')[0]
                        equipas = competition_games[i-3].replace(codigo,'')
                        arbitro = competition_games[i-2].split(' ')
                        arbitro =' '.join(arbitro[1:])
                        n_arbitro = competition_games[i-2].split(' ')[0]
                        arbitro_assistente_2 = competition_games[-2].split(' ')
                        arbitro_assistente_2 = ' '.join(arbitro_assistente_2[1:])
                        n_arbitro_assistente_2 = competition_games[-2].split(' ')[0]                    


                        #--------------Arbitro Assistentes--------------:
                        for inside_info in competition_games:
                            if competition_games == competition_game_check:
                                pass
                            else:
                                if inside_info == 'ARBITRO ASSISTENTE 1':
                                    competition_game_check = competition_games.copy()
                                    arbitro_assistente_1 = competition_games[n-1].split(' ')
                                    arbitro_assistente_1 = ' '.join(arbitro_assistente_1[1:])
                                    n_arbitro_assistente_1 = competition_games[n-1].split(' ')[0]
                                    dia = competition_games[n+1].split(' ')[0]
                                    hora = competition_games[n+1].split(' ')[1]
                                    n=0
                                n+=1
                        n=0

                        competition_game_check = []
                        codigo_jogo[codigo] = []

                        #--------------Campo e local--------------:
                        campo = competition_games[i].split('-')[0].split('(')[0]
                        if '-' in competition_games[i]:

                            if competition_games[i].split('-')[1].split(' ')[-1]:
                                local = competition_games[i].split('-')[1]

                            if not competition_games[i].split('-')[1].split(' ')[-1]:
                                local_1 = competition_games[i].split('-')[1]
                                local_2 = competition_games[i+1]
                                local = local_1+local_2
                        else:
                            try:
                                local = competition_games[i+1].split('-')[1]
                            except:
                                local = None

                        #--------------Appends--------------:           
                        codigo_jogo[codigo].append(equipas)
                        codigo_jogo[codigo].append(arbitro)
                        codigo_jogo[codigo].append(n_arbitro)
                        codigo_jogo[codigo].append(arbitro_assistente_1)
                        codigo_jogo[codigo].append(n_arbitro_assistente_1)
                        codigo_jogo[codigo].append(arbitro_assistente_2)
                        codigo_jogo[codigo].append(n_arbitro_assistente_2)
                        codigo_jogo[codigo].append(campo)
                        codigo_jogo[codigo].append(local)
                        codigo_jogo[codigo].append(dia)
                        codigo_jogo[codigo].append(hora)
            i=0
        jogos_info_3_referee[competition_keys] = codigo_jogo
        codigo_jogo = defaultdict(list) 
    
    return jogos_info_3_referee

