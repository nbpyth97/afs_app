from msvcrt import LK_RLCK
import pandas as pd
import numpy as np

lista = ['Portugal', 'Brasil', 'China', 'Ucrania', 'Colombia', 'Tailandia', 'Espanha', 'Uruguai', 'Japao', 'Russia', 'Venezuela', 'Filipinas', 'Inglaterra', 'Argentina', 'Coreia', 'França', 'Chile', 'Malasia', '10', '100', '1000', '20', '200', '2000', '30', '300', '3000', 'Portugal / Ucrania', 'Brasil / Colombia', 'China / Tailanda']

import excel_doc_afs as eda
df = eda.jogos_do_arbitro(1129)
new_mygames = pd.concat([df[0],df[1],df[2]])

print(new_mygames)

new_mygames["de A"] = ""
new_mygames["para A"] = ""
new_mygames["de AA1"] = ""
new_mygames["para AA1"] = ""
new_mygames["de AA2"] = ""
new_mygames["para AA2"] = ""
new_mygames['km A'] = ""
new_mygames['km AA1'] = ""
new_mygames['km AA2'] = ""
new_mygames['Itinerário'] = ""

for num in range(len(new_mygames)):
    viagem = new_mygames.columns.get_loc('de A')
    print("*"*10)
    for i in range(len(lista)):
        print(i)
        if num+i>len(lista):
            break
        else:
            if i % (len(new_mygames)) == 0:
                print(lista[num+i])
                new_mygames.iloc[num,viagem] = lista[num+i]
                viagem+=1

pd.set_option("display.max_rows", None, "display.max_columns", None)
print(new_mygames.columns.get_loc('de A'))


