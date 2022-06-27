# DatathONS---Time-6

Repositório para o DatathONS
Scripts em python para tratamento de dados do (Desafio 2): Análise da relação carga x temperatura para o estado de São Paulo.

## Descrição dos procedimentos realizados

`Tratamento dos dados do inmet.csv`: O arquivo inmet.csv fornecido para o desafio é muito grande, para poder trabalhar um melhor ambiente de trabalho o script [split_regions.py](utils/split_regions.py) separa o arquivo de acordo com a coluna 'nom_long' criado arquivos divididos com o nome das regiões analisadas.

`Separação dos arquivos de regiões`: Para uma melhor analíse, o script [separar_distribuidora.py](utils/separar_distribuidora.py) separa as regiões de acordo com a area de atuação das distribuidoras de energia

`Processamento das distribuidoras`: O script [processar_distribuidora.py](utils/processar_distribuidora.py) faz o processamento de todas as regiões que a distribuidora atua e cria uma planilha com as informações: Data, Carga no momento, Temperatura máxima no momento de cada região da distribuidora 