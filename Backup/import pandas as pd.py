import pandas as pd
import numpy as np

# Lista de envases para replicar
envases = ['Envase 01', 'Envase 02', 'Envase 03', 'Envase 04', 'Envase 05', 'Envase 06']

# Componentes da encaixotadora e do robô paletizador
componentes_encaixotadora = [
    "Empurrar potes", "Subir e descer potes", "Montar caixa"
]
componentes_paletizador = [
    "Empurrar bandeja (cima)", "Empurrar bandeja (baixo)", "Empurrar bandeja (avante)", 
    "Controle de altura", "Ventosas (pegar papelão)", "Garras (abrir)", "Garras (fechar)", "Garras (manter)"
]

# Função para gerar dados para cilindros
def gerar_dados_para_circuitos(envases, componentes_encaixotadora, componentes_paletizador):
    new_data = []
    circuito_counter = 1
    
    for envase in envases:
        # Define circuito baseado na lógica: 2, 4, 6 com encaixotadora; 1, 3, 5 direto ao robô
        if envase in ['Envase 02', 'Envase 04', 'Envase 06']:
            componentes = componentes_encaixotadora + componentes_paletizador
        else:
            componentes = componentes_paletizador
        
        # Geração de dados para cada componente
        for i, componente in enumerate(componentes):
            for j in range(1, 5):  # Supondo 4 cilindros por componente
                cod = f"O_V{circuito_counter}.{i+1}.{j}"
                descricao = f"{componente} | Eletroválvula 01, conjunto {i+1}, cilindro {j}"
                
                # Gerar valor de ativação (perto, igual ou acima de 25 milhões)
                value = np.random.choice([np.random.randint(20000000, 24999999), 25000000, np.random.randint(25000001, 30000000)])
                
                new_data.append({
                    "cod": cod,
                    "descricao": descricao,
                    "value": value,
                    "máquina": envase,
                    "circuito": circuito_counter
                })
        
        circuito_counter += 1
    
    return pd.DataFrame(new_data)

# Gerar os dados fictícios
dados_ficticios = gerar_dados_para_circuitos(envases, componentes_encaixotadora, componentes_paletizador)

# Salvar os dados em um arquivo Excel (.xlsx)
output_path = r'C:\Users\ter07068\OneDrive - M DIAS BRANCO S.A. INDUSTRIA E COMERCIO DE ALIMENTOS\Área de Trabalho\Python\Excel\dados_ficticios_envases.xlsx'
dados_ficticios.to_excel(output_path, index=False)

print("Dados gerados e salvos com sucesso!")
