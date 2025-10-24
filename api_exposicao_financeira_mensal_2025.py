import requests
import pandas as pd
import json

# Endpoint base da API
BASE_URL = "https://dadosabertos.ccee.org.br/api/3/action/datastore_search"

# ID do dataset EXPOSICAO_FINANCEIRA_MENSAL 2025
RESOURCE_ID = "bfba2fcf-ccd5-47a3-86f9-c6a1e8ba8fbf"

# Parâmetros da requisição
params = {
    "resource_id": RESOURCE_ID,
    "limit": 10000  
}

# Requisição GET à API
response = requests.get(BASE_URL, params=params)
data = response.json()

# Verifica se a API respondeu corretamente
if not data.get("success"):
    raise Exception("Erro na consulta à API da CCEE")

# Converte os registros para DataFrame
records = data["result"]["records"]
df = pd.DataFrame(records)

print(df)

# Mostra colunas disponíveis 
print("Colunas disponíveis:")
print(df.columns.tolist())

# Salva DataFrame em CSV
caminho = r"C:\Users\thais.dias\Documents\Way2\exposicao_financeira_2025.csv"
df.to_csv(caminho, index=False, encoding='utf-8')