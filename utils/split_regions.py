import pandas as pd

path_file = 'Datathons_pec_carga\inmet.csv'

df = pd.read_csv(path_file, header=0, delimiter=";")
coluna = "nom_longo"

unique_values = df[coluna].unique()
for label in unique_values:
    df_label = df[df[coluna]==label]
    target_file = "separados/{label}.csv".format(label=label)
    df_label.to_csv(target_file, index=False, header=True, mode='a', sep=";")
