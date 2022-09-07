import pandas as pd

def jogos_do_arbitro(n_arbitro_input):
    from games_afs_info import referee_1,referee_2,referee_3
    import pandas as pd
    import os
    
    referee_1_2 = referee_1() | referee_2() | referee_3()
    print("referee_1_2:",referee_1_2)
    n_arbitro = n_arbitro_input
    n_arbitro= "({})".format(n_arbitro)
    games_of_referee=[]
    i=0

    for keys in referee_1_2.keys():
        for games in referee_1_2[keys]:
            if n_arbitro in referee_1_2[keys][games]:
                games_of_referee.append(referee_1_2[keys][games])
                games_of_referee[i].append(games)
                games_of_referee[i].append(keys)

                if ' ' in games_of_referee[i]:
                    games_of_referee[i].remove(" ")

                i+=1


    jogos_1 = []
    jogos_2 = []
    jogos_3 = []

    df_jogos_1_referee = pd.DataFrame(jogos_1)
    df_jogos_2_referees = pd.DataFrame(jogos_2)
    df_jogos_3_referees = pd.DataFrame(jogos_3)


    for i in games_of_referee:
        if len(i) < 10:
            if not df_jogos_1_referee.empty:
                df_jogos_1_referee= df_jogos_1_referee.append(pd.DataFrame([i],columns =['Jogo','Árbitro','NºÁrbitro','Campo',
                                                                   'Local','Dia','Hora','NºJogo','prova']), ignore_index=True)
            else:
                df_jogos_1_referee = pd.DataFrame([i],columns =['Jogo','Árbitro','NºÁrbitro','Campo',
                                                                   'Local','Dia','Hora','NºJogo','prova'])


        if 10<=len(i)<=11:
            if not df_jogos_2_referees.empty:
                df_jogos_2_referees = df_jogos_2_referees.append(pd.DataFrame([i],columns =['Jogo','Árbitro','NºÁrbitro','2ºÁrbitro','Nº2ºÁrbitro',
                                                                   'Campo','Local','Dia','Hora','NºJogo','prova']),ignore_index=True)
            else:
                df_jogos_2_referees = pd.DataFrame([i],columns =['Jogo','Árbitro','NºÁrbitro','2ºÁrbitro','Nº2ºÁrbitro',
                                                                   'Campo','Local','Dia','Hora','NºJogo','prova'])


        if len(i)>=12:
            if not df_jogos_3_referees.empty:
                df_jogos_3_referees=df_jogos_3_referees.append(pd.DataFrame([i],columns=['Jogo','Árbitro','NºÁrbitro','AA1','NºAA1','AA2','NºAA2',
                                                                   'Campo','Local','Dia','Hora','NºJogo','prova']),ignore_index=True)

            else:
                df_jogos_3_referees = pd.DataFrame([i],columns =['Jogo','Árbitro','NºÁrbitro','AA1','NºAA1','AA2','NºAA2',
                                                                   'Campo','Local','Dia','Hora','NºJogo','prova'])

    try:
        #separate 1 referee:
        separated_teams = df_jogos_1_referee['Jogo'].str.split("-", n = 1, expand = True)
        df_jogos_1_referee["Equipa A"]= separated_teams[0]
        df_jogos_1_referee["Equipa B"]= separated_teams[1]
        df_jogos_1_referee.drop(columns =["Jogo"], inplace = True)
    except:
        print('Não Existe jogos com 1 árbitro')

    try:
        #separate 2 referees:
        separated_teams = df_jogos_2_referees['Jogo'].str.split("-", n = 1, expand = True)
        df_jogos_2_referees["Equipa A"]= separated_teams[0]
        df_jogos_2_referees["Equipa B"]= separated_teams[1]
        df_jogos_2_referees.drop(columns =["Jogo"], inplace = True)   
    except:
        print('Não existe jogos com 2 árbitros')

    try:
        #separate 3 referees:
        separated_teams = df_jogos_3_referees['Jogo'].str.split("-", n = 1, expand = True)
        df_jogos_3_referees["Equipa A"]= separated_teams[0]
        df_jogos_3_referees["Equipa B"]= separated_teams[1]
        df_jogos_3_referees.drop(columns =["Jogo"], inplace = True)
    except:
        print('Não Existe jogos com 3 árbitros')    
    
    return df_jogos_1_referee,df_jogos_2_referees,df_jogos_3_referees,n_arbitro

print(jogos_do_arbitro(665))
