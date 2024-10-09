import pandas as pd

# Caminho para a planilha historico
historico_path = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Excel\historico.xlsx'

# Caminho para a planilha de dados armazenados
dados_armazenados_path = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Excel\dados_armazenados.xlsx'


# Carregar a planilha historico
historico = pd.read_excel(historico_path)

# Tentar carregar a planilha de dados armazenados
try:
    dados_armazenados = pd.read_excel(dados_armazenados_path)
except FileNotFoundError:
    # Se a planilha de dados armazenados não existir, criar uma nova
    dados_armazenados = pd.DataFrame(columns=['cod', 'descricao', 'value', 'envase'])

# Agrupar os dados do historico por 'cod' e 'descricao' e somar os valores correspondentes
historico_agrupado = historico.groupby(['cod', 'descricao', 'envase']).sum().reset_index()

# Perguntar ao usuário se o cilindro foi trocado
troca_cilindro = input("O cilindro foi trocado? (Digite 'sim' ou 'nao'): ").lower()

if troca_cilindro == 'sim':
    cod_trocado = input("Digite o código do cilindro que foi trocado: ")
    
    # Zerar a contagem do código especificado
    dados_armazenados.loc[dados_armazenados['cod'] == cod_trocado, 'value'] = 0

# Atualizar os valores na planilha de dados armazenados
for idx, row in historico_agrupado.iterrows():
    cod = row['cod']
    descricao = row['descricao']
    value = row['value']
    envase = row['envase']
    
    # Verificar se já existe uma entrada para essa combinação de 'cod', 'descricao' e 'envase'
    mask = (dados_armazenados['cod'] == cod) & (dados_armazenados['descricao'] == descricao) & (dados_armazenados['envase'] == envase)
    if mask.any():
        # Se já existir, somar o valor ao valor existente
        dados_armazenados.loc[mask, 'value'] += value
    else:
        # Se não existir, adicionar uma nova entrada
        new_entry = pd.DataFrame({'cod': [cod], 'descricao': [descricao], 'value': [value], 'envase': [envase]})
        dados_armazenados = pd.concat([dados_armazenados, new_entry], ignore_index=True)

# Salvar os dados atualizados na planilha de dados armazenados
dados_armazenados.to_excel(dados_armazenados_path, index=False)

print("Dados armazenados atualizados com sucesso.")
