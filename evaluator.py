import games_afs_info as games
import pandas as pd

def evaluation(referee_function_1,referee_function_2,referee_function_3):


    accuracy_list=[]
    df_1 = pd.DataFrame.from_dict(referee_function_1,orient='index')
    df_2 = pd.DataFrame.from_dict(referee_function_2,orient='index')
    df_3 = pd.DataFrame.from_dict(referee_function_3,orient='index')

    count_error = 0

    for i in df_1.columns:
        if '.' in i:
            pass
        else:
            count_error+=1

    count_error = 0

    for i in df_2.columns:
        if '.' in i:
            pass
        else:
            count_error+=1

    count_error = 0

    for i in df_3.columns:
        if '.' in i:
            pass
        else:
            count_error+=1

    try:
        print('*'*20)
        accuracy_1referees = round((1 - count_error / len(df_1.columns))*100,2)
        print('Accuracy:', accuracy_1referees,'%')
        accuracy_2referees = round((1 - count_error / len(df_2.columns))*100,2)
        print('Accuracy:', accuracy_2referees,'%')
        accuracy_3referees = round((1 - count_error / len(df_3.columns))*100,2)
        print('Accuracy:', accuracy_3referees,'%\n')
    except Exception as e:
        print(e)
    
    try:
        print('Total Accuracy:',round((accuracy_1referees + accuracy_2referees + accuracy_3referees) / 3,2),'%')
    except Exception as e:
        print(e)

    print('*'*20)
    print('Diferença de jogos com 1 árbitro e o Algoritmo:', games.count_games_1_referee-len(df_1.columns))
    print('Diferença de jogos com 2 árbitros e o Algoritmo:', games.count_games_2_referees-len(df_2.columns))
    print('Diferença de jogos com 3 árbitros e o Algoritmo:', games.count_games_3_referee-len(df_3.columns))



print('CHANGING 2:',evaluation(games.referee_1(),games.referee_2(),games.referee_3()))