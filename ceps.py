import pandas as pd

# Lista de CEPs fictícios de algumas cidades
ceps = [
    '01311-000', # Bela Vista, SP
    '01419-000', # Cerqueira César, SP
    # '04538-100', # Itaim Bibi, SP
    # '22041-001', # Copacabana, RJ
    # '20040-002', # Centro, RJ
    # '30140-001', # Santo Agostinho, MG
    # '70040-000', # Asa Norte, DF
    # '90020-004', # Centro Histórico, RS
    # '80010-000', # Centro, PR
    # '60160-230'  # Meireles, CE
]

# Cria um DataFrame do pandas
df_ceps = pd.DataFrame(ceps, columns=['CEP'])

# Salva o DataFrame em um arquivo CSV
df_ceps.to_csv('ceps_para_pesquisa.csv', index=False)

print("Arquivo 'ceps_para_pesquisa.csv' gerado com sucesso!")
