import pandas as pd
import os
from os import walk
import numpy as np
import sys
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import statsmodels.api as sm

distribuidoras = [
    "CPFL PAULISTA",
    "CPFL PIRATININGA",
    "CPFL SANTA CRUZ",
    "EDP SP",
    "ELEKTRO",
    "ELETROPAULO",
    "ENERGISA SSE-SP",
]

def escreverRegressoes(df, path):
    correlacoes = []
    if not os.path.isdir(path + "/extra"):
        try:
            os.mkdir(path + "/extra")
        except OSError as error: 
            print(error)
    for i in range(1, df.shape[1]-1):
        carga = np.array(df.iloc[:, 1])
        temp_col = df.iloc[:, (i+1)]
        temp = np.array(temp_col)
        X_sm = sm.add_constant(temp)
        results = sm.OLS(carga, X_sm).fit()
        results.summary()
        results.predict(X_sm)
        # print(results.summary())
        correlacoes.append([temp_col.name, df.iloc[:, 1].corr(temp_col)])
        f = open(path + "/extra/" + temp_col.name + ".txt", "w")
        f.write(results.summary().as_text())
        f.close()
    f = open(path + "/extra/correlacoes.txt", "w")
    for corr in correlacoes:
        f.write("{}:\t{}\n".format(corr[0], corr[1]))
    f.close()


def progress_bar(current, total, bar_length=30):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '
    ending = '\n' if current == total else '\r'
    print(f'Arrumando dataframe. Progresso: [{arrow}{padding}] {int(fraction*100)}%', end=ending)

file_cargas = 'Datathons_pec_carga\seriesCargaSp.csv'
data_cargas = {}
os.system('cls' if os.name == 'nt' else 'clear')
print("Iniciando a leitura do arquivo de cargas..")
df_cargas = pd.read_csv(file_cargas, header=0, delimiter=";")#, nrows=1000)
df_cargas = df_cargas.sort_values(['val_itemserieoriginal'])

print("Arquivo lido.")
rows_len = df_cargas.shape[0]
ultimo_tempo_cargas = {}
i=0
for ind,row in df_cargas.iterrows():
    progress_bar(i + 1, rows_len)
    i=i+1
    if not row['nom_seriehistorica'][3:] in data_cargas:
        data_cargas[row['nom_seriehistorica'][3:]] = {}
    valor = row['val_itemserieoriginal']
    if isinstance(valor, str):
        valor = valor.replace(",", ".")
    data_cargas[row['nom_seriehistorica'][3:]][row['din_ocorrencia']] = valor
    ultimo_tempo_cargas[row['nom_seriehistorica'][3:]] = row['din_ocorrencia']
distribuidoras_finalizadas = []

for folder in distribuidoras:
    os.system('cls' if os.name == 'nt' else 'clear')
    path_folder = "distribuidoras_municipios_sp/" + folder
    filenames = next(walk(path_folder), (None, None, []))[2] 
    data = {}

    horarios = {}
    horarios_list = []

    print('Processando distribuidora: ' + folder)
    output_filename = "Data_Temperatura_" + folder + ".csv"
    if len(filenames) > 0 :
        for path in filenames:
            if path == output_filename:
                continue
            if path[:-4] == ".txt":
                continue
            path = path[:-4]
            print("Lendo arquivo: " + path_folder + "/" + path + '.csv')
            df = pd.read_csv(path_folder + "/" + path + '.csv', header=0, delimiter=";", usecols = ['id_varmeteo', 'din_medicao', 'val_medicao'])
            df = df.sort_values(['din_medicao'])
            df = df[df['id_varmeteo']=='TEM_MAX']
            data[path] = {}
            for _,row in df.iterrows():
                data[path][row['din_medicao']] = row['val_medicao']
                if not row['din_medicao'] in horarios:
                    horarios[row['din_medicao']] = True
                    horarios_list.append(row['din_medicao'])
    horarios_list.sort()

    final = pd.DataFrame(data={'data':[], 'Carga':[]})
    for key in data:
        final[key] = []

    final['data'] = horarios_list
    i = 0
    l_list = len(horarios_list)
    lastTime = False
    for date in horarios_list:
        if lastTime:
            break
        progress_bar(i, l_list)
        for key in data:
            if date in data[key]:
                final.loc[i, key] = data[key][date]
            if date in data_cargas[folder]:
                final.loc[i, 'Carga'] = data_cargas[folder][date]
            else:
                final.loc[i, 'Carga'] = 0


        i = i + 1
    final = final[final["Carga"] != 0]
    final = final.interpolate(method="linear", limit_area="inside")
    final = final.dropna()
    final[2:] = round(final[2:], 2)
    final.iloc[:, 1] = pd.to_numeric(final.iloc[:, 1], errors='coerce')
    final.to_csv(path_folder + "/Data_Temperatura_" + folder + ".csv", index=False, header=True, mode='w', sep=";")
    escreverRegressoes(final, path_folder)
    distribuidoras_finalizadas.append(
        {
            'nome':folder,
            'path':path_folder + "/Data_Temperatura_" + folder + ".csv"
        }
    )
os.system('cls' if os.name == 'nt' else 'clear')
print("FINALIZADO!\n")
for dis in distribuidoras_finalizadas:
    print('{}: {}\n'.format(dis['nome'], dis['path']))