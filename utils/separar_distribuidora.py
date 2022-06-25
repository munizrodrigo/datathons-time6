import pandas as pd
import os
from unidecode import unidecode

#### CONSTANTES
WRITE_CSV = input("Deseja gerar arquivos .csv?\n").lower() in ["yes", "sim"]

#### CAMINHO DOS ARQUIVOS
file_cargas = 'Datathons_pec_carga\seriesCargaSp.csv'
file_areas = 'Datathons_pec_carga\Distribuidoras_Area_Atuacao.xlsx'
file_temp = 'Datathons_pec_carga\inmet.csv'

# substituir nom_longos com municipios
substituir = {
    "Sao Paulo - Mirante de Santana": "Sao Paulo",
    "Sao Paulo - Mirante de Santana2": "Sao Paulo",
}

def df_unidecode(df, colunas = None):
    if colunas == None:
        colunas = df.columns.values.tolist()
    for coluna in colunas:
        print("Decoding " + coluna)
        df[coluna] = df[coluna].apply(unidecode)
    return df

def readData(path):
    if len(path) < 4:
        print("Erro ao ler arquivo de caminho: " + path)
        return False
    else:
        extension = path.split(".")[-1]
        if extension == "csv":
            return pd.read_csv(path, header=0, delimiter=";")
        elif extension == "xlss":
            return pd.read_excel(file_areas, header=0)
        print("Erro: extensão {ext} não aceita. Somente aceita extensões .csv e .xls".format(ext=extension))
        return False


## Municipios com acento

##### DISTRIBUIDORAS
print("Lendo " + file_cargas)
df_cargas = readData(file_cargas)
cargas_colunas = df_cargas.columns.values.tolist()
distribuidoras = df_cargas["nom_seriehistorica"].unique()

# for string in distribuidoras:
#     string = string[3::]
distribuidoras = list(pd.Series(distribuidoras).str[3:])
print("Distribuidoras: " + ', '.join(distribuidoras))
dict_distribuidoras = {}
for key in distribuidoras:
    dict_distribuidoras[key] = []

##### TEMPERATURA
print("Lendo " + file_temp)
df_temp = readData(file_temp)
df_temp = df_unidecode(df_temp, ["nom_longo"])
temp_colunas = df_temp.columns.values.tolist()
coluna = "nom_longo"
municipios = df_temp[coluna].unique()
print("Municipios com dados de temperatura: " + ', '.join(municipios))

##### AREAS
print("Reading " + file_areas)
df_areas = readData(file_areas)
df_areas = df_unidecode(df_areas, ["Município"])
# areas_colunas = df_areas.columns.values.tolist()
# distribuidoras_area = df_areas["Distribuidora"].unique()

## Geração de tabelas distribuidora -> municipio
dict_distribuidoras = {}
for _,row in df_areas.iterrows():
    municipio = row["Município"]
    if municipio in municipios:
        if row["Distribuidora"] in dict_distribuidoras.keys():
            dict_distribuidoras[row["Distribuidora"]].append(municipio)
        else:
            dict_distribuidoras[row["Distribuidora"]] = []
            dict_distribuidoras[row["Distribuidora"]].append(municipio)

#### Criar pasta e arquivos
if not os.path.isdir("separados-distribuidoras"):
    try:
        os.mkdir("separados-distribuidoras")
    except OSError as error: 
        print(error)

founds = []
for key in dict_distribuidoras:
    path = "separados-distribuidoras/" + key
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError as error: 
            print(error)
    for municipio in dict_distribuidoras[key]:
        df_label = df_temp[df_temp[coluna]==municipio]
        target_file = "{path}/{label}.csv".format(path=path, label=municipio)
        print(key, " --> ", municipio)
        if WRITE_CSV:
            print("Gerando arquivo {label}.csv".format(label=municipio))
            df_label.to_csv(target_file, index=False, header=True, mode='a', sep=";")
        founds.append(municipio)

print("\nNão encontrado:")
for municipio in municipios:
    if not municipio in founds:
        path = "separados-distribuidoras/Não Encontrados"
        if not os.path.isdir(path):
            try:
                os.mkdir(path)
            except OSError as error: 
                print(error)
        df_label = df_temp[df_temp[coluna]==municipio]
        target_file = "{path}/{label}.csv".format(path=path, label=municipio)

        # print("{m}".format(m=municipio))
        # df_aux = df_temp[df_temp[coluna] == municipio]
        # print(df_aux)

        if WRITE_CSV:
            print("Gerando arquivo {label}.csv".format(label=municipio))
            df_label.to_csv(target_file, index=False, header=True, mode='a', sep=";")

# while True:
#     m = input("Procurar municipio em area de distribuição:\n").lower()
#     print("Distribuidora:")
#     print(df_areas.loc[df_areas['Município'].str.lower() == m])
    # print("\n\nTemperatura:")
    # print(df_temp.loc[df_temp['nom_longo'].str.lower() == m])

