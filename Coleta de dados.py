import datetime as dt
import pandas as pd
import requests
import os

def ler_tags_do_arquivo(filepath):
    tags = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            partes = line.strip().split(',')
            if len(partes) == 4:
                tag_info = {
                    'tag': partes[0],
                    'cod': partes[1],
                    'descricao': partes[2],
                    'envase': partes[3]
                }
                tags.append(tag_info)
    return tags

def events(tag, time_from, time_to):
    time_from = time_from.strftime('%Y-%m-%dT06:00:00')
    time_to = time_to.strftime('%Y-%m-%dT05:59:00')

    url = f'https://api.st-one.io/v1/mdiasbranco_gme/events/{tag}?timeFrom={time_from}&timeTo={time_to}'
    headers = {
        'Accept': 'application/json',
        'Authorization': 'UbeGO4CmLDgMltQAP_ZA-e_cdW9xLc0Pc40RhRfsH_uD9htlo75V7o-zLMA_G3TR9xg9h5Q'
    }
    response = requests.get(url=url, headers=headers)

    if response.status_code != 200:
        print(f"Erro ao acessar a API: {response.status_code}")
        return []

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON")
        return []

def events_process(tags, time_from, time_to):
    historian = pd.DataFrame()

    for tag_info in tags:
        tag = tag_info['tag']
        cod = tag_info['cod']
        descricao = tag_info['descricao']
        data = events(tag, time_from, time_to)
        if not data:
            continue

        df = pd.DataFrame(data)
        if 'info' in df.columns:
            df = df.drop(columns='info')
        df['cod'] = cod
        df['descricao'] = descricao
        df['envase'] = tag_info['envase']
        historian = pd.concat([historian, df], axis=0)

    if historian.empty:
        print("O DataFrame historian está vazio após o processamento dos eventos.")
        zero_entry = {'time': dt.datetime.now(), 'cod': '', 'descricao': '', 'envase': '', 'value': 0}
        historian = pd.DataFrame([zero_entry])

    historian['time'] = pd.to_datetime(historian['time'])
    historian['time'] = historian['time'].dt.tz_localize(None)
    historian = historian.drop_duplicates(subset=['time', 'cod', 'descricao'])

    historian['value'] = pd.to_numeric(historian['value'], errors='coerce')
    historian = historian.groupby(['cod', 'descricao', 'envase']).agg({'value': 'sum'}).reset_index()

    return historian

# Endereço do arquivo de tags
tags_filepath = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Finais\Cilindros\Tags.txt'
tags = ler_tags_do_arquivo(tags_filepath)

end_date = dt.datetime.now().replace(hour=5, minute=59, second=0, microsecond=0)
start_date = end_date - dt.timedelta(days=1)

historian_df = events_process(tags, start_date, end_date)

output_dir = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Excel'
historico_path = os.path.join(output_dir, "historico.xlsx")
historian_df.to_excel(historico_path, index=False)
print(f"Os dados foram salvos com sucesso no arquivo: {historico_path}")

dados_armazenados_path = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Excel\dados_armazenados.xlsx'

historico = pd.read_excel(historico_path)

try:
    dados_armazenados = pd.read_excel(dados_armazenados_path)
except FileNotFoundError:
    dados_armazenados = pd.DataFrame(columns=['cod', 'descricao', 'value', 'envase'])

historico_agrupado = historico.groupby(['cod', 'descricao', 'envase']).sum().reset_index()

for idx, row in historico_agrupado.iterrows():
    cod = row['cod']
    descricao = row['descricao']
    value = row['value']
    envase = row['envase']

    mask = (dados_armazenados['cod'] == cod) & (dados_armazenados['descricao'] == descricao) & (dados_armazenados['envase'] == envase)
    if mask.any():
        dados_armazenados.loc[mask, 'value'] += value
    else:
        new_entry = pd.DataFrame({'cod': [cod], 'descricao': [descricao], 'value': [value], 'envase': [envase]})
        dados_armazenados = pd.concat([dados_armazenados, new_entry], ignore_index=True)

dados_armazenados.to_excel(dados_armazenados_path, index=False)

print("Dados armazenados atualizados com sucesso.")
